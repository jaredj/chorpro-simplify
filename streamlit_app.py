import streamlit as st
import re

def remove_parentheses_around_numbers(line):
    return re.sub(r'\[([^]]*)\]\(([0-9]*)\)', r'[\1]', line)

def remove_comment_tags(line):
    return re.sub(r'{comment: ([^}]*)}', r'\1:', line)

def bold_complex_labels(line):
    if '[' not in line and ']' not in line:
        return re.sub(r'^(.* [^0-9a-zA-Z].*):', lambda match: '<b>' + match.group(1) + ':</b>', line)
    return line

def format_verse_line(line):
    def lcfirst(match):
        return match.group(1).lower().capitalize() + match.group(2) + ":"
    return re.sub(r'([A-Z\s]*)([0-9]*):', lcfirst, line)

def remove_metadata_line(line):
    metadata_keywords = [
        'title', 'subtitle', 'artist', 'key', 'time', 'tempo',
        'ccli_license', 'ccli', 'copyright', 'footer'
    ]
    return any(line.startswith('{' + keyword) for keyword in metadata_keywords)

def remove_copyright_line(line):
    copyright_patterns = [
        r'^©',
        r'^CCLI .*#',
        r'SongSelect®'
    ]
    return any(re.search(pattern, line) for pattern in copyright_patterns)

def should_remove_line(line):
    return remove_metadata_line(line) or remove_copyright_line(line)

def remove_dashes_before_chords(line):
    return re.sub(r'\s*-\s*\[', '[', line)

# Function to split the input string into elements of type 'lyric', 'chord', or 'space'.
def split_into_elements(text):
    elements = []
    in_chord = False
    current_content = ''
    current_type = ''
    for char in text:
        if char == '[':
            if current_content:
                elements.append({'type': current_type, 'content': current_content})
            in_chord = True
            current_content = '['
            current_type = 'chord'
        elif char == ']':
            current_content += ']'
            elements.append({'type': current_type, 'content': current_content})
            in_chord = False
            current_content = ''
        elif in_chord:
            current_content += char
        else:
            if char.strip():
                if current_type != 'lyric':
                    if current_content:
                        elements.append({'type': current_type, 'content': current_content})
                    current_type = 'lyric'
                    current_content = ''
                current_content += char
            else:
                if current_type != 'space':
                    if current_content:
                        elements.append({'type': current_type, 'content': current_content})
                    current_type = 'space'
                    current_content = ''
                current_content += char
    if current_content:
        elements.append({'type': current_type, 'content': current_content})
    return elements

# Function to split the parsed content into 'beginning', 'middle', and 'end' sections.
def split_into_sections(elements):
    first_lyric_idx = next((i for i, el in enumerate(elements) if el['type'] == 'lyric'), None)
    last_lyric_idx = next((i for i, el in enumerate(reversed(elements)) if el['type'] == 'lyric'), None)
    if last_lyric_idx is not None:
        last_lyric_idx = len(elements) - 1 - last_lyric_idx
    sections = {
        'beginning': elements[:first_lyric_idx] if first_lyric_idx is not None else [],
        'middle': elements[first_lyric_idx:last_lyric_idx+1] if first_lyric_idx is not None and last_lyric_idx is not None else [],
        'end': elements[last_lyric_idx+1:] if last_lyric_idx is not None else []
    }
    return sections

# Function to transform the 'beginning' section
def transform_beginning(beginning_section):
    transformed_beginning = []
    beginning_section = [el for i, el in enumerate(beginning_section) if not (el['type'] == 'space' and (i == 0 or i == len(beginning_section) - 1))]
    for el in beginning_section:
        if el['type'] == 'space':
            transformed_beginning.append({'type': 'space', 'content': ' '})
        else:
            transformed_beginning.append(el)
    return transformed_beginning

# Function to transform the 'middle' section
def transform_middle(middle_section):
    transformed_middle = []
    prev_was_chord = False
    for el in middle_section:
        if el['type'] == 'space':
            if not prev_was_chord:
                transformed_middle.append({'type': 'space', 'content': ' '})
        else:
            transformed_middle.append(el)
            if el['type'] == 'chord':
                prev_was_chord = True
            else:
                prev_was_chord = False
    return transformed_middle

# Function to reassemble the transformed sections into a single string
def assemble_line(beginning, middle, end):
    return ''.join([el['content'] for el in beginning + middle + end])

def condense_spacing(line: str) -> str:
    parsed_elements = split_into_elements(line)
    has_lyric = any(el['type'] == 'lyric' for el in parsed_elements)

    if not has_lyric:
        return line

    sections = split_into_sections(parsed_elements)
    transformed_beginning = transform_beginning(sections['beginning'])
    transformed_middle = transform_middle(sections['middle'])

    return assemble_line(transformed_beginning, transformed_middle, sections['end'])

# Function to simplify chords by removing any numbers, possibly in parentheses, from the end of any chord.
def simplify_chords(line):
    elements = split_into_elements(line)
    for el in elements:
        if el['type'] == 'chord':
            # Remove any text and numbers, possibly in parentheses, from the end of any chord
            el['content'] = re.sub(r'(/[a-z0-9]+|\([a-z0-9]+\)|\d+)+$', '', el['content'].replace("]", "")) + "]"
    return assemble_line(elements, [], [])

def process_text_content(text_content):
    lines = text_content.strip().split('\n')
    transformed_lines = []
    
    for line in lines:
        if should_remove_line(line):
            continue
        transformed_line = remove_parentheses_around_numbers(line)
        transformed_line = remove_comment_tags(transformed_line)
        transformed_line = bold_complex_labels(transformed_line)
        transformed_line = format_verse_line(transformed_line)
        transformed_line = remove_dashes_before_chords(transformed_line)
        transformed_line = condense_spacing(transformed_line)
        transformed_line = simplify_chords(transformed_line)
        transformed_lines.append(transformed_line)
        
    return '\n'.join(transformed_lines).strip()

def main():
    st.title("ChordPro Simplifier")
    st.write("Upload your ChordPro text to convert it into a simplified format.")

    input_text = st.text_area("Input your ChordPro text here:", height=300)
    if input_text:
        output_text = process_text_content(input_text)
        st.text_area("Simplified ChordPro Text:", value=output_text, height=300, key="output")

if __name__ == "__main__":
    main()

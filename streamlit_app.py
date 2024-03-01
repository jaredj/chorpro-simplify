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

import re

def remove_parentheses_around_numbers(line):
    return re.sub(r'\[([^]]*)\]\(([0-9]*)\)', r'[\1]', line)

def remove_comment_tags(line):
    return re.sub(r'{comment: ([^}]*)}', r'\1:', line)

# Additional functions would be defined here...


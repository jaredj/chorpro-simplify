import os
from streamlit_app import process_text_content

def test_process_text_against_expected_outputs():
    input_dir = 'test/test_inputs/'
    output_dir = 'test/test_outputs/'
    
    # Iterate over each file in the test inputs directory
    for input_file in os.listdir(input_dir):
        with open(os.path.join(input_dir, input_file), 'r') as file:
            input_text = file.read()
        
        # Process the input text
        processed_text = process_text_content(input_text)
        
        # Load the expected output
        with open(os.path.join(output_dir, input_file), 'r') as file:
            expected_output = file.read()

        # Compare the processed text with the expected output
        assert processed_text == expected_output, f"Mismatch found in {input_file}"
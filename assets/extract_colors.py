import sys
import re

def parse_scss_file(input_file, output_file):
    # Read SCSS file
    with open(input_file, 'r') as file:
        scss_content = file.read()

    # Find color values using regular expression
    color_pattern = r'(#(?:[0-9a-fA-F]{3}){1,2}|rgba?\([^)]+\)|hsva?\([^)]+\)|hsla?\([^)]+\))'
    color_matches = re.findall(color_pattern, scss_content)

    # Remove duplicates and sort color values
    color_values = sorted(set(color_matches))

    # Extract block names from SCSS content
    block_pattern = r'(?<=\}).*?(?=\{)'
    block_names = re.findall(block_pattern, scss_content, re.DOTALL)

    # Generate variable names for colors based on block names
    color_variables = []
    variable_index = 0
    for block in block_names:
        block = block.strip().lower()
        for index, color in enumerate(color_values):
            variable_name = '{}Color{}'.format(block, index)
            if variable_name not in color_variables:
                color_variables.append(variable_name)
            else:
                variable_name = '{}Color{}'.format(block, variable_index)
                color_variables.append(variable_name)
                variable_index += 1

    # Replace color occurrences with generated variables
    for color, variable in zip(color_values, color_variables):
        scss_content = scss_content.replace(color, '${}'.format(variable))

    # Generate variables section at the top of the file
    variables_section = ''.join(['${}: {};\n'.format(variable, color) for variable, color in zip(color_variables, color_values)])

    # Insert variables section at the top of the file
    scss_content = variables_section + scss_content

    # Write modified SCSS file
    with open(output_file, 'w') as file:
        file.write(scss_content)

    print("Parsing and replacement complete!")

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python extract_colors.py <input_file> <output_file>")
    sys.exit(1)

# Extract the input and output file paths from command-line arguments
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Call the function to parse the SCSS file
parse_scss_file(input_file_path, output_file_path)
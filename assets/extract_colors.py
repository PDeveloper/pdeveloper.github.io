import sys
import re

def parse_scss_file(input_file, output_file):
    # Read SCSS file
    with open(input_file, 'r') as file:
        scss_content = file.read()

    # Find color values using regular expression
    color_pattern = r'(#(?:[0-9a-fA-F]{3}){1,2}|rgb(?:a)?\([^)]+\)|hsv(?:a)?\([^)]+\)|hsl(?:a)?\([^)]+\))'
    color_matches = re.finditer(color_pattern, scss_content)

    # Store color positions and values
    color_positions = []
    color_values = []

    # Iterate over color matches
    for match in color_matches:
        color_positions.append(match.span())
        color_values.append(match.group())

    # Generate variable names for colors
    color_variables = ['${}'.format(variable) for variable in ['color{}'.format(index) for index in range(len(color_values))]]

    # Replace color occurrences with generated variables
    offset = 0
    for position, variable in zip(color_positions, color_variables):
        start, end = position
        start += offset
        end += offset
        scss_content = scss_content[:start] + variable + scss_content[end:]
        offset += len(variable) - (end - start)

    # Generate variables section at the top of the file
    variables_section = ''.join(['{}: {};\n'.format(variable, color) for variable, color in zip(color_variables, color_values)])

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
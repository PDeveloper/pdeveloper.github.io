import sys
import re

def invert_color(color_value):
    if color_value.startswith('#'):
        # Hexadecimal color value
        hex_value = color_value.lstrip('#')
        if len(hex_value) == 3:
            # Expand shorthand hex to full 6-digit representation
            hex_value = ''.join(c * 2 for c in hex_value)
        if hex_value:
            r, g, b = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
            inverted_r = 255 - r
            inverted_g = 255 - g
            inverted_b = 255 - b
            inverted_hex = '#{:02x}{:02x}{:02x}'.format(inverted_r, inverted_g, inverted_b)
            return inverted_hex
    elif color_value.startswith('rgb'):
        # RGB or RGBA color value
        rgb_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', color_value)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            inverted_r = 255 - r
            inverted_g = 255 - g
            inverted_b = 255 - b
            if rgb_match.group().startswith('rgba'):
                alpha = re.search(r'[\d.]+', color_value).group()
                inverted_rgb = 'rgba({}, {}, {}, {})'.format(inverted_r, inverted_g, inverted_b, alpha)
            else:
                inverted_rgb = 'rgb({}, {}, {})'.format(inverted_r, inverted_g, inverted_b)
            return inverted_rgb
    elif color_value.startswith('hsv'):
        # HSV or HSVA color value
        hsv_match = re.match(r'hsva?\((\d+),\s*(\d+)%?,\s*(\d+)%?(?:,\s*[\d.]+)?\)', color_value)
        if hsv_match:
            h, s, v = map(int, hsv_match.groups())
            inverted_h = (h + 180) % 360
            inverted_s = 100 - s
            inverted_v = 100 - v
            if hsv_match.group().startswith('hsva'):
                alpha = re.search(r'[\d.]+', color_value).group()
                inverted_hsv = 'hsva({}, {}%, {}%, {})'.format(inverted_h, inverted_s, inverted_v, alpha)
            else:
                inverted_hsv = 'hsv({}, {}%, {}%)'.format(inverted_h, inverted_s, inverted_v)
            return inverted_hsv
    elif color_value.startswith('hsl'):
        # HSL or HSLA color value
        hsl_match = re.match(r'hsla?\((\d+),\s*(\d+)%?,\s*(\d+)%?(?:,\s*[\d.]+)?\)', color_value)
        if hsl_match:
            h, s, l = map(int, hsl_match.groups())
            inverted_h = (h + 180) % 360
            inverted_s = 100 - s
            inverted_l = 100 - l
            if hsl_match.group().startswith('hsla'):
                alpha = re.search(r'[\d.]+', color_value).group()
                inverted_hsl = 'hsla({}, {}%, {}%, {})'.format(inverted_h, inverted_s, inverted_l, alpha)
            else:
                inverted_hsl = 'hsl({}, {}%, {}%)'.format(inverted_h, inverted_s, inverted_l)
            return inverted_hsl

    return color_value

def transform_theme(input_file, output_file):
    with open(input_file, 'r') as file:
        scss_content = file.read()

    # Find all color values in the SCSS content along with their positions
    color_matches = [(match.group(), match.start()) for match in re.finditer(r'#[0-9a-fA-F]{3,6}|rgba?\([\d.,\s]+\)|hsla?\([\d.,%\s]+\)', scss_content)]

    # Replace each color value with inverted color at the corresponding position
    for color_value, position in color_matches:
        inverted_color = invert_color(color_value)
        scss_content = scss_content[:position] + scss_content[position:].replace(color_value, inverted_color, 1)

    with open(output_file, 'w') as file:
        file.write(scss_content)

    print("Transformation complete!")

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python invert_colors.py <input_file> <output_file>")
    sys.exit(1)

# Extract the input and output file paths from command-line arguments
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Call the function to transform the theme
transform_theme(input_file_path, output_file_path)
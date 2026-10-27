
import re
import xml.etree.ElementTree as ET

def to_gray_and_white(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    def convert_color(color):
        if not color:
            return color

        color = color.strip().lower()

        # Handle named black
        if color == "black":
            return "#000000"

        # Handle hex colors: #RGB or #RRGGBB
        if re.fullmatch(r"#[0-9a-f]{3}", color):
            color = "#" + "".join(c * 2 for c in color[1:])

        if re.fullmatch(r"#[0-9a-f]{6}", color):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

        # Handle rgb(r, g, b)
        else:
            match = re.fullmatch(
                r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
                color
            )
            if not match:
                return color

            r, g, b = map(int, match.groups())

        # Keep pure black black
        if (r, g, b) == (0, 0, 0):
            return "#000000"

        # Convert brightness to the range 128–255
        brightness = (r + g + b) / 3
        gray = int(128 + brightness / 255 * 127)

        return f"#{gray:02x}{gray:02x}{gray:02x}"

    # Process SVG attributes such as fill and stroke
    for element in root.iter():
        for attribute in ("fill", "stroke", "stop-color", "color"):
            value = element.get(attribute)
            if value:
                element.set(attribute, convert_color(value))

        # Process inline CSS declarations
        style = element.get("style")
        if style:
            def replace_css(match):
                return (
                    match.group(1)
                    + convert_color(match.group(2))
                    + match.group(3)
                )

            style = re.sub(
                r"((?:fill|stroke|stop-color|color)\s*:\s*)"
                r"(#[0-9a-fA-F]{3,6}|rgb\([^)]*\)|black|white)",
                replace_css,
                style,
                flags=re.IGNORECASE,
            )
            element.set("style", style)

    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Saved to {output_path}")


# Example usage
to_gray_and_white(
    "graphs/vampire_density_7_lim100000_scale50.svg",
    "graphs/vampire_density_half_lim100000_scale50.svg"
)

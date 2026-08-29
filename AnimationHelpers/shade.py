import sys

def shade_color(hex_color, opacity):
    """
    Darken a hex color as if it were drawn with the given opacity
    over a black background.
    """
    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = round(r * opacity)
    g = round(g * opacity)
    b = round(b * opacity)

    return f"#{r:02X}{g:02X}{b:02X}"

print(shade_color(sys.argv[1], float(sys.argv[2])))
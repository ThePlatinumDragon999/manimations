import xml.etree.ElementTree as ET

def change_white_color(input_path, output_path, new_color):
    tree = ET.parse(input_path)
    root = tree.getroot()

    # SVG namespace
    ns = "{http://www.w3.org/2000/svg}"

    white_values = ("white", "#fff", "#ffffff")

    for element in root.iter():
        # Change white fills
        fill = element.get("fill", "").lower()
        if fill in white_values:
            element.set("fill", new_color)

        # Change white strokes
        stroke = element.get("stroke", "").lower()
        if stroke in white_values:
            element.set("stroke", new_color)

        # Also handle inline CSS styles
        style = element.get("style", "")
        for white in white_values:
            style = style.replace(f"fill:{white}", f"fill:{new_color}")
            style = style.replace(f"stroke:{white}", f"stroke:{new_color}")

        if style:
            element.set("style", style)

    tree.write(
        output_path,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"Saved to {output_path}")


change_white_color(
    "graphs/vampire_density_7_full_lim10000_scale50.svg",
    "graphs/vampire_density_7_pink_lim10000_scale50.svg",
    "#b00b69"
)
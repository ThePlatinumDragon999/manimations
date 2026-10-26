
import xml.etree.ElementTree as ET

def to_black_and_white(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()

    # SVG namespace
    ns = "{http://www.w3.org/2000/svg}"

    # Make the background black.
    for element in root.iter():
        if element.tag == f"{ns}rect":
            fill = element.get("fill", "").lower()

            # Preserve the black background rectangle.
            if fill not in ("black", "#000", "#000000"):
                element.set("fill", "white")

    tree.write(
        output_path,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"Saved to {output_path}")


to_black_and_white(
    "graphs/vampire_density_7_lim10000_scale50.svg",
    "graphs/vampire_density_7_full_lim10000_scale50.svg"
)
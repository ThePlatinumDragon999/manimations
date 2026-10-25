from PIL import Image

def to_black_and_white(input_path, output_path):
    # Open the image
    img = Image.open(input_path).convert("RGB")
    
    # Create a new image with the same size
    bw_img = Image.new("RGB", img.size, "black")
    
    # Process each pixel
    pixels = img.load()
    bw_pixels = bw_img.load()
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # If the pixel is not black, make it white
            if (r, g, b) != (0, 0, 0):
                bw_pixels[x, y] = (255, 255, 255)
    
    # Save the result
    bw_img.save(output_path)
    print(f"Saved to {output_path}")

# Example usage:
to_black_and_white("vampire_density_6_lim100000_scale50.png", "vampire_density_6_full_lim100000_scale50.png")

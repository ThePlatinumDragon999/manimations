from PIL import Image

def grayscale_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)
    
    # Convert to grayscale
    grayscale = image.convert("L")
    
    # Save the result
    grayscale.save(output_path)
    print(f"Grayscale image saved as {output_path}")

# Example usage:
# Replace these with your own file paths
grayscale_image("vampire_density_red.png", "vampire_density_white_small.png")

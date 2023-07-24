from PIL import Image

def colorize_green(rgba_file_path, binary_mask_path, output_path):
    # Open the RGBA image
    rgba_img = Image.open(rgba_file_path)

    # Open the binary mask (gray scale) image
    mask_img = Image.open(binary_mask_path)

    # Check if the sizes of the two images match
    if rgba_img.size != mask_img.size:
        raise ValueError("The sizes of the two images do not match.")

    # Create a blank image of the same size to store the final colored image
    colored_img = Image.new("RGBA", rgba_img.size)

    # Iterate over each pixel in the images
    for x in range(rgba_img.width):
        for y in range(rgba_img.height):
            # Get the RGBA pixel from the RGBA image
            r, g, b, a = rgba_img.getpixel((x, y))

            # Get the value of the pixel in the binary mask (0 to 255)
            mask_value = mask_img.getpixel((x, y))

            # Convert the mask value to a boolean (True if >= 1 / 255, else False)
            is_mask_true = mask_value >= 1

            # If the binary mask is true, color the pixel green (r=0, g=255, b=0)
            if is_mask_true:
                colored_img.putpixel((x, y), (0, 255, 0, a))
            else:
                colored_img.putpixel((x, y), (r, g, b, a))

    # Save the final colored image
    colored_img.save(output_path)

if __name__ == "__main__":
    rgba_file_path = "results\\additional\\2020-04-11\\finalShadowMaskFancy.tif"
    binary_mask_path = "results\\additional\\2020-04-11\\cloudMaskRaw.tif"
    output_path = "results\\additional\\2020-04-11\\finalShadowMaskFancyModified.tif"

    colorize_green(rgba_file_path, binary_mask_path, output_path)
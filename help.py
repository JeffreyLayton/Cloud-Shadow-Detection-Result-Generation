from os import path
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def colorize_green():
    rgba_file_path = "results\\additional\\2020-04-11\\finalShadowMaskFancy.tif"
    binary_mask_path = "results\\additional\\2020-04-11\\cloudMaskRaw.tif"
    output_path = "results\\additional\\2020-04-11\\finalShadowMaskFancyModified.tif"
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



def load_binary_image(file_path):
    # Load binary image as grayscale with values >0 being True and 0 otherwise
    img = Image.open(file_path).convert("L")
    return np.array(img) > 0

def load_truth_image(file_path):
    # Load RGBA image and set RGB values (0, 255, 0) as True and others as False
    img = Image.open(file_path).convert("RGBA")
    return np.all(np.array(img) == [0, 255, 0, 255], axis=-1)

def count_permutations(binary_images, truth_image):
    permutations = np.zeros((16,), dtype=float)
    npixels = truth_image.size

    for tru_i in range(2):
        for pot_i in range(2):
            for obj_i in range(2):
                for fin_i in range(2):
                    is_part =           (truth_image      == bool(tru_i))
                    is_part = is_part & (binary_images[0] == bool(pot_i))
                    is_part = is_part & (binary_images[1] == bool(obj_i))
                    is_part = is_part & (binary_images[2] == bool(fin_i))
                    count = np.sum(is_part)
                    index = tru_i * 8 + pot_i * 4 + obj_i * 2 + fin_i
                    permutations[index] = count / npixels

    return permutations

def plot_bar_graph(permutations):
    labels = ["F - FFF", "F - FFT", "F - FTF", "F - FTT"," F - TFF", "F - TFT", "F - TTF", "F - TTT",
              "T - FFF", "T - FFT", "T - FTF", "T - FTT"," T - TFF", "T - TFT", "T - TTF", "T - TTT"]
    
    # Find indices where permutations is non-zero
    non_zero_indices = np.nonzero(permutations)
    # Create filtered labels and permutations based on non-zero indices
    labels = [labels[i] for i in non_zero_indices[0]]
    permutations = permutations[non_zero_indices]

    x = np.arange(len(labels))
    plt.bar(x, permutations)
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.xlabel("Permutations")
    plt.ylabel("Percent of Total")
    plt.title("Permutations of the shadow mask values referenced to the baseline")

    caption = "In the label A - XYZ, A refers to the baseline, X refers to the potential mask,"
    caption += " Y refers to the object-based mask and Z referse to the final mask."
    plt.text(0.5, -0.25, caption, transform=plt.gca().transAxes, ha='center', fontsize=10)

    # Annotate each bar with its corresponding percentage value
    for i, val in enumerate(permutations):
        plt.text(i, val, f"{val:.2%}", ha='center', va='bottom', fontsize=9, color='black')

    plt.grid(axis="y")
    plt.show()

def display_image_from_bool_array(bool_array, title="Image"):
    # Convert the boolean NumPy array to an integer array (0 for False, 255 for True)
    int_array = np.uint8(bool_array) * 255

    # Create an image from the integer array
    img = Image.fromarray(int_array, mode="L")

    # Display the image using matplotlib
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.title(title)
    plt.show()

def per_pixel_statistics(binary_path, truth_path):
    # Replace these file paths with your actual file paths
    binary_file_paths = [   
                            path.join(binary_path,"candidateShadowMaskRaw.tif"),
                            path.join(binary_path,"objectBasedShadowMaskRaw.tif"),
                            path.join(binary_path,"finalShadowMaskRaw.tif")
                        ]
    truth_file_path = path.join(truth_path,"shadowBaseline.tif")

    binary_images = [load_binary_image(file_path) for file_path in binary_file_paths]
    truth_image = load_truth_image(truth_file_path)

    # display_image_from_bool_array(truth_image, truth_file_path)
    # display_image_from_bool_array(binary_images[0], binary_file_paths[0])
    # display_image_from_bool_array(binary_images[1], binary_file_paths[1])
    # display_image_from_bool_array(binary_images[2], binary_file_paths[2])

    return count_permutations(binary_images, truth_image)


if __name__ == "__main__":
    #colorize_green()
    dat_eval_root_dir = 'data\\evaluation'
    res_eval_root_dir = 'results\\evaluation'

    dir_pairs = []

    for sub_dir in os.listdir(dat_eval_root_dir):
        data_dir = path.join(dat_eval_root_dir, sub_dir)
        if path.isdir(data_dir):
            res_dir = path.join(res_eval_root_dir, sub_dir)
            if path.exists(res_dir):
                dir_pairs.append((data_dir,res_dir))

    all_permutations_array = np.zeros((16, len(dir_pairs)))
    for i in range(len(dir_pairs)):
        print(dir_pairs[i])
        all_permutations_array[:, i] = per_pixel_statistics(dir_pairs[i][1], dir_pairs[i][0])

    average_permutations = np.mean(all_permutations_array, axis=1)
    plot_bar_graph(average_permutations)
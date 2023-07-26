import math
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

def count_permutations(binary_images, truth_image, cloud_image):
    permutations = np.zeros((16,), dtype=float)
    cloud_image_inv = cloud_image == False
    npixels = np.sum(cloud_image_inv)

    for tru_i in range(2):
        for pot_i in range(2):
            for obj_i in range(2):
                for fin_i in range(2):
                    is_part =           (truth_image      == bool(tru_i))
                    is_part = is_part & (binary_images[0] == bool(pot_i))
                    is_part = is_part & (binary_images[1] == bool(obj_i))
                    is_part = is_part & (binary_images[2] == bool(fin_i))
                    is_part = is_part & cloud_image_inv
                    count = np.sum(is_part)
                    index = tru_i * 8 + pot_i * 4 + obj_i * 2 + fin_i
                    permutations[index] = count / npixels

    return permutations

def plot_stacked_bar_graph(data_list, stacked_lists):
    stacked_labels = [stacked_list[0] for stacked_list in stacked_lists]
    data_list_percent = [(pair[0], pair[1] * 100) for pair in data_list]
    bbox_props = dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', alpha=0.7)
    # Creating the stacked bar graph
    max_v = 0
    for id_stacked_list, stacked_list in enumerate(stacked_lists):
        current_bottom = 0
        for stacked_el in stacked_list[1]:
            name = data_list_percent[stacked_el][0]
            value = data_list_percent[stacked_el][1]
            plt.bar(id_stacked_list, value, bottom=current_bottom, edgecolor='black')
            
            plt.text(id_stacked_list + 0.35, current_bottom + value - 0.05, name + f" ({value:.2f}%)", ha='right', fontsize=10, bbox=bbox_props)
            current_bottom += value
        plt.text(id_stacked_list - 0.4, current_bottom + 0.005, f"{current_bottom:.2f}%", ha='left', fontsize=12)
        max_v = max(max_v, math.ceil(current_bottom))

    # Adjusting plot aesthetics (optional)
    plt.xticks(range(len(stacked_labels)), stacked_labels)

    y_tick_positions = np.arange(0, max_v, 0.1)  # Set y tick positions every 0.05 (from 0 to 100)
    y_tick_labels = [f"{i:.1f}%" for i in y_tick_positions]  # Format the y tick labels as percentages
    plt.yticks(y_tick_positions, y_tick_labels)

    plt.xlabel('Type of Pixel Progression', labelpad=10, fontsize=17)
    plt.ylabel('Average Percentages', labelpad=10, fontsize=17)
    plt.title('Average Percentage of Pixel Progression Relavent to Probability Analysis Correction')
    plt.grid(axis="y")

    # Display the plot
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
    cloud_file_path = path.join(binary_path,"cloudMaskRaw.tif")

    binary_images = [load_binary_image(file_path) for file_path in binary_file_paths]
    truth_image = load_truth_image(truth_file_path)
    cloud_image =  load_binary_image(cloud_file_path)

    # display_image_from_bool_array(truth_image, truth_file_path)
    # display_image_from_bool_array(binary_images[0], binary_file_paths[0])
    # display_image_from_bool_array(binary_images[1], binary_file_paths[1])
    # display_image_from_bool_array(binary_images[2], binary_file_paths[2])

    return count_permutations(binary_images, truth_image, cloud_image)


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
    labelled_average_permutations = [
        ("F - FFF", average_permutations[0]),
        ("F - FFT", average_permutations[1]),
        ("F - FTF", average_permutations[2]),
        ("F - FTT", average_permutations[3]),
        ("F - TFF", average_permutations[4]),
        ("F - TFT", average_permutations[5]),
        ("F - TTF", average_permutations[6]),
        ("F - TTT", average_permutations[7]),
        ("T - FFF", average_permutations[8]),
        ("T - FFT", average_permutations[9]),
        ("T - FTF", average_permutations[10]),
        ("T - FTT", average_permutations[11]),
        ("T - TFF", average_permutations[12]),
        ("T - TFT", average_permutations[13]),
        ("T - TTF", average_permutations[14]),
        ("T - TTT", average_permutations[15]),
    ]
    bar_combinations = [
        ("Shadow Pixels Correctly Added", [9,13]),
        ("Shadow Pixels Incorrectly Not Added", [12,8]),
        ("Non-Shadow Pixels Incorrectly Added", [1,5])
    ]
    plot_stacked_bar_graph(labelled_average_permutations, bar_combinations)
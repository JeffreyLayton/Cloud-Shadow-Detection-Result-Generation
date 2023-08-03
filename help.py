import math
from os import path
import os
import numpy as np
import matplotlib.pyplot as plt
import json
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



def plot_stacked_bar_graph(data_list, stacked_lists):
    stacked_labels = [stacked_list[0] for stacked_list in stacked_lists]
    data_list_percent = [(pair[0], pair[1] * 100) for pair in data_list]
    bbox_props = dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', alpha=0.7)
    # Creating the stacked bar graph
    max_v = 0
    for id_stacked_list, stacked_list in enumerate(stacked_lists):
        current_bottom = 0
        for stacked_el in stacked_list[1]:
            name = data_list_percent[stacked_el[0]][0]
            value = data_list_percent[stacked_el[0]][1]
            color = stacked_el[1]
            plt.bar(id_stacked_list, value, bottom=current_bottom, color=color, edgecolor='black')
            
            plt.text(id_stacked_list + 0.35, current_bottom + value - 0.05, name + f" ({value:.2f}%)", ha='right', fontsize=10, bbox=bbox_props)
            current_bottom += value
        plt.text(id_stacked_list - 0.4, current_bottom + 0.005, f"{current_bottom:.2f}%", ha='left', fontsize=12)
        max_v = max(max_v, math.ceil(current_bottom))

    # Adjusting plot aesthetics (optional)
    plt.xticks(range(len(stacked_labels)), stacked_labels)

    y_tick_positions = np.arange(0, max_v, 0.2)
    y_tick_labels = [f"{i:.1f}%" for i in y_tick_positions]  # Format the y tick labels as percentages
    plt.yticks(y_tick_positions, y_tick_labels)

    plt.xlabel('Type of Pixel Progression', labelpad=10, fontsize=17)
    plt.ylabel('Average Percentages', labelpad=10, fontsize=17)
    plt.title('Average Percentage of Pixel Progression Relevant to Probability Analysis Correction')
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

def plot_graph(heights, dots):
    plt.figure(figsize=(10, 6))
    num_subfolders = dots.shape[1]
    #for i in range(num_subfolders):
        #plt.plot(heights, dots[:, i], label=f'Subfolder {i+1}')

    average_dots = np.mean(dots, axis=1)
    plt.plot(heights, average_dots, label='Average', linewidth=2, color='black')

    x_tick_positions = np.arange(0, 2000, 25)
    plt.xticks(x_tick_positions)

    y_tick_positions = np.arange(-2, 2, 0.05)
    plt.yticks(y_tick_positions)

    plt.xlabel('Height', fontsize=14)
    plt.ylabel('Mean Dot Product', fontsize=14)
    plt.title('Average of Satellite Mean Dot Products at Various Satellite Heights', fontsize=16)
    #plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    bar_combinations = [
        ("Shadow Pixels Correctly Added", [(9,(0.53, 0.81, 0.98)),(13,(0.25, 0.41, 0.88))]),
        ("Shadow Pixels Incorrectly Not Added", [(12,(1.0,0.3,0.3)),(8, (0.3,1.0,0.3))]),
        ("Non-Shadow Pixels Incorrectly Added", [(1,(1.0, 0.75, 0.4)),(5,(1.0, 0.5, 0.0))])
    ]
    plot_stacked_bar_graph(labelled_average_permutations, bar_combinations)

    plot_graph(heights, dots)

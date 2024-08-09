import cv2
import argparse
import numpy as np
import math
from src.alphabets import *
from PIL import Image, ImageFont, ImageDraw

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="./data/img_input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="./data/img_output.jpg", help="Path to output image file")
    # parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="complex")
    parser.add_argument("--background", type=tuple, default=(224, 224, 224), help="background's color")
    parser.add_argument("--num_cols", type=int, default=150, help="number of character for output's width")
    args = parser.parse_args()
    return args

def main(opt):
    # Load the input image
    image = cv2.imread(opt.input, 1)

    # Get the dimensions of the input image
    height, width, _ = image.shape

    # Calculate the dimensions of each cell in the grid
    cell_width = width // opt.num_cols
    cell_height = cell_width * 2
    num_rows = int(height / cell_height)

    # Load the font and calculate character dimensions
    font = ImageFont.truetype("./fonts/Antonio-Regular.ttf", size=20)
    left, top, right, bottom = font.getbbox('A')
    char_width = right - left
    char_height = bottom - top
    print(f"{char_width}x{char_height}")

    # Create a new image for the ASCII art output
    image_width = char_width * opt.num_cols
    image_height = char_height * num_rows
    out_image = Image.new("RGB", (image_width, image_height), opt.background)
    draw = ImageDraw.Draw(out_image)

    # Iterate through each cell in the grid
    for i in range(num_rows):
        for j in range(opt.num_cols):
            # Extract the sub-image for the current cell
            sub_image = image[int(i*cell_height):int((i+1)*cell_height), 
                            int(j*cell_width):int((j+1)*cell_width)]
            
            # Calculate the average color of the sub-image
            avg_color = np.sum(np.sum(sub_image, axis=0), axis=0) // (cell_height*cell_width)
            avg_color = tuple(avg_color)
            
            # Determine the index of the ASCII character based on brightness
            index = int(np.mean(sub_image) / 255 * len(GENERAL[opt.mode]))
            
            # Draw the ASCII character on the output image
            draw.text((j*char_width, i*char_height), GENERAL[opt.mode][index], 
                    fill=avg_color, font=font)

    # Save the resulting ASCII art image
    out_image.save(opt.output)

if __name__ == "__main__":
    opt = get_args();
    main(opt)
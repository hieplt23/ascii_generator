import cv2
import argparse
import numpy as np
from src.alphabets import *

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="./data/img_input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="./data/txt_output.txt", help="Path to output text file")
    # parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="complex")
    parser.add_argument("--num_cols", type=int, default=100, help="number of character for output's width")
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

    # Create a new txt file for the ASCII art output
    out_image = open(opt.output, "w")

    # Iterate through each cell in the grid
    for i in range(num_rows):
        for j in range(opt.num_cols):
            # Extract the sub-image for the current cell
            sub_image = image[int(i*cell_height):int((i+1)*cell_height), 
                            int(j*cell_width):int((j+1)*cell_width)]
            
            # Determine the index of the ASCII character based on brightness
            index = int(np.mean(sub_image) / 255 * len(GENERAL[opt.mode]))
            
            out_image.write(GENERAL[opt.mode][index])
            
        out_image.write("\n")
        
    out_image.close()

if __name__ == "__main__":
    opt = get_args();
    main(opt)
import cv2
import numpy as np
import time
import os
from collections import Counter


def quantize_color(color, bin_size=16):
    return tuple((val // bin_size) * bin_size for val in color)

def get_mode_color(pixels, threshold=0.3, bin_size=16):
    quantized = [quantize_color(tuple(pixel), bin_size) for pixel in pixels]
    counter = Counter(quantized)
    most_common, count = counter.most_common(1)[0]
    if count / len(pixels) > threshold:
        return most_common
    else:
        return None
    

def process_image(image, num_cols, threshold=0.3, bin_size=16):
    height, width, _ = image.shape

    # Calculate the grid width based on the number of columns
    grid_width = width // num_cols
    remainder_w = width % num_cols  # Remainder pixels in width

    # Calculate the number of rows based on grid width
    num_rows = (height + grid_width - 1) // grid_width  # Round up if needed
    remainder_h = height % grid_width  # Remainder pixels in height

    # Output image
    output = np.zeros_like(image)

    for row in range(num_rows):
        for col in range(num_cols):
            x_start = col * grid_width
            y_start = row * grid_width

            # Adjust the last column to ensure it doesn't extend beyond the image width
            if col == num_cols - 1:
                x_end = width  # Make sure the last column takes up the remaining space
            else:
                x_end = (col + 1) * grid_width

            # Adjust the last row to ensure it doesn't extend beyond the image height
            if row == num_rows - 1:
                y_end = height  # Make sure the last row takes up the remaining space
            else:
                y_end = (row + 1) * grid_width

            # Extract the current cell from the image
            cell = image[y_start:y_end, x_start:x_end]
            pixels = cell.reshape(-1, 3)

            # Calculate the mean color of the current box
            mean_color = tuple(np.mean(pixels, axis=0).astype(np.uint8))

            # Try quantized mode
            mode_color = get_mode_color(pixels, threshold=threshold, bin_size=bin_size)
            final_color = mode_color if mode_color else mean_color

            # Fill the cell with the final color
            output[y_start:y_end, x_start:x_end] = final_color

    # Draw black grid lines (optional, to visualize the grid)
    for col in range(1, num_cols):
        x = col * grid_width
        cv2.line(output, (x, 0), (x, height), (0, 0, 0), 1)
    for row in range(1, num_rows):
        y = row * grid_width
        cv2.line(output, (0, y), (width, y), (0, 0, 0), 1)

    return output

def get_user_input(image_width, num_cols):
    remainder = image_width % num_cols

    if remainder != 0:
        # Calculate the next nearest number of columns
        suggested_cols = image_width // (image_width // num_cols) 

                # Only prompt the user if the suggestion is different
        if suggested_cols != num_cols:
            leftover = image_width % suggested_cols
            print(f"Current number of columns ({num_cols}) does not perfectly divide the width ({image_width}).")
            print(f"Suggested number of columns: {suggested_cols} (leaving only {leftover} pixels leftover).")
            user_choice = input(f"Do you want to use {suggested_cols} columns instead? (y/n): ").lower()
            
            if user_choice == 'y':
                return suggested_cols
            
    return num_cols

# --- Main entry point ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Grid-based color simplification.")
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("num_cols", type=int, help="Width of each grid square")
    parser.add_argument("--output", default="output.png", help="Path for the output image")
    args = parser.parse_args()

    img = cv2.imread(args.image_path)
    if img is None:
        raise ValueError("Could not load image. Check the path.")
    else:
        print("Image loaded successfully:", img.shape)

    # Get user input for columns (if needed)
    adjusted_num_cols = get_user_input(img.shape[1], args.num_cols)

    #Processing the image
    result = process_image(img, adjusted_num_cols)

    # Ensure the Outputs folder exists
    output_dir = "Outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Saving the image to the Outputs folder
    timestamp = time.strftime("%d%m%y_%H%M%S")  # Day, Month, Year, Time
    output_filename = os.path.join(output_dir, f"output_{timestamp}.png")
    cv2.imwrite(output_filename, result)
    print(f"Output saved to {output_filename}")


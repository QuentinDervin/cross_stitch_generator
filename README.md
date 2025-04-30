# Grid-Based Image Color Simplification for Cross Stitch Patterns

This program takes an image and divides it into a grid, simplifying each section into a single dominant color. 
The purpose of this tool is to help **create cross-stitch patterns** by reducing an image to a color grid where each cell represents one stitch.

You can input an image and choose the number of columns for the grid. 
The program will generate a new image in which each section of the grid is filled with the most common or mean color in that section. 
This makes it easy to visualize patterns based on color rather than pixels.

# How to Use

1. **Prepare your environment**
    Make sure you have Python installed and install the necessary dependencies.
    ```
    pip install opencv-python numpy
    ```

3. **Run the program**
    Run the following command in your terminal to run the program:
    ```
    python grid_color_reduction.py <image_path> <num_columns> --output <output_image_name>
    ```
    - <image_path>: Path to the input image file.
    - <num_columns>: The number of columns in the grid.
    - <output_image_name>: The name of the output image file (optional, default is output_date_time.png).
  
    Example:
    ```
    python grid_color_reduction.py example_image.png 100 --output cross_stitch_pattern.png 
    ```

How It Works
1. **Image Processing**: The image is divided into a grid based on the specified number of columns. Each grid box is filled with the most common or mean color found in that section of the image.
2. **User Input**: You provide the number of columns, and the program calculates the grid size based on the image width.
3. **Output**: The result is a new image, where each section of the grid is a color block representing the original image's dominant color.

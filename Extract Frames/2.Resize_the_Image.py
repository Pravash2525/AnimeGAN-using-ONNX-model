
import os
from PIL import Image

# =========================================================================
# mention the size of image in kbs
max_size_kb = 80
# =========================================================================

# Paths to input and output directories
input_directory = "./img_sequences/"
# output_directory = input_directory
output_directory = "./output/"

# Function to resize and save images
def resize_images(input_dir, output_dir):            # change the img_size if need
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each file in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Open the image
        with Image.open(input_path) as img:
            # Calculate the compression quality to achieve the desired file size
            img_quality = 100
            while True:
                # Save the image with the current compression quality
                img.save(output_path, quality=img_quality)

                # Check if the file size is less than the maximum allowed size
                if os.path.getsize(output_path) <= max_size_kb * 1024:
                    break

                # If not, reduce the quality and try again
                img_quality -= 5

            print(f"Resized '{filename}' with quality {img_quality}%")

# Call the function to resize images
resize_images(input_directory, output_directory)




# import os
# from PIL import Image

# # Input and output directories
# input_directory = "./img_sequences/"
# output_directory = "./output/"
# target_file_size_kb = 100                # Target file size in kilobytes

# # Function to process images and reduce file size
# def process_images(input_dir, output_dir, target_size_kb):
#     # Create the output directory if it doesn't exist
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

# # ==========================================================================================================
#     # Process each image in the input directory
#     for filename in os.listdir(input_dir):
#         if filename.endswith(('.jpg', '.jpeg', '.png')):  # Process only image files
#             input_path = os.path.join(input_dir, filename)
#             output_path = os.path.join(output_dir, filename)

#             # Open the image
#             image = Image.open(input_path)

#             # Reduce file size
#             while os.path.getsize(output_path) / 1024 > target_size_kb:
#                 # Resize the image to reduce dimensions
#                 width, height = image.size
#                 new_width = int(width * 0.9)  # Reduce width by 10%
#                 new_height = int(height * 0.9)  # Reduce height by 10%
#                 image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)    # PIL.Image.LANCZOS or PIL.Image.Resampling.LANCZOS

#                 # Save the image with reduced quality
#                 image.save(output_path, optimize=True, quality=85)  # Adjust quality as needed

#             print(f"Processed: {filename} -> {output_path}")


# # Process images
# process_images(input_directory, output_directory, target_file_size_kb)






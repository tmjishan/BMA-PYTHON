import os
from PIL import Image

def convert_and_reduce_to_webp(image_path, quality=90):
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        return

    try:
        # Open the image
        with Image.open(image_path) as img:
            # Grab the directory and filename, dropping the original extension for .webp output
            dir_name, full_filename = os.path.split(image_path)
            filename, _ = os.path.splitext(full_filename)
            
            # Setting the output extension always to .webp
            output_filename = f"{filename}_reduced.webp"
            output_path = os.path.join(dir_name, output_filename)
            
            # Check image mode for transparency (RGBA/LA) support in WebP.
            # Good for safety and optimal compression.
            if img.mode in ('RGBA', 'LA') and quality == 90:
                # Set lossless to True if quality condition is met
                lossless = True
            else:
                lossless = False
            
            # --- FILE SIZE CHECK CONDITION ---
            # os.path.getsize() returns file size in Bytes. 
            # 200 KB = 200 * 1024 Bytes = 204800 Bytes
            file_size_bytes = os.path.getsize(image_path)
            
            if file_size_bytes >= (600 * 1024):
                print(f"Image size is greater than 600KB ({file_size_bytes / 1024:.2f} KB). Resizing to 1/6...")
                # Optional: Resize the image dimensions to 1/6 of original size
                new_size = (img.width // 6, img.height // 6)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            elif file_size_bytes >= (200 * 1024):
                print(f"Image size is greater than 200KB ({file_size_bytes / 1024:.2f} KB). Resizing to 1/2...")
                # Optional: Resize the image dimensions to 1/2 of original size
                new_size = (img.width // 2, img.height // 2)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

           
            else:
                print(f"Image size is {file_size_bytes / 1024:.2f} KB (<= 200KB). Skipping resize to maintain quality.")
            
            # Explicitly specifying format='WEBP' while saving
            # method=6 provides the best compression quality (slowest but most effective)
            img.save(
                output_path, 
                format='WEBP', 
                optimize=True, 
                quality=quality, 
                method=6,
                lossless=lossless
            )
            
            print(f"Success! Converted & Reduced image saved to:\n{output_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get the image path from the terminal input
    user_input = input("Enter the path to the image file: ").strip()
    
    # Remove surrounding quotes if the user dragged and dropped the file
    user_input = user_input.strip("'\"")
    
    convert_and_reduce_to_webp(user_input)
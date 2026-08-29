import os
from PIL import Image

def convert_and_reduce_to_jpeg(image_path, quality=85): # JPEG-এর জন্য 85 quality স্ট্যান্ডার্ড
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        return

    try:
        # Open the image
        with Image.open(image_path) as img:
            # Grab the directory and filename
            dir_name, full_filename = os.path.split(image_path)
            filename, _ = os.path.splitext(full_filename)
            
            # Setting the output extension to .jpg
            # output_filename = f"{filename}_reduced.jpg"
            output_filename = f"{filename}.jpg"
            output_path = os.path.join(dir_name, output_filename)
            
            # File size check in Bytes
            file_size_bytes = os.path.getsize(image_path)
            current_img = img

            # Resizing logic based on your requirements
            if file_size_bytes >= (600 * 1024):
                print(f"Image size is greater than 600KB ({file_size_bytes / 1024:.2f} KB). Resizing to 1/6...")
                new_size = (img.width // 6, img.height // 6)
                current_img = img.resize(new_size, Image.Resampling.LANCZOS)

            elif file_size_bytes >= (200 * 1024):
                print(f"Image size is greater than 200KB ({file_size_bytes / 1024:.2f} KB). Resizing to 1/2...")
                new_size = (img.width // 2, img.height // 2)
                current_img = img.resize(new_size, Image.Resampling.LANCZOS)
            else:
                print(f"Image size is {file_size_bytes / 1024:.2f} KB (<= 200KB). Skipping resize.")

            # --- JPEG TRANSPARENCY HANDLING ---
            # RGBA বা LA mode থাকলে background white করে RGB-তে convert করতে হবে
            if current_img.mode in ('RGBA', 'LA', 'P'):
                print("Transparency detected. Converting to RGB with white background...")
                background = Image.new("RGB", current_img.size, (255, 255, 255))
                # Paste the image over the white background using alpha channel as mask
                background.paste(current_img, mask=current_img.split()[3] if current_img.mode == 'RGBA' else None)
                current_img = background
            elif current_img.mode != 'RGB':
                current_img = current_img.convert('RGB')
            
            # Explicitly specifying format='JPEG'
            current_img.save(
                output_path, 
                format='JPEG', 
                optimize=True, 
                quality=quality
            )
            
            final_size = os.path.getsize(output_path) / 1024
            print(f"Success! Converted & Reduced image saved to:\n{output_path}")
            print(f"Original Size: {file_size_bytes / 1024:.2f} KB | New Size: {final_size:.2f} KB")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_input = input("Enter the path to the image file: ").strip()
    user_input = user_input.strip("'\"")
    
    # Running the function for JPEG
    convert_and_reduce_to_jpeg(user_input, quality=85)
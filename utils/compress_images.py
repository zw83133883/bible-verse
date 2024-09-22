from PIL import Image
import os

def compress_image(input_path, output_path, quality=85, target_size=(1080, 1920)):
    try:
        with Image.open(input_path) as img:
            resized_img = img.resize(target_size)
            resized_img.save(output_path, optimize=True, quality=quality)
    except Exception as e:
        print(f"Error compressing image: {e}")

def compress_images_in_directory(directory_path, output_directory, quality=85, target_size=(1080, 1920)):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for filename in os.listdir(directory_path):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, filename)
            compress_image(input_path, output_path, quality=quality, target_size=target_size)

if __name__ == "__main__":
    input_dir = "static/horoscope-images"
    output_dir = "static/compressed_images"
    compress_images_in_directory(input_dir, output_dir, quality=85, target_size=(1080, 1920))

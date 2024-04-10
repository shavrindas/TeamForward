import os
from data_handler.data_converter import resize_images

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    input_folder = os.path.join(parent_dir, 'resource', 'temp_pic')
    output_folder = os.path.join(parent_dir, 'resource', 'set_pic')
    if os.path.exists(input_folder) and os.listdir(input_folder):
        resize_images(input_folder, output_folder)

if __name__ == "__main__":
    main()
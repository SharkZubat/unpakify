import os
import sys
import argparse

def extract_pak_file(pak_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        with open(pak_file, 'rb') as pak:
            # Simulate the extraction process (replace with actual extraction logic)
            data = pak.read()
            # Write the data to the output folder (replace with actual file writing logic)
            output_file_path = os.path.join(output_folder, os.path.basename(pak_file))
            with open(output_file_path, 'wb') as out_file:
                out_file.write(data)
        print(f'Successfully extracted: {pak_file} to {output_folder}')
    except Exception as e:
        print(f'Failed to extract {pak_file}: {e}')

def main():
    parser = argparse.ArgumentParser(description='Unpakify Tool to extract normal and corrupted pak files.')
    parser.add_argument('-c', '--check', help='Pak file to be extracted', required=True)
    parser.add_argument('-f', '--folder', help='New folder name for extraction', required=False)
    
    args = parser.parse_args()
    
    pak_file = args.check
    if not args.folder:
        output_folder = os.path.splitext(pak_file)[0]
    else:
        output_folder = args.folder

    extract_pak_file(pak_file, output_folder)

if __name__ == "__main__":
    main()

import os
import sys
import argparse
import shutil

def extract_pak_file(pak_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        # Assuming "unpakify" is a command line tool to extract .pak files
        os.system(f'unpakify extract "{pak_file}" "{output_folder}"')
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

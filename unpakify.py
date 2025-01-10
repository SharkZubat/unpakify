import os
import sys
import argparse
import subprocess

def extract_pak_file(pak_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        result = subprocess.run(['unpakify', 'extract', pak_file, output_folder], check=True, capture_output=True, text=True)
        print(f'Successfully extracted: {pak_file} to {output_folder}')
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Failed to extract {pak_file}: {e}')
        print(e.stderr)
    except FileNotFoundError:
        print('Error: unpakify command not found. Make sure the unpakify tool is installed and available in your system\'s PATH.')

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

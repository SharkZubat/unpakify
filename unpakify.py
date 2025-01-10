import os
import sys
import argparse
import struct

def extract_pak_file(pak_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        with open(pak_file, 'rb') as pak:
            # Read the pak file header (assuming a specific format, adjust as needed)
            header = pak.read(12)  # Example header size
            num_files = struct.unpack('I', header[8:12])[0]  # Example unpacking

            for _ in range(num_files):
                # Read file entry metadata (adjust based on actual format)
                entry_header = pak.read(24)  # Example entry size
                file_name_size = struct.unpack('I', entry_header[:4])[0]
                file_name = pak.read(file_name_size).decode('utf-8')

                # Create directories if needed
                file_path = os.path.join(output_folder, file_name)
                if file_name.endswith('/'):
                    os.makedirs(file_path, exist_ok=True)
                    continue

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Read and write file content
                file_size = struct.unpack('I', entry_header[16:20])[0]  # Example unpacking
                file_data = pak.read(file_size)
                with open(file_path, 'wb') as out_file:
                    out_file.write(file_data)

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

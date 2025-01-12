import os
import sys
import argparse
import struct

def sanitize_file_name(file_name, max_length=255):
    # Replace invalid characters with an underscore and limit length
    sanitized_name = ''.join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in file_name)[:max_length]
    # Further limit the length of the file name to avoid errors
    sanitized_name = sanitized_name[:max_length]
    print(f"Sanitized file name: {sanitized_name}")
    return sanitized_name

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
                file_name_bytes = pak.read(file_name_size)

                try:
                    file_name = file_name_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    file_name = file_name_bytes.decode('latin1')

                file_name = sanitize_file_name(file_name)

                # Ensure the file path is within acceptable limits
                file_path = os.path.join(output_folder, file_name[:max_length-100])
                if len(file_path) > 255:
                    file_path = file_path[:255]
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

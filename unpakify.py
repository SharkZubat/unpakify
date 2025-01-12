import os
import sys
import argparse
import struct
import string

def sanitize_file_name(file_name, max_length=255):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_name = ''.join(c if c in valid_chars else '_' for c in file_name)
    sanitized_name = sanitized_name[:max_length].rstrip(". ")
    print(f"Sanitized file name: {sanitized_name}")
    return sanitized_name

def extract_pak_file(pak_file, output_folder, max_length=255):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    try:
        with open(pak_file, 'rb') as pak:
            header = pak.read(12)
            if len(header) < 12:
                raise Exception("Header too small")
            num_files = struct.unpack('I', header[8:12])[0]

            for _ in range(num_files):
                entry_header = pak.read(24)
                if len(entry_header) < 24:
                    raise Exception("Entry header too small")
                file_name_size = struct.unpack('I', entry_header[:4])[0]
                if file_name_size > 1000:  # Adjust this threshold as needed
                    print(f"Warning: Unusually large file name size ({file_name_size} bytes). Skipping entry.")
                    pak.seek(20, os.SEEK_CUR)  # Skip the rest of the entry
                    continue
                file_name_bytes = pak.read(file_name_size)
                if len(file_name_bytes) < file_name_size:
                    print(f"Warning: Expected {file_name_size} bytes for file name but got {len(file_name_bytes)} bytes. Skipping entry.")
                    continue

                try:
                    file_name = file_name_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    file_name = file_name_bytes.decode('latin1')

                file_name = sanitize_file_name(file_name, max_length)

                file_path = os.path.join(output_folder, file_name)
                if len(file_path) > 255:
                    file_path = file_path[:255]
                if file_name.endswith('/'):
                    os.makedirs(file_path, exist_ok=True)
                    continue

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                file_size = struct.unpack('I', entry_header[16:20])[0]
                with open(file_path, 'wb') as out_file:
                    while file_size > 0:
                        chunk_size = min(file_size, 1024 * 1024)  # Read in 1MB chunks
                        file_data = pak.read(chunk_size)
                        if not file_data:
                            raise Exception("File data too small")
                        out_file.write(file_data)
                        file_size -= len(file_data)

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

    extract_pak_file(pak_file, output_folder, max_length=255)

if __name__ == "__main__":
    main()

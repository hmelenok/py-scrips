import os

def get_unique_chars_from_files(directory, output_file):
    unique_chars = set()

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                unique_chars.update(text)
    
    # Sort the unique characters
    sorted_unique_chars = sorted(unique_chars)
    
    # Write the sorted unique characters to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for char in sorted_unique_chars:
            file.write(char)

    print(f"Unique characters have been written to {output_file}")

# Set the directory path and output file path
directory_path = 'training-annotations'  # Replace with your directory path
output_file_path = 'unique_chars.txt'  # Replace with your desired output file path

# Call the function to get unique characters and write them to a file
get_unique_chars_from_files(directory_path, output_file_path)

import os

def rename_files(directory, old_extension, new_extension):
    for filename in os.listdir(directory):
        if filename.endswith(old_extension):
            # Define the new filename
            new_filename = filename.replace(old_extension, new_extension)
            # Get the full file paths
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed: {old_file} to {new_file}")

# Set the directory path
directory_path = 'training-annotations'  # Replace with your directory path

# Call the function to rename files
rename_files(directory_path, '.png', '.txt')

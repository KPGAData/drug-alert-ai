import os
import mimetypes

def get_file_type(file_path):
    """
    Determine the type of file based on its extension and content.
    
    Args:
    file_path (str): Path to the file
    
    Returns:
    str: Description of the file type
    """
    # Get the file extension
    _, extension = os.path.splitext(file_path)
    
    # Use mimetypes to guess the file type
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if extension:
        return f"File extension: {extension}"
    elif mime_type:
        return f"MIME type: {mime_type}"
    else:
        return "Unknown file type"

def test_file_types():
    """
    Test the get_file_type function with various file types.
    """
    test_files = [
        "document.txt",
        "image.jpg",
        "spreadsheet.xlsx",
        "program.py",
        "webpage.html",
        "unknown_file"
    ]
    
    for file in test_files:
        file_type = get_file_type(file)
        print(f"File: {file} - {file_type}")

# Run the test
if __name__ == "__main__":
    test_file_types()
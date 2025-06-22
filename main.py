from google import genai
from google.genai import types
import requests
import pathlib
from PIL import Image, ExifTags
import argparse
from datetime import datetime
import os
import shutil
import mimetypes

"""
This program intelligently reads the contents of your files, then automatically applies meaningful, 
consistent naming—transforming messy, cryptic filenames like IMG_1234.jpg into structured, 
descriptive names that reflect the actual content.
"""

Key = os.environ['google_api_key']

client = genai.Client(api_key=Key)
image_dir="src"
root_directory = os.getcwd()    # set the programs working directory
root_img_directory= rf"{root_directory}/{image_dir}" #Set the root directory for the images
os.makedirs("renamed", exist_ok=True)
dest_directory=rf"{root_directory}/renamed/"
mimetypes.init()


image_prompt = """
You are an intelligent assistant whose task is to **rename image files** based on their visual content. For each image provided:

1. Analyze its content: identify main objects, scene, context, and any visible text or metadata.
2. Generate a concise, descriptive filename in **snake_case** or **PascalCase**, with lowercase letters, no spaces, and no special characters. Use underscores (_) between parts if snake_case.
3. If the image has a recognizable date (e.g., on a sign, receipt image, screenshot timestamp), include it in `YYYY-MM-DD` format at the start.
4. Otherwise omit the date. Always include a short contextual description (2–4 words) from the content. Optional tags like `sunset`, `invoice`, `diagram`, `screenshot`, `group_photo`, etc.
5. Append the original file extension (e.g., `.jpg`, `.png`).

**Output format**: Return **only the new filename** (with extension), without extra punctuation, commentary, or file path.

---

**Examples**:

- Input: image of a coffee cup on a receipt dated June 10, 2025 → Output: `2025-06-10_coffee_receipt.jpg`
- Input: screenshot of an error dialog from Windows → Output: `windows_error_dialog.png`
- Input: photo of a family at the beach → Output: `family_beach_photo.jpg`
- Input: diagram showing network topology → Output: `network_topology_diagram.png`

---

Respond with just the filename. Do not explain your reasoning.```
"""

def understandImage(image_path, mime="image/jpeg", extra=""):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image = types.Part.from_bytes(data=image_bytes, mime_type=mime)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"{image_prompt} here are some extra details about the image(if there was any): {extra}", image],
    )
    return str(response.text)

def understandDocument(path, mime, extra=""):
    """
    PDF - application/pdf
    JavaScript - application/x-javascript, text/javascript
    Python - application/x-python, text/x-python
    TXT - text/plain
    HTML - text/html
    CSS - text/css
    Markdown - text/md
    CSV - text/csv
    XML - text/xml
    RTF - text/rtf
    """
    # Retrieve and encode the file byte
    # filepath = pathlib.Path('./src/embedded-images.pdf')
    filepath = pathlib.Path(path)
    
    #Ensure correct prompt engineering to get correct filename output
    prompt = f"""You are a seasoned data management and file organization expert with deep expertise in standardizing file naming conventions 
                for optimal retrieval and archival. I need your specialized knowledge to analyze the content of the provided file {filepath} 
                and generate a standardized, descriptive filename that adheres to best practices.  

            Please structure the filename as follows, ensuring it captures all critical metadata:  

            - **Topic**: Identify the primary subject or category of the file (e.g., Report, Invoice, Dataset).  
            - **Content**: Specify the detailed content or context (e.g., Sales_Q2, SurveyResponses, Wedding_Smiths).  
            - **Date/Sequence**: If applicable, include a relevant date (YYYY-MM-DD) or sequence number (e.g., 001).  
            - **Filetype**: Append the correct file extension (e.g., .pdf, .csv, .jpg).  

            Apply your expertise in metadata extraction and naming conventions to ensure the filename is:  
            - Clear, concise, and machine-readable.  
            - Consistent with industry standards for file organization.  
            - Optimized for searchability and archival purposes.  

            Here are some extra details about the image(if the user provided): {extra}

            Your output must strictly follow the format: `topic-content.filetype` (e.g., `Invoice_Apple_2025_Q1.pdf`). Do not include additional text or explanations—only the standardized filename.
                """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type=mime,
            ),
        prompt]
    )
    return str(response.text)

def getExifData(path):
    if path.endswith("jpg"):
        img = Image.open(path)  #Open the image for Editing
        try:
            exif = img.getexif() 
            # Date configuring
            dateAndTime = exif[306]    #306 is date and time
            inputFormat = "%Y:%m:%d %H:%M:%S" #specify the format to pass it to datetime
            date_object = datetime.strptime(dateAndTime, inputFormat) #understands the date and time
            dateStruct = "%Y-%B-%d"  #naming structure of the image file 
            date = date_object.strftime(dateStruct)
            return date
        except:
            return
    else:
        try:
            stats = os.stat(path)
            modification_time = datetime.fromtimestamp(stats.st_mtime)
            inputFormat = "%Y-%m-%d %H:%M:%S.%f" #specify the format to pass it to datetime
            date_object = datetime.strptime(str(modification_time), inputFormat) #understands the date and time
            dateStruct = "%Y-%B-%d"  #naming structure of the image file 
            date = date_object.strftime(dateStruct)
            return date
        except Exception as e:
            print(e)

def get_mime_type(filename: str) -> str:
    # Normalize by extension, lowercased
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # Custom mappings for your list
    custom = {
        '.pdf': 'application/pdf',
        '.js':  'application/x-javascript',
        '.py':  'application/x-python',
        '.txt': 'text/plain',
        '.html':'text/html',
        '.htm': 'text/html',
        '.css': 'text/css',
        '.md':  'text/md',
        '.csv': 'text/csv',
        '.xml': 'text/xml',
        '.rtf': 'text/rtf',
    }
    if ext in custom:
        return custom[ext]

    # Fallback to standard library
    mime, _ = mimetypes.guess_type(filename, strict=False)
    if mime:
        return mime

    # Final fallback
    return 'text/plain'

def rename(source):
    source_dir = source
    print("Renaming Files...")
    for original_filename in os.listdir(source_dir):
        path = os.path.join(source_dir, original_filename)
        exif = getExifData(path)
        mime = get_mime_type(original_filename)
        if original_filename.lower().endswith(("jpg", "png", "jpeg", "webp")):
            # file name generation
            dest_filename = understandImage(image_path=path, mime=mime, extra=exif).strip()
            dest_filename = str(dest_filename)
        else:
            # file name generation
            dest_filename = understandDocument(path=path, mime=mime, extra=exif).strip()
            dest_filename = str(dest_filename)

        # accessing folders and files for moving
        original_full_path = os.path.join(root_img_directory, original_filename) #get the full path to the original image
        dest_full_path = os.path.join(dest_directory, dest_filename)
        
        # File Moving            
        shutil.copy(original_full_path, dest_full_path)    #move the file to the folder
        print(f"{original_filename} --> {dest_filename}")
    

def parse_args():
    parser = argparse.ArgumentParser(
                    prog='AI Based File Renamer ',
                    description='AI Based File Renamer',
                    epilog="""Renames all your images, PDF's and PlainText Document files in the source directory with NLP and OCR and places them in the source directory 
                    """)
    parser.add_argument('-s', '--source')      # option that takes a value

    return parser.parse_args()

def main():
    args=parse_args()
    source = args.source
    try:
        if os.path.isdir(source):
            rename(source)
            print(f"Folder 'Rename' created. Your renamed files are in this folder.\nHere is the link to the directory: {dest_directory}")
        else:
            print("Invalid folder! ")
    except FileNotFoundError:
        print("The Specified file was not found!")
    # except Exception as e:
    #     print(e)

if __name__=="__main__":
    main()

#rename()
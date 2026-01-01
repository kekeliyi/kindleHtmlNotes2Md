import os
import re
import hashlib
import base64

def clean_filename(filename):
    """Sanitize input to be safe for filenames."""
    # Keep it simple, alphanumeric and some common safe chars
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def get_short_image_name(book_title, index, ext):
    """Generate a short, safe filename for images."""
    # Use MD5 hash of title to keep filename unique but short
    title_hash = hashlib.md5(book_title.encode('utf-8')).hexdigest()[:8]
    return f"img_{title_hash}_{index}.{ext}"

def extract_base64_image(img_tag, book_title, index, images_dir):
    """
    Extracts base64 data from an img tag, saves it to disk, 
    and returns the relative path for Markdown.
    """
    src = img_tag.get('src', '')
    if not src.startswith('data:image'):
        return None

    try:
        # Format usually: data:image/jpeg;base64,.....
        header, encoded = src.split(',', 1)
        ext = 'jpg'
        if 'png' in header:
            ext = 'png'
        
        file_name = get_short_image_name(book_title, index, ext)
        file_path = os.path.join(images_dir, file_name)
        
        # Ensure images directory exists
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        with open(file_path, "wb") as f:
            f.write(base64.b64decode(encoded))
            
        return f"images/{file_name}"
    except Exception as e:
        print(f"Error extracting image: {e}")
        return None

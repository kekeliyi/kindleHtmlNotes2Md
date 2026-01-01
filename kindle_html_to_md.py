import os
import re
import base64
import hashlib
from bs4 import BeautifulSoup

# Configuration
INPUT_DIR = "/Users/yili/Library/Mobile Documents/iCloud~md~obsidian/Documents/YL_ios/05_Books/01_KindleNotes"
OUTPUT_DIR = "/Users/yili/Library/Mobile Documents/iCloud~md~obsidian/Documents/YL_ios/05_Books/Books2025"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

def clean_filename(filename):
    """Sanitize input to be safe for filenames."""
    # Keep it simple, alphanumeric and some common safe chars
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def get_short_image_name(book_title, index, ext):
    """Generate a short, safe filename for images."""
    # Use MD5 hash of title to keep filename unique but short
    title_hash = hashlib.md5(book_title.encode('utf-8')).hexdigest()[:8]
    return f"img_{title_hash}_{index}.{ext}"

def extract_base64_image(img_tag, book_title, index):
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
        file_path = os.path.join(IMAGES_DIR, file_name)
        
        # Ensure images directory exists
        if not os.path.exists(IMAGES_DIR):
            os.makedirs(IMAGES_DIR)

        with open(file_path, "wb") as f:
            f.write(base64.b64decode(encoded))
            
        return f"images/{file_name}"
    except Exception as e:
        print(f"Error extracting image: {e}")
        return None

def process_file(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    
    # Extract Title
    title_div = soup.find('div', class_='bookTitle')
    if not title_div:
        print("No book title found, skipping.")
        return
        
    book_title = title_div.get_text(strip=True)
    clean_title = clean_filename(book_title)
    
    # Prepare Output
    md_content = []
    
    body_container = soup.find('div', class_='bodyContainer')
    if not body_container:
        print("No bodyContainer found.")
        return

    img_count = 0
    current_section = None
    
    # We loop through all relevant elements in order
    for element in body_container.children:
        if element.name == 'div':
            classes = element.get('class', [])
            
            if 'sectionHeading' in classes:
                # Top level Chapter Header
                # Usage in Kindle HTML: usually "Chapter X"
                text = element.get_text(strip=True)
                md_content.append(f"\n# {text}\n")
                current_section = None # Reset subsection on new chapter
                
            elif 'noteHeading' in classes:
                # Info: Highlight(color) - Section Title > Page ...
                # Or: Note - Section Title > Page ...
                raw_text = element.get_text(strip=True)
                
                # Regex to find section title:
                # Pattern: (Highlight(...) - | Note - ) (Captured Title) ( > Page ...)
                # Note: The separator ' > ' seems standard for Kindle exports.
                match = re.search(r'^(?:Highlight\(.*?\)|Note)\s*-\s*(.*?)\s*>\s*', raw_text)
                
                if match:
                    section_title = match.group(1).strip()
                    
                    # If this is a new section title we haven't seen in this block, print it
                    # But suppress if it's just the extracted chapter title or empty
                    if section_title and section_title != current_section:
                        md_content.append(f"\n## {section_title}\n")
                        current_section = section_title
                
            elif 'noteText' in classes:
                text = element.get_text(strip=True)
                
                # Check previous element to determine if this is a "Note" or "Highlight"
                prev = element.find_previous_sibling('div')
                is_note = False
                if prev and 'noteHeading' in prev.get('class', []):
                    prev_text = prev.get_text(strip=True)
                    if prev_text.strip().startswith('Note'):
                        is_note = True
                
                if is_note:
                    md_content.append(f"- Note: {text}")
                else:
                    md_content.append(f"- {text}")
                    
            elif 'notebookGraphic' in classes:
                # Images (Handwritten notes)
                img = element.find('img')
                if img:
                    img_path = extract_base64_image(img, book_title, img_count)
                    if img_path:
                        # Add a newline for spacing
                        md_content.append(f"\n![Handwritten Note]({img_path})\n")
                        img_count += 1
                        
    # Save file
    output_path = os.path.join(OUTPUT_DIR, f"{clean_title}.md")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    print(f"Created: {output_path}")

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Input directory not found: {INPUT_DIR}")
        return

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.html')]
    if not files:
        print("No HTML files found.")
        return
        
    for filename in files:
        process_file(os.path.join(INPUT_DIR, filename))

if __name__ == "__main__":
    main()

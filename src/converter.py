import os
import re
from bs4 import BeautifulSoup
from .utils import clean_filename, extract_base64_image

class KindleConverter:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        
        # Ensure output directories exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

    def convert_all(self):
        """Process all HTML files in the input directory."""
        if not os.path.exists(self.input_dir):
            print(f"Input directory not found: {self.input_dir}")
            return

        files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.html')]
        if not files:
            print("No HTML files found.")
            return
            
        print(f"Found {len(files)} HTML files. Starting conversion...")
        for filename in files:
            self.process_file(os.path.join(self.input_dir, filename))
        print("Conversion complete.")

    def process_file(self, filepath):
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
        # Some exports might just have body without bodyContainer, but we stick to previous logic for now
        # If needed, we can add fallbacks here.
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
                        # Pass images_dir to the helper
                        img_path = extract_base64_image(img, book_title, img_count, self.images_dir)
                        if img_path:
                            # Add a newline for spacing
                            md_content.append(f"\n![Handwritten Note]({img_path})\n")
                            img_count += 1
                            
        # Save file
        output_path = os.path.join(self.output_dir, f"{clean_title}.md")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
        print(f"Created: {output_path}")

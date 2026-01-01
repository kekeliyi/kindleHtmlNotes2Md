# Kindle HTML Notes to Markdown Converter

This tool converts Kindle Notes exported as HTML files into clean, structured Markdown files suitable for Obsidian or other Markdown note-taking apps. It also extracts images (handwritten notes) from the HTML and saves them locally.

## Why this tool?

Existing solutions like Obsidian plugins or generic HTML converters didn't meet my specific needs, leading to the creation of this custom repository. The main motivations are:

1.  **Support for Sideloaded Books**: many Obsidian plugins only fetch notes for books purchased directly from Amazon. This tool processes the HTML files exported directly from the Kindle app, working seamlessly for imported `.epub` or other sideloaded documents.
2.  **Handwritten Note Support**: Standard converters often ignore the handwritten notes and sketches made on the Kindle Scribe. This tool extracts these images (base64 encoded in the HTML) and embeds them into the Markdown notes.
3.  **Custom Aesthetics & Structure**: Generic converters often produce cluttered or unappealing output. This tool provides a highly structured, aesthetically pleasing Markdown format with clean headers and bullet points, exactly how I want them.

## Features

- **Parses Kindle HTML Exports**: Reads standard Kindle HTML note exports.
- **Structured Markdown Output**: 
  - Converts Book Title to Filename.
  - Extracts Chapters as H1 (`#`).
  - Extracts Section Headings (from "Highlight ... - Section > Page") as H2 (`##`).
  - Formats Highlights and Notes as bullet points.
- **Image Extraction**: 
  - Detects base64 encoded images (handwritten notes).
  - Saves them as `.jpg` or `.png` files in an `images/` subdirectory.
  - Inserts markdown image links (`![...]`) in the logical position.
- **Batch Processing**: Converts all `.html` files in the configured input directory.

## Project Structure

```
kindleHtmlNotes2Md/
├── config.json           # Local configuration (ignored by git)
├── config.example.json   # Template configuration
├── requirements.txt      # Python dependencies
├── run.py                # Entry point script
├── src/                  # Source code
│   ├── parser.py         # Parsing logic
│   ├── converter.py      # Conversion orchestration
│   ├── utils.py          # Helper functions
│   └── main.py           # Main logic
```

## Setup & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    - Copy `config.example.json` to `config.json`:
      ```bash
      cp config.example.json config.json
      ```
    - Edit `config.json` and set your paths:
      ```json
      {
          "input_dir": "/path/to/your/kindle/html/notes",
          "output_dir": "/path/to/your/output/folder"
      }
      ```

3.  **Run**:
    ```bash
    python run.py
    ```

## Output

The tool will generate `.md` files in the specified `output_dir`. Images used in the notes will be saved in `output_dir/images`.

## License

[MIT](LICENSE)

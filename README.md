# Kindle HTML Notes to Markdown Converter

This tool converts Kindle Notes exported as HTML files into clean, structured Markdown files suitable for Obsidian or other Markdown note-taking apps. It also extracts images (handwritten notes) from the HTML and saves them locally.

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

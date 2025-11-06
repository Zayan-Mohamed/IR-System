# Document Reader MVP

A simple document search system that allows users to search for words and see how many times they appear in each document.

## Features

✅ **Document Loading**: Supports .txt and .pdf files  
✅ **Word Search**: Search for any word across all documents  
✅ **Word Counting**: Shows frequency of words per document  
✅ **Multiple Interfaces**: Command line and web interface  
✅ **Statistics**: View document statistics and word counts

## Quick Start

1. **Activate Virtual Environment**

   ```bash
   source venv/bin/activate
   ```

2. **Run CLI Version**

   ```bash
   python cli.py
   ```

3. **Run Web Interface**
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage Examples

### CLI Commands

- `search apple` - Search for the word "apple"
- `add` - Add a new document interactively
- `stats` - Show document statistics
- `words` - Show all unique words
- `help` - Show available commands
- `quit` - Exit the program

### Web Interface

1. Open browser to the Streamlit URL (usually http://localhost:8501)
2. Use the search box to find words
3. Add documents via the sidebar
4. View statistics in real-time

## Project Structure

```
doc-reader/
├── venv/                    # Virtual environment
├── documents/               # Document storage folder
│   ├── fruits.txt          # Sample document
│   ├── vehicles.txt        # Sample document
│   └── technology.txt      # Sample document
├── document_processor.py   # Core processing logic
├── cli.py                  # Command line interface
├── streamlit_app.py        # Web interface
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Technical Details

### Core Components

1. **DocumentProcessor**: Handles document loading, text preprocessing, and word counting
2. **CLI Interface**: Simple command-line interaction
3. **Web Interface**: Modern Streamlit-based UI

### Text Processing

- Converts text to lowercase
- Removes punctuation and special characters
- Tokenizes using NLTK (with fallback to simple split)
- Counts word frequencies per document

### Supported Formats

- `.txt` files (UTF-8 and Latin-1 encoding)
- `.pdf` files (using PyPDF2)

## Example Output

```
Search for: apple
✅ 'apple' found in 2 document(s):

  📄 fruits.txt: 6 times
  📄 recipes.txt: 2 times

📊 Total occurrences: 8
```

## Dependencies

- `nltk==3.8.1` - Natural language processing
- `streamlit==1.29.0` - Web interface
- `PyPDF2==3.0.1` - PDF reading

## Installation

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## MVP Goals Achieved

✅ Load and analyze documents  
✅ Let users search for words  
✅ Show how often words appear per document  
✅ Basic UI and command-line interaction  
✅ Simple and clean codebase

## Future Enhancements

- Support for more file formats (DOCX, RTF)
- Advanced search (phrases, regex)
- Document similarity analysis
- Export search results
- API endpoints

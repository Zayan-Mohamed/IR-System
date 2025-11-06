"""
Document Reader MVP - Core Document Processing Module

This module handles document loading, preprocessing, and word counting.
"""

import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import nltk
from PyPDF2 import PdfReader

class DocumentProcessor:
    def __init__(self, documents_folder: str = "documents"):
        """Initialize the document processor."""
        self.documents_folder = documents_folder
        self.word_counts = {}  # Store word counts per document
        self.documents = {}    # Store document content
        self._ensure_nltk_data()
    
    def _ensure_nltk_data(self):
        """Download required NLTK data if not present."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text."""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters, keep only alphanumeric and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def _tokenize_and_count(self, text: str) -> Dict[str, int]:
        """Tokenize text and count word frequencies."""
        # Clean the text
        clean_text = self._clean_text(text)
        
        # Tokenize using NLTK
        try:
            tokens = nltk.word_tokenize(clean_text)
        except:
            # Fallback to simple split if NLTK fails
            print("NLTK Failed. Trying simple split")
            tokens = clean_text.split()
        
        # Count word frequencies
        word_count = defaultdict(int)
        for token in tokens:
            if len(token) > 1:  # Skip single characters
                word_count[token] += 1
        
        return dict(word_count)
    
    def _read_txt_file(self, file_path: str) -> str:
        """Read content from a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    def _read_pdf_file(self, file_path: str) -> str:
        """Read content from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def load_documents(self) -> int:
        """Load all documents from the documents folder."""
        if not os.path.exists(self.documents_folder):
            os.makedirs(self.documents_folder)
            print(f"Created documents folder: {self.documents_folder}")
            return 0
        
        loaded_count = 0
        
        for filename in os.listdir(self.documents_folder):
            file_path = os.path.join(self.documents_folder, filename)
            
            if os.path.isfile(file_path):
                content = ""
                
                if filename.lower().endswith('.txt'):
                    content = self._read_txt_file(file_path)
                elif filename.lower().endswith('.pdf'):
                    content = self._read_pdf_file(file_path)
                else:
                    print(f"Skipping unsupported file: {filename}")
                    continue
                
                if content.strip():
                    self.documents[filename] = content
                    self.word_counts[filename] = self._tokenize_and_count(content)
                    loaded_count += 1
                    print(f"Loaded: {filename}")
                else:
                    print(f"Warning: Empty content in {filename}")
        
        print(f"Total documents loaded: {loaded_count}")
        return loaded_count
    
    def add_document(self, name: str, content: str) -> bool:
        """Add a document directly with content."""
        if not content.strip():
            print("Error: Empty content provided")
            return False
        
        self.documents[name] = content
        self.word_counts[name] = self._tokenize_and_count(content)
        print(f"Added document: {name}")
        return True
    
    def search_word(self, word: str) -> List[Tuple[str, int]]:
        """Search for a word across all documents."""
        word = word.lower().strip()
        results = []
        
        for doc_name, word_count in self.word_counts.items():
            count = word_count.get(word, 0)
            if count > 0:
                results.append((doc_name, count))
        
        # Sort by count (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def search_phrase(self, phrase: str) -> List[Tuple[str, int]]:
        """Search for a phrase across all documents."""
        phrase = phrase.lower().strip()
        results = []
        
        for doc_name, content in self.documents.items():
            # Search in the original content, not tokenized words
            content_lower = content.lower()
            count = content_lower.count(phrase)
            if count > 0:
                results.append((doc_name, count))
        
        # Sort by count (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def search(self, query: str) -> List[Tuple[str, int]]:
        """Unified search method that handles both words and phrases."""
        query = query.strip()
        
        # If query contains spaces, treat as phrase
        if ' ' in query:
            return self.search_phrase(query)
        else:
            return self.search_word(query)
    
    def get_document_stats(self) -> Dict[str, Dict[str, int]]:
        """Get statistics for all documents."""
        stats = {}
        for doc_name, content in self.documents.items():
            word_count = self.word_counts[doc_name]
            stats[doc_name] = {
                'total_words': sum(word_count.values()),
                'unique_words': len(word_count),
                'characters': len(content)
            }
        return stats
    
    def get_all_words(self) -> List[str]:
        """Get all unique words across all documents."""
        all_words = set()
        for word_count in self.word_counts.values():
            all_words.update(word_count.keys())
        return sorted(list(all_words))
    
    def search_phrase_naive(self, phrase: str, text: str) -> int:
        """Naive string matching for phrase counting."""
        phrase = phrase.lower()
        text = text.lower()
        count = 0
        start = 0
        
        while True:
            pos = text.find(phrase, start)
            if pos == -1:
                break
            count += 1
            start = pos + 1
        
        return count

    def search_phrase_kmp(self, phrase: str, text: str) -> int:
        """KMP algorithm for phrase matching."""
        def build_lps(pattern):
            lps = [0] * len(pattern)
            length = 0
            i = 1
            
            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps
        
        phrase = phrase.lower()
        text = text.lower()
        
        if not phrase:
            return 0
        
        lps = build_lps(phrase)
        count = 0
        i = j = 0
        
        while i < len(text):
            if phrase[j] == text[i]:
                i += 1
                j += 1
            
            if j == len(phrase):
                count += 1
                j = lps[j - 1]
            elif i < len(text) and phrase[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        
        return count

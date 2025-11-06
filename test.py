#!/usr/bin/env python3
"""
Test script for Document Reader MVP
"""

from document_processor import DocumentProcessor

def test_document_processor():
    """Test the core functionality."""
    print("Testing Document Processor...")
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Load documents
    count = processor.load_documents()
    print(f" Loaded {count} documents")
    
    # Test search
    test_words = ['apple', 'car', 'technology', 'the']
    
    for word in test_words:
        results = processor.search_word(word)
        print(f"\n🔍 Search '{word}':")
        if results:
            for doc, count in results:
                print(f"{doc}: {count} times")
        else:
            print(f"Not found")
    
    # Show stats
    print(f"\n Statistics:")
    stats = processor.get_document_stats()
    for doc, stat in stats.items():
        print(f"   📄 {doc}: {stat['total_words']} words, {stat['unique_words']} unique")
    
    print(f"\n All tests completed!")

if __name__ == "__main__":
    test_document_processor()

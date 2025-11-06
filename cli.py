"""
Document Reader MVP - Command Line Interface

Simple CLI for searching words in documents.
"""

import sys
from document_processor import DocumentProcessor

class DocumentReaderCLI:
    def __init__(self):
        self.processor = DocumentProcessor()
    
    def display_banner(self):
        """Display welcome banner."""
        print("=" * 50)
        print("📘 DOCUMENT READER - MVP")
        print("=" * 50)
        print("Search for words across your documents!")
        print()
    
    def display_menu(self):
        """Display main menu options."""
        print("\nAvailable commands:")
        print("1. 'search <word>' - Search for a word")
        print("2. 'add' - Add a new document")
        print("3. 'stats' - Show document statistics")
        print("4. 'words' - Show all unique words")
        print("5. 'help' - Show this menu")
        print("6. 'quit' - Exit the program")
        print("-" * 50)
    
    def format_search_results(self, word: str, results, search_type="word"):
        """Format and display search results."""
        if not results:
            print(f"❌ '{word}' not found in any documents.")
            return
        
        print(f"✅ '{word}' found in {len(results)} document(s):")
        print()
        
        for doc_name, count in results:
            print(f"  📄 {doc_name}: {count} time{'s' if count > 1 else ''}")
        
        total_occurrences = sum(count for _, count in results)
        print(f"\n📊 Total occurrences: {total_occurrences}")
    
    def add_document_interactive(self):
        """Interactive document addition."""
        print("\n📝 Add New Document")
        print("-" * 20)
        
        name = input("Enter document name (e.g., 'my_doc.txt'): ").strip()
        if not name:
            print("❌ Invalid name.")
            return
        
        print("Enter document content (press Enter twice to finish):")
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            line = input()
            if line.strip() == "":
                empty_lines += 1
            else:
                empty_lines = 0
            lines.append(line)
        
        # Remove the extra empty lines at the end
        while lines and lines[-1] == "":
            lines.pop()
        
        content = "\n".join(lines)
        
        if self.processor.add_document(name, content):
            print(f"✅ Document '{name}' added successfully!")
        else:
            print("❌ Failed to add document.")
    
    def show_stats(self):
        """Display document statistics."""
        stats = self.processor.get_document_stats()
        
        if not stats:
            print("📭 No documents loaded.")
            return
        
        print(f"\n📊 Document Statistics ({len(stats)} documents)")
        print("-" * 40)
        
        for doc_name, doc_stats in stats.items():
            print(f"📄 {doc_name}:")
            print(f"   Total words: {doc_stats['total_words']}")
            print(f"   Unique words: {doc_stats['unique_words']}")
            print(f"   Characters: {doc_stats['characters']}")
            print()
    
    def show_all_words(self):
        """Display all unique words."""
        all_words = self.processor.get_all_words()
        
        if not all_words:
            print("📭 No words found.")
            return
        
        print(f"\n📚 All Unique Words ({len(all_words)} total)")
        print("-" * 40)
        
        # Display words in columns
        columns = 4
        for i, word in enumerate(all_words):
            print(f"{word:<15}", end="")
            if (i + 1) % columns == 0:
                print()
        
        if len(all_words) % columns != 0:
            print()
    
    def process_command(self, command: str):
        """Process user command."""
        command = command.strip()
        
        if command.lower().startswith('search '):
            query = command[7:].strip()  # Extract everything after "search "
            if query:
                results = self.processor.search(query)  # This should work
                search_type = "phrase" if ' ' in query else "word"
                self.format_search_results(query, results, search_type)
            else:
                print("❌ Please specify a word or phrase to search for.")
        
        elif command == 'add':
            self.add_document_interactive()
        
        elif command == 'stats':
            self.show_stats()
        
        elif command == 'words':
            self.show_all_words()
        
        elif command == 'help':
            self.display_menu()
        
        elif command == 'quit':
            return False
        
        else:
            print(f"❌ Unknown command: '{command}'")
            print("Type 'help' for available commands.")
        
        return True
    
    def run(self):
        """Main CLI loop."""
        self.display_banner()
        
        # Load documents
        print("🔄 Loading documents...")
        count = self.processor.load_documents()
        
        if count == 0:
            print("📁 No documents found in 'documents' folder.")
            print("You can add documents manually using the 'add' command.")
        
        self.display_menu()
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if not command:
                    continue
                
                if not self.process_command(command):
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break

def main():
    """Main entry point."""
    cli = DocumentReaderCLI()
    cli.run()

if __name__ == "__main__":
    main()

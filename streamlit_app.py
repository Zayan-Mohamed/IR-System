"""
Document Reader MVP - Streamlit Web Interface

Modern web interface for searching words in documents.
"""

import streamlit as st
import pandas as pd
from document_processor import DocumentProcessor

# Configure page
st.set_page_config(
    page_title="Document Reader MVP",
    page_icon="📘",
    layout="wide"
)

@st.cache_resource
def get_processor():
    """Get cached document processor instance."""
    return DocumentProcessor()

def load_documents():
    """Load documents and cache the processor."""
    processor = get_processor()
    count = processor.load_documents()
    return processor, count

def main():
    # Header
    st.title("📘 Document Reader MVP")
    st.markdown("### Search for words across your documents")
    
    # Initialize processor
    processor, doc_count = load_documents()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📁 Document Management")
        st.info(f"Documents loaded: {doc_count}")
        
        # Add new document
        with st.expander("➕ Add New Document"):
            doc_name = st.text_input("Document Name", placeholder="e.g., article.txt")
            doc_content = st.text_area("Document Content", height=150)
            
            if st.button("Add Document"):
                if doc_name and doc_content:
                    if processor.add_document(doc_name, doc_content):
                        st.success(f"Document '{doc_name}' added!")
                        st.rerun()
                    else:
                        st.error("Failed to add document")
                else:
                    st.error("Please provide both name and content")
        
        # Document statistics
        if st.button("📊 Refresh Stats"):
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Search")
        
        # Search interface
        search_word = st.text_input(
            "Enter word to search:",
            placeholder="e.g., apple",
            help="Search is case-insensitive"
        )
        
        if search_word:
            with st.spinner("Searching..."):
                # Change this line from:
                # results = processor.search_word(search_word)
                # To:
                results = processor.search(search_word)  # ✅ Use unified search
            
            if results:
                search_type = "phrase" if ' ' in search_word else "word"
                st.success(f"Found '{search_word}' in {len(results)} document(s)")
                
                # Display results
                df = pd.DataFrame(results, columns=["Document", "Count"])
                st.dataframe(df, use_container_width=True)
                
                # Chart
                if len(results) > 1:
                    st.bar_chart(df.set_index("Document"))
                
                # Total count
                total = sum(count for _, count in results)
                st.metric("Total Occurrences", total)
                
            else:
                st.warning(f"No matches found for '{search_word}'")
    
    with col2:
        st.header("📊 Statistics")
        
        stats = processor.get_document_stats()
        
        if stats:
            # Overall stats
            total_docs = len(stats)
            total_words = sum(s['total_words'] for s in stats.values())
            total_unique = len(processor.get_all_words())
            
            st.metric("Total Documents", total_docs)
            st.metric("Total Words", f"{total_words:,}")
            st.metric("Unique Words", f"{total_unique:,}")
            
            # Document details
            with st.expander("📄 Document Details"):
                for doc_name, doc_stats in stats.items():
                    st.subheader(doc_name)
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Words", doc_stats['total_words'])
                    with col_b:
                        st.metric("Unique", doc_stats['unique_words'])
                    with col_c:
                        st.metric("Chars", doc_stats['characters'])
        else:
            st.info("No documents loaded yet")
    
    # Footer
    st.markdown("---")
    st.markdown("**Document Reader MVP** - Search words across documents efficiently")

if __name__ == "__main__":
    main()

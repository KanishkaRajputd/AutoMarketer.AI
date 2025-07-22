import PyPDF2
import io
import streamlit as st


def extract_pdf_content(uploaded_file):
    """
    Extract text content from uploaded PDF file.
    
    Args:
        uploaded_file (streamlit.UploadedFile): Streamlit uploaded file object
        
    Returns:
        dict: Dictionary containing file info and extracted content
              Format: {'name': str, 'content': str, 'size': int, 'pages': int}
    """
    try:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        
        # Extract text from all pages
        extracted_text = ""
        total_pages = len(pdf_reader.pages)
        
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text() + "\n"
        
        # Clean up the extracted text
        cleaned_text = clean_extracted_text(extracted_text)
        
        # Return structured data
        return {
            'name': uploaded_file.name,
            'content': cleaned_text,
            'size': uploaded_file.size,
            'pages': total_pages,
            'type': uploaded_file.type
        }
        
    except Exception as e:
        st.error(f"Error extracting PDF content: {str(e)}")
        return {
            'name': uploaded_file.name,
            'content': f"Error extracting content from PDF: {str(e)}",
            'size': uploaded_file.size,
            'pages': 0,
            'type': uploaded_file.type
        }


def clean_extracted_text(text):
    """
    Clean and normalize extracted text from PDF.
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return "No text content found in PDF"
    
    # Remove excessive whitespace and normalize line breaks
    import re
    
    # Remove multiple consecutive whitespaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove excessive line breaks
    text = re.sub(r'\n+', '\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Ensure minimum content length
    if len(text.strip()) < 10:
        return "No meaningful text content found in PDF"
    
    return text


def validate_pdf_file(uploaded_file):
    """
    Validate uploaded PDF file before processing.
    
    Args:
        uploaded_file (streamlit.UploadedFile): Streamlit uploaded file object
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not uploaded_file:
        return False, "No file uploaded"
    
    # Check file type
    if uploaded_file.type != "application/pdf":
        return False, "File must be a PDF document"
    
    # Check file size (200MB limit)
    max_size = 200 * 1024 * 1024  # 200MB in bytes
    if uploaded_file.size > max_size:
        return False, f"File size ({uploaded_file.size / (1024*1024):.1f} MB) exceeds 200MB limit"
    
    # Check minimum size
    if uploaded_file.size < 100:  # Less than 100 bytes
        return False, "File appears to be empty or corrupted"
    
    return True, "Valid PDF file"


def get_pdf_metadata(uploaded_file):
    """
    Extract metadata from PDF file.
    
    Args:
        uploaded_file (streamlit.UploadedFile): Streamlit uploaded file object
        
    Returns:
        dict: PDF metadata information
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        
        metadata = {
            'pages': len(pdf_reader.pages),
            'title': '',
            'author': '',
            'subject': '',
            'creator': '',
            'producer': '',
            'creation_date': '',
            'modification_date': ''
        }
        
        # Extract metadata if available
        if pdf_reader.metadata:
            metadata.update({
                'title': pdf_reader.metadata.get('/Title', ''),
                'author': pdf_reader.metadata.get('/Author', ''),
                'subject': pdf_reader.metadata.get('/Subject', ''),
                'creator': pdf_reader.metadata.get('/Creator', ''),
                'producer': pdf_reader.metadata.get('/Producer', ''),
                'creation_date': str(pdf_reader.metadata.get('/CreationDate', '')),
                'modification_date': str(pdf_reader.metadata.get('/ModDate', ''))
            })
        
        return metadata
        
    except Exception as e:
        return {
            'pages': 0,
            'error': f"Could not extract metadata: {str(e)}"
        }


# Example usage and testing
if __name__ == "__main__":
    print("PDF Content Extraction Utility")
    print("This module provides functions to extract text content from PDF files.")
    print("Use extract_pdf_content(uploaded_file) to process Streamlit uploaded files.") 
import re
import os


def sanitize_collection_name(filename):
    """
    Sanitize filename to create a valid ChromaDB collection name.
    
    ChromaDB collection names must:
    - Be 3-63 characters long
    - Start and end with alphanumeric characters
    - Contain only alphanumeric characters, hyphens, and underscores
    - Not contain consecutive hyphens or underscores
    
    Args:
        filename (str): Original filename to sanitize
        
    Returns:
        str: Sanitized collection name safe for ChromaDB
    """
    if not filename:
        return "default_collection"
    
    # Remove file extension
    name = os.path.splitext(filename)[0]
    
    # Convert to lowercase
    name = name.lower()
    
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^a-z0-9\-_]', '_', name)
    
    # Remove consecutive underscores/hyphens
    name = re.sub(r'[-_]+', '_', name)
    
    # Ensure it starts and ends with alphanumeric characters
    name = re.sub(r'^[^a-z0-9]+', '', name)
    name = re.sub(r'[^a-z0-9]+$', '', name)
    
    # Ensure minimum length
    if len(name) < 3:
        name = f"doc_{name}_collection"
    
    # Ensure maximum length
    if len(name) > 63:
        name = name[:60] + "_doc"
    
    # Final check - if empty after sanitization, use default
    if not name:
        name = "default_collection"
    
    return name


def validate_collection_name(collection_name):
    """
    Validate if a collection name meets ChromaDB requirements.
    
    Args:
        collection_name (str): Collection name to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not collection_name:
        return False, "Collection name cannot be empty"
    
    if len(collection_name) < 3:
        return False, "Collection name must be at least 3 characters long"
    
    if len(collection_name) > 63:
        return False, "Collection name must be at most 63 characters long"
    
    if not re.match(r'^[a-z0-9]', collection_name):
        return False, "Collection name must start with an alphanumeric character"
    
    if not re.match(r'[a-z0-9]$', collection_name):
        return False, "Collection name must end with an alphanumeric character"
    
    if not re.match(r'^[a-z0-9\-_]+$', collection_name):
        return False, "Collection name can only contain alphanumeric characters, hyphens, and underscores"
    
    if re.search(r'[-_]{2,}', collection_name):
        return False, "Collection name cannot contain consecutive hyphens or underscores"
    
    return True, "Valid collection name"


# Example usage and test cases
if __name__ == "__main__":
    test_cases = [
        "My Document.pdf",
        "sales-report_2024.xlsx", 
        "Marketing Strategy (Final).docx",
        "user@email.com_data.pdf",
        "file with spaces and symbols!@#.txt",
        "a.pdf",  # Too short
        "a" * 70 + ".pdf",  # Too long
        "123_valid_name.pdf",
        "special-chars_@#$%^&*().pdf"
    ]
    
    print("Testing sanitize_collection_name function:")
    print("-" * 50)
    
    for test_case in test_cases:
        sanitized = sanitize_collection_name(test_case)
        is_valid, message = validate_collection_name(sanitized)
        
        print(f"Input: {test_case}")
        print(f"Output: {sanitized}")
        print(f"Valid: {is_valid} - {message}")
        print("-" * 30) 
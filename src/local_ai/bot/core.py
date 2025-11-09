import unicodedata
import string

"""
Handler for processing user input.
"""

def process_input(user_text: str) -> str:
    """
    1. Sanitize the input. 
    2. Process the input (gen response)
    3. Output the response!
    """
    user_text = sanitize_input(user_text)
    return user_text

def sanitize_input(input_string: str) -> str:
    """
    trim, 
    to lowercase, 
    unicode normalization, 
    collapse whitespace. 
    Return sanitized input.
    """
    user_text = input_string.lower() # Convert to lowercase.
    user_text = unicodedata.normalize('NFC', user_text) # Normalize..
    user_text = user_text.strip() # Remove leading and trailing whitespace.

    # Clear punctuation.
    translator = str.maketrans('', '', string.punctuation)
    cleaned_user_text = user_text.translate(translator) 
    
    print(cleaned_user_text)
    return cleaned_user_text
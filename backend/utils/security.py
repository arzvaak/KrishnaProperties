import bleach

def sanitize_input(text):
    """
    Sanitizes the input text by stripping HTML tags and attributes.
    """
    if not isinstance(text, str):
        return text
    return bleach.clean(text, strip=True)

def sanitize_dict(data):
    """
    Recursively sanitizes a dictionary.
    """
    if not isinstance(data, dict):
        return data
    
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned[key] = sanitize_input(value)
        elif isinstance(value, dict):
            cleaned[key] = sanitize_dict(value)
        elif isinstance(value, list):
            cleaned[key] = [sanitize_input(item) if isinstance(item, str) else item for item in value]
        else:
            cleaned[key] = value
    return cleaned

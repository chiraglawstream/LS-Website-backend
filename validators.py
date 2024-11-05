import re
import bleach

def validate_phone_number(phone: str) -> str:
    phone_regex = re.compile(r'^\+?1?\d{9,12}$')  # Validates phone numbers of 9 to 12 digits, allowing optional country code
    if not phone_regex.match(phone):
        raise ValueError("Invalid phone number format")
    return phone

def sanitize_message(message: str) -> str:
    # Remove any HTML tags and JavaScript using bleach
    return bleach.clean(message, tags=[], strip=True)

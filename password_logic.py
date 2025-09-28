
import random
import secrets
import string

# --- Character Sets ---
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
NUMBERS = string.digits
SYMBOLS = string.punctuation

SIMILAR_CHARS = "il1Lo0O"
AMBIGUOUS_CHARS = "{}[]()/'\"`~,;:.<>"

def generate_password(length, use_upper, use_lower, use_numbers, use_symbols, exclude_similar):
    """
    Generates a random password based on specified criteria.
    """
    char_pool = []
    if use_upper:
        char_pool.extend(list(UPPERCASE))
    if use_lower:
        char_pool.extend(list(LOWERCASE))
    if use_numbers:
        char_pool.extend(list(NUMBERS))
    if use_symbols:
        char_pool.extend(list(SYMBOLS))

    if not char_pool:
        return None, "No character types selected."

    if exclude_similar:
        char_pool = [char for char in char_pool if char not in SIMILAR_CHARS]

    # Ensure the pool isn't empty after excluding characters
    if not char_pool:
        return None, "Character set is empty after exclusions."

    # Use secrets for cryptographic randomness
    try:
        password = "".join(secrets.choice(char_pool) for _ in range(length))
    except IndexError:
        # This can happen if the character pool becomes empty after filtering
        return None, "Could not generate password from the given character set."

    return password, None


def check_strength(password):
    """
    Checks the strength of a password and returns a label and score.
    """
    if not password:
        return "EMPTY", 0

    length = len(password)
    has_lower = any(c in LOWERCASE for c in password)
    has_upper = any(c in UPPERCASE for c in password)
    has_number = any(c in NUMBERS for c in password)
    has_symbol = any(c in SYMBOLS for c in password)

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    
    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_number:
        score += 1
    if has_symbol:
        score += 1

    # Adjust score based on variety
    variety = sum([has_lower, has_upper, has_number, has_symbol])
    if variety >= 3:
        score += 1

    # Return strength label based on score
    if score >= 7:
        return "STRONG", score
    elif score >= 4:
        return "MEDIUM", score
    else:
        return "WEAK", score


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_length = len(keyword)
    for i in range(len(plaintext)):
        symbol = plaintext[i]
        if keyword[i % key_length].isupper():
            key = ord(keyword[i % key_length]) - ord("A")
        else:
            key = ord(keyword[i % key_length]) - ord("a")
        if symbol.isupper():
            if 65 <= ord(symbol) + key <= 90:
                ciphertext += chr((ord(symbol) + key))
            else:
                ciphertext += chr((ord(symbol) + key) - 26)
        elif symbol.islower():
            if 97 <= ord(symbol) + key <= 122:
                ciphertext += chr((ord(symbol) + key))
            else:
                ciphertext += chr((ord(symbol) + key) - 26)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_length = len(keyword)
    for i in range(len(ciphertext)):
        symbol = ciphertext[i]
        if keyword[i % key_length].isupper():
            key = ord(keyword[i % key_length]) - ord("A")
        else:
            key = ord(keyword[i % key_length]) - ord("a")
        if symbol.isupper():
            if 65 <= ord(symbol) - key <= 90:
                plaintext += chr((ord(symbol) - key))
            else:
                plaintext += chr((ord(symbol) - key) + 26)
        elif symbol.islower():
            if 97 <= ord(symbol) - key <= 122:
                plaintext += chr((ord(symbol) - key))
            else:
                plaintext += chr((ord(symbol) - key) + 26)
        else:
            plaintext += symbol
    return plaintext

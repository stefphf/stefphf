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
        symbol = str(plaintext[i])
        if symbol.isupper():
            key = ord(keyword[i % key_length]) - ord("A")
            if 65 <= ord(symbol) + key <= 90:
                ciphertext += chr((ord(symbol) + key))
            else:
                ciphertext += chr((ord(symbol) + key) - 26)
        elif symbol.islower():
            key = ord(keyword[i % key_length]) - ord("a")
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
        element = str(ciphertext[i])
        if element.isupper():
            key = ord(keyword[i % key_length]) - ord("A")
            if 65 <= ord(element) - key <= 90:
                plaintext += chr((ord(element) - key))
            else:
                plaintext += chr((ord(element) - key) + 26)
        elif element.islower():
            key = ord(keyword[i % key_length]) - ord("a")
            if 97 <= ord(element) - key <= 122:
                plaintext += chr((ord(element) - key))
            else:
                plaintext += chr((ord(element) - key) + 26)
        else:
            plaintext += element
    return plaintext

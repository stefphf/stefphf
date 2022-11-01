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
    alphabet_low = "abcdefghijklmnopqrstuvwxyz"
    alphabet_high = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_length = len(keyword)
    for i in range(len(plaintext)):
        if plaintext[i] in alphabet_high:
            key = ord(keyword[i % key_length]) - ord("A")
            ciphertext += alphabet_high[(alphabet_high.find(plaintext[i]) + key) % 26]
        elif plaintext[i] in alphabet_low:
            key = ord(keyword[i % key_length]) - ord("a")
            ciphertext += alphabet_low[(alphabet_low.find(plaintext[i]) + key) % 26]
        else:
            ciphertext += plaintext[i]
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
    alphabet_low = "abcdefghijklmnopqrstuvwxyz"
    alphabet_high = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key_length = len(keyword)
    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet_high:
            key = ord(keyword[i % key_length]) - ord("A")
            plaintext += alphabet_high[(alphabet_high.find(ciphertext[i]) - key) % 26]
        elif ciphertext[i] in alphabet_low:
            key = ord(keyword[i % key_length]) - ord("a")
            plaintext += alphabet_low[(alphabet_low.find(ciphertext[i]) - key) % 26]
        else:
            plaintext += ciphertext[i]
    return plaintext

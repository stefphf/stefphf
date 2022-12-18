import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        symbol = plaintext[i]
        if symbol.isupper():
            if 65 <= ord(symbol) + shift <= 90:
                ciphertext += chr((ord(symbol) + shift))
            else:
                ciphertext += chr((ord(symbol) + shift) - 26)
        elif symbol.islower():
            if 97 <= ord(symbol) + shift <= 122:
                ciphertext += chr((ord(symbol) + shift))
            else:
                ciphertext += chr((ord(symbol) + shift) - 26)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext: str = ""
    for i in range(len(ciphertext)):
        symbol = ciphertext[i]
        if symbol.isupper():
            if 65 <= ord(symbol) - shift <= 90:
                plaintext += chr((ord(symbol) - shift))
            else:
                plaintext += chr((ord(symbol) - shift) + 26)
        elif symbol.islower():
            if 97 <= ord(symbol) - shift <= 122:
                plaintext += chr((ord(symbol) - shift))
            else:
                plaintext += chr((ord(symbol) - shift) + 26)
        else:
            plaintext += symbol
    return plaintext


def caesar_breaker_brute_force(dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift

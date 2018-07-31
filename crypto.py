import base64
from itertools import cycle, permutations
from typing import Tuple, List

from database import CharacterFrequencyDatabase


def encrypt_rep_key_xor(text: str, key: str) -> bytes:
    """ Encrypt text using a repeating-key XOR cipher. """
    return bytes(ord(text_char) ^ ord(key_char) for text_char, key_char in zip(text, cycle(key)))


def decrypt_rep_key_xor(encrypted: bytes, key: str) -> str:
    """ Decrypt text using a repeating-key XOR cipher. """
    letters = (chr(encrypted_byte ^ ord(key_char)) for encrypted_byte, key_char in zip(encrypted, cycle(key)))
    return ''.join(letters)


def break_rep_key_xor(encrypted: bytes, min_key_size=2, max_key_size=40, n_key_size_blocks=2) -> Tuple[str, str]:
    """ Find the key for a repeating key XOR encrypted text and decrypt it."""
    smallest_distance, key_size = None, None
    for test_key_size in range(min_key_size, max_key_size + 1):
        key_size_blocks = get_blocks(encrypted, test_key_size, n_key_size_blocks)
        distances = []
        for index1, index2 in permutations(range(n_key_size_blocks), r=2):
            key_size_block1, key_size_block2 = key_size_blocks[index1], key_size_blocks[index2]
            distances.append(edit_distance(key_size_block1, key_size_block2) / test_key_size)
        distance = sum(distances) / len(distances)
        if smallest_distance is None or distance < smallest_distance:
            smallest_distance = distance
            key_size = test_key_size
    # Split the encrypted bytes in blocks of length key_size.
    n_blocks = len(encrypted) // key_size
    blocks = get_blocks(encrypted, key_size, n_blocks)
    # Transpose the blocks: make a block that is the first byte of every block and so on.
    transposed_blocks = [bytes(transposed_block) for transposed_block in zip(*blocks)]
    # Solve each block as if it was single-character XOR and combine the single-character keys to get the whole key.
    key = ''.join((break_single_character_xor(transposed_block)[0] for transposed_block in transposed_blocks))
    return key, decrypt_rep_key_xor(encrypted, key)


def get_blocks(encrypted: bytes, key_size: int, n_blocks: int) -> List[bytes]:
    return [encrypted[i * key_size:(i + 1) * key_size] for i in range(n_blocks)]


def edit_distance(bytes1: bytes, bytes2: bytes) -> float:
    """ Calculate the edit (Hamming) distance between two byte sequences. """
    if not isinstance(bytes1, bytes) or not isinstance(bytes2, bytes):
        raise ValueError('Inputs must be bytes!')
    if len(bytes1) != len(bytes2):
        raise ValueError('Inputs must have same length!')
    distance = 0
    for byte1, byte2 in zip(bytes1, bytes2):
        binary1, binary2 = (bin(byte)[2:].zfill(8) for byte in (byte1, byte2))
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(binary1, binary2))
    return distance


def break_single_character_xor(encrypted: bytes) -> Tuple[str, str]:
    """ Find the key for a single character XOR encrypted text and decrypt it. """
    db = CharacterFrequencyDatabase('character_data')
    decrypted = [''.join(chr(byte ^ ord(key)) for byte in encrypted) for key in db]
    scores = [db.score_text(string) for string in decrypted]
    key_index = arg_min_index(scores)
    chars = [char for char in db]
    key = chars[key_index]
    return key, decrypted[key_index]


def _arg_min(pairs):
    return min(pairs, key=lambda x: x[1])[0]


def arg_min_index(values: List[float]) -> int:
    return _arg_min(enumerate(values))


def _arg_max(pairs):
    return max(pairs, key=lambda x: x[1])[0]


def arg_max_index(values):
    """ Find the index of the largest value in a list.

    Args:
        values: A list of values.

    Returns:
        The index (int) of the largest value in values.
    """
    return _arg_max(enumerate(values))


def hex_to_base64(hex_string):
    """ Convert a hex encoded string to base64.

    Args:
        hex_string: A hex encoded string.

    Returns:
        The base64 encoded bytes string.
    """
    return base64.b64encode(bytes.fromhex(hex_string))


def fixed_xor(encoded_1, encoded_2):
    """ Take two equal length strings, hex decode them and produce their XOR combination.

    Args:
        encoded_1: First string.
        encoded_2: Second string.

    Returns:
        A instance of the bytes class containing the XOR combination of the two input strings.
    """
    if not isinstance(encoded_1, str) or not isinstance(encoded_2, str):
        raise ValueError('Inputs must be strings!')
    if len(encoded_1) != len(encoded_2):
        raise ValueError('Inputs must have same length!')
    buffer_1, buffer_2 = [bytes.fromhex(string) for string in [encoded_1, encoded_2]]
    return bytes([byte_1 ^ byte_2 for byte_1, byte_2 in zip(buffer_1, buffer_2)])


def detect_single_byte_xor_cipher(encrypted, n=5):
    """ Detect a single byte XOR encrypted hex encoded string and decrypt it.

    Args:
        encrypted: A list of hex encoded strings
        n: Integer, number of strings to return. (Default=5)

    Returns:
        The first n most probable decrypted strings.
    """
    strings = [break_single_character_xor(byte) for byte in bytes.fromhex(encrypted)]
    return sorted(strings, key=lambda s: -s.count(' '))[:n]


def main():
    with open('challenge_6_data.txt', 'r') as f:
        encrypted = base64.b64decode(f.read())
        decrypted = break_rep_key_xor(encrypted, n_key_size_blocks=4)
        print(decrypted[0])
        print(decrypted[1])


if __name__ == '__main__':
    main()

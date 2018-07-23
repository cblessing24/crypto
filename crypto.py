import codecs


def hex_to_base64(hex_bytes):
    return codecs.encode(codecs.decode(hex_bytes, 'hex_codec'), 'base64_codec')


def fixed_xor(string_1, string_2):
    """ Take two equal length strings, hex decode them and produce their XOR combination.

    Args:
        string_1: First string.
        string_2: Second string.

    Returns:
        A instance of the bytes class containing the XOR combination of the two input strings.
    """
    if not isinstance(string_1, str) or not isinstance(string_2, str):
        raise ValueError('Inputs must be strings!')
    if len(string_1) != len(string_2):
        raise ValueError('Inputs must have same length!')
    buffer_1, buffer_2 = [bytes.fromhex(string) for string in [string_1, string_2]]
    return bytes([byte_1 ^ byte_2 for byte_1, byte_2 in zip(buffer_1, buffer_2)])


def main():
    string_1 = '1c0111001f010100061a024b53535009181c'
    string_2 = '686974207468652062756c6c277320657965'
    solution = '746865206b696420646f6e277420706c6179'

    print(fixed_xor(string_1, string_2).hex() == solution)


if __name__ == '__main__':
    main()

import codecs


def hex_to_base64(hex_bytes):
    return codecs.encode(codecs.decode(hex_bytes, 'hex_codec'), 'base64_codec')


def main():
    hex_bytes = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print(hex_to_base64(hex_bytes))


if __name__ == '__main__':
    main()

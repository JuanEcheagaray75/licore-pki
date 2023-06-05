from cryptography.hazmat.primitives.hashes import BLAKE2b
from cryptography.hazmat.primitives import hashes


def base_blake2_test():

    # Official test vector from RFC 7693
    # https://datatracker.ietf.org/doc/html/rfc7693#page-13

    hasher = hashes.Hash(BLAKE2b(64))
    message = 'abc'
    hasher.update(message.encode('ascii'))
    expected = 'BA80A53F981C4D0D6A2797B69F12F6E94C212F14685AC4B74B12BB6FDBFFA2D17D87C5392AAB792DC252D5DE4533CC9518D38AA8DBF1925AB92386EDD4009923'
    assert hasher.finalize().hex().upper() == expected


def extra_blake2_test():

    # Custom made test vector derived from the official test vector
    # once the function was validated
    with open('test_blake.txt', 'r') as f:
        expected = f.read().splitlines()

        for line in expected:
            message = line.split(',')[0].strip()
            expected_hash = line.split(',')[1].strip()

            hasher = hashes.Hash(BLAKE2b(64))
            hasher.update(message.encode('ascii'))
            assert hasher.finalize().hex().upper() == expected_hash


if __name__ == '__main__':
    base_blake2_test()
    extra_blake2_test()
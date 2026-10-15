ROTORS = {
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
}
NOTCHES = {"I": "Q", "II": "E", "III": "V"}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _clean(text):
    return "".join(c for c in text.upper() if c.isalpha() and c.isascii())


def _inverse(wiring):
    inverse = [0] * 26
    for i, value in enumerate(wiring):
        inverse[ord(value) - 65] = i
    return inverse


def _parse_key(key):
    key = _clean(key)
    if len(key) != 3:
        raise ValueError("Kunci Enigma harus terdiri dari 3 huruf posisi rotor. Contoh: AAA")
    return [ord(c) - 65 for c in key]


def enigma_transform(text, key):
    source = _clean(text)
    positions = _parse_key(key)
    rotor_names = ["I", "II", "III"]
    wirings = [ROTORS[name] for name in rotor_names]
    inverses = [_inverse(wiring) for wiring in wirings]
    notches = [ord(NOTCHES[name]) - 65 for name in rotor_names]
    output = []

    for char in source:
        middle_at_notch = positions[1] == notches[1]
        right_at_notch = positions[2] == notches[2]

        if middle_at_notch:
            positions[0] = (positions[0] + 1) % 26
            positions[1] = (positions[1] + 1) % 26
        elif right_at_notch:
            positions[1] = (positions[1] + 1) % 26
        positions[2] = (positions[2] + 1) % 26

        value = ord(char) - 65

        for index in (2, 1, 0):
            shift = positions[index]
            value = (ord(wirings[index][(value + shift) % 26]) - 65 - shift) % 26

        value = ord(REFLECTOR_B[value]) - 65

        for index in (0, 1, 2):
            shift = positions[index]
            value = (inverses[index][(value + shift) % 26] - shift) % 26

        output.append(chr(value + 65))

    return "".join(output)


def enigma_encrypt(text, key):
    return enigma_transform(text, key)


def enigma_decrypt(text, key):
    return enigma_transform(text, key)

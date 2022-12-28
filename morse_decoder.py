class Morse_decoder:
    def __init__(self):
        # The following dictionary contains mapping of sequence of dots and dashes to character
        # Based on Morse code
        self.__morse_decode_dict = {".-": 'א',
                            "-...": 'ב',
                            "--.": 'ג',
                            "-..": 'ד',
                            "---": 'ה',
                            ".": 'ו',
                            "--..": 'ז',
                            "....": 'ח',
                            "..-": 'ט',
                            "..": 'י',
                            "-.-": 'כ',
                            ".-..": 'ל',
                            "--": 'מ',
                            "-.": 'נ',
                            "-.-.": 'ס',
                            ".---": 'ע',
                            ".--.": 'פ',
                            ".--": 'צ',
                            "--.-": 'ק',
                            ".-.": 'ר',
                            "...": 'ש',
                            "-": 'ת',
                            "-----": '0',
                            ".----": '1',
                            "..---": '2',
                            "...--": '3',
                            "-....": '4',
                            ".....": '5',
                            "-....": '6',
                            "--...": '7',
                            "---..": '8',
                            "----.": '9',
                            ".-.-.-": '.',
                            "--..--": ',',
                            "..--..": '?',
                            "-.-.--": '!',
                            "-..-.": '/',
                            "-.--.-": '(',
                            "-.--.": ')',
                            ".-...": '&',
                            "---...": ':',
                            "-.-.-.": ';',
                            "-...-": '=',
                            ".-.-.": '+',
                            "-....-": '-',
                            "..--.-": '_',
                            ".-..-.": '"',
                            "...-..-": '$',
                            ".--.-.": '@' }

    # Returns the letter which represent the Morse sequence code, that being received as string
    def convert_sign_seq_to_letter(self, str):
        if str in self.__morse_decode_dict:
            return self.__morse_decode_dict[str]
        return None

    # Unit testing:
def test_decoder():
    dec = Morse_decoder()
    assert(dec.convert_sign_seq_to_letter(".--.-.") == '@')


def test_decoder_negative():
    dec = Morse_decoder()
    assert(dec.convert_sign_seq_to_letter("xx") == None)

test_decoder()
test_decoder_negative()
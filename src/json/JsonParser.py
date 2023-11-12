
from os.path import getsize
from typing import Generator, Any

from json.JsonTokens import Token, JInt


class JsonParser(object):
    def __init__(self, path: str, allow_traling_comma: bool = True):
        self.path = path
        self.fp = open(path, 'r')
        self.allow_traling_comma = allow_traling_comma
        self._result: dict = dict()

    def parse_file(self) -> dict:
        building_key: bool = True


        for _, char in enumerate(self.fp.read()):
            key = self._key_builder()
            value = self._value_builder()
            pass

        self.fp.close()

        return self._result

    def _key_builder(self) -> str:
        key: str = ""

        for _, char in enumerate(self.fp.read()):
            pass

        return key

    def _value_builder(self) -> Any:
        value: Any = ""

        for _, char in enumerate(self.fp.read()):
            pass

        return value

    def _string_builder(self, closing_char: str) -> str:
        result: str = ""

        for _, char in enumerate(self.fp.read()):
            if char == closing_char:
                break

            if char == '\\':
                special: str = self.fp.read()
                char = self._get_special_char(special)

                if char == None:
                    continue

            result += char

        return result

    def _get_special_char(self, char: str) -> str | None:
        special_chars: dict[str, str] = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "0": "\0"
        }

        return special_chars.get(char, None)

if __name__ == "__main__":
    exit(1)

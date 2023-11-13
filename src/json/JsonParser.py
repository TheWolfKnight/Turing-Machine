
from typing import Any
from enum import Enum


class _ScopeChange(Enum):
    Increase = 0
    Decrease = 1


class JsonParser(object):
    def __init__(self, path: str, allow_traling_comma: bool = False):
        self.path = path
        self.fp = open(path, 'r')
        self.file_size: int = self.fp.tell()
        self.allow_traling_comma = allow_traling_comma
        self._result: dict = dict()

    def parse_file(self) -> dict:
        scopes: list[str] = list()

        for _, char in enumerate(self.fp.read()):
            key = self._key_builder()

            if key is Exception:
                continue

            key = str(key)

            value = self._value_builder()

            if value is _ScopeChange:
                match value:
                    case _ScopeChange.Increase:
                        scopes.append(key)
                    case _ScopeChange.Decrease:
                        scopes.pop()
                continue

            value = str(value)

            target_dict: dict = self._result

            for scope in scopes:
                target_dict = dict(target_dict.get(scope, None))

            target_dict[key] = self._convert_value(value)

        self.fp.close()

        return self._result

    def _key_builder(self) -> str | Exception:
        key: str = ""

        for _, char in enumerate(self.fp.read()):
            if char in "{} \n\t":
                continue
            if char in "\"\'":
                key = self._string_builder(char)
                break

        if len(key) < 1:
            return Exception("Key could not be found")

        return key

    def _value_builder(self) -> _ScopeChange | str:
        value: str = ""

        for _, char in enumerate(self.fp.read()):
            if char == ':':
                break

        if self.fp.tell() == self.file_size:
            raise Exception()

        for _, char in enumerate(self.fp.read()):
            if char in " \n\t":
                continue

            if char in "\"\'":
                value = self._string_builder(char)
                break
            elif char.isalnum():
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

    def _convert_value(self, val: str) -> Any:
        pass


if __name__ == "__main__":
    exit(1)

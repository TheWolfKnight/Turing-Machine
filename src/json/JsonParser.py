
from dataclasses import dataclass
from typing import Any, Type
from enum import Enum


class _ScopeChange(Enum):
    Increase = 0
    Decrease = 1


@dataclass
class _ValueTypeWrapper(object):
    def __init__(self, val: Any, typ: Type):
        self.value = val
        self.type = typ

    @classmethod
    def cast(cls, this: Any) -> "_ValueTypeWrapper":
        if "__vtw__" in dir(this):
            return this

        raise Exception("Cannot convert to _ValueTypeWrapper")

    def __vtw__(self) -> None:
        pass


class JsonParser(object):
    def __init__(self, path: str, allow_traling_comma: bool = False):
        self.path = path
        self.fp = open(path, 'r')
        self._get_file_size()
        self.allow_traling_comma = allow_traling_comma
        self._result: dict = dict()

    def _get_file_size(self):
        self.fp.seek(0, 2)
        self.file_size: int = self.fp.tell()
        self.fp.seek(0, 0)

    def parse_file(self) -> dict:
        scopes: list[str] = list()

        while not self._file_is_eof():
            key = self._key_builder()

            if key is _ScopeChange.Decrease:
                scopes.pop()
                continue

            key = str(key)

            value = self._value_builder()

            if value is _ScopeChange.Increase:
                scopes.append(key)
                continue

            value = _ValueTypeWrapper.cast(value)

            target_dict: dict = self._result

            i: int = 0

            for scope in scopes:
                tmp = target_dict.get(scope, None)

                if tmp is None:
                    target_dict[key] = dict()

                target_dict = target_dict[key]
                i += 1


            target_dict[key] = self._convert_value(value)

            print(f"{('  '*i)}key: {key}")
            print(f"{('  '*i)}value {value.value}")


        self.fp.close()

        return self._result

    def _key_builder(self) -> str | _ScopeChange:
        key: str = ""

        while not self._file_is_eof():
            char: str = self.fp.read(1)

            if char == '}':
                return _ScopeChange.Decrease

            if char in "{ \n\t":
                continue
            if char in "\"\'":
                key = self._string_builder(char)
                break

        return key

    def _value_builder(self) -> _ScopeChange | _ValueTypeWrapper:

        while not self._file_is_eof():
            char = self.fp.read(1)
            if char == ':':
                break

        if self.fp.tell() == self.file_size:
            raise Exception()

        while not self._file_is_eof():
            char = self.fp.read(1)
            if char in " \n\t":
                continue

            if char in "\"\'":
                value = self._string_builder(char)
                return _ValueTypeWrapper(value, type(str))
            elif char.isnumeric():
                value = char + self._string_builder(',')
                return _ValueTypeWrapper(value, type(int))
            elif char == '[':
                value = self._list_builder()
                return _ValueTypeWrapper(value, type(list))
            elif char == '{':
                return _ScopeChange.Increase

        raise Exception("Unrechable Code")

    def _list_builder(self) -> list:
        result: list = []

        while not self._file_is_eof:
            pass

        return result

    def _string_builder(self, closing_char: str) -> str:
        result: str = ""

        while not self._file_is_eof():
            char = self.fp.read(1)
            if char == closing_char:
                break

            if char == '\\':
                special: str = self.fp.read(1)
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

    def _convert_value(self, val: _ValueTypeWrapper) -> Any:
        return val.value

    def _file_is_eof(self):
        return self.fp.tell() > self.file_size


if __name__ == "__main__":
    exit(1)

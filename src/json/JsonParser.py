
from dataclasses import dataclass
from typing import Any, Type, Iterator, Callable
from enum import Enum


from wrappers import FileWrapper, StringWrapper


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
        self.fp = FileWrapper(path)
        self.allow_traling_comma = allow_traling_comma
        self._result: dict = dict()

    def parse_file(self) -> dict:
        result = self._parse_content(self.fp, self._file_is_eof)
        return result

    def _parse_content(self, content: Iterator[str], stop_condition: Callable[[], bool]) -> dict:
        scopes: list[str] = list()

        while not stop_condition():
            key = self._key_builder(content, stop_condition)

            if key is _ScopeChange.Decrease:
                scopes.pop()
                continue

            key = str(key)

            value = self._value_builder(content, stop_condition)

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

    def _key_builder(self, content: Iterator[str], stop_condition: Callable[[], bool]) -> str | _ScopeChange:
        key: str = ""

        while not stop_condition():
            char: str = next(content)

            if char == '}':
                return _ScopeChange.Decrease

            if char in "{ \n\t":
                continue
            if char in "\"\'":
                key = self._string_builder(char, content, stop_condition)
                break

        return key

    def _value_builder(self, content: Iterator[str], stop_condition: Callable[[], bool]) -> _ScopeChange | _ValueTypeWrapper:

        while not stop_condition():
            char = next(content)
            if char == ':':
                break

        if stop_condition():
            raise Exception()

        while not stop_condition():
            char = next(content)
            if char in " \n\t":
                continue

            if char in "\"\'":
                value = self._string_builder(char, content, stop_condition)
                return _ValueTypeWrapper(value, type(str))
            elif char.isnumeric():
                value = char + self._string_builder(',', content, stop_condition)
                return _ValueTypeWrapper(value, type(int))
            elif char == '[':
                value = self._list_builder(content, stop_condition)
                return _ValueTypeWrapper(value, type(list))
            elif char == '{':
                return _ScopeChange.Increase

        raise Exception("Unrechable Code")

    def _list_builder(self, content: Iterator[str], stop_condition: Callable[[], bool]) -> list:
        result: list = []

        depth: int = 1

        while not stop_condition():
            char: str = next(content)

            if not depth:
                break

            if char == ']':
                depth -= 1
            elif char == '[':
                depth += 1
                result.append([])
            elif char in "\"\'":
                value = self._string_builder(char, content, stop_condition)
                result.append(value)
            elif char.isnumeric():
                value = self._string_builder(',', content, stop_condition)
                result.append(value)




        return result

    def _num_indent(self, val: str) -> int | float:
        if not val.isnumeric():
            raise Exception("NaN")

        if '.' in val and val.count('.') == 1:
            return float(val)
        else:
            return int(val)

    def _string_builder(self, closing_char: str, content: Iterator[str], stop_condition: Callable[[], bool]) -> str:
        result: str = ""

        while not stop_condition():
            char = next(content)
            if char == closing_char:
                break

            if char == '\\':
                special: str = next(content)
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
        return self.fp.file_is_finished()


if __name__ == "__main__":
    exit(1)

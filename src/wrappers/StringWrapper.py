
from typing import Iterator


class StringWrapper(Iterator[str]):
    def __init__(self, content: str):
        self.content = content
        self._content_length = len(self.content)
        self._cursor: int = 0

    def end_of_string(self) -> bool:
        return self._cursor > self._content_length

    def __next__(self) -> str | None:
        if self.end_of_string():
            return None
        self._cursor += 1
        return self.content[self._cursor-1]


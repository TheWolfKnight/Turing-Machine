
from typing import Iterator


class FileWrapper(Iterator[str]):
    def __init__(self, path: str):
        self.fp = open(path, 'r')
        self.fp.seek(0, 2)
        self.file_size = self.fp.tell()
        self.fp.seek(0, 0)

    def close(self):
        self.fp.close()

    def file_is_finished(self) -> bool:
        return self.file_size < self.fp.tell()

    def __next__(self) -> str | None:
        if self.file_is_finished():
            return None
        return self.fp.read(1)

if __name__ == "__main__":
    exit(1)


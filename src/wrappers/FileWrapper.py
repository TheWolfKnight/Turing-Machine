
from wrappers.IterWrapper import IIterWrapper


class FileWrapper(IIterWrapper):
    def __init__(self, path: str):
        self.file = open(path, 'r')
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0, 0)

    def close(self):
        self.file.close()

    def file_is_finished(self) -> bool:
        return self.file_size <= self.file.tell()

    def __next__(self) -> str | None:
        if self.file_is_finished():
            return None
        return self.file.read(1)

    def step_back(self, i) -> None:
        step = self.file.tell() - i
        self.file.seek(step, 0)


if __name__ == "__main__":
    exit(1)



from typing import Iterator


class IIterWrapper(Iterator[str]):
    def __next__(self) -> str:
        ...

    def step_back(self, i) -> None:
        ...


if __name__ == "__main__":
    exit(0)

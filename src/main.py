
from sys import argv
from typing import Iterator

from json.JsonParser import JsonParser


def main(args: list[str]):
    parser = JsonParser("./tmp/test.json")
    parser.parse_file()


if __name__ == "__main__":
    main(argv)
    exit(0)

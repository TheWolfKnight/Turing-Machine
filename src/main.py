
from sys import argv

from json.JsonParser import JsonParser


def main(args: list[str]):
    parser = JsonParser("./tmp/test.json")
    result = parser.parse_file()


if __name__ == "__main__":
    main(argv)
    exit(0)


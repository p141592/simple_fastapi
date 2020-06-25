#!/usr/bin/env python

# Сконвертировать .env файл в строку для gclou
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()


def convert(filename):
    result = {}
    r = re.compile(r"^[\w]*=.*")
    for line in open(filename, "r").readlines():
        if re.match(r, line):
            key, value = line.strip().split("=")
            result[key] = value
    return ",".join([f'{key}="{value}"' for key, value in result.items()])


if __name__ == "__main__":
    _env = Path(sys.argv[1] or BASE_DIR.joinpath(".env"))
    print(convert(_env))
    sys.exit(0)

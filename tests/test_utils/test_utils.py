import os
from pathlib import Path

from utils.convert_env import convert


def test_convert(tmpdir):
    _p = Path(".").absolute() / "temp_file.txt"
    _f = open(_p, "w")
    _f.write("WELCOME_STRING=Hello world\nPYTHONPATH=/opt/application\n")
    _f.close()

    result = convert(_p)
    assert result == 'WELCOME_STRING="Hello world",PYTHONPATH="/opt/application"'
    os.remove(_p)

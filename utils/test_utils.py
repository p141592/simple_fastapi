from convert_env import convert

def test_convert(tmpdir):
    p = tmpdir.join("hello.txt")
    p.write("WELCOME_STRING=Hello world\nPYTHONPATH=/opt/application\n")
    result = convert(p.strpath)
    assert result == 'WELCOME_STRING="Hello world",PYTHONPATH="/opt/application"'


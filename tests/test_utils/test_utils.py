from utils.convert_env import convert


def test_convert(tmp_path):
    env_file = tmp_path / "temp_file.txt"
    env_file.write_text("WELCOME_STRING=Hello world\nPYTHONPATH=/opt/application\n")

    result = convert(env_file)

    assert result == 'WELCOME_STRING="Hello world",PYTHONPATH="/opt/application"'

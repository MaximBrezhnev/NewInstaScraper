from AutoParser import AutoParser


def get_parser(
        username: str = None,
        password: str = None,
        session_file: str = None,
):
    return AutoParser(
        username=username,
        password=password,
        session_file=session_file,
    )
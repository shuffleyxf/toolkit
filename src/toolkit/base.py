import os


def is_win() -> bool:
    """
    :return: 若当前为windows系统返回True，否则返回False
    """
    return os.name == 'nt'


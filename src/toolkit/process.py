import ctypes

from base import is_win
from error import ToolkitException

_SW_HIDE = 0    # 隐藏窗口
_SW_NORMAL = 1  # 正常展示
_SW_MAXIMIZE = 3    # 窗口最大化
_SW_MINIMIZE = 6    # 窗口最小化


def elevate(program: str, params: str = '', graphic_type: int = _SW_NORMAL):
    """
    以管理员权限执行程序
    :param program: 程序路径
    :param params: 传参
    :param graphic_type: 图形界面展示类型
    :return:
    """
    if not is_win():
        raise Exception("elevate only supported on windows")
    if graphic_type not in (_SW_HIDE, _SW_NORMAL, _SW_MINIMIZE, _SW_MAXIMIZE):
        raise ToolkitException(f"illegal argument: graphic_type can't be {graphic_type}")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", program, params, None, graphic_type)



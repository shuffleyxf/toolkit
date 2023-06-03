import inspect
import time

from error import ToolkitException


def wait_for(condition: callable, interval: float = 1, timeout: float = -1) -> bool:
    """
    等待某条件发生
    :param condition: 函数
    :param interval: 检测间隔
    :param timeout: 超时时间
    :return: 若最终条件为真返回True，否则返回False
    """
    sig = inspect.signature(condition)
    try:
        sig.bind()
    except TypeError:
        raise ToolkitException("Illegal condition!")
    cost = 0
    while not condition():
        if 0 <= timeout <= cost:
            return False
        time.sleep(interval)
        cost += interval
    return True

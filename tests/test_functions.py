import time

import pytest

from error import ToolkitException
from functions import wait_for


def test_wait_for():
    data = {'age': 1}

    # 测试签名校验
    with pytest.raises(ToolkitException):
        wait_for(lambda x: data['age'] == 10)

    # 测试结果
    assert wait_for(lambda: data['age'] == 1) is True

    assert wait_for(lambda: data['age'] == 10, timeout=1) is False

    # 测试超时
    now = time.time()
    assert wait_for(lambda: time.time() - now > 2, timeout=1) is False

    now = time.time()
    assert wait_for(lambda: time.time() - now > 2, timeout=3) is True

    # 测试间隔
    data['check_times'] = 0
    now = time.time()

    def check():
        data['check_times'] += 1
        return time.time() - now > 1
    wait_for(check, interval=1)
    assert data['check_times'] < 5

    data['check_times'] = 0
    now = time.time()
    wait_for(check, interval=0.1)
    assert data['check_times'] > 5


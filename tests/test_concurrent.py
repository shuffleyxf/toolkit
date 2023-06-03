import pytest
from concurrent import RWLock
from error import ToolkitException


class TestRWLock:
    def test_lock(self):
        rw_lock = RWLock()

        assert rw_lock.read_acquire() is True
        assert rw_lock.write_acquire(block=False) is False  # 读写互斥
        assert rw_lock.read_acquire() is True  # 读读共享
        assert rw_lock.write_acquire(block=True, timeout=0.5) is False  # 超时支持

        with pytest.raises(ToolkitException):
            rw_lock.write_release()  # 未获取时释放
        rw_lock.read_release()  # 正常释放读锁
        rw_lock.read_release()  # 正常释放读锁

        with pytest.raises(ToolkitException):  # 未获取时释放
            rw_lock.read_release()
        with pytest.raises(ToolkitException):  # 未获取时释放
            rw_lock.read_release()

        assert rw_lock.write_acquire() is True
        assert rw_lock.read_acquire(block=False) is False  # 读写互斥
        with pytest.raises(ToolkitException):  # 未获取时释放
            rw_lock.read_release()
        rw_lock.write_release()  # 正常释放写锁

import threading

from error import ToolkitException


class RWLock(object):
    """
    非公平读写锁
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._extra = threading.Lock()
        self.read_num = 0

    def _acquire(self, block: bool, timeout: float) -> bool:
        if block:
            return self._lock.acquire(blocking=True, timeout=timeout)
        else:
            return self._lock.acquire(blocking=False)

    def read_acquire(self, block: bool = True, timeout: float = -1) -> bool:
        ret = True
        with self._extra:
            if self.read_num == 0:
                ret = self._acquire(block, timeout)
            if ret:
                self.read_num += 1
        return ret

    def read_release(self):
        with self._extra:
            if self.read_num <= 0:
                raise ToolkitException("Read lock not acquired!")
            self.read_num -= 1
            if self.read_num == 0:
                self._lock.release()

    def write_acquire(self, block: bool = True, timeout: float = -1) -> bool:
        return self._acquire(block, timeout)

    def write_release(self):
        with self._extra:
            if self.read_num > 0:
                raise ToolkitException("Write lock not acquired!")
            self._lock.release()

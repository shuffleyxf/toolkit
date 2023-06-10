import threading

from error import ToolkitException


class RWLock(object):
    """
    非公平读写锁
    """
    _FREE = 0
    _READ = 1
    _WRITE = 2

    def __init__(self):
        self._state = self._FREE
        self._cond = threading.Condition()
        self.read_num = 0

    def read_acquire(self, block: bool = True, timeout: float = -1) -> bool:
        while True:
            with self._cond:
                if self._state == self._FREE:
                    self._state = self._READ
                    self.read_num = 1
                    return True
                elif self._state == self._READ:
                    self.read_num += 1
                    return True
                elif not block:
                    return False
                elif timeout >= 0:
                    block = False
                self._cond.wait(timeout=timeout)

    def read_release(self):
        with self._cond:
            if self._state != self._READ:
                raise ToolkitException("Read lock not acquired!")

            self.read_num -= 1
            if self.read_num == 0:
                self._state = self._FREE
                self._cond.notify()

    def write_acquire(self, block: bool = True, timeout: float = -1) -> bool:
        while True:
            with self._cond:
                if self._state == self._FREE:
                    self._state = self._WRITE
                    return True
                elif not block:
                    return False
                elif timeout >= 0:
                    block = False
                self._cond.wait(timeout=timeout)

    def write_release(self):
        with self._cond:
            if self._state != self._WRITE:
                raise ToolkitException("Write lock not acquired!")

            self._state = self._FREE
            self._cond.notify()

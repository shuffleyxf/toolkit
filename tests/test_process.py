import pytest

from process import *


@pytest.mark.skip(reason="Require manual verification")
def test_elevate():
    elevate("notepad.exe")

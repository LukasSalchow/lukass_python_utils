import logging
import random
import re
import sys
from subprocess import CalledProcessError
from time import sleep

import pytest

from lukass_python_utils.utilities import MAJOR_PYTHON_VERSION
from lukass_python_utils.utilities import MINOR_PYTHON_VERSION_WITH_ADD_NOTE
from lukass_python_utils.utilities import get_time_logger
from lukass_python_utils.utilities import run_shell_command


@pytest.mark.unit
def test_get_time_logger(caplog):
    time_logger = get_time_logger(__file__)
    with caplog.at_level(logging.INFO):
        with time_logger('sleep'):
            sleep(.1)

    time_str = re.findall(r'[\:\d]+\.+[0-9]+', caplog.text.replace('\n', ''))[0]
    *other, seconds = time_str.split(':')

    assert all(map(lambda x: x in ['0', '00'], other))
    assert .1 < float(seconds) < .2


@pytest.mark.unit
def test_run_shell_command_add_info():
    non_existing_file = str(random.randint(10 ** 10, 10 ** 11 - 1))
    with pytest.raises(CalledProcessError):
        run_shell_command(['ls', non_existing_file])
    major, minor, *_ = sys.version_info
    if major == MAJOR_PYTHON_VERSION and minor >= MINOR_PYTHON_VERSION_WITH_ADD_NOTE:
        try:
            run_shell_command(['ls', non_existing_file])
        except CalledProcessError as e:
            assert 'No such file or directory' in e.__notes__[1] and non_existing_file in e.__notes__[1]

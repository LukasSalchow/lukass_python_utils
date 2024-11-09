import logging
import random
import re
from subprocess import TimeoutExpired
from time import sleep

import pytest
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
def test_run_shell_command_file_not_found():
    with pytest.raises(RuntimeError) as e:
        run_shell_command(['ls', str(random.randint(10 ** 10, 10 ** 11 - 1))])
        assert 'No such file or directory' in repr(e)


@pytest.mark.unit
def test_run_shell_command_timeout():
    with pytest.raises(TimeoutExpired) as e:
        run_shell_command(['sleep', '1'], timeout=1e-6)
        assert 'No such file or directory' in repr(e)

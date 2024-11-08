import logging
import re
from datetime import datetime
from datetime import timedelta
from time import sleep

import pytest
from src.lukass_python_utils.utilities import get_time_logger


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

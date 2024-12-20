"""Utilities for personal use."""

import contextlib
import logging
import subprocess
import sys
import time
from collections.abc import Callable, Generator, Sequence
from datetime import timedelta

MAJOR_PYTHON_VERSION = 3
MINOR_PYTHON_VERSION_WITH_ADD_NOTE = 11


def get_logger(name: str, log_level: int = logging.DEBUG) -> logging.Logger:
    """Sets up a logger including information like file name and line number."""
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    # In the following format "-8s" make s sure no matter the log level, the rest of the message is aligned.
    formatter = logging.Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S',
    )
    console_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger


def get_time_logger(
    name: str,
    log_level: int = logging.DEBUG,
) -> Callable[[str], contextlib._GeneratorContextManager[None]]:
    """Logs the time a block or function takes. Can be invoked as a decorator or as a context manager."""
    logger = get_logger(name, log_level=log_level)

    @contextlib.contextmanager
    def log_time(title: str) -> Generator[None, None, None]:
        logger.info(f'{title} has started')
        start = timedelta(seconds=time.monotonic_ns() / 10**9)
        yield
        delta = timedelta(seconds=time.monotonic_ns() / 10**9) - start
        logger.info(f'{title} took {delta}')

    return log_time


def run_shell_command(command: Sequence[str], timeout: float = 10) -> subprocess.CompletedProcess[bytes]:
    """Wrapper for "subprocess.run" that adds the output in case of an error."""
    try:
        output = subprocess.run(  # noqa: S603
            command,
            capture_output=True,
            timeout=timeout,
            check=True,
        )
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        major, minor, *_ = sys.version_info
        if major == MAJOR_PYTHON_VERSION and minor >= MINOR_PYTHON_VERSION_WITH_ADD_NOTE:
            if e.stdout is not None:
                e.add_note(f'{e.stdout.decode("utf-8")=}')
            if e.stderr is not None:
                e.add_note(f'{e.stderr.decode("utf-8")=}')
        raise

    return output

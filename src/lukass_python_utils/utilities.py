"""Utilities for personal use."""

import contextlib
import logging
import subprocess
import time
from collections.abc import Callable, Generator, Sequence
from datetime import timedelta


def get_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
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
    log_level: int = logging.INFO,
) -> Callable[[str], contextlib.AbstractContextManager[None]]:
    """Logs the time a block or function takes. Can be invoked as a decorator or as a context manager."""
    logger = get_logger(name, log_level=log_level)

    @contextlib.contextmanager
    def log_time(title: str) -> Generator[None, None, None]:
        logger.info(f'started {title}')
        start = timedelta(seconds=time.monotonic_ns())
        yield
        logger.info(f'{title} took {(timedelta(seconds=time.monotonic_ns()) - start) / 10 ** 9} seconds.')

    return log_time


def run_shell_command(command: Sequence[str], timeout: int = 10) -> subprocess.CompletedProcess[bytes]:
    """Wrapper for "subprocess.run" that adds the output in case of an error."""
    try:
        output = subprocess.run(  # noqa: S603
            command,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        if e.output is not None:
            e.add_note(f"{e.stdout.decode("utf-8")}")
            e.add_note(f"{e.stderr.decode("utf-8")}")
        raise
    if output.returncode != 0:
        message = '\n'.join(
            (
                f'{output.returncode=}',
                f'{output.stdout.decode("utf-8")=}',
                f'{output.stderr.decode("utf-8")=}',
            ),
        )
        raise RuntimeError(message)

    return output

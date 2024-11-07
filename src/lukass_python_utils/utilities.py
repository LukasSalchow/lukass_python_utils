import logging
import subprocess
from typing import Sequence


def get_logger(name: str, log_level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    # In the following format "-8s" make s sure no matter the log level, the rest of the message is aligned.
    formatter = logging.Formatter(
        fmt='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(console_handler)
    return logger


def run_shell_command(command: Sequence[str], timeout=10) -> subprocess.CompletedProcess[bytes]:
    """Wrapper for "subprocess.run" that adds the output in case of an error."""
    try:
        output = subprocess.run(  # noqa: S603
            command,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        if e.output is not None:
            e.add_note("\noutput =\n" + e.output.decode())
        raise
    if output.returncode != 0:
        message = "\n".join(
            (
                "returned error code: " + str(output.returncode),
                output.stdout.decode("utf-8"),
                output.stderr.decode("utf-8"),
            )
        )
        raise RuntimeError(message)

    return output

import subprocess
from typing import Sequence

TIMEOUT = 10


def run_shell_command(command: Sequence[str], timeout=TIMEOUT) -> subprocess.CompletedProcess[bytes]:
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

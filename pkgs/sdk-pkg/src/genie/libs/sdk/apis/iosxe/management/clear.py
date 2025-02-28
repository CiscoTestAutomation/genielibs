"""Clear Idle VTY sessions"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# utils
from genie.libs.sdk.apis.utils import time_to_int

log = logging.getLogger(__name__)


def clear_idle_vty_sessions(device, idle_timeout=60):
    ''' Execute clear line on idle vty sessions
        Agrs:
            device ('obj'): Device object
            idle_timeout (int, optional): idle session timeout. Defaults to 60
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    output = device.parse("show users")
    log.debug(f"Parsed output of show users {output}")
    line_number = []
    # get line dict values
    line_dict = output.get("line", {})
    for line, line_data in line_dict.items():
        # clear line only for non active sessions
        if 'vty' in line and not line_data.get("active"):
            # convert the timestamp to seconds using the utility function
            # Use Dq to get the value of idle timeout
            idle_time = line_data.get("idle")
            if idle_time:
                if time_to_int(idle_time) > idle_timeout:
                    get_line_num = line.split(" ")[0]
                    line_number.append(get_line_num)
            else:
                log.warning("Cannot find the idle timeout, not clearing vty sessions")
                return

    if len(line_number) > 0:
        for line in line_number:
            device.execute(f"clear line {line}")
    else:
        log.info("No idle sessions, not clearing vty sessions")
        return

import time
from unicon.eal.dialogs import Statement, Dialog
import logging 

logger = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def execute_monitor_event_trace_crypto_pki(
                                            device,
                                            action,
                                            clear=False,
                                            continuous=False,
                                            disable=False,
                                            dump=False,
                                            enable=False,
                                            internal=False,
                                            one_shot=False,
                                            event_data_url=None,
                                            pretty=False,
                                            cancel=False
                                        ):
    """
    Execute 'monitor event-trace crypto pki <action>' command with optional flags.

    Args:
        device (obj): Device object on which to run the command.
        action (str): Must be either 'event' or 'error'.
        clear (bool): Clear the trace buffer.
        continuous (bool): Continuously display latest trace entries.
        disable (bool): Disable event/error tracing.
        dump (bool): Dump trace buffer to a file.
        enable (bool): Enable event/error tracing.
        internal (bool): (Only for 'event') Use 'internal' sub-mode.
        one_shot (bool): Stop automatically when buffer wraps.
        event_data_url (str): URL to store event data.
        pretty (bool): Dump trace in ASCII format.
        cancel (bool): Cancel continuous monitoring.
    Returns:
        None
    Raises:
        SubCommandFailure: If command execution fails.
        ValueError: If invalid action is provided.
    """

    if action not in ["event", "error"]:
        raise ValueError("Action must be either 'event' or 'error'.")

    if action == "error" and internal:
        raise ValueError("The 'internal' option is only valid with 'event' action.")

    cmds = []

    if action == "event" and internal:
        if clear:
            cmds.append("monitor event-trace crypto pki event internal clear")
        if continuous:
            cmds.append("monitor event-trace crypto pki event internal continuous")
            if cancel:
                cmds.append("monitor event-trace crypto pki event internal continuous cancel")
        if disable:
            cmds.append("monitor event-trace crypto pki event internal disable")
        if dump:
            if pretty and event_data_url:
                cmds.append(f"monitor event-trace crypto pki event internal dump pretty {event_data_url}")
            elif event_data_url:
                cmds.append(f"monitor event-trace crypto pki event internal dump {event_data_url}")
            else:
                cmds.append("monitor event-trace crypto pki event internal dump")
        if enable:
            cmds.append("monitor event-trace crypto pki event internal enable")
        if one_shot:
            cmds.append("monitor event-trace crypto pki event internal one-shot")

    elif action == "event" and not internal:
        if clear:
            cmds.append("monitor event-trace crypto pki event clear")
        if continuous:
            cmds.append("monitor event-trace crypto pki event continuous")
            if cancel:
                cmds.append("monitor event-trace crypto pki event continuous cancel")
        if disable:
            cmds.append("monitor event-trace crypto pki event disable")
        if dump:
            if pretty and event_data_url:
                cmds.append(f"monitor event-trace crypto pki event dump pretty {event_data_url}")
            elif event_data_url:
                cmds.append(f"monitor event-trace crypto pki event dump {event_data_url}")
            else:
                cmds.append("monitor event-trace crypto pki event dump")
        if enable:
            cmds.append("monitor event-trace crypto pki event enable")
        if one_shot:
            cmds.append("monitor event-trace crypto pki event one-shot")

    elif action == "error":
        if clear:
            cmds.append("monitor event-trace crypto pki error clear")
        if continuous:
            cmds.append("monitor event-trace crypto pki error continuous")
            if cancel:
                cmds.append("monitor event-trace crypto pki error continuous cancel")
        if disable:
            cmds.append("monitor event-trace crypto pki error disable")
        if dump:
            if pretty and event_data_url:
                cmds.append(f"monitor event-trace crypto pki error dump pretty {event_data_url}")
            elif event_data_url:
                cmds.append(f"monitor event-trace crypto pki error dump {event_data_url}")
            else:
                cmds.append("monitor event-trace crypto pki error dump")
        if enable:
            cmds.append("monitor event-trace crypto pki error enable")
        if one_shot:
            cmds.append("monitor event-trace crypto pki error one-shot")

    try:
        device.execute(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute monitor event-trace crypto pki command: {e}")
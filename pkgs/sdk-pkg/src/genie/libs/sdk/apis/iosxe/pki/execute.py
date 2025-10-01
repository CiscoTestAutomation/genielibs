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
        

def clear_crypto_pki(device, benchmarks=False, counters=False, crl=False):
    """
    Execute 'clear crypto pki <option>' commands based on flags.

        Args:
            device (obj): pyATS device object.
            benchmarks (bool): Clear PKI Benchmark Data if True.
            counters (bool): Clear PKI Counters if True.
            crl (bool): Clear Certificate Revocation List (CRL) if True.
        Returns:
            None
        Raises:
            SubCommandFailure: If device.execute fails.
    """
    cmds = []

    if benchmarks:
        cmds.append("clear crypto pki benchmarks")
    if counters:
        cmds.append("clear crypto pki counters")
    if crl:
        cmds.append("clear crypto pki crl")

    try:
        for cmd in cmds:
            device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute clear crypto pki command(s): {e}")


def execute_crypto_pki_certificate_validate(device, tp_name):
    """
    Execute 'crypto pki certificate validate <tp_name>' command.
        Args:
            device (obj): Device object on which to run the command.
            tp_name (str): Trustpoint name whose certificate needs validation.
        Returns:
            None
        Raises:
            SubCommandFailure: If command execution fails.
    """
    cmd = [f'crypto pki certificate validate {tp_name}']
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to validate crypto pki certificate: {e}")


def execute_trim_crypto_pki_certificate(device, server_name=None, generate_expired_list=False, url=None, trim_url=False):
    """
    Execute crypto pki server trim commands to manage certificate trimming operations.
        Args:
            device (`obj`): Device object
            server_name (`str`): Name of the PKI server
            generate_expired_list (`bool`): Generate expired certificate list. Default is False.
            url (`str`): URL for trim operations (required if generate_expired_list or trim_url is True)
            trim_url (`bool`): Execute trim operation with URL. Default is False.
        Returns:
            str: Command execution output
        Raises:
            ValueError: If URL is required but not provided
            SubCommandFailure: If command execution fails
    """
    cmds = []
    
    if generate_expired_list and url:
        cmds.append(f"crypto pki server {server_name} trim generate expired-list url {url}")

    if trim_url and url:
        cmds.append(f"crypto pki server {server_name} trim url {url}")

    if not cmds:
        raise ValueError("No valid trim operation specified. Enable generate_expired_list or trim_url.")

    try:
        output = device.execute(cmds)
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute crypto pki server trim commands: {e}")

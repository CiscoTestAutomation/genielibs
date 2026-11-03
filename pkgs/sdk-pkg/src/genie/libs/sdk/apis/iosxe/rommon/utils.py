''' Utility functions for rommon'''

import time
import logging
import re
import inspect
from functools import partial
from threading import Event

from pyats.log.utils import banner
from pyats.utils.secret_strings import to_plaintext

# Unicon
from unicon import Connection
from unicon.core.errors import SubCommandFailure, StateMachineError
from unicon.eal.dialogs import Statement, Dialog
from concurrent.futures import ThreadPoolExecutor, wait as wait_futures, ALL_COMPLETED
from unicon.plugins.iosxe.statements import grub_prompt_handler, please_reset_handler, rommon_prompt_handler
from unicon.plugins.generic.patterns import GenericPatterns
from unicon.plugins.generic.statements import (
    authentication_statement_list, custom_auth_statements,
    generic_statements)

# Genie
from genie.libs.clean.exception import FailedToBootException
from genie.libs.sdk.apis.iosxe.rommon.get import _normalize_image_paths
from genie.libs.sdk.apis.iosxe.rommon.configure import (
    _capture_rommon_tftp_image, _verify_rommon_tftp_file,
    configure_rommon_tftp, configure_rommon_tftp_ha,
)

log = logging.getLogger(__name__)

def device_rommon_boot(device, golden_image=None, tftp_boot=None, error_pattern=[],
                       grub_activity_pattern=None, timeout=None, *, tftp_boot_state=None):
    '''Boot device using golden image or using tftp image
        Args:
            device: device object
            golden_image(`list`): Golden image to boot the device.
            tftp_boot:
                image: One image path or supported Clean image/file metadata.
                tftp_server('str'): tftp server information.
                Explicit TFTP options override a default golden image in Clean
                recovery data, but an explicitly supplied golden_image still
                takes precedence as before.
            error_pattern(`list`): Error patterns to check for during boot.
            grub_activity_pattern(`str`): Custom grub activity pattern.
                Defaults to '.*Use the UP and DOWN arrow keys to select.*'
            timeout(`int`, optional): Timeout for boot operation. If not provided,
                uses device_recovery timeout or defaults to 2000 seconds.

            tftp_boot_state (dict, optional): Stage-owned transport selection cache
                shared across outer retries. Omit for a standalone boot operation.
                Reuses the successfully configured provider transport path and
                does not modify the caller's image metadata.

        Return:
            None
        Raise:
            Exception
    '''

    log.info(f'Get the recovery details from clean for device {device.name}')
    recovery_info = device.api.get_recovery_details(golden_image, tftp_boot)
    cmd = ""

    # Explicit TFTP options must not fall back to a configured golden image.
    use_tftp = (bool(tftp_boot) and not golden_image) or not recovery_info['golden_image']
    if tftp_boot_state is None:
        tftp_boot_state = {}
    if use_tftp and not tftp_boot_state:
        resolved_tftp = recovery_info.get('tftp_boot', {})
        if 'image' in resolved_tftp:
            # Legacy/plugin selectors must receive paths, not image/file wrappers.
            image_paths = _normalize_image_paths(resolved_tftp['image'])
            recovery_info = {**recovery_info, 'tftp_image': image_paths,
                             'tftp_boot': {**resolved_tftp, 'image': image_paths}}
        cmd, selected_image = device.api.get_tftp_boot_command(recovery_info)
        # Reject invalid paths returned by platform API overrides.
        selected_image = _normalize_image_paths(selected_image)[0]
    elif use_tftp:
        selected_image = _normalize_image_paths(tftp_boot_state.get('image'))[0]
        cmd = tftp_boot_state['command']

    # For HA/stack devices, ensure all consoles are in rommon before proceeding
    if device.is_ha and hasattr(device, 'subconnections'):
        log.info(f'Checking console states for HA/stack device {device.name}')
        rommon_conns = [con for con in device.subconnections if con.state_machine.current_state == 'rommon']
        non_rommon_conns = [con for con in device.subconnections if con.state_machine.current_state != 'rommon']

        # Only sync if there's a MIX of states (some rommon, some not)
        if rommon_conns and non_rommon_conns:
            log.info(f'Mixed console states detected - synchronizing all consoles to rommon state')
            log.info(f'Rommon consoles: {[con.alias for con in rommon_conns]}')
            log.info(f'Non-rommon consoles: {[con.alias for con in non_rommon_conns]}')
            device.rommon()
        else:
            pass

        final_states = {con.alias: con.state_machine.current_state for con in device.subconnections}
        log.info(f'Final console states after synchronization: {final_states}')
        if not all(state == 'rommon' for state in final_states.values()):
            raise Exception(f"{device.name} failed to sync all consoles to rommon state")

    # Execute config register in rommon state
    log.info(f"Setting config register for device {device.name}")
    device.api.execute_set_config_register(config_register='0x0')

    # Execute reset command, supported platforms: asr1k, isr4k
    log.info(f"Executing ROMMON reset for device {device.name}")
    device.api.execute_rommon_reset()

    # Configure ignore startup config
    log.info(f"Setting ignore startup config for device {device.name}")
    device.api.configure_ignore_startup_config()

    # To boot using golden image
    if not use_tftp:
        log.info(banner("Booting device '{}' with the Golden images".\
                        format(device.name)))
        log.info("Golden image information found:\n{}".format(recovery_info['golden_image']))
        golden_image = recovery_info['golden_image'][0]
        cmd = f"{golden_image}"

    # To boot using tftp information
    else:
        log.info(banner("Booting device '{}' with the Tftp images".\
                        format(device.name)))
        log.info("Tftp boot information found:\n{}".format(recovery_info['tftp_boot']))
        # Setting rommon variables for booting
        log.info(f'Setting the rommon variables for TFTP boot device {device.name}')
        configure = (configure_rommon_tftp_ha if device.is_ha and hasattr(device, 'subconnections')
                     else configure_rommon_tftp)
        if tftp_boot_state:
            # Replay the validated transport path, not its provider transformation.
            tftp_boot_state['configure']()
        else:
            if cmd.startswith('tftp://'):
                # A URL selector has already performed provider translation.
                configure(device, image_path=selected_image)
            else:
                api = (device.api.configure_rommon_tftp_ha if configure is configure_rommon_tftp_ha
                       else device.api.configure_rommon_tftp)
                with _capture_rommon_tftp_image() as configured_images:
                    api(image_path=selected_image)
                if not configured_images or len(set(configured_images)) != 1:
                    raise SubCommandFailure(
                        'ROMMON TFTP provider did not expose one successfully configured transport image. '
                        'Use a provider that delegates to configure_rommon_tftp; aborting boot.')
                selected_image = _normalize_image_paths(configured_images[0])[0]
            tftp_boot_state.update(command=cmd, image=selected_image,
                                   configure=partial(configure, device, image_path=selected_image))
            log.info('Selected authoritative ROMMON TFTP transport image: %s', selected_image)

    # Timeout for device to reload - use provided timeout or get from device_recovery
    if timeout is None:
        timeout = device.clean.get('device_recovery', {}).get('timeout', 2000)
    boot_timeout = 60

    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    def task(conn, cmd, timeout, grub_activity_pattern):
        """
        Sets the image to boot in the connection's context and transitions
        the connection's state machine to 'enable' mode.
        This function is designed to be executed concurrently for multiple connections and
        handles the necessary steps to boot the device with that image.
        """

        # if we have grub activity pattern then we need to update the context with grub boot image
        if grub_activity_pattern:
            image_to_boot = conn.context.get('grub_boot_image')
            conn.context['grub_boot_image'] = cmd

        # check for image to boot if we have a value store it and replace it with the golden image
        image_to_boot = conn.context.get('image_to_boot')
        conn.context['image_to_boot'] = cmd

        def _set_selected_tftp_file():
            output = conn.execute(f'TFTP_FILE={selected_image}', timeout=timeout)
            # Some ROMMONs return assignment errors as text instead of raising.
            if isinstance(output, str):
                usage = re.search(r'\bUsage:\s*set\b[^\r\n]*', output, re.IGNORECASE)
                if usage:
                    raise SubCommandFailure(
                        f'ROMMON rejected TFTP_FILE assignment: {usage.group(0)}')
            _verify_rommon_tftp_file(device, selected_image, connection=conn)

        # these statments needed for booting from grub menu
        def _grub_boot_device(spawn, session, context):
            # '\033' == <ESC>
            spawn.send('\033')
            time.sleep(0.5)

        grub_prompt_stmt = \
            Statement(pattern=r'.*grub *>.*',
                    action=_grub_boot_device,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        grub_boot_stmt = \
            Statement(pattern=r'.*Use the UP and DOWN arrow keys to select.*',
                    action=grub_prompt_handler,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        def _mark_switch_conflict(spawn, session, context):
            log.info('Detected switch number conflict with peer. Will resend boot command at switch prompt.')

        def _rommon_switch_boot(spawn, session, context):
            session.setdefault('boot_attempt_count', 0)

            if session['boot_attempt_count'] >= spawn.settings.MAX_BOOT_ATTEMPTS:
                raise Exception(
                    "Too many failed boot attempts detected from ROMMON."
                    if 'image_to_boot' in context
                    else "ROMMON prompt detected but image_to_boot not provided."
                )

            if use_tftp:
                # A failed boot may reset ROMMON variables before this inner retry.
                _set_selected_tftp_file()

            cmd = 'boot {}'.format(context['image_to_boot']) \
                if 'image_to_boot' in context else ''

            session['boot_attempt_count'] += 1
            log.info('Reached switch prompt. Sending boot command to boot the device.')
            log.info(f'Boot command to send: {context.get("image_to_boot")}')
            log.info(f"ROMMON boot attempt "
                     f"{session['boot_attempt_count']}/{spawn.settings.MAX_BOOT_ATTEMPTS}")
            spawn.sendline(cmd)

        switch_conflict_stmt = \
            Statement(pattern=r'.*switch num conflicts with peer.*',
                    action=_mark_switch_conflict,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        switch_prompt_stmt = \
            Statement(pattern=GenericPatterns().rommon_prompt,
                    action=_rommon_switch_boot,
                    args=None,
                    loop_continue=True,
                    continue_timer=False)

        dialog = Dialog([grub_boot_stmt, grub_prompt_stmt, switch_conflict_stmt, switch_prompt_stmt])

        # bring rommon to disable state
        try:
            conn.state_machine.go_to('disable',
                                     conn.spawn,
                                     timeout=timeout,
                                     context=conn.context,
                                     dialog=dialog)
        finally:
            # Restore context even if a boot or TFTP_FILE assignment failed.
            if grub_activity_pattern:
                conn.context['grub_boot_image'] = image_to_boot
            conn.context['image_to_boot'] = image_to_boot
    executor = None
    try:
        futures = []
        executor = ThreadPoolExecutor(max_workers=len(conn_list))
        for conn in conn_list:
            # Submit each connection's task to the executor.
            futures.append(executor.submit(
                task,
                conn,
                cmd,
                timeout,
                grub_activity_pattern,
            ))
        wait_futures(futures, timeout=timeout, return_when=ALL_COMPLETED)
        for future in futures:
            # wait() does not propagate worker failures or report incomplete boots.
            future.result(timeout=0)
    except SubCommandFailure:
        raise
    except Exception as e:
        # Unicon wraps fatal dialog actions; do not turn an assignment rejection
        # into a retryable boot failure and lose its actionable error message.
        if isinstance(e, StateMachineError) and isinstance(e.__cause__, SubCommandFailure):
            raise SubCommandFailure(str(e.__cause__)) from e
        log.error(str(e))
        raise FailedToBootException(f"Failed to boot the device {device.name}: {e}") from e
    else:
        # Verify that all connections have left rommon state before
        # declaring the boot successful.
        for conn in conn_list:
            state_machine = getattr(conn, 'state_machine', None)
            current_state = getattr(state_machine, 'current_state', None)
            if current_state == 'rommon':
                log.error(f"Device {device.name} remained in rommon state after boot attempt")
                raise FailedToBootException(f"Failed to boot the device {device.name}")
        log.info(f"Successfully boot the device {device.name}")
        log.info(f"Waiting for {boot_timeout} seconds for device to stabilize after booting")
        time.sleep(boot_timeout)

    finally:
        if executor is not None:
            # Do not start an outer Clean retry while an earlier boot is still sending commands.
            executor.shutdown(wait=True)

    if device.is_ha:
        # designate handle method will bring the device to enable mode
        device.connection_provider.designate_handles()
    else:
        device.enable()

    # Init connection settings (term length, etc.)
    log.info('Initialize connection settings')
    device.connection_provider.init_connection()

    # Configure the login credentials
    log.info(f'Configure the login credentials {device.name}')
    device.api.configure_management_credentials()

    # Unconfigure the ignore startup config
    log.info(f'Unconfigure the ignore startup config {device.name}')
    device.api.unconfigure_ignore_startup_config()

    # verify the rommon variable
    log.info(f'verify the ignore startup config on {device.name}')
    if device.api.verify_ignore_startup_config():
        raise Exception(f"Failed to unconfigure the ignore startup config on {device.name}")

    # Execute write memory
    log.info(f'Executing write memory {device.name}')
    device.api.execute_write_memory()

def send_break_boot(device, console_activity_pattern= None,
                    console_breakboot_char=None, console_breakboot_telnet_break=None,
                    grub_activity_pattern=None, grub_breakboot_char=None,
                    break_count=2, timeout=60):
    """ Connects to the device, waits for the (console or grub) activity pattern and
        sends break boot character to interrupt boot. Device is expected to reach rommon state.

        On reconnect, configured Unicon login credentials are used to
        authenticate an intermediate terminal server before monitoring boot.

        Args:
            device ('obj'): Device object
            console_activity_pattern (str): Pattern to send the break at. Defaults to
                                            three or more consecutive dots.
            console_breakboot_char (str): Character to send when console_activity_pattern is matched. Default to '\x03'.
            console_breakboot_telnet_break (bool): Use telnet `send break` to interrupt device boot.
            grub_activity_pattern (str): Break pattern on the device for grub boot mode
            grub_breakboot_char (str): Character to send when grub_activity_pattern is matched
            break_count (int, optional): Number of break commands to send. Defaults to 2.
            timeout (int, optional): Break boot process timeout. Defaults to 60.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    console_activity_pattern = console_activity_pattern or r'\.{3,}'
    console_breakboot_char = console_breakboot_char or '\x03'

    def telnet_breakboot(spawn, break_count, cancel_event=None):
        """ Breaks the booting process on a device using telnet `send break`

            Args:
                spawn (obj): Spawn connection object
                break_count (int): Number of break commands to send
                cancel_event (Event, optional): Stops further device input
                    when set

            Returns:
                None
        """

        log.info(f"Found the console_activity_pattern! Breaking the boot process using telnet break.")

        for _ in range(break_count):
            if cancel_event is not None and cancel_event.is_set():
                return
            log.info(f"Using telnet break")
            spawn.send('\x1d')
            spawn.expect(r'telnet>\s*$')
            if cancel_event is not None and cancel_event.is_set():
                return
            spawn.sendline('send break')
            spawn.expect('.+')
            if cancel_event is not None and cancel_event.is_set():
                return
            time.sleep(2)
            if cancel_event is not None and cancel_event.is_set():
                return

    def console_breakboot(spawn, break_count, break_char, rommon_patterns,
                          cancel_event=None):
        """ Breaks the booting process on a device

            Args:
                spawn (obj): Spawn connection object
                break_count (int): Number of break commands to send
                break_char (str): Char to send
                rommon_patterns (list): ROMMON state prompt patterns
                cancel_event (Event, optional): Stops further device input
                    when set

            Returns:
                None
        """

        log.info("Found the console_activity_pattern! Breaking the boot process.")

        for _ in range(break_count):
            if cancel_event is not None and cancel_event.is_set():
                return
            log.info(f"Sending {repr(break_char)}")
            spawn.send(break_char)
            time.sleep(1)
            if cancel_event is not None and cancel_event.is_set():
                return
            # Dialog cannot evaluate state patterns while this synchronous
            # action runs. Check the last line, matching prompt-detection
            # semantics, before sending another break.
            spawn.read_update_buffer()
            lines = spawn.buffer.splitlines()
            if lines and any(
                    re.search(pattern, lines[-1])
                    for pattern in rommon_patterns):
                return

    def grub_breakboot(spawn, context, break_char, cancel_event=None):
        """ Breaks the booting process on a device

            Args:
                spawn (obj): Spawn connection object
                context (dict): Context dictionary
                break_char (str): Char to send
                cancel_event (Event, optional): Stops further device input
                    when set

            Returns:
                None
        """

        log.info(f"Found the grub_activity_pattern! Breaking the boot process "
                 f"by sending {repr(break_char)}")

        if cancel_event is not None and cancel_event.is_set():
            return
        spawn.send(break_char)
        # Set boot_cmd to ENTER for C8KV grub> mode
        # ENTER boots the highlighted entry
        context['boot_cmd'] = '\r'

    # Set a target for each recovery session
    # so it's easier to distinguish expect debug logs on the console.
    if (getattr(device, "is_ha", False) and not getattr(device, "subconnections", None)) or \
            (not getattr(device, "is_ha", False) and not getattr(device, "spawn", None)):
        device.instantiate(connection_timeout=timeout)

    def get_connections(parent=None):
        """Return the connection objects currently owned by the device."""
        if parent is None:
            parent = device.default
        if device.is_ha:
            # Prefer the current parent connection. OS/token discovery may
            # replace device.default while connect() is in progress, and the
            # old connection's subconnection/spawn references are stale.
            parent_subconnections = getattr(parent, 'subconnections', None)
            if isinstance(parent_subconnections, (list, tuple)) and \
                    parent_subconnections:
                return list(parent_subconnections)
            device_subconnections = getattr(
                device, 'subconnections', None)
            if isinstance(device_subconnections, (list, tuple)) and \
                    device_subconnections:
                return list(device_subconnections)
        return [parent]

    conn_list = get_connections()

    def get_break_boot_dialog(connections, cancel_event=None):
        """Build the statements that are specific to interrupting boot."""
        break_boot_dialog = Dialog()

        # Either use break character or telnet escape break
        # break character is ctrl-c by default
        if console_activity_pattern and console_breakboot_char and \
                not console_breakboot_telnet_break:
            rommon_patterns = []
            for connection in connections:
                pattern = connection.state_machine.get_state('rommon').pattern
                if pattern not in rommon_patterns:
                    rommon_patterns.append(pattern)
            action_args = {
                'break_count': break_count,
                'break_char': console_breakboot_char,
                'rommon_patterns': rommon_patterns,
            }
            if cancel_event is not None:
                action_args['cancel_event'] = cancel_event
            break_boot_dialog.append(
                Statement(pattern=console_activity_pattern,
                          action=console_breakboot,
                          args=action_args,
                          loop_continue=True,
                          continue_timer=False))

        # telnet escape is used only if user specified
        if console_activity_pattern and console_breakboot_telnet_break:
            action_args = {'break_count': break_count}
            if cancel_event is not None:
                action_args['cancel_event'] = cancel_event
            break_boot_dialog.append(
                Statement(pattern=console_activity_pattern,
                          action=telnet_breakboot,
                          args=action_args,
                          loop_continue=True,
                          continue_timer=False))

        # grub_activity_pattern is used only if user specified
        if grub_activity_pattern and grub_breakboot_char:
            action_args = {'break_char': grub_breakboot_char}
            if cancel_event is not None:
                action_args['cancel_event'] = cancel_event
            break_boot_dialog.append(
                Statement(pattern=grub_activity_pattern,
                          action=grub_breakboot,
                          args=action_args,
                          loop_continue=True,
                          continue_timer=False))

        return break_boot_dialog

    def get_connected_break_boot_dialog(conn, cancel_event):
        """Build the replacement dialog for an existing connection."""
        def update_state(spawn, state):
            """Log matched state prompt and update current_state."""
            spawn.log.info(
                f'Device reached {state.name} state in break boot stage')
            conn.state_machine.update_cur_state(state.name)

        connection_dialog = get_break_boot_dialog(
            [conn], cancel_event=cancel_event)

        # Add all state patterns as break-boot dialog exit points and update
        # current_state here, like state_machine.go_to() does for transitions.
        for state in conn.state_machine.states:
            connection_dialog.append(
                Statement(
                    state.pattern,
                    action=update_state,
                    args={'state': state},
                )
            )
        log.debug(f'Final connection dialog {connection_dialog}')

        return connection_dialog

    def verify_rommon_state(con):
        if con.state_machine.current_state != 'rommon':
            # Check the device state after breaking the boot process if not in
            # rommon. Avoid the extra probe when the dialog already matched
            # rommon, as some sessions close immediately after the prompt.
            con.sendline()
            con.state_machine.go_to(
                'any', spawn=con.spawn, context=con.context,
                timeout=timeout)

        if con.state_machine.current_state != 'rommon':
            log.warning(f"The device {device.name} is not in rommon")

    def task(con, cancel_event):

        dialog = get_connected_break_boot_dialog(con, cancel_event)

        # Use configured login credentials during break-boot handling.
        login_creds = con.context.get('login_creds')
        had_cred_list = 'cred_list' in con.context
        previous_cred_list = con.context.get('cred_list')
        if login_creds:
            con.context['cred_list'] = login_creds

        try:
            dialog.process(
                con.spawn,
                timeout=timeout,
                context=con.context,
                prompt_recovery=True
            )

            if cancel_event.is_set():
                return
            verify_rommon_state(con)
        finally:
            if had_cred_list:
                con.context['cred_list'] = previous_cred_list
            else:
                con.context.pop('cred_list', None)

    if not device.connected:
        connect_parameters = inspect.signature(Connection.connect).parameters
        required_parameters = {'connection_dialog', 'skip_initialization'}
        if not required_parameters.issubset(connect_parameters):
            raise SubCommandFailure(
                'send_break_boot requires a Unicon version whose '
                'Connection.connect() supports connection_dialog and '
                'skip_initialization')

        # Let Unicon own the initial connection and any connection-refused
        # recovery. The replacement dialog prevents normal connection
        # statements from sending input while this API is trying to interrupt
        # boot, and skip_initialization stops after authoritative state
        # detection without token learning or normal provider initialization.
        parent = device.default
        original_connection_timeouts = [
            (connection, connection.connection_timeout)
            for connection in conn_list
        ]
        try:
            for connection, _ in original_connection_timeouts:
                connection.connection_timeout = timeout
            # The replacement dialog bypasses Unicon's login dialog. Retain
            # its authentication handlers, but not other connection handlers
            # that may send input during the boot-break window. Multi-RP and
            # stack providers use this dialog for every subconnection.
            connection_dialog = Dialog([
                generic_statements.connection_refused_stmt,
            ])
            custom_patterns = set()
            for connection in conn_list:
                for statement in custom_auth_statements(
                        connection.settings.LOGIN_PROMPT,
                        connection.settings.PASSWORD_PROMPT) or []:
                    if statement.pattern not in custom_patterns:
                        connection_dialog.append(statement)
                        custom_patterns.add(statement.pattern)
            # Password OK acknowledges the terminal server, not the DUT.
            # Its normal callback probes the console and may miss boot output.
            for statement in authentication_statement_list:
                if statement is not generic_statements.password_ok_stmt:
                    connection_dialog.append(statement)
            for statement in get_break_boot_dialog(conn_list):
                connection_dialog.append(statement)
            parent.connect(
                connection_dialog=connection_dialog,
                skip_initialization=True)
        finally:
            for connection, original_timeout in original_connection_timeouts:
                connection.connection_timeout = original_timeout

        # Refresh the references defensively if a provider replaced the
        # connection object while establishing the session. Do not copy
        # temporary attributes from the previous object to the replacement.
        conn_list = get_connections(getattr(device, 'default', parent))
        for con in conn_list:
            verify_rommon_state(con)
        return

    futures = {}
    executor = ThreadPoolExecutor(max_workers=len(conn_list))
    try:
        for con in conn_list:
            cancel_event = Event()
            future = executor.submit(
                task,
                con,
                cancel_event,
            )
            futures[future] = (con, cancel_event)
        done, not_done = wait_futures(
            list(futures), timeout=timeout, return_when=ALL_COMPLETED)

        # Propagate exceptions from workers that completed within the timeout.
        worker_error = None
        for future in futures:
            if future in done:
                try:
                    future.result()
                except Exception as error:
                    if worker_error is None:
                        worker_error = error

        if worker_error is not None or not_done:
            for future in not_done:
                con, cancel_event = futures[future]
                cancel_event.set()
                if not future.cancel():
                    try:
                        con.spawn.close()
                    except Exception as error:
                        log.warning(
                            'Failed to close %s while cancelling break boot: '
                            '%s', getattr(con, 'alias', 'connection'), error)

            # Running workers must release their spawn before the caller can
            # reuse or clean up the connection.
            executor.shutdown(wait=True, cancel_futures=True)
            executor = None

        if worker_error is not None:
            raise worker_error

        if not_done:
            raise SubCommandFailure(
                f'Break boot timed out after {timeout} seconds for device '
                f'{device.name}; {len(not_done)} connection(s) did not finish')
    finally:
        if executor is not None:
            executor.shutdown(wait=True, cancel_futures=True)

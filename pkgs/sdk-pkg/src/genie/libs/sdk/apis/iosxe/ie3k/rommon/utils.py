''' Utility functions for rommon'''

import time
import logging

from pyats.log.utils import banner

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from concurrent.futures import ThreadPoolExecutor, wait as wait_futures, ALL_COMPLETED
from unicon.plugins.generic.patterns import GenericPatterns

# Genie
from genie.libs.clean.exception import FailedToBootException


log = logging.getLogger(__name__)


def device_rommon_boot(device, golden_image=None, tftp_boot=None, error_pattern=[],
                       grub_activity_pattern=None, timeout=None):
    '''Boot device using `golden_image` or with images obtained from `get_recovery_details`.

    Differs from IOS-XE implementation in that:
        - TFTP boot is not supported in IE3k, related logic is removed.
        - Config register cannot be set in IE3k, so related config/verification steps are removed.
        - No grub boot in IE3k, so grub_activity_pattern is not applicable.
        - Supports retry on multiple golden images obtained from `get_recovery_details`, whereas
          IOS-XE implementation only attempts to boot with a single golden image.
        - Increased default timeout of 3600 seconds over 2000 seconds for IOS-XE to accomodate
          for multiple boot attempts with different images.
        - Extra logic to destroy threads still attempting to boot after overall timeout is
          reached, to prevent orphaned threads from continuing to run indefinitely.

    Args:
        device: device object
        golden_image(`list`): Golden image to boot the device.
        tftp_boot: Unused, TFTP boot is not supported for IE3k.
        error_pattern(`list`): Unused.
        grub_activity_pattern(`str`): Unused, Grub boot is not supported for IE3k.
        timeout(`int`, optional): Timeout for boot operation. If not provided,
            uses device_recovery timeout or defaults to 3600 seconds.

    Return:
        None

    Raise:
        Exception if:
            1. If device fails to boot within the timeout period.
            2. If device remains in rommon state after boot attempt.
    '''

    log.info(f'Get the recovery details from clean for device {device.name}')
    recovery_info = device.api.get_recovery_details(golden_image, None)

    log.info(f"Executing ROMMON reset for device {device.name}")
    device.api.execute_rommon_reset()

    images = []
    if recovery_info:
        images = recovery_info.get('golden_image') or []

    if images:
        log.info(banner("Booting device '{}' with the Golden images".\
                        format(device.name)))
        log.info("Golden image information found:\n{}".format(images))
    else:
        log.info(
            f"No SSA golden image found for device {device.name}. "
            "Will attempt default ROMMON 'boot' command."
        )
        images = [None]

    # Timeout for device to reload - use provided timeout or get from device_recovery
    if timeout is None:
        timeout = device.clean.get('device_recovery', {}).get('timeout', 3600)
    boot_deadline = time.monotonic() + timeout

    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    def task(conn, images, deadline):
        """
        Iterates over all golden images, attempting to boot the device with each one.
        For each image, up to MAX_BOOT_ATTEMPTS boot commands are sent before moving
        on to the next image. A fresh Dialog is created per image so that the
        boot_attempt_count resets between images.
        This function is designed to be executed concurrently for multiple connections.
        """

        boot_cmd_orig = conn.context.get('boot_cmd')

        def _mark_switch_conflict(spawn, session, context):
            log.info('Detected switch number conflict with peer. Will resend boot command at switch prompt.')

        def _rommon_switch_boot(spawn, session, context):
            session.setdefault('boot_attempt_count', 1)

            if session['boot_attempt_count'] >= spawn.settings.MAX_BOOT_ATTEMPTS:
                raise Exception(
                    "Too many failed boot attempts detected from ROMMON."
                    if 'boot_cmd' in context
                    else "ROMMON prompt detected but boot_cmd not provided."
                )

            boot_cmd = context.get('boot_cmd') or 'boot'

            session['boot_attempt_count'] += 1
            log.info('Reached switch prompt. Sending boot command to boot the device.')
            log.info(f'Boot command to send: {boot_cmd}')
            log.info(f"ROMMON boot attempt "
                     f"{session['boot_attempt_count']}/{spawn.settings.MAX_BOOT_ATTEMPTS}")
            spawn.sendline(boot_cmd)

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

        last_exc = None
        for image in images:
            remaining_timeout = deadline - time.monotonic()
            if remaining_timeout <= 0:
                conn.context['boot_cmd'] = boot_cmd_orig
                raise Exception(
                    f"Overall timeout expired before booting image '{image}' on "
                    f"connection '{conn.alias}'. Last error: {last_exc}"
                )

            if image:
                log.info(f"Attempting to boot connection '{conn.alias}' with image: {image}")
                conn.context['boot_cmd'] = f"boot {image}"
            else:
                log.info(f"Attempting to boot connection '{conn.alias}' with boot variable image")
                conn.context['boot_cmd'] = 'boot'

            # Create a fresh Dialog per image so boot_attempt_count resets each time
            dialog = Dialog([switch_conflict_stmt, switch_prompt_stmt])

            # Bring rommon to disable state
            try:
                conn.state_machine.go_to('disable',
                                         conn.spawn,
                                         timeout=remaining_timeout,
                                         context=conn.context,
                                         dialog=dialog)
            except Exception as e:
                last_exc = e
                log.warning(f"Boot attempt with image '{image}' on connection '{conn.alias}' "
                            f"failed: {e}. Trying next image.")

            # Successfully left rommon - stop trying further images
            if conn.state_machine.current_state != 'rommon':
                conn.context['boot_cmd'] = boot_cmd_orig
                return
            else:
                log.warning(f"Connection '{conn.alias}' remained in rommon after booting "
                            f"with image '{image}'. Trying next image.")

        conn.context['boot_cmd'] = boot_cmd_orig
        raise Exception(
            f"All golden images exhausted for connection '{conn.alias}'. "
            f"Last error: {last_exc}"
        )

    futures = []
    executor = ThreadPoolExecutor(max_workers=len(conn_list))
    try:
        for conn in conn_list:
            # Submit each connection's task to the executor.
            futures.append(executor.submit(
                task,
                conn,
                images,
                boot_deadline,
            ))

        done, not_done = wait_futures(futures, timeout=timeout, return_when=ALL_COMPLETED)
        if not_done:
            raise FailedToBootException(
                f"Failed to boot device {device.name}. Timeout expired after {timeout} seconds "
                f"with {len(not_done)} connection(s) still booting."
            )

        for future in done:
            try:
                future.result()
            except Exception as exc:
                raise FailedToBootException(
                    f"Failed to boot device {device.name}: {exc}"
                ) from exc
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    # Identify all connections that are still in rommon.
    rommon_connections = []
    for conn in conn_list:
        state_machine = getattr(conn, 'state_machine', None)
        current_state = getattr(state_machine, 'current_state', None)
        if current_state == 'rommon':
            conn_alias = getattr(conn, 'alias', 'unknown')
            rommon_connections.append(conn_alias)
            log.error(
                f"Connection '{conn_alias}' on device '{device.name}' "
                f"remained in rommon after boot attempts."
            )

    if rommon_connections:
        raise FailedToBootException(
            f"Failed to boot device {device.name}. Connections still in rommon: "
            f"{', '.join(rommon_connections)}"
        )

    log.info(f"Successfully boot the device {device.name}")

    log.info("Waiting for 60 seconds for device to stabilize after booting")
    time.sleep(60)

    if device.is_ha:
        # designate handle method will bring the device to enable mode
        device.connection_provider.designate_handles()
    else:
        device.enable()

    # Init connection settings (term length, etc.)
    log.info('Initialize connection settings')
    device.connection_provider.init_connection()

    log.info(f'Configure the login credentials {device.name}')
    device.api.configure_management_credentials()

    log.info(f'Executing write memory {device.name}')
    device.api.execute_write_memory()

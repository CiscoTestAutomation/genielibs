'''
cheetah AP specific clean stages
'''

# Python
import logging
import re
import time
import traceback

# Genie
from genie.metaparser.util.schemaengine import Optional, Or
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.stages.stages import (
    ConfigureManagement as GenericConfigureManagement,
)
from genie.metaparser.util.exceptions import InvalidCommandError

#pyATS
from pyats.utils.fileutils import FileUtils


# Unicon
from unicon.eal.dialogs import Dialog, Statement
from unicon.core.errors import SubCommandFailure, ConnectionError, StateMachineError, TimeoutError

from genie.libs.clean.wireless_registration import (
    WirelessAPRegistration,
    normalize_radio_mac,
)

# Logger
log = logging.getLogger(__name__)


class ConfigureManagement(GenericConfigureManagement):
    """Verify DHCP management connectivity on a Cheetah AP."""

    exec_order = [
        "check_management_interface_status",
        "ping_gateway",
    ]

    def check_management_interface_status(self, steps, device, **kwargs):
        """Verify the active management interface has a DHCP address."""
        with steps.start("Check management interface status") as step:
            try:
                output = device.parse("show ip interface brief")
            except Exception as e:
                step.failed(
                    "Failed to parse management interface status",
                    from_exception=e,
                )

            for interface, interface_details in output.get(
                "interfaces", {}
            ).items():
                if interface_details.get("active"):
                    break
            else:
                step.failed("No active management interface found")

            if (
                interface_details.get("status") != "up"
                or interface_details.get("protocol") != "up"
            ):
                step.failed(f"Management interface {interface} is down")

            ip_address = interface_details.get("ip_address")
            if ip_address in (None, "n/a", "unassigned"):
                step.failed(
                    f"Management interface {interface} has no IPv4 address"
                )

            if interface_details.get("method", "").lower() != "dhcp":
                step.failed(
                    f"Management interface {interface} is not using DHCP"
                )

            step.passed(
                f"Management interface {interface} is up with IPv4 "
                f"address {ip_address}"
            )

    def ping_gateway(
        self,
        steps,
        device,
        ping_attempts=GenericConfigureManagement.PING_ATTEMPTS,
        ping_sleep=GenericConfigureManagement.PING_SLEEP,
        **kwargs,
    ):
        """Discover the DHCP gateway and verify it is reachable."""
        with steps.start("Get gateway from DHCP lease") as step:
            try:
                output = device.parse("show ip dhcp lease")
            except Exception as e:
                step.failed("Failed to parse DHCP lease", from_exception=e)

            interfaces = output.get("interfaces", {})
            gateway = None
            source_interface = None
            for interface_name, interface_details in interfaces.items():
                for lease in interface_details.get("leases", []):
                    if lease.get("active") and lease.get("state") == "bound":
                        gateway = lease.get("gw")
                        source_interface = interface_name
                        break
                if gateway:
                    break

            if not gateway or gateway == "0.0.0.0":
                step.failed("No active DHCP gateway found")

        with steps.start(f"Ping gateway {gateway}") as step:
            last_exception = None
            for attempt in range(1, ping_attempts + 1):
                try:
                    device.ping(
                        addr=gateway,
                        source=source_interface,
                        timeout=120,
                        count=5,
                    )
                    step.passed("Ping to gateway successful")
                except Exception as e:
                    last_exception = e
                    if attempt < ping_attempts:
                        log.warning(
                            "Ping to gateway '%s' failed (attempt #%s of %s): %s\n"
                            "Retrying in %s seconds.",
                            gateway,
                            attempt,
                            ping_attempts,
                            e,
                            ping_sleep,
                        )
                        time.sleep(ping_sleep)

            step.failed(
                f"Ping to gateway {gateway} failed after {ping_attempts} attempts",
                from_exception=last_exception,
            )


class PrimeAp(BaseStage):
    """This stage primes accesspoint to desired controller

    Stage Schema
    ------------
    prime_ap:

        controller_name (str, optional): Name of the controller where AP needs
                                         to join. If omitted, the stage uses
                                         ``device.custom.controller_name`` or,
                                         for a single C9800 controller,
                                         the controller device name.

        controller_ip_address (str, optional): IPv4/IPv6 address of the
                                               controller where AP needs to
                                               join. If omitted, the stage
                                               uses the controller's wireless
                                               management IPv4 address, then
                                               its top-level management IPv4
                                               address. AP custom
                                               ``controller_ip_address`` is
                                               not used.

        max_time (int, optional): Maximum duration for AP priming and
                                  coordinated registration. Defaults to 900

        readiness_timeout (int, optional): Maximum time to wait for the WLC
                                           worker to complete its earlier
                                           clean stages and signal readiness.
                                           Defaults to 3600

        check_interval (int, optional): KIPC readiness polling interval in
                                        seconds. Defaults to 30

        sleep_time (int, optional): Deprecated compatibility option. Accepted
                                    but ignored.

    Example
    -------
    prime_ap:
        controller_name: "ewlc-5"
        controller_ip_address: "9.4.62.41"
"""
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 900
    WLC_READINESS_TIMEOUT = 3600
    CHECK_INTERVAL = 30
    CONSOLE_TAIL_LENGTH = 8192

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('controller_name'): str,
        Optional('controller_ip_address'): str,
        Optional('coordination_group'): str,
        Optional('ap_id'): str,
        Optional('ap_name'): str,
        Optional('radio_mac'): str,
        Optional('readiness_timeout'): int,
        Optional('dialog_poll_interval'): int,
        Optional('console_fail_fast_patterns'): list,
        Optional('max_time'): int,
        Optional('check_interval'): int,
        Optional('sleep_time'): int,

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'prime_ap_to_controller',
        'verify_primed_ap',
    ]

    @staticmethod
    def _get_controller_details(device, controller_name, controller_ip_address):
        """Resolve the controller details used by the AP priming stage.

        Both controller fields are optional. The clean-stage controller name
        takes precedence over AP custom data, followed by the name of a single
        C9800 controller. The clean-stage controller IP takes precedence over
        the controller wireless-management IPv4 address, which falls back to
        the controller top-level management IPv4 address. AP custom
        ``controller_ip_address`` is not used.
        """
        # Clean-stage values have the highest precedence, followed by the AP
        # custom controller name.
        custom = getattr(device, 'custom', {}) or {}
        controller_name = controller_name or custom.get('controller_name')

        testbed = getattr(device, 'testbed', None)
        testbed_devices = getattr(testbed, 'devices', {}) if testbed else {}
        controllers = [
            testbed_device for testbed_device in testbed_devices.values()
            if str(getattr(testbed_device, 'model', '')).lower() == 'c9800'
        ]

        # Auto-discovery is limited to a single C9800 controller for the current AP.
        controller = testbed_devices.get(controller_name) if controller_name else None
        if (controller is None and len(controllers) == 1 and
                str(getattr(device, 'platform', '')).lower() == 'ap'):
            controller = controllers[0]
            controller_name = controller_name or controller.name
        if controller is not None:
            management = getattr(controller, 'management', {}) or {}
            wireless_management = management.get('wireless', {}) or {}
            address = (wireless_management.get('address', {}) or {}).get('ipv4')
            if not address:
                address = (management.get('address', {}) or {}).get('ipv4')
            if isinstance(address, (list, tuple)):
                address = address[0] if address else None
            if address and hasattr(address, 'ip'):
                address = address.ip
            controller_ip_address = controller_ip_address or (
                str(address).split('/')[0] if address else None)

        missing = [
            name for name, value in (
                ('controller_name', controller_name),
                ('controller_ip_address', controller_ip_address),
            ) if not value
        ]
        if missing:
            raise ValueError(
                'PrimeAp requires {} in the clean stage, AP custom, or '
                'testbed'.format(', '.join(missing)))

        return controller_name, controller_ip_address

    @staticmethod
    def _get_controller_device(device, controller_name):
        """Resolve the controller device used for AP state verification."""
        testbed = getattr(device, 'testbed', None)
        testbed_devices = getattr(testbed, 'devices', {}) if testbed else {}
        controller = testbed_devices.get(controller_name)
        if controller:
            return controller

        for testbed_device in testbed_devices.values():
            if getattr(testbed_device, 'alias', None) == controller_name:
                return testbed_device

        controllers = [testbed_device for testbed_device in testbed_devices.values()
                       if str(getattr(testbed_device, 'model', '')).lower() == 'c9800']
        if len(controllers) == 1:
            return controllers[0]

        raise ValueError(
            'Unable to identify controller device for {}'.format(controller_name))

    @staticmethod
    def _get_reload_dialog():
        """Create a dialog that stops when the AP starts reloading."""
        return Dialog([
            Statement(
                pattern=(
                    r'(?:reboot:\s+Restarting\s+system|'
                    r'\[(?:\x1b\[[0-9;]*m)?\s*OK\s*'
                    r'(?:\x1b\[[0-9;]*m)?\])'),
                loop_continue=False,
                continue_timer=False,
            ),
        ])

    @staticmethod
    def _get_login_dialog(device, controller_name):
        """Create a dialog for an AP reboot login, using default credentials."""
        username, password = device.api.get_username_password(creds='default')
        statements = [
            Statement(
                pattern=(
                    r'.*AP has joined controller\s+{}\s*$'.format(
                        re.escape(controller_name))),
                action='sendline()',
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'.*Username:\s*$',
                action=lambda spawn: spawn.sendline(username),
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'.*Password:\s*$',
                action=lambda spawn: spawn.sendline(password),
                loop_continue=False,
                continue_timer=False,
            ),
        ]
        return Dialog(statements)

    @staticmethod
    def _get_registration(
            device, coordination_context=None, ap_id=None, ap_name=None,
            radio_mac=None):
        """Create the AP registration adapter for injected KIPC state.

        Args:
            device (obj): AP device being cleaned.
            coordination_context (object, optional): Explicit KIPC context
                for this coordinated Clean worker.
            ap_id (str, optional): Logical AP participant identifier.
            ap_name (str, optional): AP name used in registration evidence.
            radio_mac (str, optional): Known AP radio MAC, when supplied.

        Returns:
            tuple or None: Registration adapter and resolved AP identity, or
                ``None`` when the device is not running coordinated Clean.
        """
        context = coordination_context
        if context is None:
            return None

        custom = getattr(device, 'custom', {}) or {}
        ap_id = ap_id or custom.get('ap_id') or getattr(
            device, 'alias', None) or device.name
        ap_name = ap_name or custom.get('ap_name') or device.name
        registration = WirelessAPRegistration(
            context,
            {ap_id: {'ap_id': ap_id, 'ap_name': ap_name,
                     'radio_mac': radio_mac}},
        )
        return registration, ap_id, ap_name, radio_mac

    @staticmethod
    def _get_registration_dialog(
            device, registration, ap_id, controller_name, patterns):
        """Create the AP console dialog used during coordinated registration.

        Args:
            device (obj): AP device being monitored.
            registration (WirelessAPRegistration): Group registration state.
            ap_id (str): AP participant identifier.
            controller_name (str): Expected controller name.
            patterns (list): Console patterns that fail registration fast.

        Returns:
            tuple: Dialog and the confirmation/failure exception classes.
        """
        username, password = device.api.get_username_password(creds='default')

        class RegistrationConfirmed(Exception):
            pass

        class RegistrationFailed(Exception):
            pass

        def check_registration(spawn):
            if registration.is_registration_confirmed(ap_id):
                raise RegistrationConfirmed()
            if registration.is_registration_failed(ap_id):
                raise RegistrationFailed(registration.snapshot_ap(ap_id))

        def fail_fast(spawn, failure_pattern):
            raise RegistrationFailed(
                'AP console failure: {}'.format(failure_pattern))

        statements = [
            Statement(
                pattern=(r'.*AP has joined controller\s+{}\s*$'.format(
                    re.escape(controller_name))),
                action='sendline()',
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'.*Username:\s*$',
                action=lambda spawn: spawn.sendline(username),
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'.*Password:\s*$',
                action=lambda spawn: spawn.sendline(password),
                loop_continue=True,
                continue_timer=False,
            ),
        ]
        for pattern in patterns or []:
            statements.append(Statement(
                pattern=pattern,
                action=lambda spawn, failure_pattern=pattern: fail_fast(
                    spawn, failure_pattern),
                loop_continue=False,
                continue_timer=False,
            ))
        statements.append(Statement(
            pattern=r'(?s).+',
            action=check_registration,
            loop_continue=True,
            continue_timer=False,
        ))
        return Dialog(statements), RegistrationConfirmed, RegistrationFailed

    @classmethod
    def _get_console_failure_evidence(cls, device, error):
        """Return bounded AP-console evidence without exposing credentials."""
        console_tail = ''
        spawn = getattr(device, 'spawn', None)
        if spawn is not None:
            try:
                spawn.read_update_buffer()
            except Exception:
                pass
            try:
                console_tail = getattr(spawn, 'buffer', '')
            except Exception:
                console_tail = ''
        console_tail = re.sub(
            r'(?im)(password|secret|token)\s*[:=]\s*\S+',
            r'\1: <redacted>',
            str(console_tail or ''),
        )[-cls.CONSOLE_TAIL_LENGTH:]
        return {
            'error': type(error).__name__,
            'console_tail': console_tail,
        }

    @staticmethod
    def _detect_and_enable_after_login(device):
        """Detect the AP console state and enter enable mode when needed."""
        device.state_machine.detect_state(device.spawn, device.context)
        state = device.state_machine.current_state
        log.info(
            "AP %s Unicon state after login: %s",
            device.name,
            state,
        )
        if state == 'disable':
            log.info(
                "AP %s is in disable state; moving to enable state",
                device.name,
            )
            device.enable()
            log.info(
                "AP %s Unicon state after enable: %s",
                device.name,
                device.state_machine.current_state,
            )

    @staticmethod
    def _get_radio_mac(device):
        """Read the AP radio MAC from structured parser output.

        Args:
            device (obj): Connected AP device.

        Returns:
            str: Normalized AP radio MAC in dotted lowercase form.

        Raises:
            ValueError: If the AP output does not contain a radio MAC.
        """
        log.info(
            "AP %s resolving radio MAC with show interfaces dot11radio 0",
            device.name,
        )
        try:
            parsed = device.parse('show interfaces dot11radio 0')
            radio_mac = parsed['interface']['Dot11Radio0'][
                'radio_mac_address']
        except (KeyError, TypeError) as error:
            raise ValueError(
                'Unable to learn AP radio MAC from parsed '
                'show interfaces dot11radio 0 output') from error
        normalized = normalize_radio_mac(radio_mac)
        log.info("AP %s radio MAC resolved from parser", device.name)
        return normalized

    def _monitor_registration(
            self, device, registration, ap_id, controller_name, deadline,
            dialog_poll_interval, console_fail_fast_patterns):
        """Monitor AP console and KIPC until registration reaches a terminal state.

        Args:
            device (obj): AP device being monitored.
            registration (WirelessAPRegistration): Group registration state.
            ap_id (str): AP participant identifier.
            controller_name (str): Expected controller name.
            deadline (int or float): Absolute monotonic AP registration
                                     deadline.
            dialog_poll_interval (int or float): Console poll interval.
            console_fail_fast_patterns (list): Console failure patterns.

        Raises:
            RuntimeError: If KIPC reports failure/cancellation or registration
                reaches the deadline.
        """
        dialog, registration_confirmed, registration_failed = \
            self._get_registration_dialog(
                device, registration, ap_id, controller_name,
                console_fail_fast_patterns)
        while True:
            result = registration.wait_for_registration(ap_id, 0)
            if result.get('status') == 'confirmed':
                return
            if result.get('status') == 'failed':
                log.error(
                    "AP %s registration failed according to KIPC: %s",
                    device.name,
                    result,
                )
                raise RuntimeError(str(result))
            if result.get('status') == 'cancelled':
                log.error(
                    "AP %s registration was cancelled by KIPC",
                    device.name,
                )
                raise RuntimeError('KIPC coordination was cancelled')

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                log.error(
                    "AP %s registration deadline reached",
                    device.name,
                )
                registration.signal_registration_failed(
                    ap_id, 'registration timeout')
                raise RuntimeError('AP registration timed out')

            try:
                dialog.process(
                    device.spawn,
                    timeout=min(remaining, dialog_poll_interval),
                )
            except TimeoutError:
                log.warning(
                    "AP %s registration dialog poll timed out; continuing "
                    "until WLC confirmation or stage deadline",
                    device.name,
                )
                continue
            except registration_confirmed:
                log.info(
                    "AP %s registration confirmed while processing console "
                    "output", device.name)
                return
            except registration_failed as error:
                log.error(
                    "AP %s registration failed while processing console "
                    "output: %s", device.name, error)
                registration.signal_registration_failed(
                    ap_id, str(error))
                raise

    def prime_ap_to_controller(self, device, steps, controller_name=None, controller_ip_address=None,
                               coordination_group=None, ap_id=None,
                               ap_name=None, radio_mac=None,
                               coordination_context=None,
                               readiness_timeout=WLC_READINESS_TIMEOUT,
                               dialog_poll_interval=1,
                               console_fail_fast_patterns=None,
                               max_time=MAX_TIME,
                               check_interval=CHECK_INTERVAL,
                               sleep_time=None):
        """Prime an AP and coordinate completion through the WLC worker.

        Args:
            device (obj): AP device being cleaned.
            steps (obj): Clean step manager.
            controller_name (str, optional): Target WLC logical name.
            controller_ip_address (str, optional): Target WLC address.
            coordination_group (str, optional): Expected KIPC group name.
            ap_id (str, optional): AP participant alias.
            ap_name (str, optional): AP name used for WLC evidence.
            radio_mac (str, optional): AP radio MAC, learned when omitted.
            coordination_context (object, optional): Explicit KIPC context
                for this coordinated Clean worker.
            readiness_timeout (int): Maximum WLC readiness wait.
            dialog_poll_interval (int): AP console polling interval.
            console_fail_fast_patterns (list, optional): Failure patterns.
            max_time (int): Maximum duration for AP priming and registration.
            check_interval (int): KIPC readiness polling interval.
            sleep_time (int): Deprecated compatibility option. Accepted but
                              ignored.

        Returns:
            None: Clean stage failures are reported through ``steps``.
        """
        registration = self._get_registration(
            device, coordination_context=coordination_context, ap_id=ap_id,
            ap_name=ap_name, radio_mac=radio_mac)
        if coordination_group and registration is None:
            raise RuntimeError(
                'Coordinated prime_ap requires an injected KIPC context')
        # An injected context selects the coordinated path; without it,
        # prime_ap keeps the existing standalone behavior.
        if registration is not None:
            registration, ap_id, ap_name, radio_mac = registration
            with steps.start(
                    "Wait for WLC readiness before priming AP-{}".format(
                        device.name)) as step:
                if (coordination_group and
                        coordination_group != registration.kipc.group_id):
                    registration.signal_registration_failed(
                        ap_id,
                        "AP coordination group does not match the injected "
                        "KIPC context")
                    step.failed(
                        "AP coordination group does not match the injected "
                        "KIPC context")
                    return
                readiness_deadline = time.monotonic() + readiness_timeout
                log.info(
                    "AP %s waiting for WLC readiness in coordination group "
                    "%s (timeout %s seconds)",
                    device.name, registration.kipc.group_id,
                    readiness_timeout)
                while True:
                    remaining = readiness_deadline - time.monotonic()
                    if remaining <= 0:
                        ready = {'status': 'timeout'}
                        break
                    ready = registration.wait_for_wlc_ready(
                        min(check_interval, remaining))
                    if ready.get('status') != 'timeout':
                        break
                    log.info(
                        "AP %s is still waiting for WLC readiness; "
                        "%s seconds remain",
                        device.name,
                        max(0, int(readiness_deadline - time.monotonic())))
                log.info(
                    "AP %s received WLC readiness result: %s",
                    device.name, ready.get('status'))
                if ready.get('status') != 'ready':
                    step.failed(
                        "WLC was not ready for AP registration: {}".format(
                            ready))
                    return

            controller_name, controller_ip_address = self._get_controller_details(
                device, controller_name, controller_ip_address)
            stage_deadline = time.monotonic() + max_time
            with steps.start(
                    "Prime AP-{} to Controller-{}".format(
                        device.name, controller_name)) as step:
                remaining = stage_deadline - time.monotonic()
                if remaining <= 0:
                    registration.signal_registration_failed(
                        ap_id, 'AP stage deadline expired before priming')
                    step.failed('AP stage deadline expired before priming')
                    return
                try:
                    radio_mac = self._get_radio_mac(device)
                    state_machine = getattr(device, 'state_machine', None)
                    log.info(
                        "AP %s starting CAPWAP configuration through the AP "
                        "worker; Unicon state=%s",
                        device.name,
                        getattr(state_machine, 'current_state', None),
                    )
                    log.info(
                        "AP %s is ready for CAPWAP configuration; WLC "
                        "communication remains through KIPC",
                        device.name)
                    prime_result = device.api.execute_prime_ap(
                            controller_ip_address=controller_ip_address,
                            controller_name=controller_name)
                    log.info(
                        "AP %s CAPWAP configuration returned %s",
                        device.name,
                        prime_result,
                    )
                    if not prime_result:
                        log.error("AP %s CAPWAP priming returned failure", device.name)
                        raise RuntimeError('Failed to prime the AP')
                    log.info(
                        "AP %s publishing configured state through KIPC",
                        device.name,
                    )
                    registration.signal_ap_configured(
                        ap_id, ap_name, radio_mac)
                    log.info(
                        "AP %s signaled configured; waiting for WLC "
                        "registration confirmation",
                        device.name)
                    self._monitor_registration(
                        device, registration, ap_id, controller_name,
                        stage_deadline, dialog_poll_interval,
                        console_fail_fast_patterns)
                    # _monitor_registration returns only after KIPC observes
                    # terminal WLC confirmation; otherwise it raises.
                    log.info(
                        "AP %s registration confirmed by WLC through KIPC",
                        device.name)
                    self._detect_and_enable_after_login(device)
                except Exception as error:
                    log.exception(
                        "AP %s PrimeAp failed before registration confirmation",
                        device.name,
                    )
                    if not registration.is_registration_confirmed(ap_id):
                        registration.signal_registration_diagnostics(
                            ap_id,
                            self._get_console_failure_evidence(device, error),
                        )
                        registration.signal_registration_failed(
                            ap_id,
                            'AP registration stage failed ({})'.format(
                                type(error).__name__))
                    step.failed('Failed to register AP', from_exception=error)
            return

        controller_name, controller_ip_address = self._get_controller_details(
            device, controller_name, controller_ip_address)
        with steps.start("Priming the AP-{} to Controller-{}".format(device.name, controller_name)) as step:
            # Preserve standalone callers that omit the template connect
            # stage by connecting immediately before the first AP command.
            device.connect()
            if not device.api.execute_prime_ap(
                    controller_ip_address=controller_ip_address,
                    controller_name=controller_name):
                step.failed("Failed to prime the AP")
            try:
                log.info(
                    "Waiting up to %s seconds for AP %s to start reloading",
                    max_time,
                    device.name,
                )
                self._get_reload_dialog().process(
                    device.spawn, timeout=max_time)
                reload_started = True
            except TimeoutError:
                log.info("AP %s did not start a reload", device.name)
                reload_started = False

            try:
                if reload_started:
                    login_dialog = self._get_login_dialog(device, controller_name)
                    log.info(
                        "Waiting up to %s seconds for the AP login prompt",
                        max_time,
                    )
                    login_dialog.process(
                        device.spawn, timeout=max_time)
                    self._detect_and_enable_after_login(device)

            except (SubCommandFailure, TimeoutError, ConnectionError,
                    StateMachineError, InvalidCommandError) as e:
                step.failed("Failed to complete AP priming", from_exception=e)

    def verify_primed_ap(self, device, steps, controller_name=None, controller_ip_address=None,
                         coordination_group=None, ap_id=None, ap_name=None,
                         radio_mac=None, coordination_context=None,
                         max_time=MAX_TIME,
                         check_interval=CHECK_INTERVAL):
        """Verify AP operation, controller identity, and registration state.

        Args:
            device (obj): AP device being cleaned.
            steps (obj): Clean step manager.
            controller_name (str, optional): Expected controller name.
            controller_ip_address (str, optional): Expected controller address.
            coordination_group (str, optional): Expected KIPC group name.
            ap_id (str, optional): AP participant alias.
            ap_name (str, optional): AP name used for standalone verification.
            radio_mac (str, optional): AP radio MAC identity.
            coordination_context (object, optional): Explicit KIPC context
                for this coordinated Clean worker.
            max_time (int): Standalone verification polling window.
            check_interval (int): Standalone verification polling interval.

        Returns:
            None: Verification failures are reported through ``steps``.
        """
        controller_name, controller_ip_address = self._get_controller_details(
            device, controller_name, controller_ip_address)

        with steps.start(
                "Validate if the AP has joined the intended controller") as step:
            try:
                registration = self._get_registration(
                    device, coordination_context=coordination_context,
                    ap_id=ap_id, ap_name=ap_name, radio_mac=radio_mac)
                controller = self._get_controller_device(device, controller_name)
                if registration is None:
                    if coordination_group:
                        step.failed(
                            'Coordinated prime_ap requires an injected '
                            'KIPC context')
                        return
                    controller.connect()
                    ap_state = controller.api.get_ap_state(ap_name=device.name)
                    if (ap_state or '').lower() != 'registered':
                        step.failed(
                            "AP {} has not joined right controller".format(
                                device.name))
                    standalone_verified = self._verify_standalone(
                        device,
                        getattr(controller, 'name', controller_name),
                        controller_ip_address,
                        max_time,
                        check_interval,
                    )
                else:
                    registration, ap_id, _, _ = registration
                    if not registration.is_registration_confirmed(ap_id):
                        step.failed(
                            "AP {} has not received WLC registration "
                            "confirmation".format(device.name))
                    # Coordinated KIPC confirmation already gates this final
                    # one-shot verification; retry ownership stays with the
                    # complete WLC/AP group.
                    standalone_verified = (
                        device.api.verify_operation_state(
                            operation_state="UP") and
                        device.api.verify_controller_name(
                            controller_name=getattr(
                                controller, 'name', controller_name)) and
                        device.api.verify_controller_ip(
                            controller_ip_address=controller_ip_address))

                if not standalone_verified:
                    log.error(
                        "AP %s failed operation/controller verification",
                        device.name,
                    )
                    step.failed("AP {} has not joined right controller".format(device.name))
            except (SubCommandFailure, TimeoutError, ConnectionError,
                    StateMachineError, InvalidCommandError) as e:
                log.error(
                    "AP %s verification failed: %s",
                    device.name,
                    e,
                )
                step.failed("Failed due to exception",from_exception=e)

    @staticmethod
    def _verify_standalone(
            device, controller_name, controller_ip_address, max_time,
            check_interval):
        """Poll standalone AP verification until all checks pass or timeout.

        Args:
            device (obj): AP device being verified.
            controller_name (str): Expected controller name.
            controller_ip_address (str): Expected controller address.
            max_time (int): Maximum polling duration in seconds.
            check_interval (int): Polling interval in seconds.

        Returns:
            bool: True when all standalone checks pass before the deadline.
        """
        timeout = Timeout(max_time, check_interval)
        while timeout.iterate():
            operation_state_verified = device.api.verify_operation_state(
                operation_state="UP")
            controller_name_verified = device.api.verify_controller_name(
                controller_name=controller_name)
            controller_ip_verified = device.api.verify_controller_ip(
                controller_ip_address=controller_ip_address)
            if (operation_state_verified and controller_name_verified and
                    controller_ip_verified):
                return True
            log.info(
                "AP %s standalone verification is still pending: "
                "operation=%s controller_name=%s controller_ip=%s",
                device.name,
                operation_state_verified,
                controller_name_verified,
                controller_ip_verified,
            )
            timeout.sleep()

        log.error(
            "AP %s standalone verification timed out after %s seconds",
            device.name,
            max_time,
        )
        return False


class EraseApConfiguration(BaseStage):
    """This stage erases the AP configuration

       Stage Schema
       ------------
       erase_ap_configuration:
           login_credentials_alias (str): Alias of login credentials to use after write erase which will be mentioned in TB yaml

           max_time (int, optional): Maximum time for which this clean stage will try to associate Ap to controller.
               Defaults to 900

           check_interval (int, optional): Interval for retry mechanism in seconds. Defaults to 30


       Example
       -------
       erase_ap_configuration:
            login_credentials_alias: "erase"
            max_time: "600"
   """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 900
    CHECK_INTERVAL = 30

    # ============
    # Stage Schema
    # ============
    schema = {
        "login_credentials_alias": str,
        Optional('max_time'): int,
        Optional('check_interval'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'erase_configs',
    ]

    def erase_configs(self, device, steps, login_credentials_alias, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):
        with steps.start("Erasing the AP-{}".format(device.name)) as step:
            if not device.api.execute_erase_ap():
                step.failed("Failed to erase the AP")
            time.sleep(300)
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                try:
                    if not device.is_connected():
                        device.destroy()
                        device.connect(login_creds=login_credentials_alias)
                    device.execute("show version")
                    break
                except (SubCommandFailure, StateMachineError, ConnectionError, InvalidCommandError):
                    device.disconnect()
                    timeout.sleep()
            else:
                step.failed("Failed to login to device after erasing the AP configs")


class LoadApImage(BaseStage):
    """This stage loads new AP image

           Stage Schema
           ------------
           load_ap_image:
               ap_image_path (str): Absolute path where ap image is located

               server(str): Server alias which has AP image

               protocol(str): protocol through which AP image will be loaded

               retries(int, optional): Number of times image download needs to be tried

               max_time (int, optional): Maximum time for which this clean stage will try to clean ap.
                   Defaults to 1200




           Example
           -------
           load_ap_image:
                ap_image_path: "/auto/wnbu-groups-builds/FAST_BUNDLING/polaris_dev/6640/ap3g3-k9w8-tar.master-cisco.202309180209"
                server: "tftp"
                max_time: "1200"
       """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 1200
    PROTOCOL = "http"
    RETRIES = 1
    RETRY_SLEEP_TIME = 30

    # ============
    # Stage Schema
    # ============
    schema = {
        "server": str,
        Optional("ap_image_path"): str,
        Optional("protocol"): str,
        Optional('retries'): int,
        Optional('max_time'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'load_image'
    ]

    def load_image(self, device, steps, ap_image_path, server, protocol=PROTOCOL, max_time=MAX_TIME, retries=RETRIES, retry_sleep_time=RETRY_SLEEP_TIME):
        try:
            if not hasattr(device.testbed, 'servers'):
                self.failed("Cannot find any servers in the testbed")
            fu = FileUtils(testbed=device.testbed)
            server_ip = fu.get_server_block(server).get('address')
            username, password = fu.get_auth(server)
            with steps.start("Load image in to device-{} and verify if its loaded correctly".format(device.name)) as step:
                if not ap_image_path.startswith("/"):
                    ap_image_path = "/" + ap_image_path
                full_image_path = "{}://{}{}".format(protocol, server_ip, ap_image_path)
                if not device.api.execute_archive_download(full_image_path, max_time, username, password, reload=True, retries=retries, 
                                                           retry_sleep_time=retry_sleep_time):
                    step.failed("Failed to load AP image")
        except Exception as e:
            log.exception(e)
            self.failed("Failed to load image on AP")


import copy
import unittest
import logging
from unittest import mock
from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.stages import Reload

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from pyats.topology import loader
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE
import unicon
unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2

logger = logging.getLogger(__name__)

class TestIosXEPluginHAConnect(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE ASR HA device """

    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXE(port=0, state='cat9k_rommon', hostname='R1')
        cls.md.start()

        cls.testbed = """
        devices:
          R1:
            os: iosxe
            type: cat9k
            credentials:
                default:
                    username: cisco
                    password: cisco
                enable:
                    password: Secret12345
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}

        """.format(cls.md.ports[0])

    @classmethod
    def tearDownClass(self):
        self.md.stop()

    def test_disconnect_and_reconnect_fail(self):
        tb = loader.load(self.testbed)
        self.reload = Reload()
        device = tb.devices.R1
        device.connect(mit=True)
        steps = Steps()
        with self.assertRaises(TerminateStepSignal):
          self.reload.disconnect_and_reconnect(
                  steps=steps, device=device
              )
        self.assertEqual(Failed, steps.details[0].result)


class TestIosXEReloadManualBoot(unittest.TestCase):
    """Unit tests for the manual-boot fallback of the Reload stage.

    When the boot variable is missing the device drops to the bootloader and
    the stage performs a manual boot. On GRUB based platforms (e.g. cat9kv)
    the bootloader does not accept a ``boot <image>`` command, so a user
    supplied ``grub_boot_image`` must be honored to select the desired GRUB
    menu entry. This test verifies that fallback honors ``grub_boot_image``.
    """

    def setUp(self):
        # RELOAD_SERVICE_ARGS is a mutable class attribute that the stage
        # updates in place. Snapshot and restore it so tests stay isolated.
        self._orig_service_args = copy.deepcopy(Reload.RELOAD_SERVICE_ARGS)

    def tearDown(self):
        Reload.RELOAD_SERVICE_ARGS = self._orig_service_args

    def _build_device(self):
        """Build a mocked device whose first reload triggers the fallback."""
        device = mock.MagicMock()
        device.name = 'R1'
        device.is_ha = False

        def parse_side_effect(command, *args, **kwargs):
            if command == 'show version':
                return {'version': {'system_image': 'boot:packages.conf'}}
            # 'show boot' -> no configuration_register, keep test simple
            return {}

        device.parse.side_effect = parse_side_effect

        # The first device.reload() simulates the boot variable being absent.
        # It invokes the break_reload action attached to the reply dialog,
        # which raises the stage's internal ReloadError and sends execution
        # into the manual-boot fallback. Subsequent calls are the manual boot.
        state = {'count': 0}

        def reload_side_effect(*args, **kwargs):
            state['count'] += 1
            if state['count'] == 1:
                reply = kwargs.get('reply')
                for statement in reply:
                    action = getattr(statement, 'action', None)
                    if getattr(action, '__name__', '') == 'break_reload':
                        action(**statement.args)
            return ''

        device.reload.side_effect = reload_side_effect
        return device

    def test_manual_boot_honors_grub_boot_image(self):
        device = self._build_device()
        reload_stage = Reload()
        steps = Steps()
        reload_service_args = {
            'timeout': 1800,
            'reload_creds': 'default',
            'prompt_recovery': False,
            'error_pattern': [],
            'grub_boot_image': 'GOLDEN IMAGE',
        }

        reload_stage.reload(
            steps=steps,
            device=device,
            reload_service_args=reload_service_args,
        )

        # The manual boot (last reload call) must select the GRUB menu entry
        # and must NOT send an invalid 'boot <image>' reload_command.
        manual_boot_call = device.reload.call_args_list[-1]
        self.assertEqual(
            manual_boot_call.kwargs.get('grub_boot_image'), 'GOLDEN IMAGE')
        self.assertNotIn('reload_command', manual_boot_call.kwargs)
        self.assertEqual([], manual_boot_call.kwargs['error_pattern'])
        self.assertEqual(1800, manual_boot_call.kwargs['timeout'])
        self.assertEqual('default', manual_boot_call.kwargs['reload_creds'])
        self.assertFalse(manual_boot_call.kwargs['prompt_recovery'])
        self.assertFalse(manual_boot_call.kwargs['device_recovery'])


class TestIosXEReload(unittest.TestCase):
    """Unit tests for IOSXE clean reload handling."""

    def setUp(self):
        self._orig_service_args = copy.deepcopy(Reload.RELOAD_SERVICE_ARGS)
        self.cls = Reload()
        self.device = Mock()
        self.device.name = 'R1'
        self.device.is_ha = False
        self.device.sendline = Mock()
        self.device.rommon = Mock()
        self.device.api.execute_set_config_register = Mock()

    def tearDown(self):
        Reload.RELOAD_SERVICE_ARGS = self._orig_service_args

    def test_reload_preserves_reload_service_args(self):
        def reload_side_effect(**kwargs):
            if self.device.reload.call_count == 1:
                for statement in kwargs['reply']:
                    if ('Boot variable either does not exist'
                            in statement.pattern):
                        statement.action(**statement.args)
            return ''

        steps = Steps()
        reload_service_args = {
            'timeout': 1800,
            'reload_creds': 'default',
            'prompt_recovery': False,
            'error_pattern': [],
        }
        self.device.reload = Mock(side_effect=reload_side_effect)
        self.device.parse = Mock(side_effect=[
            {'version': {'system_image': 'bootflash:packages.conf'}},
            {'active': {'configuration_register': '0x2102'}},
        ])

        self.cls.reload(
            steps=steps,
            device=self.device,
            reload_service_args=reload_service_args,
        )

        self.assertEqual(2, self.device.reload.call_count)
        reload_call = self.device.reload.call_args_list[1].kwargs
        self.assertEqual('boot bootflash:packages.conf',
                         reload_call['reload_command'])
        self.assertEqual([], reload_call['error_pattern'])
        self.assertEqual(1800, reload_call['timeout'])
        self.assertEqual('default', reload_call['reload_creds'])
        self.assertFalse(reload_call['prompt_recovery'])
        self.assertFalse(reload_call['device_recovery'])


if __name__ == '__main__':
    unittest.main()

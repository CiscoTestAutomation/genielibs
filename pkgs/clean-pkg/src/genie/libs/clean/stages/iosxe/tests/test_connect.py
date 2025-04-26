import unittest
from unittest.mock import MagicMock, Mock, call, patch
import logging

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from pyats.topology import loader
from genie.libs.clean.stages.iosxe.stages import Connect
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE
import unicon

from unicon.core.errors import UniconBackendDecodeError
from unicon.plugins.tests.mock.mock_device_iosxe_cat9k import MockDeviceTcpWrapperIOSXECat9k
from textwrap import dedent

unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2

logger = logging.getLogger(__name__)

class TestIosXEConnect(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE ASR HA device """

    @classmethod
    def setUpClass(self):
        self.md = MockDeviceTcpWrapperIOSXE(hostname='R1', port=0, state='general_enable')
        self.md.start()
        testbed = """
        testbed:
          servers:
            http:
              dynamic: true
              protocol: http
            ftp:
              dynamic: true
              protocol: ftp
            tftp:
              dynamic: true
              protocol: tftp
        devices:
          R1:
            os: iosxe
            type: router
            tacacs:
                username: cisco
            passwords:
                tacacs: cisco
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
        """.format(self.md.ports[0])

        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(mit=True)

    @classmethod
    def tearDownClass(self):
        self.device.disconnect()
        self.md.stop()

    def test_connect(self):
        steps = Steps()
        self.connect = Connect()
        self.connect(steps=steps, device=self.device)
        self.assertEqual(Passed, steps.details[0].result)


    @patch('unicon.eal.backend.pty_backend.Spawn._read', Mock(return_value=b'\xcej'))
    def test_connect_speed_fail(self):
        self.device.settings.UNICON_BACKEND_DECODE_ERROR_LIMIT = 3
        steps = Steps()
        self.device.api.configure_management_console = MagicMock()
        try:
            self.device.disconnect()
            self.connect = Connect()
            self.connect(steps=steps, device=self.device)
            self.device.settings.UNICON_BACKEND_DECODE_ERROR_LIMIT = None
        except:
            ...
        self.device.api.configure_management_console.assert_called_once()


class TestIosXEConnect_1(unittest.TestCase):

    def test_connect(self):
        steps = Steps()

        md = MockDeviceTcpWrapperIOSXECat9k(port=0, state='general_exec', hostname='R1')
        md.start()

        testbed = dedent("""
        devices:
            R1:
                os: iosxe
                platform: cat9k
                credentials:
                    default:
                        password: cisco
                connections:
                    cli:
                        command: 'telnet 127.0.0.1 {}'
            """.format(md.ports[0]))
        tb = loader.load(testbed)
        device = tb.devices.R1

        cls = Connect()

        # To mock the device recovery processor
        mock_parent = Mock()
        mock_parent.device_recovery_processor = True
        # Create a mock section object with the mock parent
        mock_section = Mock()
        mock_section.parent = mock_parent
        cls.parameters = {'section': mock_section}

        try:
            cls.connect(steps=steps, device=device)
        except Exception:
            raise
        finally:
            device.disconnect()
            md.stop()

        # STEP 1: Connecting to the device is set to false,
        # if the recovery processor is enabled.
        self.assertFalse(steps.steps[0].result_rollup)

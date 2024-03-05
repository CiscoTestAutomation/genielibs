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



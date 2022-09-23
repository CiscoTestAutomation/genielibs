
import unittest
import logging

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

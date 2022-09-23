import unittest
import logging

from genie.libs.clean.stages.stages import Reload

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from pyats.topology import loader
from unicon.plugins.tests.mock.mock_device_iosxr import MockDeviceTcpWrapperIOSXR
import unicon
unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2

logger = logging.getLogger(__name__)

class TestIosXRreload(unittest.TestCase):
    """ Run unit testing on a mocked IOSXR device """
    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXR(port=0, state = 'ncs5k_enable', hostname='R1')
        cls.md.start()

        cls.testbed = """
        devices:
          R1:
            os: iosxr
            type: ncs5k
            credentials:
                default:
                    username: lab
                    password: lab
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

    def test_reload_pass(self):
        tb = loader.load(self.testbed)
        self.reload = Reload()
        device = tb.devices.R1
        steps = Steps()
        device.connect()
        self.reload(steps=steps, device=device)
        self.assertEqual(Passed, steps.details[0].result)

import unittest
from unittest.mock import MagicMock, Mock, call, patch
import logging

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.topology import loader
from genie.libs.clean.stages.stages import Connect

import unicon
from unicon.plugins.tests.mock.mock_device_nxos import MockDeviceTcpWrapperNXOS

unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2

logger = logging.getLogger(__name__)


class TestConnect(unittest.TestCase):
    """ Run unit testing on a mocked NXOS device """

    def test_connect(self):
        self.md = MockDeviceTcpWrapperNXOS(hostname='R1', port=0, state='exec')
        self.md.start()
        testbed = """
       devices:
          R1:
            os: nxos
            platform: n9k
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

        tb = loader.load(testbed)
        device = tb.devices.R1
        
        steps = Steps()
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
            self.md.stop()
        
        # STEP 1: Connecting to the device is set to false,
        # if the recovery processor is enabled.
        self.assertFalse(steps.steps[0].result_rollup)
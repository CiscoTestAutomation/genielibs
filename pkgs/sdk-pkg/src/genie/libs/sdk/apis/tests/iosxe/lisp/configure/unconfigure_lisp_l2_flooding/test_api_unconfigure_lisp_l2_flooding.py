import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.lisp.configure import unconfigure_lisp_l2_flooding


class TestUnconfigureLispL2Flooding(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          FE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_lisp_l2_flooding(self):
        result = unconfigure_lisp_l2_flooding(self.device, '2', '110', '239.0.0.1', 'arp-nd', 'unknown-unicast')
        expected_output = None
        self.assertEqual(result, expected_output)

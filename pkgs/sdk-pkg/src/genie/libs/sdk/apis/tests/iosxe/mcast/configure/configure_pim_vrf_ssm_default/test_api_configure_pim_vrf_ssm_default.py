import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mcast.configure import configure_pim_vrf_ssm_default


class TestConfigurePimVrfSsmDefault(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          peer2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['peer2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pim_vrf_ssm_default(self):
        result = configure_pim_vrf_ssm_default(self.device, 'red')
        expected_output = None
        self.assertEqual(result, expected_output)

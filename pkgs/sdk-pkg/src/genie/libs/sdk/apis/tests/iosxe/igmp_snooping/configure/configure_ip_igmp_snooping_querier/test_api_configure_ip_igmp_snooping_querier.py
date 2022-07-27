import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import configure_ip_igmp_snooping_querier


class TestConfigureIpIgmpSnoopingQuerier(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Cat9300_VTEP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9300_VTEP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_igmp_snooping_querier(self):
        result = configure_ip_igmp_snooping_querier(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

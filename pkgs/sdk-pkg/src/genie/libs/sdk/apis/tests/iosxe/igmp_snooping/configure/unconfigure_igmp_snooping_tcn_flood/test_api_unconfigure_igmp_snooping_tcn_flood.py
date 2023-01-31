import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import unconfigure_igmp_snooping_tcn_flood


class TestUnconfigureIgmpSnoopingTcnFlood(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9200L_STK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9200L_STK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_igmp_snooping_tcn_flood(self):
        result = unconfigure_igmp_snooping_tcn_flood(self.device, 'GigabitEthernet2/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)

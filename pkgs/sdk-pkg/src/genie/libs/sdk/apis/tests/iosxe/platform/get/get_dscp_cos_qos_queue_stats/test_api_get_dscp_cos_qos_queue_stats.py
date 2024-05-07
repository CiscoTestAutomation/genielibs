import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_dscp_cos_qos_queue_stats


class TestGetDscpCosQosQueueStats(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SG-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SG-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_dscp_cos_qos_queue_stats(self):
        result = get_dscp_cos_qos_queue_stats(self.device, 'FortyGigabitEthernet1/1/0/15', 'Egress COS7', 'Egress DSCP27', 'active', None, 'switch')
        expected_output = ('Frames        Bytes', 0, 23939)
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_traffic_packet_counters


class TestGetInterfaceTrafficPacketCounters(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3300-8U2X-tgen1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3300-8U2X-tgen1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_interface_traffic_packet_counters(self):
        result = get_interface_traffic_packet_counters(self.device, 'GigabitEthernet1/6', ['in_pkts',
 'out_pkts',
 'out_errors',
 'out_collision',
 'out_interface_resets',
 'out_babble',
 'out_late_collision',
 'out_deferred',
 'in_errors',
 'in_crc_errors'])
        expected_output = {'in_crc_errors': 0,
 'in_errors': 0,
 'in_pkts': 0,
 'out_babble': 0,
 'out_collision': 0,
 'out_deferred': 0,
 'out_errors': 0,
 'out_interface_resets': 1,
 'out_late_collision': 0,
 'out_pkts': 0}
        self.assertEqual(result, expected_output)

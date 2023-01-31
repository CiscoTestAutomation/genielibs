import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.get import get_kpi_value_in_show_kpi_report_id


class TestGetKpiValueInShowKpiReportId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
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
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_kpi_value_in_show_kpi_report_id(self):
        result = get_kpi_value_in_show_kpi_report_id(self.device, 1668458555, 'hardware_inventory')
        expected_output = [{'cname': 'Switch2', 'part_no': 'C9300-48U', 'serial_no': 'FCW2137L0E2'},
 {'cname': 'c93xx Stack', 'part_no': 'C9300-48U', 'serial_no': 'FCW2137L0E2'},
 {'cname': 'StackPort2/1',
  'part_no': 'STACK-T1-1M',
  'serial_no': 'MOC2117A9QX'},
 {'cname': 'StackPort2/2',
  'part_no': 'STACK-T1-1M',
  'serial_no': 'LCC2109G0LM'},
 {'cname': 'PowerSupply2/B',
  'part_no': 'PWR-C1-715WAC',
  'serial_no': 'DCA2210G3R5'},
 {'cname': 'FRUUplinkModule2/1',
  'part_no': 'C3850-NM-4-10G',
  'serial_no': 'FOC19312K2N'}]
        self.assertEqual(result, expected_output)

import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_platform_component_temp_info


class TestGetPlatformComponentTempInfo(unittest.TestCase):

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
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_platform_component_temp_info(self):
        result = get_platform_component_temp_info(self.device)
        expected_output = {'Slot1/Inlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                 'alarm_status': 'false',
                 'alarm_threshold': 0,
                 'temp_avg': 31,
                 'temp_instant': 31,
                 'temp_interval': 180000000000,
                 'temp_max': 31,
                 'temp_min': 31},
 'Slot1/Outlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                  'alarm_status': 'false',
                  'alarm_threshold': 0,
                  'temp_avg': 36,
                  'temp_instant': 36,
                  'temp_interval': 180000000000,
                  'temp_max': 36,
                  'temp_min': 36},
 'Slot2/Inlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                 'alarm_status': 'false',
                 'alarm_threshold': 0,
                 'temp_avg': 28,
                 'temp_instant': 28,
                 'temp_interval': 180000000000,
                 'temp_max': 28,
                 'temp_min': 28},
 'Slot2/Outlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                  'alarm_status': 'false',
                  'alarm_threshold': 0,
                  'temp_avg': 34,
                  'temp_instant': 34,
                  'temp_interval': 180000000000,
                  'temp_max': 34,
                  'temp_min': 34},
 'Slot3/Coretemp': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                    'alarm_status': 'false',
                    'alarm_threshold': 0,
                    'temp_avg': 50,
                    'temp_instant': 51,
                    'temp_interval': 180000000000,
                    'temp_max': 50,
                    'temp_min': 50},
 'Slot3/UADP': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                'alarm_status': 'false',
                'alarm_threshold': 0,
                'temp_avg': 59,
                'temp_instant': 59,
                'temp_interval': 180000000000,
                'temp_max': 59,
                'temp_min': 59},
 'Slot3/inlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                 'alarm_status': 'false',
                 'alarm_threshold': 0,
                 'temp_avg': 30,
                 'temp_instant': 30,
                 'temp_interval': 180000000000,
                 'temp_max': 30,
                 'temp_min': 30},
 'Slot3/outlet': {'alarm_severity': 'openconfig-alarm-types:UNKNOWN',
                  'alarm_status': 'false',
                  'alarm_threshold': 0,
                  'temp_avg': 43,
                  'temp_instant': 43,
                  'temp_interval': 180000000000,
                  'temp_max': 43,
                  'temp_min': 43}}
        self.assertEqual(result, expected_output)

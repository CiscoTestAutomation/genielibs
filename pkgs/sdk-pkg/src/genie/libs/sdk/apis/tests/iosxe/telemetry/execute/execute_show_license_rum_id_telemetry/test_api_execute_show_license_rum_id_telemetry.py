import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.execute import execute_show_license_rum_id_telemetry


class TestExecuteShowLicenseRumIdTelemetry(unittest.TestCase):

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

    def test_execute_show_license_rum_id_telemetry(self):
        result = execute_show_license_rum_id_telemetry(self.device)
        expected_output = ('1667873757          DELETED   N     TELEMETRY\r\n'
 '1667873760          DELETED   N     TELEMETRY\r\n'
 '1667873763          DELETED   N     TELEMETRY\r\n'
 '1667873766          DELETED   N     TELEMETRY\r\n'
 '1667873769          DELETED   N     TELEMETRY\r\n'
 '1667873770          DELETED   N     TELEMETRY\r\n'
 '1667873781          DELETED   N     TELEMETRY\r\n'
 '1667873784          DELETED   N     TELEMETRY\r\n'
 '1667873789          DELETED   N     TELEMETRY\r\n'
 '1667873792          DELETED   N     TELEMETRY\r\n'
 '1667873799          DELETED   N     TELEMETRY\r\n'
 '1667873802          DELETED   N     TELEMETRY\r\n'
 '1667873805          DELETED   N     TELEMETRY\r\n'
 '1667873808          DELETED   N     TELEMETRY\r\n'
 '1667873815          DELETED   N     TELEMETRY\r\n'
 '1667873822          DELETED   N     TELEMETRY\r\n'
 '1667873825          DELETED   N     TELEMETRY\r\n'
 '1667873828          DELETED   N     TELEMETRY\r\n'
 '1667873831          DELETED   N     TELEMETRY\r\n'
 '1667873834          DELETED   N     TELEMETRY\r\n'
 '1667873837          DELETED   N     TELEMETRY\r\n'
 '1667873840          DELETED   N     TELEMETRY\r\n'
 '1667873843          DELETED   N     TELEMETRY\r\n'
 '1667873846          DELETED   N     TELEMETRY\r\n'
 '1667873849          DELETED   N     TELEMETRY\r\n'
 '1667873852          DELETED   N     TELEMETRY\r\n'
 '1667873855          DELETED   N     TELEMETRY\r\n'
 '1667873858          DELETED   N     TELEMETRY\r\n'
 '1667873861          DELETED   N     TELEMETRY\r\n'
 '1667873864          DELETED   N     TELEMETRY\r\n'
 '1667873871          DELETED   N     TELEMETRY\r\n'
 '1667873874          DELETED   N     TELEMETRY\r\n'
 '1667873877          DELETED   N     TELEMETRY\r\n'
 '1667873880          DELETED   N     TELEMETRY\r\n'
 '1667873883          DELETED   N     TELEMETRY\r\n'
 '1667873886          DELETED   N     TELEMETRY\r\n'
 '1667873889          DELETED   N     TELEMETRY\r\n'
 '1667873892          DELETED   N     TELEMETRY\r\n'
 '1667873895          DELETED   N     TELEMETRY\r\n'
 '1667873898          DELETED   N     TELEMETRY\r\n'
 '1667873901          DELETED   N     TELEMETRY\r\n'
 '1667873904          DELETED   N     TELEMETRY\r\n'
 '1667873907          DELETED   N     TELEMETRY\r\n'
 '1667873910          DELETED   N     TELEMETRY\r\n'
 '1667873913          DELETED   N     TELEMETRY\r\n'
 '1667873916          DELETED   N     TELEMETRY\r\n'
 '1667873919          DELETED   N     TELEMETRY\r\n'
 '1667873922          DELETED   N     TELEMETRY\r\n'
 '1667873929          DELETED   N     TELEMETRY\r\n'
 '1667873932          DELETED   N     TELEMETRY\r\n'
 '1667873935          DELETED   N     TELEMETRY\r\n'
 '1667873938          DELETED   N     TELEMETRY\r\n'
 '1667873941          DELETED   N     TELEMETRY')
        self.assertEqual(result, expected_output)

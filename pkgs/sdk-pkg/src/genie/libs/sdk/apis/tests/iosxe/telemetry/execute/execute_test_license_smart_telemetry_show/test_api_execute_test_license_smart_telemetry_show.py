import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.execute import execute_test_license_smart_telemetry_show


class TestExecuteTestLicenseSmartTelemetryShow(unittest.TestCase):

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

    def test_execute_test_license_smart_telemetry_show(self):
        result = execute_test_license_smart_telemetry_show(self.device)
        expected_output = ('{"version":"2.0","asset_identification":{"report_id":1667873941,"asset":{"name":"regid.2017-05.com.cisco.C9300,v1_727af1d9-6c39-4444-b301-863f81445b72"},"instance":{"sudi":{"udi_pid":"C9300-48U","udi_serial_number":"FCW2137L0E2"},"product_instance_identifier":"360b8a0f-7713-4f20-846f-03281350f9d3"}},"meta":{"report_type":"telemetry","utility_enabled":false,"ha_udi":[{"role":"Active","sudi":{"udi_pid":"C9300-48U","udi_serial_number":"FCW2137L0E2"}},{"role":"Standby","sudi":{"udi_pid":"C9300-48U","udi_serial_number":"FOC2624Y70Z"}}]},"measurements":[{"start_time":1668402512,"end_time":1668402529,"metric_name":"Telemetry '
 'Meta '
 'Info","values":[{"type":"report_id","value":"1668402529"},{"type":"policy_version","value":"17.11.1"},{"type":"engine_version","value":"17.11.1"},{"type":"policy_file_version","value":"1"},{"type":"timezone","value":"18446744073709526416"},{"type":"version","value":"0"},{"type":"product_id","value":"C9300-48U"},{"type":"serial_number","value":"FCW2137L0E2"},{"type":"software_version","value":"17.11.1"},{"type":"metadata","value":""}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402529,"meta":[{"type":"report_id","value":"1668402529"}],"metric_name":"hardware_inventory","values":[{"type":"json_encode","value":"[{\\"cname\\":\\"Switch2\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"Switch8\\",\\"serial_no\\":\\"FOC2624Y70Z\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"c93xx '
 'Stack\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"StackPort2/1\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort2/2\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/1\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/2\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"PowerSupply2/B\\",\\"serial_no\\":\\"DCA2210G3R5\\",\\"part_no\\":\\"PWR-C1-715WAC\\"},{\\"cname\\":\\"PowerSupply8/A\\",\\"serial_no\\":\\"DTN2106V0HE\\",\\"part_no\\":\\"PWR-C1-1100WAC\\"},{\\"cname\\":\\"FRUUplinkModule2/1\\",\\"serial_no\\":\\"FOC19312K2N\\",\\"part_no\\":\\"C3850-NM-4-10G\\"},{\\"cname\\":\\"FRUUplinkModule8/1\\",\\"serial_no\\":\\"FOC17167MHJ\\",\\"part_no\\":\\"C3850-NM-4-1G\\"}]"}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402550,"metric_name":"Telemetry '
 'Meta '
 'Info","values":[{"type":"report_id","value":"1668402550"},{"type":"policy_version","value":"17.11.1"},{"type":"engine_version","value":"17.11.1"},{"type":"policy_file_version","value":"1"},{"type":"timezone","value":"18446744073709526416"},{"type":"version","value":"0"},{"type":"product_id","value":"C9300-48U"},{"type":"serial_number","value":"FCW2137L0E2"},{"type":"software_version","value":"17.11.1"},{"type":"metadata","value":""}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402550,"meta":[{"type":"report_id","value":"1668402550"}],"metric_name":"hardware_inventory","values":[{"type":"json_encode","value":"[{\\"cname\\":\\"Switch2\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"Switch8\\",\\"serial_no\\":\\"FOC2624Y70Z\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"c93xx '
 'Stack\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"StackPort2/1\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort2/2\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/1\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/2\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"PowerSupply2/B\\",\\"serial_no\\":\\"DCA2210G3R5\\",\\"part_no\\":\\"PWR-C1-715WAC\\"},{\\"cname\\":\\"PowerSupply8/A\\",\\"serial_no\\":\\"DTN2106V0HE\\",\\"part_no\\":\\"PWR-C1-1100WAC\\"},{\\"cname\\":\\"FRUUplinkModule2/1\\",\\"serial_no\\":\\"FOC19312K2N\\",\\"part_no\\":\\"C3850-NM-4-10G\\"},{\\"cname\\":\\"FRUUplinkModule8/1\\",\\"serial_no\\":\\"FOC17167MHJ\\",\\"part_no\\":\\"C3850-NM-4-1G\\"}]"}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402831,"metric_name":"Telemetry '
 'Meta '
 'Info","values":[{"type":"report_id","value":"1668402831"},{"type":"policy_version","value":"17.11.1"},{"type":"engine_version","value":"17.11.1"},{"type":"policy_file_version","value":"1"},{"type":"timezone","value":"18446744073709526416"},{"type":"version","value":"0"},{"type":"product_id","value":"C9300-48U"},{"type":"serial_number","value":"FCW2137L0E2"},{"type":"software_version","value":"17.11.1"},{"type":"metadata","value":""}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402831,"meta":[{"type":"report_id","value":"1668402831"}],"metric_name":"hardware_inventory","values":[{"type":"json_encode","value":"[{\\"cname\\":\\"Switch2\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"Switch8\\",\\"serial_no\\":\\"FOC2624Y70Z\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"c93xx '
 'Stack\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"StackPort2/1\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort2/2\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/1\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/2\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"PowerSupply2/B\\",\\"serial_no\\":\\"DCA2210G3R5\\",\\"part_no\\":\\"PWR-C1-715WAC\\"},{\\"cname\\":\\"PowerSupply8/A\\",\\"serial_no\\":\\"DTN2106V0HE\\",\\"part_no\\":\\"PWR-C1-1100WAC\\"},{\\"cname\\":\\"FRUUplinkModule2/1\\",\\"serial_no\\":\\"FOC19312K2N\\",\\"part_no\\":\\"C3850-NM-4-10G\\"},{\\"cname\\":\\"FRUUplinkModule8/1\\",\\"serial_no\\":\\"FOC17167MHJ\\",\\"part_no\\":\\"C3850-NM-4-1G\\"}]"}],"log_time":1668402884},{"start_time":1668402512,"end_time":1668402903,"metric_name":"Telemetry '
 'Meta '
 'Info","values":[{"type":"report_id","value":"1668402903"},{"type":"policy_version","value":"17.11.1"},{"type":"engine_version","value":"17.11.1"},{"type":"policy_file_version","value":"1"},{"type":"timezone","value":"18446744073709526416"},{"type":"version","value":"0"},{"type":"product_id","value":"C9300-48U"},{"type":"serial_number","value":"FCW2137L0E2"},{"type":"software_version","value":"17.11.1"},{"type":"metadata","value":""}],"log_time":1668402907},{"start_time":1668402512,"end_time":1668402903,"meta":[{"type":"report_id","value":"1668402903"}],"metric_name":"hardware_inventory","values":[{"type":"json_encode","value":"[{\\"cname\\":\\"Switch2\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"Switch8\\",\\"serial_no\\":\\"FOC2624Y70Z\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"c93xx '
 'Stack\\",\\"serial_no\\":\\"FCW2137L0E2\\",\\"part_no\\":\\"C9300-48U\\"},{\\"cname\\":\\"StackPort2/1\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort2/2\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/1\\",\\"serial_no\\":\\"LCC2109G0LM\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"StackPort8/2\\",\\"serial_no\\":\\"MOC2117A9QX\\",\\"part_no\\":\\"STACK-T1-1M\\"},{\\"cname\\":\\"PowerSupply2/B\\",\\"serial_no\\":\\"DCA2210G3R5\\",\\"part_no\\":\\"PWR-C1-715WAC\\"},{\\"cname\\":\\"PowerSupply8/A\\",\\"serial_no\\":\\"DTN2106V0HE\\",\\"part_no\\":\\"PWR-C1-1100WAC\\"},{\\"cname\\":\\"FRUUplinkModule2/1\\",\\"serial_no\\":\\"FOC19312K2N\\",\\"part_no\\":\\"C3850-NM-4-10G\\"},{\\"cname\\":\\"FRUUplinkModule8/1\\",\\"serial_no\\":\\"FOC17167MHJ\\",\\"part_no\\":\\"C3850-NM-4-1G\\"}]"}],"log_time":1668402907}]}')
        self.assertEqual(result, expected_output)

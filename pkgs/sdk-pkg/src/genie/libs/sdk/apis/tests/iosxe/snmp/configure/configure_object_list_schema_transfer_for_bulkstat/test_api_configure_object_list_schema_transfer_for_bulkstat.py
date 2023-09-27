import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_object_list_schema_transfer_for_bulkstat


class TestConfigureObjectListSchemaTransferForBulkstat(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T1-9300-SP1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T1-9300-SP1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_object_list_schema_transfer_for_bulkstat(self):
        result = configure_object_list_schema_transfer_for_bulkstat(self.device, 'transfer', 'myObject', 'mySchema', 'myTransfer', None, '1', 'GigabitEthernet1/0/6', 'schemaASCII', '3', '247483647', 'tftp://<202.153.144.2/auto/tftpboot/logsTransfer', 'enable', 'logging on')
        expected_output = None
        self.assertEqual(result, expected_output)

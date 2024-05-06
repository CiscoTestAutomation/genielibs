import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.transceiver.get import transceiver_info


class TestTransceiverInfo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          A2-9300-3M:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9300
            custom:
                abstraction:
                    order: [os, model]
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A2-9300-3M']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_transceiver_info(self):
        result = transceiver_info(self.device)
        expected_output = {'connector_type': ['openconfig-transport-types:LC_CONNECTOR'],
 'form_factor': ['openconfig-transport-types:SFP'],
 'serial_no': ['FNS17462988'],
 'transceiver': ['TenGigabitEthernet3/1/1'],
 'vendor_name': ['CISCO-FINISAR'],
 'vendor_part': ['FTLX8571D3BCL-C2'],
 'vendor_rev': ['A']}
        self.assertEqual(result, expected_output)

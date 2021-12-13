import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.configure import clear_device_tracking_database


class TestClearDeviceTrackingDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_device_tracking_database(self):
        result = clear_device_tracking_database(device=self.device, options=None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_1(self):
        result = clear_device_tracking_database(device=self.device, options=[{'force': True}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_2(self):
        result = clear_device_tracking_database(device=self.device, options=[{'policy': 'test'}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_3(self):
        result = clear_device_tracking_database(device=self.device, options=[{'vlanid': 10}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_4(self):
        result = clear_device_tracking_database(device=self.device, options=[{'interface': {'force': True, 'interface': 'te1/0/1'}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_5(self):
        result = clear_device_tracking_database(device=self.device, options=[{'interface': {'interface': 'te1/0/1', 'vlanid': 10}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_6(self):
        result = clear_device_tracking_database(device=self.device, options=[{'mac': {'address': 'dead.beef.0001', 'target': {'force': True}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_7(self):
        result = clear_device_tracking_database(device=self.device, options=[{'mac': {'address': 'dead.beef.0001', 'target': {'interface': 'te1/0/1'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_8(self):
        result = clear_device_tracking_database(device=self.device, options=[{'mac': {'address': 'dead.beef.0001', 'target': {'policy': 'test'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_9(self):
        result = clear_device_tracking_database(device=self.device, options=[{'mac': {'address': 'dead.beef.0001', 'target': {'vlanid': 10}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_10(self):
        result = clear_device_tracking_database(device=self.device, options=[{'address': {'address': '20.20.20.20', 'target': {'force': True}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_11(self):
        result = clear_device_tracking_database(device=self.device, options=[{'address': {'address': '20.20.20.20', 'target': {'interface': 'te1/0/1'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_12(self):
        result = clear_device_tracking_database(device=self.device, options=[{'address': {'address': '20.20.20.20', 'target': {'policy': 'test'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_13(self):
        result = clear_device_tracking_database(device=self.device, options=[{'address': {'address': '20.20.20.20', 'target': {'vlanid': 10}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_14(self):
        result = clear_device_tracking_database(device=self.device, options=[{'prefix': {'address': '3001::1/48', 'target': {'force': True}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_15(self):
        result = clear_device_tracking_database(device=self.device, options=[{'prefix': {'address': '3001::1/48', 'target': {'interface': 'te1/0/1'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_16(self):
        result = clear_device_tracking_database(device=self.device, options=[{'prefix': {'address': '3001::1/48', 'target': {'policy': 'test'}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_clear_device_tracking_database_17(self):
        result = clear_device_tracking_database(device=self.device, options=[{'prefix': {'address': '3001::1/48', 'target': {'vlanid': 10}}}])
        expected_output = None
        self.assertEqual(result, expected_output)

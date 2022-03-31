import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.verify import interface_counter_check


class TestInterfaceCounterCheck(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          P1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['P1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_interface_counter_check(self):
        result = interface_counter_check(self.device, 'ten1/0/15', 44938, 200, 'outucastpkts', 60, 10)
        expected_output = True
        self.assertEqual(result, expected_output)

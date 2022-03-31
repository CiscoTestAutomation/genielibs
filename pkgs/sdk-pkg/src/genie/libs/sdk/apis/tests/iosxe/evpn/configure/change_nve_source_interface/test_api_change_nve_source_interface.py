import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.configure import change_nve_source_interface


class TestChangeNveSourceInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CL4-c9500:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CL4-c9500']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_change_nve_source_interface(self):
        result = change_nve_source_interface(self.device, '1', 'Loopback1')
        expected_output = None
        self.assertEqual(result, expected_output)

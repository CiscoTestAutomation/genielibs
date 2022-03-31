import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import unconfigure_global_stackwise_virtual


class TestUnconfigureGlobalStackwiseVirtual(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          farscape-pinfra-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: STARTREK
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['farscape-pinfra-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_global_stackwise_virtual(self):
        result = unconfigure_global_stackwise_virtual(self.device)
        expected_output = ('no stackwise-virtual\r\n'
 'no stackwise-virtual\r\n'
 'Please reload the switch to disable Stackwise Virtual functionality\r\n')
        self.assertEqual(result, expected_output)

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.redundancy.execute import execute_redundancy_reload
from genie.libs.sdk.apis.utils import sanitize


class TestExecuteRedundancyReload(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_redundancy_reload(self):
        result = execute_redundancy_reload(self.device, 'peer')
        expected_output = ('Stack is in Half ring setup; Reloading a switch might cause stack split\r\n'
 'Reload peer [confirm]\r\n'
 'Preparing to reload peer')
        # Device output inconsistently includes device prompt
        if result.endswith('#'):
            expected_output += '\r\nstartrek-1#'
        self.assertEqual(sanitize(result), sanitize(expected_output))

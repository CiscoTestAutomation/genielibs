import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.SVI.configure import configure_SVI_Autostate
# Unicon
from unicon.core.errors import SubCommandFailure

class TestConfigureSviAutostate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          gry48-l2-san:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: '9500'
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['gry48-l2-san']
        try:
          self.device.connect(
              learn_hostname=True,
              init_config_commands=[],
              init_exec_commands=[]
          )
        except SubCommandFailure:
          raise SubCommandFailure(
            "Could not configure SVI state"
            )

    def test_configure_SVI_Autostate(self):
        result = configure_SVI_Autostate(self.device, 'Vlan500')
        expected_output = None
        self.assertEqual(result, expected_output)

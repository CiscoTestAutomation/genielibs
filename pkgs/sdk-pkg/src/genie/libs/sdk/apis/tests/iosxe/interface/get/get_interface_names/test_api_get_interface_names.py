import os
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_names
from pyats.topology import loader


class TestGetInterfaceNames(TestCase):

    @classmethod
    def setUpClass(self):
        
        testbed = f"""
        devices:
          ott-c9300-66:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: cat9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ott-c9300-66']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )
        

    def test_get_interface_names(self):
        result = get_interface_names(self.device)
        

        

import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_new_model


class TestUnconfigureAaaNewModel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          HCR_pk:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['HCR_pk']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_aaa_new_model(self):
        result = unconfigure_aaa_new_model(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)

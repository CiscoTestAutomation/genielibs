import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.span.configure import configure_local_span_source


class TestConfigureLocalSpanSource(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9400_L2_DUT:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat3k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400_L2_DUT']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_local_span_source(self):
        result = configure_local_span_source(self.device, 10, 'interface', 'Gi1/0/3', 'tx')
        expected_output = None
        self.assertEqual(result, expected_output)

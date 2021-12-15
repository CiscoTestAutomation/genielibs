import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.jinja.get import load_jinja_template


class TestLoadJinjaTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_load_jinja_template(self):
        result = load_jinja_template('', 'interface.j2', interface='Gi0/0', desc='test description')
        expected_output = 'interface Gi0/0\n description test description'
        self.assertEqual(result, expected_output)

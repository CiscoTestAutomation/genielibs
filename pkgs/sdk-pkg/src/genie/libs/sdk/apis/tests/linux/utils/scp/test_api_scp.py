import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.utils import scp


class TestScp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          lnx:
            os: linux
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir mock_data --state execute
          R1:
            os: iosxe
            credentials:
              default:
                username: user
                password: test
            connections:
              a:
                command: invalid
              vty:
                host: lnx
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['lnx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_scp(self):
        result = scp(self.device, local_path='/tmp/test.txt', remote_path='/tmp/test2.txt', remote_device='R1', remote_via='vty')
        self.assertEqual(result, True)

    def test_scp_negative(self):
        result = scp(self.device, local_path='/tmp/does_not_exist.txt', remote_path='/tmp/test2.txt', remote_device='R1', remote_via='vty')
        self.assertEqual(result, False)

    def test_scp_exception(self):
        with self.assertRaisesRegex(ValueError, 'Please specify remote_via with a connection name that has an ip or host attribute'):
          scp(self.device, local_path='/tmp/test.txt', remote_path='/tmp/test2.txt', remote_device='R1')

    def test_scp_password(self):
        result = scp(self.device, local_path='/tmp/test2.txt', remote_path='/tmp/test3.txt', remote_device='R1', remote_via='vty')
        self.assertEqual(result, True)

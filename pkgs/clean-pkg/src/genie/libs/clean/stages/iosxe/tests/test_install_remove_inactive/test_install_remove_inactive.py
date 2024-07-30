import unittest

from pyats.results import Passed
from pyats.topology import loader
from pyats.aetest.steps import Steps
from genie.libs.clean.stages.iosxe.stages import InstallRemoveInactive


class TestIosXEConnect(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE c8kv device """

    @classmethod
    def setUp(cls):
        # Make sure we have a unique Steps() object for result verification
        cls.steps = Steps()

        cls.image = 'image.bin'
        
        # And we want the following methods to be mocked to simulate the stage.        
        cls.install_remove_inactive = InstallRemoveInactive()
    
    def test_install_remove_inactive_force_remove_false_pass_n(self):

        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state remove_inactive_no
                        protocol: unknown
                os: iosxe
                platform: c8kv
                type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        with self.assertLogs(level='DEBUG') as log:
            self.install_remove_inactive(steps=self.steps, device=self.device, images=[self.image], force_remove=False)
            self.assertIn(f'{self.image} is among the files to be deleted. send no so the {self.image} is not deleted.', log.output[1])

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)


    def test_install_remove_inactive_force_remove_false_pass_y(self):

        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state remove_inactive_yes
                        protocol: unknown
                os: iosxe
                platform: c8kv
                type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        with self.assertLogs(level='DEBUG') as log:
            self.install_remove_inactive(steps=self.steps, device=self.device, images=[self.image], force_remove=False, timeout=60)
            self.assertIn(f'{self.image} is not among the files to be deleted. Hence, send yes to delete files.', log.output[1])

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)


    def test_install_remove_inactive_force_remove_true_pass_y(self):

        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state remove_inactive_yes_forcefully
                        protocol: unknown
                os: iosxe
                platform: c8kv
                type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        with self.assertLogs(level='DEBUG') as log:
            self.install_remove_inactive(steps=self.steps, device=self.device, images=[self.image])
            self.assertIn(f'Sending yes to delete files without checking {self.image} in among the files to be deleted.', log.output[1])

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)

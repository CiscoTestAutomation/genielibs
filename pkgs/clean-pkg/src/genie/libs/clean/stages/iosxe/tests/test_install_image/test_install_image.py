import unittest
from pyats.results import Passed
from pyats.topology import loader
from pyats.aetest.steps import Steps
from genie.libs.clean.stages.iosxe.stages import InstallImage

class TestInstallImage(unittest.TestCase):
    """ Run unit testing on a mocked IOSXE cat9k device """

    @classmethod
    def setUp(cls):
        # Make sure we have a unique Steps() object for result verification
        cls.steps = Steps()
        cls.image = 'image.bin'
        # And we want the following methods to be mocked to simulate the stage.
        cls.install_image = InstallImage()


    def test_issu_in_progress(self):
        testbed = """
        devices:
            router:
                connections:
                    defaults:
                        class: unicon.Unicon
                    a:
                        command: mock_device_cli --os iosxe --mock_data_dir mock_data --state install_add_activate_commit_error
                        protocol: unknown
                os: iosxe
                platform: cat9k
                type: router
        """
        self.cls = InstallImage()
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

        # Mock the history attribute
        self.cls.history = {
            "InstallImage": type('MockParameters', (), {
                'parameters': {"image_mapping": {}}
            })()
        }

        with self.assertLogs(level='DEBUG') as log:
            self.cls.install_image(steps=self.steps, device=self.device, images=[self.image])

        # Check the results is as expected.
        self.assertEqual(Passed, self.steps.details[0].result)


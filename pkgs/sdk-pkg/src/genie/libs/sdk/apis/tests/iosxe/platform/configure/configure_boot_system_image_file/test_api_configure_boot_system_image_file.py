from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_system_image_file


class TestConfigureBootSystemImageFile(TestCase):

    def test_configure_boot_system_image_file(self):
        device = Mock()
        result = configure_boot_system_image_file(
            device,
            'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',
            None
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot system flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',)
        )

    def test_configure_boot_system_image_file_1(self):
        device = Mock()
        result = configure_boot_system_image_file(
            device,
            'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',
            'all'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot system switch all flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',)
        )

    def test_configure_boot_system_image_file_2(self):
        device = Mock()
        result = configure_boot_system_image_file(
            device,
            'flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',
            2
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('boot system switch 2 flash:cat9k-espbase.BLD_POLARIS_DEV_LATEST_20230406_174734.SSA.pkg',)
        )
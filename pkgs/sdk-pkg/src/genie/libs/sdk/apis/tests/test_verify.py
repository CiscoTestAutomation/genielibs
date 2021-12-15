import unittest
from unittest.mock import MagicMock, Mock
from genie.libs.sdk.apis.verify import verify_current_image


class TestVerifyApis(unittest.TestCase):

    def test_verify_current_image(self):
        device = MagicMock()
        device.name = 'aDevice'
        device.api = MagicMock()

        # Test succeeds normally, same dir and same image (no Exception)
        device.api.get_running_image = \
            Mock(return_value=('bootflash:csr1000v-rpboot.16.09.01.SPA.pkg'))
        verify_current_image(
            device, 
            images=['bootflash:csr1000v-rpboot.16.09.01.SPA.pkg']
        )

        # Test succeeds if running image has preceeding '/' (no Exception)
        device.api.get_running_image = \
            Mock(return_value=('bootflash:/csr1000v-rpboot.16.09.01.SPA.pkg'))
        verify_current_image(device, images=['bootflash:csr1000v-rpboot.16.09.01.SPA.pkg'])

        # Test succeeds if provided image has preceeding '/' (no Exception)
        device.api.get_running_image = \
            Mock(return_value=('bootflash:csr1000v-rpboot.16.09.01.SPA.pkg'))
        verify_current_image(device, images=['bootflash:/csr1000v-rpboot.16.09.01.SPA.pkg'])


        # Test that difference in image list length raises Exception
        device.api.get_running_image = \
            Mock(return_value=('bootflash:csr1000v-rpboot.16.09.01.SPA.pkg'))
        with self.assertRaises(Exception) as cm:
            verify_current_image(
                device, 
                images=['bootflash:csr1000v-rpboot.16.09.01.SPA.pkg', 
                        'bootflash:csr1000v-rpboot.16.09.02.SPA.pkg']
            )
        self.assertIn("not of the same length", str(cm.exception))

        # Test that different image directories raises Exception
        device.api.get_running_image = \
            Mock(return_value=('boot:csr1000v-rpboot.16.09.01.SPA.pkg'))
        with self.assertRaises(Exception) as cm:
            verify_current_image(
                device, 
                images=['bootflash:csr1000v-rpboot.16.09.01.SPA.pkg']
            )
        self.assertIn("do not match", str(cm.exception))

        # Test that different image names raises Exception
        device.api.get_running_image = \
            Mock(return_value=('bootflash:csr1000v-boot.16.09.01.SPA.pkg'))
        with self.assertRaises(Exception) as cm:
            verify_current_image(
                device, 
                images=['bootflash:csr1000v-rpboot.16.09.01.SPA.pkg']
            )
        self.assertIn("do not match", str(cm.exception))

        # Test that different paths raises Exception
        device.api.get_running_image = \
            Mock(return_value=('bootflash:/some/path/to/csr1000v-boot.16.09.01.SPA.pkg'))
        with self.assertRaises(Exception) as cm:
            verify_current_image(
                device, 
                images=['bootflash:/path/to/csr1000v-boot.16.09.01.SPA.pkg']
            )
        self.assertIn("do not match", str(cm.exception))

        # Test that more dirs in path don't affect results
        device.api.get_running_image = \
            Mock(return_value=('bootflash:/some/path/to/csr1000v-boot.16.09.01.SPA.pkg'))
        verify_current_image(
            device, 
            images=['bootflash:/some/path/to/csr1000v-boot.16.09.01.SPA.pkg']
        )
        device.api.get_running_image = \
            Mock(return_value=('bootflash:/some/path/to/csr1000v-boot.16.09.01.SPA.pkg'))
        verify_current_image(
            device, 
            images=['bootflash:some/path/to/csr1000v-boot.16.09.01.SPA.pkg']
        )

        # Test changing the delimiter works
        device.api.get_running_image = \
            Mock(return_value=('bootflash\csr1000v-boot.16.09.01.SPA.pkg:01'))
        verify_current_image(
            device, 
            images=['bootflash\csr1000v-boot.16.09.01.SPA.pkg:01'], 
            delimiter_regex=r'\\'
        )


        # Test that lists of images can be compared successfully 
        device.api.get_running_image = \
            Mock(return_value=([
                'bootflash:csr1000v-boot.16.09.01.SPA.pkg',
                'bootflash/csr1000v-boot.16.09.02.SPA.pkg',
                'bootflash:/csr1000v-boot.16.09.03.SPA.pkg',
                'bootflash:dir/csr1000v-boot.16.09.04.SPA.pkg',
            ]))
        verify_current_image(
            device, 
            images=[
                'bootflash:csr1000v-boot.16.09.01.SPA.pkg',
                'bootflash/csr1000v-boot.16.09.02.SPA.pkg',
                'bootflash:/csr1000v-boot.16.09.03.SPA.pkg',
                'bootflash:dir/csr1000v-boot.16.09.04.SPA.pkg',
            ]
        )

        # Test that one discrepancy in a list of images will cause the 
        # comparison to fail
        with self.assertRaises(Exception) as cm:
            verify_current_image(
                device, 
                images=[
                    'bootflash:csr1000v-boot.16.09.01.SPA.pkg',
                    'bootflash/csr1000v-boot.16.09.02.SPA.pkg',
                    'bootflash:/csr1000v-boot.16.09.03.SPA.pkg',
                    'bootflash:dir/csr1000v-boot.16.09.05.SPA.pkg',
                ]
            )
        self.assertIn("do not match", str(cm.exception))


if __name__ == '__main__':
    unittest.main()
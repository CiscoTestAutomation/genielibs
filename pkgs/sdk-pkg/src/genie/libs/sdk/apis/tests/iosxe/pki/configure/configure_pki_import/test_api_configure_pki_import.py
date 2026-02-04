from unittest import TestCase
from unittest.mock import Mock, call
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.pki.configure import configure_pki_import


class TestConfigurePkiImport(TestCase):

    def test_configure_pki_import_success(self):
        """Test successful PKI import without errors"""
        device = Mock()
        result = configure_pki_import(
            device,
            'test1',
            'pkcs12',
            'bootflash:',
            'self.p12',
            None,
            'cisco123'
        )
        expected_output = None
        self.assertEqual(result, expected_output)
        # Verify configure was called once
        self.assertEqual(device.configure.call_count, 1)
        # Verify the correct command was used
        args = device.configure.call_args
        self.assertIn('crypto pki import test1 pkcs12 bootflash:self.p12 password cisco123', args[0][0])

    def test_configure_pki_import_trustpoint_in_use(self):
        """Test PKI import when trustpoint is already in use - should delete and retry"""
        device = Mock()
        device.configure.side_effect = [
            SubCommandFailure("% Trustpoint 'test1' is in use.\n% Please delete it or use a different label."),
            None,
            None
        ]
        result = configure_pki_import(
            device,
            'test1',
            'pkcs12',
            'bootflash:',
            'self.p12',
            None,
            'cisco123'
        )
        expected_output = None
        self.assertEqual(result, expected_output)
        # Verify configure was called 3 times (initial attempt + unconfigure + retry)
        self.assertEqual(device.configure.call_count, 3)
        # Verify first call was the import command
        first_call_args = device.configure.call_args_list[0][0][0]
        self.assertIn('crypto pki import test1 pkcs12 bootflash:self.p12 password cisco123', first_call_args)

        second_call_args = device.configure.call_args_list[1][0][0]
        self.assertIn('no crypto pki trustpoint test1', second_call_args)

        # Verify third call was the retry import command
        third_call_args = device.configure.call_args_list[2][0][0]
        self.assertIn('crypto pki import test1 pkcs12 bootflash:self.p12 password cisco123', third_call_args)

    def test_configure_pki_import_other_error(self):
        """Test PKI import with non-trustpoint error - should raise exception"""
        device = Mock()

        # Configure raises a different error
        device.configure.side_effect = SubCommandFailure("% PEM files import failed.")

        with self.assertRaises(SubCommandFailure) as context:
            configure_pki_import(
                device,
                'test1',
                'pkcs12',
                'bootflash:',
                'self.p12',
                None,
                'cisco123'
            )

        # Verify the error message contains the original error
        self.assertIn("failed to configure crypto pki import", str(context.exception))

        # Verify configure was called only once (no retry for non-trustpoint errors)
        self.assertEqual(device.configure.call_count, 1)


if __name__ == '__main__':
    import unittest
    unittest.main()

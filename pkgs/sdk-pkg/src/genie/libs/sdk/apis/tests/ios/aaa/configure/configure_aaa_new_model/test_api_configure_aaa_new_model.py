import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.aaa.configure import configure_aaa_new_model


class TestConfigureAaaNewModel(TestCase):

    def test_configure_aaa_new_model(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_aaa_new_model(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(["aaa new-model"])

    def test_configure_aaa_new_model_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            configure_aaa_new_model(device)


if __name__ == "__main__":
    unittest.main()

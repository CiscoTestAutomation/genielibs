import unittest
from unittest import TestCase
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.ios.aaa.configure import unconfigure_aaa_new_model


class TestUnconfigureAaaNewModel(TestCase):

    def test_unconfigure_aaa_new_model(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_aaa_new_model(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(["no aaa new-model"])

    def test_unconfigure_aaa_new_model_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure("error")

        with self.assertRaises(SubCommandFailure):
            unconfigure_aaa_new_model(device)


if __name__ == "__main__":
    unittest.main()

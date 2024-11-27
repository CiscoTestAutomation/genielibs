import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_aaa_new_model


class TestUnconfigureAaaNewModel(unittest.TestCase):

    def test_unconfigure_aaa_new_model(self):
        self.device = Mock()
        unconfigure_aaa_new_model(self.device)
        self.device.configure.assert_called_with([
            'no aaa new-model'
        ])

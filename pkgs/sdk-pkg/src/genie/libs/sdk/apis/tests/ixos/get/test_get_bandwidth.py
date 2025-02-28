from unittest import TestCase
from genie.libs.sdk.apis.ixos.bandwidth.get import get_bandwidth
from unittest.mock import Mock


class TestGetBandwidth(TestCase):

    def test_get_bandwidth(self):
        result = get_bandwidth("10/100/1000 Base T")
        self.assertEqual(result, 1000)

        result = get_bandwidth("100GE SR10")
        self.assertEqual(result, 100000)

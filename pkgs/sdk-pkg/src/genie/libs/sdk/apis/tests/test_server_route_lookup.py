"""Unit tests for server_route_lookup APIs."""

import unittest
import ipaddress
from unittest.mock import MagicMock

from genie.libs.sdk.apis.server_route_lookup import (
    find_server_ip_for_device_ip,
)

# device.api passes device as the first arg; tests pass a mock.
mock_device = MagicMock()


class TestFindServerIpForDeviceIp(unittest.TestCase):

    def test_ipv4_route_match_returns_server_interface_ip(self):
        servers = {
            'tftp1': {
                'address': '10.1.1.1',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '10.1.1.1/24',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_ipv6_route_match_returns_server_interface_ip(self):
        servers = {
            'server1': {
                'address': '2001:db8::1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv6': [
                            {'subnet': '2001:db8::/32', 'interface': 'eth1'}
                        ]
                    }
                },
                'interfaces': {
                    'eth1': {
                        'ipv6': '2001:db8::1/64',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '2001:db8::100', servers)
        self.assertEqual(result, '2001:db8::1')

    def test_more_specific_route_wins(self):
        servers = {
            'broad_server': {
                'address': '10.255.0.1',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '10.255.0.1/24',
                    }
                }
            },
            'specific_server': {
                'address': '10.5.0.1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.5.0.0/16', 'interface': 'mgmt0'}
                        ]
                    }
                },
                'interfaces': {
                    'mgmt0': {
                        'ipv4': '10.5.0.1/24',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.5.0.1')

    def test_non_matching_device_ip_returns_none(self):
        servers = {
            'server1': {
                'address': '192.168.1.1',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '192.168.1.0/24', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '192.168.1.1/24',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '172.16.0.5', servers)
        self.assertIsNone(result)

    def test_missing_interface_returns_none(self):
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth99'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '10.1.1.1/24',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertIsNone(result)

    def test_invalid_device_ip_raises_valueerror(self):
        servers = {}
        with self.assertRaises(ValueError):
            find_server_ip_for_device_ip(mock_device, 'not-an-ip', servers)

    def test_empty_servers_returns_none(self):
        servers = {}
        result = find_server_ip_for_device_ip(mock_device, '10.1.1.1', servers)
        self.assertIsNone(result)

    def test_interface_ip_without_prefix(self):
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '10.1.1.1',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_interface_ip_as_list(self):
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': ['10.1.1.1/24', '10.1.1.2/24'],
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_interface_ip_as_ip_interface_object(self):
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': ipaddress.ip_interface('10.1.1.1/24'),
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_multiple_routes_same_server_longest_prefix_wins(self):
        servers = {
            'server1': {
                'address': '10.5.0.1',
                'protocol': 'scp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'},
                            {'subnet': '10.5.0.0/16', 'interface': 'eth1'},
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {
                        'ipv4': '10.255.0.1/24',
                    },
                    'eth1': {
                        'ipv4': '10.5.0.1/24',
                    }
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.5.0.1')


class TestServerHostnameScoping(unittest.TestCase):
    """Tests for find_server_ip_for_device_ip with server_hostname parameter."""

    def _make_servers(self):
        return {
            'tftp-morpheus': {
                'address': '5.251.17.16',
                'server': '5.251.17.16',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '5.251.0.0/16', 'interface': 'ens192'}
                        ]
                    }
                },
                'interfaces': {
                    'ens192': {'ipv4': '5.251.17.16/16'}
                }
            },
            'tftp-testing': {
                'address': '5.40.26.169',
                'server': '5.40.26.169',
                'protocol': 'tftp',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '5.40.0.0/16', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': '5.40.26.169/16'}
                }
            },
        }

    def test_scoped_to_matching_server(self):
        """When server_hostname matches, only that server is searched."""
        servers = self._make_servers()
        # Device in 5.40.x.x — without scoping, tftp-testing would win.
        # With scoping to tftp-morpheus, no route covers 5.40.12.76.
        result = find_server_ip_for_device_ip(
            mock_device, '5.40.12.76', servers, server_hostname='5.251.17.16')
        self.assertIsNone(result)

    def test_scoped_server_has_route(self):
        """When scoped server has a covering route, return its interface IP."""
        servers = self._make_servers()
        result = find_server_ip_for_device_ip(
            mock_device, '5.40.12.76', servers, server_hostname='5.40.26.169')
        self.assertEqual(result, '5.40.26.169')

    def test_no_scoping_searches_all(self):
        """Without server_hostname, all servers are searched (existing behavior)."""
        servers = self._make_servers()
        result = find_server_ip_for_device_ip(mock_device, '5.40.12.76', servers)
        self.assertEqual(result, '5.40.26.169')

    def test_unknown_hostname_returns_none(self):
        """When server_hostname doesn't match any server, return None."""
        servers = self._make_servers()
        result = find_server_ip_for_device_ip(
            mock_device, '5.40.12.76', servers, server_hostname='99.99.99.99')
        self.assertIsNone(result)

    def test_scoped_by_interface_ip(self):
        """server_hostname can match a server's interface IP."""
        servers = {
            'myserver': {
                'address': '10.0.0.1',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '172.16.0.0/12', 'interface': 'mgmt0'}
                        ]
                    }
                },
                'interfaces': {
                    'mgmt0': {'ipv4': '172.16.1.1/12'},
                    'data0': {'ipv4': '192.168.1.1/24'},
                }
            }
        }
        # Scope by interface IP (data0), server still has route
        result = find_server_ip_for_device_ip(
            mock_device, '172.16.5.10', servers, server_hostname='192.168.1.1')
        self.assertEqual(result, '172.16.1.1')

    def test_scoped_by_server_field(self):
        """server_hostname can match a server's 'server' field."""
        servers = {
            'myserver': {
                'address': '10.0.0.1',
                'server': 'tftp.example.com',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': '10.0.0.1/8'}
                }
            }
        }
        result = find_server_ip_for_device_ip(
            mock_device, '10.5.3.2', servers, server_hostname='tftp.example.com')
        self.assertEqual(result, '10.0.0.1')

    def test_next_hop_fallback(self):
        """Route with 'next-hop' instead of 'interface' should resolve."""
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'next-hop': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': '10.1.1.1/24'}
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_invalid_subnet_in_route_skipped(self):
        """Route with an invalid subnet string is skipped without crashing."""
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': 'not-a-subnet', 'interface': 'eth0'},
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'},
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': '10.1.1.1/24'}
                }
            }
        }
        # Should skip the invalid subnet and still match the valid one
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertEqual(result, '10.1.1.1')

    def test_empty_interface_address_list_returns_none(self):
        """Empty address list for interface results in no match."""
        servers = {
            'server1': {
                'address': '10.1.1.1',
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'}
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': []}
                }
            }
        }
        result = find_server_ip_for_device_ip(mock_device, '10.5.3.2', servers)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

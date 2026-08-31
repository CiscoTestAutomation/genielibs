"""Unit tests for server_route_lookup APIs."""

import unittest
import ipaddress
from unittest.mock import MagicMock

from genie.libs.sdk.apis.server_route_lookup import (
    find_server_route_for_device_ip,
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

    def test_legacy_api_projects_ip_from_shared_route_selection(self):
        servers = {
            'server1': {
                'management': {
                    'routes': {
                        'ipv4': [
                            {'subnet': '10.0.0.0/8', 'interface': 'eth0'},
                            {'subnet': '10.5.0.0/16', 'interface': 'eth1'},
                        ]
                    }
                },
                'interfaces': {
                    'eth0': {'ipv4': '10.255.0.1/24'},
                    'eth1': {'ipv4': '10.5.0.1/24'},
                }
            }
        }

        route = find_server_route_for_device_ip(
            mock_device, '10.5.3.2', servers)
        legacy_result = find_server_ip_for_device_ip(
            mock_device, '10.5.3.2', servers)

        self.assertEqual(route, {
            'server_name': 'server1',
            'server_ip': '10.5.0.1',
            'subnet': '10.5.0.0/16',
            'interface': 'eth1',
            'prefixlen': 16,
            'family': 'ipv4',
            'server': 'server1',
            'interface_ip': '10.5.0.1',
            'prefix_length': 16,
            'address_family': 'ipv4',
        })
        self.assertEqual(legacy_result, route['server_ip'])

    def test_structured_api_uses_device_testbed_servers_by_default(self):
        device = MagicMock()
        device.testbed.servers = {
            'proxy': {
                'management': {'routes': {'ipv4': [
                    {'subnet': '10.10.0.0/16', 'interface': 'eth1'},
                ]}},
                'interfaces': {
                    'eth1': {'ipv4': '198.51.100.1/24'},
                },
            }
        }

        result = find_server_route_for_device_ip(device, '10.10.1.5')

        self.assertEqual(result, {
            'server_name': 'proxy',
            'server_ip': '198.51.100.1',
            'subnet': '10.10.0.0/16',
            'interface': 'eth1',
            'prefixlen': 16,
            'family': 'ipv4',
            'server': 'proxy',
            'interface_ip': '198.51.100.1',
            'prefix_length': 16,
            'address_family': 'ipv4',
        })

    def test_structured_api_skips_malformed_metadata_before_valid_server(self):
        servers = {
            'bad-server': 'not-a-mapping',
            'bad-routes': {
                'management': {'routes': 'not-a-mapping'},
            },
            'mixed-routes': {
                'management': {'routes': {'ipv4': [
                    'not-a-mapping',
                    {'subnet': 'not-a-subnet', 'interface': 'eth0'},
                    {'subnet': '10.20.0.0/16', 'interface': 'eth0'},
                ]}},
                'interfaces': {'eth0': {'ipv4': '192.0.2.20/24'}},
            },
        }

        with self.assertLogs(
                'genie.libs.sdk.apis.server_route_lookup', 'WARNING') as logs:
            result = find_server_route_for_device_ip(
                mock_device, '10.20.1.5', servers)

        self.assertEqual(result['server'], 'mixed-routes')
        self.assertEqual(result['interface_ip'], '192.0.2.20')
        diagnostics = '\n'.join(logs.output)
        self.assertIn('non-mapping server', diagnostics)
        self.assertIn('non-mapping management.routes', diagnostics)
        self.assertIn('non-mapping route entry', diagnostics)
        self.assertIn('invalid subnet', diagnostics)

    def test_structured_api_skips_unusable_interfaces(self):
        servers = {
            'missing-interface': {
                'management': {'routes': {'ipv4': [
                    {'subnet': '10.30.1.0/24', 'interface': 'missing'},
                ]}},
                'interfaces': {},
            },
            'wrong-family': {
                'management': {'routes': {'ipv4': [
                    {'subnet': '10.30.0.0/16', 'interface': 'eth0'},
                ]}},
                'interfaces': {'eth0': {'ipv4': '2001:db8::30/64'}},
            },
            'valid': {
                'management': {'routes': {'ipv4': [
                    {'subnet': '10.0.0.0/8', 'interface': 'eth1'},
                ]}},
                'interfaces': {'eth1': {'ipv4': '192.0.2.30/24'}},
            },
        }

        with self.assertLogs(
                'genie.libs.sdk.apis.server_route_lookup', 'WARNING') as logs:
            result = find_server_route_for_device_ip(
                mock_device, '10.30.1.5', servers)

        self.assertEqual(result, {
            'server_name': 'valid',
            'server_ip': '192.0.2.30',
            'subnet': '10.0.0.0/8',
            'interface': 'eth1',
            'prefixlen': 8,
            'family': 'ipv4',
            'server': 'valid',
            'interface_ip': '192.0.2.30',
            'prefix_length': 8,
            'address_family': 'ipv4',
        })
        diagnostics = '\n'.join(logs.output)
        self.assertIn("Interface 'missing' not found", diagnostics)
        self.assertIn('wrong-family', diagnostics)

    def test_structured_api_skips_malformed_interface_identifier(self):
        for malformed in (['eth0'], {'name': 'eth0'}):
            with self.subTest(malformed=malformed):
                servers = {
                    'server1': {
                        'management': {'routes': {'ipv4': [
                            {'subnet': '10.40.1.0/24',
                             'interface': malformed},
                            {'subnet': '10.40.0.0/16',
                             'interface': 'eth0'},
                        ]}},
                        'interfaces': {
                            'eth0': {'ipv4': '192.0.2.40/24'},
                        },
                    },
                }

                with self.assertLogs(
                        'genie.libs.sdk.apis.server_route_lookup',
                        'WARNING') as logs:
                    result = find_server_route_for_device_ip(
                        mock_device, '10.40.1.5', servers)

                self.assertEqual(result['subnet'], '10.40.0.0/16')
                self.assertEqual(result['server_ip'], '192.0.2.40')
                self.assertIn(
                    'malformed interface/next-hop', '\n'.join(logs.output))


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

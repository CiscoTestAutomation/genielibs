'''ACL Genie Ops Object Outputs for IOS'''


class AclOutput(object):

    ShowAccessLists = {
        "101": {
            "name": "101",
            "type": "ipv4-acl-type",
            "aces": {
                "10": {
                    "name": "10",
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "protocol": "ipv4",
                                "source_network": {
                                    "host 10.3.3.3": {
                                        "source_network": "host 10.3.3.3"
                                    }
                                },
                                "destination_network": {
                                    "host 10.5.5.34": {
                                        "destination_network": "host 10.5.5.34"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "ipv4": {
                                "established": False
                            }
                        }
                    }
                },
                "20": {
                    "name": "20",
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "icmp": {
                                "protocol": "icmp",
                                "source_network": {
                                    "any": {
                                        "source_network": "any"
                                    }
                                },
                                "destination_network": {
                                    "any": {
                                        "destination_network": "any"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "icmp": {
                                "established": False
                            }
                        }
                    }
                },
                "30": {
                    "name": "30",
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "protocol": "ipv4",
                                "source_network": {
                                    "host 10.34.2.2": {
                                        "source_network": "host 10.34.2.2"
                                    }
                                },
                                "destination_network": {
                                    "host 10.2.54.2": {
                                        "destination_network": "host 10.2.54.2"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "ipv4": {
                                "established": False
                            }
                        }
                    }
                },
                "40": {
                    "name": "40",
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-syslog"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "protocol": "ipv4",
                                "source_network": {
                                    "host 10.3.4.31": {
                                        "source_network": "host 10.3.4.31"
                                    }
                                },
                                "destination_network": {
                                    "host 10.3.32.3": {
                                        "destination_network": "host 10.3.32.3"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "ipv4": {
                                "established": False
                            }
                        }
                    }
                }
            }
        }
    }
    Acl_info = {
        'acls': {
            "101": {
                "name": "101",
                "type": "ipv4-acl-type",
                "aces": {
                    "10": {
                        "name": "10",
                        "actions": {
                            "forwarding": "permit",
                            "logging": "log-none"
                        },
                        "matches": {
                            "l3": {
                                "ipv4": {
                                    "protocol": "ipv4",
                                    "source_ipv4_network": {
                                        "host 10.3.3.3": {
                                            "source_ipv4_network": "host 10.3.3.3"
                                        }
                                    },
                                    "destination_ipv4_network": {
                                        "host 10.5.5.34": {
                                            "destination_ipv4_network": "host 10.5.5.34"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "20": {
                        "name": "20",
                        "actions": {
                            "forwarding": "permit",
                            "logging": "log-none"
                        }
                    },
                    "30": {
                        "name": "30",
                        "actions": {
                            "forwarding": "permit",
                            "logging": "log-none"
                        },
                        "matches": {
                            "l3": {
                                "ipv4": {
                                    "protocol": "ipv4",
                                    "source_ipv4_network": {
                                        "host 10.34.2.2": {
                                            "source_ipv4_network": "host 10.34.2.2"
                                        }
                                    },
                                    "destination_ipv4_network": {
                                        "host 10.2.54.2": {
                                            "destination_ipv4_network": "host 10.2.54.2"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "40": {
                        "name": "40",
                        "actions": {
                            "forwarding": "permit",
                            "logging": "log-syslog"
                        },
                        "matches": {
                            "l3": {
                                "ipv4": {
                                    "protocol": "ipv4",
                                    "source_ipv4_network": {
                                        "host 10.3.4.31": {
                                            "source_ipv4_network": "host 10.3.4.31"
                                        }
                                    },
                                    "destination_ipv4_network": {
                                        "host 10.3.32.3": {
                                            "destination_ipv4_network": "host 10.3.32.3"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

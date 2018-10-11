'''Dot1x Genie Ops Object Outputs for IOSXE.'''


class Dot1xOutput(object):

    ShowDot1xAllDetail = {
        "version": 3,
        "interfaces": {
          "GigabitEthernet1/0/9": {
               "interface": "GigabitEthernet1/0/9",
               "max_start": 3,
               "pae": "supplicant",
               "credentials": 'switch4',
               'supplicant': {
                    'eap': {
                        'profile': 'EAP-METH'
                    }
                },
               "timeout": {
                    "held_period": 60,
                    "start_period": 30,
                    "auth_period": 30
               }
            }
        },
        "system_auth_control": True
    }

    ShowDot1xAllStatistics = {
        "interfaces": {
            "GigabitEthernet1/0/9": {
               "interface": "GigabitEthernet1/0/9",
               "statistics": {
                    "txtotal": 3,
                    "rxreq": 0,
                    "txstart": 3,
                    "rxversion": 0,
                    "txlogoff": 0,
                    "rxinvalid": 0,
                    "rxlenerr": 0,
                    "lastrxsrcmac": "0000.0000.0000",
                    "rxtotal": 0,
                    "txresp": 0
               }
            }
        }
    }

    ShowDot1xAllSummary = {
        "interfaces": {
            "GigabitEthernet0/1": {
               "clients": {
                    "fa16.3ede.7048": {
                         "pae": "authenticator",
                         "status": "unauthorized",
                         "client": "fa16.3ede.7048"
                    },
                    "fa16.3ea5.663a": {
                         "pae": "authenticator",
                         "status": "authorized",
                         "client": "fa16.3ea5.663a"
                    },
                    "fa16.3ea5.663b": {
                         "pae": "supplicant",
                         "status": "authorized",
                         "client": "fa16.3ea5.663b"
                    },
                    "fa16.3ede.7049": {
                         "pae": "supplicant",
                         "status": "unauthorized",
                         "client": "fa16.3ede.7049"
                    }
               },
               "interface": "GigabitEthernet0/1"
            }
        }
    }

    ShowDot1xAllCount = {
        'sessions': {
            'authorized_clients': 0,
            'unauthorized_clients': 0,
            'total': 0,
        }
    }

    Dot1x_info = {
        "version": 3,
        "interfaces": {
            "GigabitEthernet1/0/9": {
                 "supplicant": {
                      "eap": {
                           "profile": "EAP-METH"
                      }
                 },
                 "credentials": "switch4",
                 "pae": "supplicant",
                 "max_start": 3,
                 "interface": "GigabitEthernet1/0/9",
                 "timeout": {
                      "auth_period": 30,
                      "start_period": 30,
                      "held_period": 60
                 },
                 "statistics": {
                      "rxinvalid": 0,
                      "rxtotal": 0,
                      "rxlenerr": 0,
                      "txresp": 0,
                      "txtotal": 3,
                      "txstart": 3,
                      "rxreq": 0,
                      "rxversion": 0,
                      "lastrxsrcmac": "0000.0000.0000",
                      "txlogoff": 0
                 }
            },
            "GigabitEthernet0/1": {
                 "clients": {
                      "fa16.3ea5.663b": {
                           "pae": "supplicant",
                           "client": "fa16.3ea5.663b",
                           "status": "authorized"
                      },
                      "fa16.3ede.7049": {
                           "pae": "supplicant",
                           "client": "fa16.3ede.7049",
                           "status": "unauthorized"
                      },
                      "fa16.3ede.7048": {
                           "pae": "authenticator",
                           "client": "fa16.3ede.7048",
                           "status": "unauthorized"
                      },
                      "fa16.3ea5.663a": {
                           "pae": "authenticator",
                           "client": "fa16.3ea5.663a",
                           "status": "authorized"
                      }
                 }
            }
        },
        "sessions": {
            "authorized_clients": 0,
            "unauthorized_clients": 0,
            "total": 0
        },
        "system_auth_control": True
    }

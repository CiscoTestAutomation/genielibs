
class PlatformOutput(object):

    # ==========================================================================
    #                               Sonic
    # ==========================================================================

    showVersion = {
        'sonic_os_version': 11,
        'sonic_software_version': 'SONiC.azure_cisco_tortuga_202305.10234-dirty-20240326.030556',
    }

    showVersion_ops_output = {
        'os': 11,
        'version': 'SONiC.azure_cisco_tortuga_202305.10234-dirty-20240326.030556', 
    }

    showPlatformInventory =  {
        "chassis": {
            "CHASSIS": {
                "description": "Cisco 8100 32x400G QSFPDD 1RU Fixed System w/o HBM, Open SW",
                "name": "CHASSIS",
                "product_id": "8101-32FH-O",
                "serial_num": "FLM25320591",
                "version": "0.41",
            }
        },
        "rp": {
            "RP0": {
                "description": "Cisco 8100 32x400G QSFPDD 1RU Fixed System w/o HBM, Open SW",
                "name": "RP0",
                "product_id": "8101-32FH-O",
                "serial_num": "FLM2528059A",
                "version": "0.41",
            }
        },
    }

    showPlatformInventory_ops_output = {
        "chassis": "8101-32FH-O",
        "chassis_sn": "FLM25320591",
        "slot": { 
            "rp": {
                "RP0": {
                    "name": "RP0",
                    "sn": "FLM2528059A"
                    }
                }
            },
        }

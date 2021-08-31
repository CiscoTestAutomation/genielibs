
class StageOutputs:

    execute_outputs = {
        'copy running-config startup-config': '''\
            PE1#copy running-config startup-config
            Destination filename [startup-config]?
            Building configuration...
            [OK]
        ''',

        'show boot': '''\
            starfleet-1#show boot
            BOOT variable = bootflash:/cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;
            Configuration Register is 0x102
            MANUAL_BOOT variable = no
            BAUD variable = 9600
            ENABLE_BREAK variable does not exist
            BOOTMODE variable does not exist
            IPXE_TIMEOUT variable does not exist
            CONFIG_FILE variable =
        ''',
    }


    parsed_outputs = {
        'show boot': {
            'active': 
                {'boot_variable': 'bootflash:/cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin;',
                'configuration_register': '0x102'}},
        'show version':
        {
        'version': {
        'bootldr_version': 'System Bootstrap, Version 17.3.1r[FC2], RELEASE SOFTWARE (P)',
        'chassis': 'C9500-24Y4C',
        'code_name': 'Amsterdam',
        'compiled_by': 'mcpre',
        'compiled_date': 'Fri 07-Aug-20 21:32',
        'disks': {
            'bootflash:': {
                'disk_size': '11161600',
            },
            'crashinfo:': {
                'disk_size': '1638400',
            },
        },
        'hostname': 'Switch',
        'image_id': 'CAT9K_IOSXE',
        "label": "RELEASE SOFTWARE (fc5)",
        'last_reload_reason': 'SMU Install',
        'license_level': 'AIR DNA Advantage',
        'mac_address': '00:a7:42:ff:bf:37',
        'main_mem': '2905019',
        'mb_assembly_num': '4874',
        'mb_rev_num': '1',
        'mb_sn': 'CAT2136L3NG',
        'mem_size': {
            'non_volatile_memory': '32768',
            'physical_memory': '16002876',
        },
        'model_num': 'C9500-24Y4C',
        'model_rev_num': 'V02',
        'next_reload_license_level': 'AIR DNA Advantage',
        'number_of_intfs': {
            'hundred_gigabit_ethernet_interfaces': '4',
        },
        'os': 'IOS-XE',
        'platform': 'Catalyst L3 Switch',
        'processor_board_id': 'CAT2136L3NG',
        'processor_type': 'X86',
        'returned_to_rom_by': 'SMU Install',
        'rom': 'IOS-XE ROMMON',
        'smart_licensing_status': 'REGISTERED/EVAL EXPIRED',
        'system_image': 'bootflash:/cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin',
        'system_sn': 'CAT2136L3NG',
        'uptime': '1 day, 3 hours, 39 minutes',
        'uptime_this_cp': '1 day, 3 hours, 41 minutes',
        'version': '17.3.1',
        'version_short': '17.3',
        'xe_version': '17.03.01',
    },
        },
        
    }

    config_outputs = {
        'no boot system bootflash:/cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin': '',
        'boot system bootflash:/cat9k_iosxe.BLD_V173_THROTTLE_LATEST_20200421_032634.SSA.bin': '',
        'config-register 0x2102': '',
    }


def get_execute_output(arg, **kwargs):
    '''Return the execute output of the given show command'''
    return StageOutputs.execute_outputs[arg]


def get_parsed_output(arg, **kwargs):
    '''Return the parsed output of the given show command '''
    return StageOutputs.parsed_outputs[arg]


def get_config_output(arg, **kwargs):
    '''Return the out of the given config string'''
    return StageOutputs.config_outputs[arg]

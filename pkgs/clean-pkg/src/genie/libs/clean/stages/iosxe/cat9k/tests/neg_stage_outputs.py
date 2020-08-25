
class StageOutputs:

    execute_outputs = {
        # Outputs from public Cisco docs:
        # https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/asr1k_rn_rel_notes/asr1k_rn_sys_req.html

        'copy running-config startup-config': '''\
            PE1#copy running-config startup-config
            Destination filename [startup-config]?
            %Error opening bootflash:running-config (Permission denied)
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
                'configuration_register': '0x102'}}
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

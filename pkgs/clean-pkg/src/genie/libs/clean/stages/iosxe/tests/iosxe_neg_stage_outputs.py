
class StageOutputs:

    connect = '''\
        Trying 1.1.1.1...
        Connected to 1.1.1.1.
        Escape character is '^]'.

        Location: 163_88_9

        PE1#
    '''

    ping_server = '''\
        PE1# ping vrf Mgmt-intf
        Protocol [ip]:
        Target IP address: 20.1.1.1
        Repeat count [5]:
        Datagram size [100]:
        Timeout in seconds [2]:
        Extended commands [n]: n
        Sweep range of sizes [n]: n
        Type escape sequence to abort.
        Sending 5, 100-byte ICMP Echos to 20.1.1.1, timeout is 2 seconds:
        .....
        Success rate is 0 percent (0/5)
    '''

    write_erase = '''\
        PE1#write erase
        Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]x
        File system erase is not confirmed or Could not be completed
    '''

    reload_output = '''\
    '''

    reload_connect = '''\
        Trying 1.1.1.1...
        Connected to 1.1.1.1.
        Escape character is '^]'.

        Location: 163_88_9

        Router#
    '''

    execute_outputs = {
        # Outputs from public Cisco docs:
        # https://www.cisco.com/c/en/us/td/docs/routers/asr1000/release/notes/asr1k_rn_rel_notes/asr1k_rn_sys_req.html

        'copy running-config startup-config': '''\
            PE1#copy running-config startup-config
            Destination filename [startup-config]?
            %Error opening bootflash:running-config (Permission denied)
        ''',

        'show bootvar': '''\
            PE1#show bootvar
            BOOT variable = harddisk:/vmlinux_PE1.bin,12;
            CONFIG_FILE variable =
            BOOTLDR variable does not exist
            Configuration register is 0x2102

            Standby not ready to show bootvar
        ''',

        'dir harddisk:/': '''\
            PE1#dir harddisk:
            Directory of harddisk:/

               11  drwx            16384   May 8 2011 09:51:48 +00:00  lost+found
            8503297  drwx            53248  Apr 25 2018 21:02:11 +00:00  tracelogs
            4882433  drwx             4096  Apr 20 2018 19:38:15 +00:00  core
               12  -rw-        989519758  Nov 12 2013 23:32:18 +00:00  vmlinux_PE1.bin
               13  -rw-             1847  Nov 14 2013 01:21:53 +00:00  golden_config
               14  -rw-             1847  Feb 23 2018 22:18:39 +00:00  default_config
            5373953  drwx             4096  Apr 20 2018 19:37:19 +00:00  virtual-instance
               16  -rw-        450610592   Feb 6 2018 19:28:15 +00:00  config_backup
               17  -rw-        989519758  Apr 20 2018 19:28:40 +00:00  latest_image.bin
               15  -rw-        450610592  Apr 14 2018 14:00:37 +00:00  another_image.bin

            78704144384 bytes total (72358244352 bytes free)
        ''',

        'copy ftp://20.1.1.1//auto/path/images/vmlinux_PE1.bin harddisk:/vmlinux_PE1.bin': '''\
            PE1#copy ftp://20.1.1.1//auto/path/images/vmlinux_PE1.bin harddisk:/vmlinux_PE1.bin
            Destination filename [vmlinux_PE1.bin]?
            Accessing ftp://20.1.1.1//auto/path/images/vmlinux_PE1.bin...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            [OK - 989519758/4096 bytes]

            989519758 bytes copied in 198.784 secs (4977864 bytes/sec)
        ''',
    }

    parsed_outputs = {
        'show version': {
            'version': 
                {'chassis': 'ASR1006',
                'chassis_sn': 'FOX1444GPWD',
                'compiled_by': 'mcpre',
                'compiled_date': 'Thu 30-Jan-20 18:53',
                'curr_config_register': '0x2102',
                'disks': 
                    {'bootflash:.': 
                        {'disk_size': '1933311',
                        'type_of_disk': 'eUSB flash'},
                    'harddisk:.': 
                        {'disk_size': '78085207',
                        'type_of_disk': 'SATA hard disk'},
                    'webui:.': 
                        {'disk_size': '0',
                        'type_of_disk': 'WebUI ODM Files'}},
                'hostname': 'PE1',
                'image_id': 'X86_64_LINUX_IOSD-UNIVERSALK9-M',
                'image_type': 'production image',
                'last_reload_reason': 'Reload Command',
                'license_level': 'advipservices',
                'license_type': 'EvalRightToUse',
                'main_mem': '4262644',
                'mem_size': {'non-volatile configuration': '32768',
                          'physical': '8388608'},
                'next_reload_license_level': 'advipservices',
                'number_of_intfs': {'Gigabit Ethernet': '8'},
                'os': 'IOS-XE',
                'platform': 'ASR1000',
                'processor_type': 'RP2',
                'returned_to_rom_by': 'Reload Command',
                'rom': 'IOS-XE ROMMON',
                'rtr_type': 'ASR1K',
                'system_image': 'harddisk:/another_image.bin',
                'uptime': '22 hours, 11 minutes',
                'uptime_this_cp': '22 hours, 13 minutes',
                'version': '16.9.5',
                'version_short': '16.9'}},

        'show bootvar': {
            'active': 
                {'boot_variable': 'harddisk:/vmlinux_PE1.bin,12',
                'configuration_register': '0x2102'},
            'next_reload_boot_variable': 'harddisk:/vmlinux_PE1.bin,12'},

        'dir harddisk:/': {
            'dir':
                {'dir': 'harddisk:/',
                'harddisk:/':
                    {'bytes_free': '72358240256',
                    'bytes_total': '78704144384',
                    'files':
                        {'vmlinux_PE1.bin':
                            {'index': '12',
                            'last_modified_date': 'Nov 12 2013 23:32:18 +00:00',
                            'permissions': '-rw-',
                            'size': '989519758'},
                        'config_backup':
                            {'index': '16',
                            'last_modified_date': 'Feb 6 2018 19:28:15 +00:00',
                            'permissions': '-rw-',
                            'size': '450610592'},
                        'another_image.bin':
                            {'index': '15',
                            'last_modified_date': 'Apr 14 2018 14:00:37 +00:00',
                            'permissions': '-rw-',
                            'size': '450610592'},
                        'core':
                            {'index': '4882433',
                            'last_modified_date': 'Apr 20 2018 19:38:15 +00:00',
                            'permissions': 'drwx',
                            'size': '4096'},
                        'default_config':
                            {'index': '14',
                            'last_modified_date': 'Feb 23 2018 22:18:39 +00:00',
                            'permissions': '-rw-',
                            'size': '1847'},
                        'latest_image.bin':
                            {'index': '17',
                            'last_modified_date': 'Apr 20 2018 19:28:40 +00:00',
                            'permissions': '-rw-',
                            'size': '989519758'},
                        'golden_config':
                            {'index': '13',
                            'last_modified_date': 'Nov 14 2013 01:21:53 +00:00',
                            'permissions': '-rw-',
                            'size': '1847'},
                        'lost+found':
                            {'index': '11',
                            'last_modified_date': 'May 8 2011 09:51:48 +00:00',
                            'permissions': 'drwx',
                            'size': '16384'},
                        'tracelogs':
                            {'index': '8503297',
                            'last_modified_date': 'Apr 25 2018 21:07:19 +00:00',
                            'permissions': 'drwx',
                            'size': '53248'},
                        'virtual-instance':
                            {'index': '5373953',
                            'last_modified_date': 'Apr 20 2018 19:37:19 +00:00',
                            'permissions': 'drwx',
                            'size': '4096'}}}}},
    }

    config_outputs = {
        'no boot system harddisk:/vmlinux_PE1.bin': '',
        'boot system harddisk:/vmlinux_PE1.bin': '',
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

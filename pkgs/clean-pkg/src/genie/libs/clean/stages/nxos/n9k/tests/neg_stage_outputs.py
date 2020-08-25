
class StageOutputs:

    connect = '''\
        Trying 1.1.1.1...
        Connected to 1.1.1.1.
        Escape character is '^]'.

        N95#
    '''

    ping_server = '''\
        N95# ping
        Vrf context to use [default] :management
        Target IP address or Hostname: 20.1.1.1
        Repeat count [5] :
        Packet-size [56] :
        Timeout in seconds [2] :
        Sending interval in seconds [0] :
        Extended commands [no] :
        Sweep range of sizes [no] :
        Sending 5, 56-bytes ICMP Echos to 20.1.1.1
        Timeout is 2 seconds, data pattern is 0xABCD

        U.U.U.U.U.
        --- 20.1.1.1 ping statistics ---
        5 packets transmitted, 0 packets received, 100.00% packet loss
    '''

    write_erase = '''\
        N95# write erase
        Warning: This command will erase the startup-configuration.
        Do you wish to proceed anyway? (y/n)  [n] n
    '''

    reload_output = '''\
    '''

    reload_connect = '''\
        Trying 1.1.1.1...
        Connected to 1.1.1.1.
        Escape character is '^]'.

        switch#
    '''

    execute_outputs = {
        # Outputs from public Cisco docs:
        # https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/release/notes/70371_nxos_rn.html

        'copy running-config startup-config': '''\
            N95# copy running-config startup-config
            copy: cannot access file '/bootflash/running-config'
        ''',

        'show boot': '''\
            Current Boot Variables:
            sup-1
            NXOS variable = bootflash:nxos.9.3.1_N95.bin
            Boot POAP Disabled

            Boot Variables on next reload:
            sup-1
            NXOS variable = bootflash:nxos.9.3.1_N95.bin
            Boot POAP Disabled
        ''',

        'dir bootflash:/': '''\
            N95# dir bootflash:
                   4096    Oct 23 17:45:01 2019  .rpmstore/
                   4096    Jan 11 04:41:27 2020  .swtam/
                      0    Jan 31 05:50:53 2020  bootflash_sync_list
                   2621    Jan 31 06:20:04 2020  golden_config
                   4096    Jan 30 05:40:05 2020  home/
             1513778688    Apr 06 21:32:17 2020  nxos.9.3.1_N95.bin
                      0    Jan 31 05:56:39 2020  platform-sdk.cmd
                   1967    Feb 07 03:06:30 2020  poap_retry_debugs.log
                   4096    Jan 11 04:42:12 2020  scripts/
                     52    Apr 27 06:51:59 2020  test_copy.txt
                     52    Apr 27 06:47:22 2020  test_copy_N95.txt
                 562326    Mar 12 01:16:43 2020  ts-pack-pnp.ts
                   4096    Oct 23 15:11:30 2019  virtual-instance/

            Usage for bootflash://sup-local
            12296761344 bytes used
            39473545216 bytes free
            51770306560 bytes total
        ''',

        'copy ftp://20.1.1.1//auto/path/images/nxos.9.3.1_N95.bin bootflash:/nxos.9.3.1_N95.bin vrf management': '''\
            N95#copy ftp://20.1.1.1//auto/path/images/nxos.9.3.1.bin bootflash:nxos.9.3.1_N95.bin vrf management
                ***** Transfer of file Completed Successfully *****
            Copy complete, now saving to disk (please wait)...
            Copy complete.
        ''',
    }

    parsed_outputs = {
        'show version': {
            'platform': 
                {'hardware': 
                    {'bootflash': '20971520 kB',
                    'chassis': 'Nexus9000 C9516',
                    'cpu': 'Intel(R) Xeon(R) CPU E5-2403 0 @ 1.80GHz',
                    'device_name': 'switch',
                    'memory': '16401664 kB',
                    'model': 'Nexus9000 C9516',
                    'processor_board_id': 'SAL1745FTPW',
                    'rp': 'Supervisor Module',
                    'slots': '16'},
                'kernel_uptime':
                    {'days': 0,
                    'hours': 0,
                    'minutes': 8,
                    'seconds': 13},
                'name': 'Nexus',
                'os': 'NX-OS',
                'reason': 'Reset due to upgrade',
                'software': 
                    {'bios_compile_time': '06/12/2016',
                    'bios_version': '08.26',
                    'system_compile_time': '2/8/2016 20:00:00 [02/09/2016 05:18:17]',
                    'system_image_file': 'bootflash:nxos.9.2.2.bin',
                    'system_version': '7.0(3)I7(1)'}}},

        'show boot': {
            'current_boot_variable':
                {'sup_number': 
                    {'sup-1':
                        {'boot_poap': 'Disabled',
                        'system_variable': 'bootflash:nxos.9.3.1_N95.bin'}}},
            'next_reload_boot_variable':
                {'sup_number':
                    {'sup-1':
                        {'boot_poap': 'Disabled',
                        'system_variable': 'bootflash:nxos.9.3.1_N95.bin'}}}},

        'dir bootflash:/': {
            'dir': 'bootflash:',
            'disk_free_space': '39473545216',
            'disk_total_space': '51770306560',
            'disk_used_space': '12296761344',
            'files':
                {'.rpmstore/':
                    {'date': 'Oct 23 2019',
                    'size': '4096',
                    'time': '17:45:01'},
                '.swtam/':
                    {'date': 'Jan 11 2020',
                    'size': '4096',
                    'time': '04:41:27'},
                'bootflash_sync_list':
                    {'date': 'Jan 31 2020',
                    'size': '0',
                    'time': '05:50:53'},
                'golden_config':
                    {'date': 'Jan 31 2020',
                    'size': '2621',
                    'time': '06:20:04'},
                'home/':
                    {'date': 'Jan 30 2020', 'size': '4096', 'time': '05:40:05'},
                'nxos.9.3.1_N95.bin':
                    {'date': 'Apr 06 2020',
                    'size': '1513778688',
                    'time': '21:32:17'},
                'platform-sdk.cmd':
                    {'date': 'Jan 31 2020',
                    'size': '0',
                    'time': '05:56:39'},
                'poap_retry_debugs.log':
                    {'date': 'Feb 07 2020',
                    'size': '1967',
                    'time': '03:06:30'},
                'scripts/':
                    {'date': 'Jan 11 2020',
                    'size': '4096',
                    'time': '04:42:12'},
                'test_copy.txt':
                    {'date': 'Apr 27 2020',
                    'size': '52',
                    'time': '06:51:59'},
                'test_copy_N95.txt':  
                    {'date': 'Apr 27 2020',
                    'size': '52',
                    'time': '06:47:22'},
                'ts-pack-pnp.ts':
                    {'date': 'Mar 12 2020',
                    'size': '562326',
                    'time': '01:16:43'},
                'virtual-instance/':
                    {'date': 'Oct 23 2019',
                    'size': '4096',
                    'time': '15:11:30'}}},
    }

    config_outputs = {
        'boot nxos bootflash:nxos.9.3.1_N95.bin': '',
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

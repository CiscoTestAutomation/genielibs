
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
        !!!!!
        Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms
    '''

    write_erase = '''\
        PE1#write erase
        Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]
        [OK]
        Erase of nvram: complete
    '''

    reload_output = '''\
        reload

        Proceed with reload? [confirm]

        Feb  2 16:00:34.751 R0/0: %PMAN-5-EXITACTION: Process manager is exiting: process exit with reload chassis code


        Initializing Hardware ...

        Calculating the ROMMON CRC ... CRC is correct

        System Bootstrap, Version 16.9(4r), RELEASE SOFTWARE

        Copyright (c) 1994-2018  by cisco Systems, Inc.


        Current image running: Boot ROM1


        Last reset cause: LocalSoft


        ASR1000-RP2 platform with 8388608 Kbytes of main memory

        File size is 0x1adbc5a0

        Located genie-iedge-asr-uut

        Image size 450610592 inode num 15, bks cnt 110013 blk size 8*512

        ####################################################################

        Boot image size = 450610592 (0x1adbc5a0) bytes



        Package header rev 0 structure detected

        Calculating SHA-1 hash...done

        validate_package_cs: SHA-1 hash:

            calculated 253ebb07:78c5e6a9:bc629ab6:49357652:f85bba69

            expected   253ebb07:78c5e6a9:bc629ab6:49357652:f85bba69

        Validating main package signatures

        Codesigning information not present, continuing

        Image validated

        IOSXEBOOT-4-BOOT_SRC: (rp/0): HD Boot



                      Restricted Rights Legend



        Use, duplication, or disclosure by the Government is

        subject to restrictions as set forth in subparagraph

        (c) of the Commercial Computer Software - Restricted

        Rights clause at FAR sec. 52.227-19 and subparagraph

        (c) (1) (ii) of the Rights in Technical Data and Computer

        Software clause at DFARS sec. 252.227-7013.



                   cisco Systems, Inc.

                   170 West Tasman Drive

                   San Jose, California 95134-1706







        Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVIPSERVICES-M), Experimental Version 15.2(20111205:144803) [mcp_dev-baljanak-mcp_dumb_patch2 201]

        Copyright (c) 1986-2012 by Cisco Systems, Inc.

        Compiled Tue 10-Jan-12 13:05 by baljanak







        Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.

        All rights reserved.  Certain components of Cisco IOS-XE software are

        licensed under the GNU General Public License ("GPL") Version 2.0.  The

        software code licensed under GPL Version 2.0 is free software that comes

        with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such

        GPL code under the terms of GPL Version 2.0.  For more details, see the

        documentation or "License Notice" file accompanying the IOS-XE software,

        or the applicable URL provided on the flyer accompanying the IOS-XE

        software.





         failed to initialize nvram

        cisco ASR1006 (RP2) processor with 4263538K/6147K bytes of memory.

        Processor board ID FOX1444GPWD

        8 Gigabit Ethernet interfaces

        32768K bytes of non-volatile configuration memory.

        8388608K bytes of physical memory.

        1933311K bytes of eUSB flash at bootflash:.

        78085207K bytes of SATA hard disk at harddisk:.






                 --- System Configuration Dialog ---



        Would you like to enter the initial configuration dialog? [yes/no]: n



        Press RETURN to get started!


        *Feb  2 16:05:05.681: %IOSXE_RP_NV-3-NV_ACCESS_FAIL: Initial read of NVRAM contents failed

        *Feb  2 16:05:10.275: %SPANTREE-5-EXTENDED_SYSID: Extended SysId enabled for type vlan

        *Feb  2 16:05:10.524: %LINK-3-UPDOWN: Interface Lsmpi0, changed state to up

        *Feb  2 16:05:10.524: %LINK-3-UPDOWN: Interface EOBC0, changed state to up

        *Feb  2 16:05:10.524: %LINEPROTO-5-UPDOWN: Line protocol on Interface VoIP-Null0, changed state to up

        *Feb  2 16:05:11.098: %IOSXE_MGMTVRF-6-CREATE_SUCCESS_INFO: Management vrf Mgmt-intf created with ID 1, ipv4 table-id 0x1, ipv6 table-id 0x1E000001

        *Feb  2 16:05:11.150: %LINK-3-UPDOWN: Interface GigabitEthernet0, changed state to down

        *Feb  2 16:05:11.150: %LINK-3-UPDOWN: Interface LIIN0, changed state to up

        *Feb  2 16:05:11.320: %DYNCMD-7-CMDSET_LOADED: The Dynamic Command set has been loaded from the Shell Manager

        *Feb  2 16:05:11.415: %DYNCMD-7-PKGINT_INSTALLED: The command package 'platform_trace' has been succesfully installed

        *

        Router>enable
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

        'show version': '''\
            PE1# show version

            Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Version 15.2(1)S, RELEASE SOFTWARE (fc1)
            Technical Support: http://www.cisco.com/techsupport
            Copyright (c) 1986-2011 by Cisco Systems, Inc.
            Compiled Sun 27-Nov-11 21:19 by mcpre

            Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
            All rights reserved. Certain components of Cisco IOS-XE software are
            licensed under the GNU General Public License ("GPL") Version 2.0. The
            software code licensed under GPL Version 2.0 is free software that comes
            with ABSOLUTELY NO WARRANTY. You can redistribute and/or modify such
            GPL code under the terms of GPL Version 2.0. For more details, see the
            documentation or "License Notice" file accompanying the IOS-XE software,
            or the applicable URL provided on the flyer accompanying the IOS-XE
            software.


            ROM: IOS-XE ROMMON

            PE1 uptime is 1 minute
            Uptime for this control processor is 3 minutes
            System returned to ROM by reload
            System restarted at 22:07:05 UTC Sun Nov 27 2011
            System image file is "tftp:/auto/tftp-smoke2/mcpdt-rp2-14/vmlinux"
            Last reload reason: PowerOn

            This product contains cryptographic features and is subject to United
            States and local country laws governing import, export, transfer and
            use. Delivery of Cisco cryptographic products does not imply
            third-party authority to import, export, distribute or use encryption.
            Importers, exporters, distributors and users are responsible for
            compliance with U.S. and local country laws. By using this product you
            agree to comply with applicable laws and regulations. If you are unable
            to comply with U.S. and local laws, return this product immediately.

            A summary of U.S. laws governing Cisco cryptographic products may be found at:
            http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

            If you require further assistance please contact us by sending email to
            export@cisco.com.

            cisco ASR1006 (RP2) processor with 4252282K/6147K bytes of memory.
            5 Gigabit Ethernet interfaces
            2 Channelized T3 ports
            32768K bytes of non-volatile configuration memory.
            8388608K bytes of physical memory.
            1925119K bytes of eUSB flash at bootflash:.
            78085207K bytes of SATA hard disk at harddisk:.

            Configuration register is 0x2102
        ''',

        'show platform': '''\
            PE1#show platform
            Chassis type: ASR1006

            Slot      Type                State                 Insert time (ago)
            --------- ------------------- --------------------- -----------------
            0         ASR1000-SIP40       ok                    2d05h
            0/0       SPA-8X1GE-V2        ok                    2d05h
            R0        ASR1000-RP2         ok, active            2d05h
            R1                            standby               2d05h
            F0        ASR1000-ESP20       ok, active            2d05h
            P0        ASR1006-PWR-AC      ps, ok.               2d05h
            P1        ASR1006-PWR-AC      ok                    2d05h

            Slot      CPLD Version        Firmware Version
            --------- ------------------- ---------------------------------------
            0         00200900            16.2(1r)
            R0        10021901            16.9(4r)
            R1        N/A                 N/A
            F0        08041102            16.2(1r)
        ''',

        'copy running-config startup-config': '''\
            PE1#copy running-config startup-config
            Destination filename [startup-config]?
            Building configuration...
            [OK]
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

        'copy ftp://rcpuser:password@20.1.1.1/vmlinux_PE1.bin harddisk:/vmlinux_PE1.bin': '''\
            PE1#copy ftp://20.1.1.1/vmlinux_PE1.bin harddisk:/vmlinux_PE1.bin
            Destination filename [vmlinux_PE1.bin]?
            Accessing ftp://20.1.1.1/vmlinux_PE1.bin...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            [OK - 989519758/4096 bytes]

            989519758 bytes copied in 198.784 secs (4977864 bytes/sec)
        ''',
    }

    parsed_outputs = {
        'show platform': {
            'main':
                {'chassis': 'ASR1006'},
                'slot':
                    {'0':
                        {'lc':
                            {'ASR1000-SIP40':
                                {'cpld_ver': '00200900',
                                'fw_ver': '16.2(1r)',
                                'insert_time': '00:32:18',
                                'name': 'ASR1000-SIP40',
                                'slot': '0',
                                'state': 'ok',
                                'subslot':
                                    {'0':
                                        {'SPA-8X1GE-V2':
                                            {'insert_time': '00:30:32',
                                            'name': 'SPA-8X1GE-V2',
                                            'state': 'ok',
                                            'subslot': '0'}}}}}},
                    'F0':
                        {'other':
                            {'ASR1000-ESP20':
                                {'cpld_ver': '08041102',
                                'fw_ver': '16.2(1r)',
                                'insert_time': '00:32:18',
                                'name': 'ASR1000-ESP20',
                                'slot': 'F0',
                                'state': 'ok, active'}}},
                    'P0':
                        {'other':
                            {'ASR1006-PWR-AC':
                                {'insert_time': '00:31:22',
                                'name': 'ASR1006-PWR-AC',
                                'slot': 'P0',
                                'state': 'ps, ok'}}},
                    'P1':
                        {'other':
                            {'ASR1006-PWR-AC':
                                {'insert_time': '00:31:21',
                                'name': 'ASR1006-PWR-AC',
                                'slot': 'P1',
                                'state': 'ok'}}},
                    'R0':
                        {'rp':
                            {'ASR1000-RP2':
                                {'cpld_ver': '10021901',
                                'fw_ver': '16.9(4r)',
                                'insert_time': '00:32:18',
                                'name': 'ASR1000-RP2',
                                'slot': 'R0',
                                'state': 'ok, active'}}},
                    'R1':
                        {'other':
                            {'':
                                {'cpld_ver': 'N/A',
                                'fw_ver': 'N/A',
                                'insert_time': '00:32:18',
                                'name': '',
                                'slot': 'R1',
                                'state': 'standby'}}}}},

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
                'system_image': 'harddisk:/vmlinux_PE1.bin',
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

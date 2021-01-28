
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

        64 bytes from 20.1.1.1: icmp_seq=0 ttl=62 time=1.547 ms
        64 bytes from 20.1.1.1: icmp_seq=1 ttl=62 time=0.734 ms
        64 bytes from 20.1.1.1: icmp_seq=2 ttl=62 time=0.953 ms
        64 bytes from 20.1.1.1: icmp_seq=3 ttl=62 time=0.714 ms
        64 bytes from 20.1.1.1: icmp_seq=4 ttl=62 time=0.666 ms

        --- 20.1.1.1 ping statistics ---
        5 packets transmitted, 5 packets received, 0.00% packet loss
        round-trip min/avg/max = 0.666/0.922/1.547 ms
    '''

    write_erase = '''\
        N95# write erase
        Warning: This command will erase the startup-configuration.
        Do you wish to proceed anyway? (y/n)  [n] y
    '''

    reload_output = '''\
        N95# reload
        This command will reboot the system. (y/n)?  [n] y

        CISCO SWITCH Ver 8.17

        CISCO SWITCH Ver 8.17
        Memory Size (Bytes): 0x0000000080000000 + 0x0000000380000000
         Relocated to memory
        Time: 4/29/2020  0:21:10
        Detected CISCO IOFPGA
        Booting from Primary Bios
        Code Signing Results: 0x0
        Using Upgrade FPGA
        FPGA Revison        : 0x22
        FPGA ID             : 0x1168153
        FPGA Date           : 0x20140915
        Reset Cause Register: 0x20
        Boot Ctrl Register  : 0x60ff
        EventLog  Register1 : 0x2000000
        EventLog  Register2 : 0xfbc77fff
        Version 2.16.1240. Copyright (C) 2013 American Megatrends, Inc.
        Board type  1
        IOFPGA @ 0xe8000000
        SLOT_ID @ 0x1b
        check_bootmode: grub: Continue grub
        Trying to read config file /boot/grub/menu.lst.local from (hd0,4)
         Filesystem type is ext2fs, partition type 0x83

        Booting bootflash:/nxos.9.3.1_N95.bin ...
        Booting bootflash:/nxos.9.3.1_N95.bin
        Trying diskboot
         Filesystem type is ext2fs, partition type 0x83
        IOFPGA ID: 1168153
        Image valid


        Image Signature verification was Successful.

        Boot Time: 4/29/2020  0:21:40
        Installing klm_card_index
        done
        Linking n9k flash devices
        creating flash devices BOOT_DEV= sda
        INIT: version 2.88 booting
        Installing ata_piix module ... done.
        Unsquashing rootfs ...
        Total size needed in bootflash is 105616
        check bootflash : OK
        Total size needed in bootflash is 40872
        check bootflash : OK
        Enabling 8250 serial driver spurious INTs workaround
        Installing isan procfs ... done.
        is_lxc: is_stby: suffix:
        Installing ftrace in non-lxc mode done
        Installing SSE module ... done.
        Creating SSE device node 247 ... done.
        Loading I2C driver ... done.
        Loading MEM scrub driver ... done.
        Installing CCTRL driver for card_type 3 without NEED_GEM ... done.
        old data: 4000004 new data: 1
        Loading IGB driver ... done.
        Checking SSD firmware ...
            Model Number:       Micron_M550_MTFDDAT064MAY
            Serial Number:      MSA19270649
            Firmware Revision:  MU01

        Checking all filesystems.
        Extracting rpms from image...
        2089841 blocks
        /etc/rc.d/rcS.d/S08setup-crdcfgdata: line 131: [: too many arguments
        Installing SPROM driver ... IS_N9K done.
        CORTINA-SUPInstalling pfmsvcs module ...done.
        Installing nvram module ... done.
        Installing if_index module with port mode 6 ... done.
        Installing fcfwd
        Installing RNI lcnd ... done.
        Installing lcnd ... done.
        Installing psdev ...
        Installing veobc module ... done.
        Checking SR card
        Card Index is 21000
        Inserting eMMC module ...
        Inserting mtdphysmap module...Inserting OBFL module ... done.
        Making OBFL character devices
        mounting plog for N9k!
        Mounting OBFL pstore for mtd
        Inserting kernel_services module ... done.
        Making kernel_services character devices
        cgroups initialized
         Removing any system startup links for cgroups-init ...
         Adding system startup for /etc/init.d/cgroups-init.
         Removing any system startup links for docker ...
        Running groupadd commands...
        NOTE: docker: Performing groupadd with [ -r docker]
        Running useradd commands...
        NOTE: docker: Performing useradd with [ -r -U -s /bin/false dockremap]
        update-alternatives: Linking /bin/vi to /usr/bin/vim.vim
        update-alternatives: Linking /usr/bin/vim to /usr/bin/vim.vim
        exit code: 1
        Starting OpenBSD Secure Shell server: sshd ... done.
        tune2fs 1.42.9 (28-Dec-2013)
        Setting reserved blocks percentage to 0% (0 blocks)
        Starting portmap daemon...
        creating NFS state directory: done
        starting 8 nfsd kernel threads: done
        starting mountd: done
        starting statd: done
        Saving image for img-sync ...
        Loading system software
        Installing local RPMS
        Patch Repository Setup completed successfully
        Creating /dev/mcelog
        Starting mcelog daemon
        INIT: Entering runlevel: 3
        Running S93thirdparty-script...

        done
        Netbroker support IS present in the kernel.
        done
        Executing Prune clis.
        Apr 29 00:22:52 %FW_APP-2-FIRMWARE_IMAGE_LOAD_SUCCESS No Firmware needed for Non SR card.
        2020 Apr 29 00:23:01  %$ VDC-1 %$  %USER-2-SYSTEM_MSG: <<%USBHSD-2-MOUNT>> logflash: online  - usbhsd
        2020 Apr 29 00:23:06  %$ VDC-1 %$ netstack: Registration with cli server complete
        2020 Apr 29 00:23:25  %$ VDC-1 %$ %USER-2-SYSTEM_MSG: ssnmgr_app_init called on ssnmgr up - aclmgr
        2020 Apr 29 00:23:35  %$ VDC-1 %$ %USER-0-SYSTEM_MSG: end of default policer - copp
        2020 Apr 29 00:23:35  %$ VDC-1 %$ %COPP-2-COPP_NO_POLICY: Control-plane is unprotected.
        2020 Apr 29 00:23:39  %$ VDC-1 %$ %CARDCLIENT-2-FPGA_BOOT_PRIMARY: IOFPGA booted from Primary
        Waiting for system online status before starting POAP ...
        2020 Apr 29 00:23:46  %$ VDC-1 %$ %VDC_MGR-2-VDC_ONLINE: vdc 1 has come online
        Waiting for system online status before starting POAP ...
        Waiting for system online status before starting POAP ...
        Waiting for system online status before starting POAP ...
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 1
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 22
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 24
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 26
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 29
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-MOD_PRESENT: Detected the presence of Module 30
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-PS_OK: Power supply 1 ok (Serial number DTM19300390)
        2020 Apr 29 00:25:20 switch %$ VDC-1 %$ %PLATFORM-2-PS_FANOK: Fan in Power supply 1 ok
        Waiting for system online status before starting POAP ...
        Waiting for system online status before starting POAP ...
        Waiting for system online status before starting POAP ...
        Waiting for system online status before starting POAP ...
        2020 Apr 29 00:27:55 switch %$ VDC-1 %$ %ASCII-CFG-2-CONF_CONTROL: System ready
        Starting Auto Provisioning ...
        Note: PnP is a day-0 feature and should not be enabled post day-0 using cli by users.
        2020 Apr 29 00:27:58 switch %$ VDC-1 %$ %POAP-2-POAP_INITED: [FOX1925G3ZC-E8:65:49:94:98:FF] - POAP process initialized
        Done

        Abort Power On Auto Provisioning [yes - continue with normal setup, skip - bypass password and basic configuration, no - continue with Power On Auto Provisioning] (yes/skip/no)[no]: yes

        2020 Apr 29 00:29:44 switch %$ VDC-1 %$ %POAP-2-POAP_FAILURE: [FOX1925G3ZC-E8:65:49:94:98:FF] - POAP DHCP discover phase failed
        2020 Apr 29 00:29:46 switch %$ VDC-1 %$ %POAP-2-POAP_INFO:   - Abort Power On Auto Provisioning [yes - continue with normal setup, skip - bypass password and basic configuration, no - continue with Power On Auto Provisioning] (yes/skip/no)[no]:
        Disabling POAP.......Disabling POAP
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ %POAP-2-POAP_INFO: [FOX1925G3ZC-E8:65:49:94:98:FF] - USB Initializing Success
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ %POAP-2-POAP_INFO: [FOX1925G3ZC-E8:65:49:94:98:FF] - USB disk not detected
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ last message repeated 1 time
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ %POAP-2-POAP_INFO: [FOX1925G3ZC-E8:65:49:94:98:FF] - Start DHCP v4 session
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ %POAP-2-POAP_DHCP_DISCOVER_START: [FOX1925G3ZC-E8:65:49:94:98:FF] - POAP DHCP Discover phase started
        2020 Apr 29 00:29:49 switch %$ VDC-1 %$ %POAP-2-POAP_INFO:   - Abort Power On Auto Provisioning [yes - continue with normal setup, skip - bypass password and basic configuration, no - continue with Power On Auto Provisioning] (yes/skip/no)[no]:
        2020 Apr 29 00:29:53 switch %$ VDC-1 %$ poap: Rolling back, please wait... (This may take 5-15 minutes)

                 ---- System Admin Account Setup ----


        Do you want to enforce secure password standard (yes/no) [y]:

          Enter the password for "admin":
          Confirm the password for "admin":

                 ---- Basic System Configuration Dialog VDC: 1 ----

        This setup utility will guide you through the basic configuration of
        the system. Setup configures only enough connectivity for management
        of the system.

        Please register Cisco Nexus9000 Family devices promptly with your
        supplier. Failure to register may affect response times for initial
        service calls. Nexus9000 devices must be registered to receive
        entitled support services.

        Press Enter at anytime to skip a dialog. Use ctrl-c at anytime
        to skip the remaining dialogs.

         Would you like to enter the basic configuration dialog (yes/no): no

        2020 Apr 29 00:30:28 switch %$ VDC-1 %$ %COPP-2-COPP_POLICY: Control-Plane is protected with policy copp-system-p-policy-strict.

        User Access Verification
        switch login: admin
        Password:

        Cisco Nexus Operating System (NX-OS) Software
        TAC support: http://www.cisco.com/tac
        Copyright (C) 2002-2019, Cisco and/or its affiliates.
        All rights reserved.
        The copyrights to certain works contained in this software are
        owned by other third parties and used and distributed under their own
        licenses, such as open source.  This software is provided "as is," and unless
        otherwise stated, there is no warranty, express or implied, including but not
        limited to warranties of merchantability and fitness for a particular purpose.
        Certain components of this software are licensed under
        the GNU General Public License (GPL) version 2.0 or
        GNU General Public License (GPL) version 3.0  or the GNU
        Lesser General Public License (LGPL) Version 2.1 or
        Lesser General Public License (LGPL) Version 2.0.
        A copy of each such license is available at
        http://www.opensource.org/licenses/gpl-2.0.php and
        http://opensource.org/licenses/gpl-3.0.html and
        http://www.opensource.org/licenses/lgpl-2.1.php and
        http://www.gnu.org/licenses/old-licenses/library.txt.

        switch#
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

        'show version': '''\
            N95# show version

            Cisco Nexus Operating System (NX-OS) Software
            TAC support: http://www.cisco.com/tac
            Copyright (C) 2002-2016, Cisco and/or its affiliates.
            All rights reserved.
            The copyrights to certain works contained in this software are
            owned by other third parties and used and distributed under their own
            licenses, such as open source.  This software is provided "as is," and unless
            otherwise stated, there is no warranty, express or implied, including but not
            limited to warranties of merchantability and fitness for a particular purpose.
            Certain components of this software are licensed under
            the GNU General Public License (GPL) version 2.0 or
            GNU General Public License (GPL) version 3.0  or the GNU
            Lesser General Public License (LGPL) Version 2.1 or
            Lesser General Public License (LGPL) Version 2.0.
            A copy of each such license is available at
            http://www.opensource.org/licenses/gpl-2.0.php and
            http://opensource.org/licenses/gpl-3.0.html and
            http://www.opensource.org/licenses/lgpl-2.1.php and
            http://www.gnu.org/licenses/old-licenses/library.txt.

            Software
              BIOS: version 08.26
              NXOS: version 7.0(3)I7(1)
              BIOS compile time:  06/12/2016
              NXOS image file is: bootflash:nxos.9.3.1_N95.bin
              NXOS compile time:  2/8/2016 20:00:00 [02/09/2016 05:18:17]

            Hardware
              cisco Nexus9000 C9516 (16 Slot) Chassis ("Supervisor Module")
              Intel(R) Xeon(R) CPU E5-2403 0 @ 1.80GHz with 16401664 kB of memory.
              Processor Board ID SAL1745FTPW

              Device name: switch
              bootflash:   20971520 kB
            Kernel uptime is 0 day(s), 0 hour(s), 8 minute(s), 13 second(s)

            Last reset at 235176 usecs after  Thu Mar  3 04:40:48 2016

              Reason: Reset due to upgrade
              System version: 7.0(3)I1(2)
              Service:

            plugin
              Core Plugin, Ethernet Plugin

            Active Package(s):
        ''',

        'show module': '''\
            N95# show module
            Mod Ports             Module-Type                       Model          Status
            --- ----- ------------------------------------- --------------------- ---------
            1    52   48x1/10G SFP+ 4x40G Ethernet Module   N9K-X9564PX           ok
            22   0    Fabric Module                         N9K-C9504-FM          ok
            24   0    Fabric Module                         N9K-C9504-FM          ok
            26   0    Fabric Module                         N9K-C9504-FM          ok
            27   0    Supervisor Module                     N9K-SUP-A             active *
            29   0    System Controller                     N9K-SC-A              active
            30   0    System Controller                     N9K-SC-A              standby

            Mod  Sw                       Hw    Slot
            ---  ----------------------- ------ ----
            1    9.3(1)IIC9(0.4)          1.6    LC1
            22   9.3(1)IIC9(0.4)          1.2    FM2
            24   9.3(1)IIC9(0.4)          1.2    FM4
            26   9.3(1)IIC9(0.4)          1.2    FM6
            27   9.3(1)IIC9(0.4)          1.5    SUP1
            29   9.3(1)IIC9(0.4)          1.4    SC1
            30   9.3(1)IIC9(0.4)          1.4    SC2


            Mod  MAC-Address(es)                         Serial-Num
            ---  --------------------------------------  ----------
            1    cc-46-d6-f4-19-bc to cc-46-d6-f4-19-ff  SAL1948TSF6
            22   NA                                      SAL1931LF0G
            24   NA                                      SAL1931LEWB
            26   NA                                      SAL1931LKVC
            27   64-f6-9d-07-0b-48 to 64-f6-9d-07-0b-59  SAL1930L1YB
            29   NA                                      SAL1930KU2E
            30   NA                                      SAL1930KU0Q

            Mod  Online Diag Status
            ---  ------------------
            1    Pass
            22   Pass
            24   Pass
            26   Pass
            27   Pass
            29   Pass
            30   Pass

            * this terminal session
        ''',

        'copy running-config startup-config': '''\
            N95# copy running-config startup-config
            [########################################] 100%
            Copy complete, now saving to disk (please wait)...
            Copy complete.
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

        'copy ftp://rcpuser:password@20.1.1.1/nxos.9.3.1_N95.bin bootflash:/nxos.9.3.1_N95.bin': '''\
            N95#copy ftp://20.1.1.1/nxos.9.3.1.bin bootflash:nxos.9.3.1_N95.bin
                ***** Transfer of file Completed Successfully *****
            Copy complete, now saving to disk (please wait)...
            Copy complete.
        ''',
    }

    parsed_outputs = {
        'show module': {
            'slot':
                {'lc':
                    {'1':
                        {'48x1/10G SFP+ 4x40G Ethernet Module':
                            {'hardware': '1.6',
                            'mac_address': 'cc-46-d6-f4-19-bc to cc-46-d6-f4-19-ff',
                            'model': 'N9K-X9564PX',
                            'online_diag_status': 'Pass',
                            'ports': '52',
                            'serial_number': 'SAL1948TSF6',
                            'slot/world_wide_name': 'LC1',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'ok'}},
                    '22':
                        {'Fabric Module':
                            {'hardware': '1.2',
                            'mac_address': 'NA',
                            'model': 'N9K-C9504-FM',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1931LF0G',
                            'slot/world_wide_name': 'FM2',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'ok'}},
                    '24':
                        {'Fabric Module':
                            {'hardware': '1.2',
                            'mac_address': 'NA',
                            'model': 'N9K-C9504-FM',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1931LEWB',
                            'slot/world_wide_name': 'FM4',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'ok'}},
                    '26':
                        {'Fabric Module':
                            {'hardware': '1.2',
                            'mac_address': 'NA',
                            'model': 'N9K-C9504-FM',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1931LKVC',
                            'slot/world_wide_name': 'FM6',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'ok'}},
                    '29':
                        {'System Controller':
                            {'hardware': '1.4',
                            'mac_address': 'NA',
                            'model': 'N9K-SC-A',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1930KU2E',
                            'slot/world_wide_name': 'SC1',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'active'}},
                    '30':
                        {'System Controller':
                            {'hardware': '1.4',
                            'mac_address': 'NA',
                            'model': 'N9K-SC-A',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1930KU0Q',
                            'slot/world_wide_name': 'SC2',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'standby'}}},
                'rp':
                    {'27':
                        {'Supervisor Module':
                            {'hardware': '1.5',
                            'mac_address': '64-f6-9d-07-0b-48 to 64-f6-9d-07-0b-59',
                            'model': 'N9K-SUP-A',
                            'online_diag_status': 'Pass',
                            'ports': '0',
                            'serial_number': 'SAL1930L1YB',
                            'slot/world_wide_name': 'SUP1',
                            'software': '9.3(1)IIC9(0.4)',
                            'status': 'active'}}}}},

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
                    'system_image_file': 'bootflash:nxos.9.3.1_N95.bin',
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

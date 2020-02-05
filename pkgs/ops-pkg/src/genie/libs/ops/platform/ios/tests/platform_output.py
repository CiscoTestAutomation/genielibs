class PlatformOutput(object):

    show_version = '''
    best-c3945-IOS3#show version
    Cisco IOS Software, C3900 Software (C3900-UNIVERSALK9-M), Version 15.0(1)M7, RELEASE SOFTWARE (fc2)
    Technical Support: http://www.cisco.com/techsupport
    Copyright (c) 1986-2011 by Cisco Systems, Inc.
    Compiled Fri 05-Aug-11 00:32 by prod_rel_team
    
    ROM: System Bootstrap, Version 15.0(1r)M13, RELEASE SOFTWARE (fc1)
    
    best-c3945-IOS3 uptime is 1 hour, 20 minutes
    System returned to ROM by reload at 10:26:47 EST Mon Dec 9 2019
    System restarted at 10:27:57 EST Mon Dec 9 2019
    System image file is "flash0:c3900-universalk9-mz.SPA.150-1.M7.bin"
    Last reload type: Normal Reload
    Last reload reason: Reload Command
    
    
    
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
              
    Cisco CISCO3945-CHASSIS (revision 1.1) with C3900-SPE150/K9 with 2027520K/69632K bytes of memory.
    Processor board ID FGL161010K8
    2 FastEthernet interfaces
    3 Gigabit Ethernet interfaces
    1 Virtual Private Network (VPN) Module
    DRAM configuration is 72 bits wide with parity enabled.
    255K bytes of non-volatile configuration memory.
    2000880K bytes of ATA System CompactFlash 0 (Read/Write)
              
              
    License Info:
              
    License UDI:
              
    -------------------------------------------------
    Device#   PID                   SN
    -------------------------------------------------
    *0        C3900-SPE150/K9       FOC16050QP6     
              
              
              
    Technology Package License Information for Module:'c3900' 
              
    -----------------------------------------------------------------
    Technology    Technology-package           Technology-package
                  Current       Type           Next reboot  
    ------------------------------------------------------------------
    ipbase        ipbasek9      Permanent      ipbasek9
    security      securityk9    Permanent      securityk9
    uc            None          None           None
    data          datak9        Permanent      datak9
              
    Configuration register is 0x2102

    '''
    dir_ios = '''
    best-c3945-IOS3#dir
    Directory of flash0:/

        1  -rw-    55298260   Mar 5 2012 20:00:48 -05:00  c3900-universalk9-mz.SPA.150-1.M7.bin
        2  -rw-        2903   Mar 5 2012 20:10:54 -05:00  cpconfig-39xx.cfg
        3  -rw-     3000320   Mar 5 2012 20:11:12 -05:00  cpexpress.tar
        4  -rw-        1038   Mar 5 2012 20:11:24 -05:00  home.shtml
        5  -rw-      122880   Mar 5 2012 20:11:36 -05:00  home.tar
        6  -rw-     1697952   Mar 5 2012 20:11:54 -05:00  securedesktop-ios-3.1.1.45-k9.pkg
        7  -rw-      415956   Mar 5 2012 20:12:10 -05:00  sslclient-win-1.1.4.176.pkg
        8  -rw-   100327256  Feb 19 2014 17:56:28 -05:00  c3900-universalk9-mz.SSA.154-2.1.T
        9  -rw-        1152   Jun 1 2018 18:08:20 -05:00  datak9.lic
       10  -rw-    98622740  Jan 21 2014 11:27:54 -05:00  c3900-universalk9-mz.SSA.154-1.19.T
       11  -rw-        8483   Jun 1 2018 17:42:48 -05:00  config_backup_20180601
       12  -rw-    64280612   Jun 1 2018 17:53:48 -05:00  c3900-tpgen_universalk9-mz.PAGENT.5.0.0
       13  -rw-        6867   Dec 9 2019 10:21:50 -05:00  config_backup_12092019
    
    2048491520 bytes total (1724481536 bytes free)
    '''
    show_inventory = '''
    best-c3945-IOS3#show inventory
    NAME: "CISCO3945-CHASSIS", DESCR: "CISCO3945-CHASSIS"
    PID: CISCO3945-CHASSIS , VID: V05 , SN: FGL161010K8
    
    NAME: "Cisco Services Performance Engine 150 for Cisco 3900 ISR on Slot 0", DESCR: "Cisco Services Performance Engine 150 for Cisco 3900 ISR"
    PID: C3900-SPE150/K9   , VID: V05 , SN: FOC16050QP6
    
    NAME: "Two-Port Fast Ethernet High Speed WAN Interface Card on Slot 0 SubSlot 3", DESCR: "Two-Port Fast Ethernet High Speed WAN Interface Card"
    PID: HWIC-2FE          , VID: V02 , SN: FOC16062824
    
    NAME: "C3900 AC Power Supply 1", DESCR: "C3900 AC Power Supply 1"
    PID: PWR-3900-AC       , VID: V03 , SN: QCS1604P0BT
    '''

    platform_all = {
        'chassis': 'CISCO3945-CHASSIS',
        'main_mem': '2027520',
        'rtr_type': 'CISCO3945-CHASSIS',
        'chassis_sn': 'FGL161010K8',
        'config_register': '0x2102',
        'dir': 'flash0:/',
        'image': 'flash0:c3900-universalk9-mz.SPA.150-1.M7.bin',
        'os': 'ios',
        'slot': {
            'oc': {
                'C3900 AC Power Supply 1': {
                    'name': 'C3900 AC Power Supply 1',
                    'sn': 'QCS1604P0BT',
                },
            },
            'rp': {
                '0': {
                    'subslot': {
                        '3': {
                            'name': 'HWIC-2FE',
                            'sn': 'FOC16062824',
                        },
                    },
                },
            },
        },
        'version': '15.0(1)M7',
    }
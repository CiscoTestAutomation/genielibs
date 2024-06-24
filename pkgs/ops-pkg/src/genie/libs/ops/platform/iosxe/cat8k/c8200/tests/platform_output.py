
class PlatformOutput(object):

    # ==========================================================================
    #                               C8200
    # ==========================================================================

    showVersion = {
        'version': {
            'chassis': 'C8200-1N-4T',
            'chassis_sn': 'FGL2420L6EE',
            'compiled_by': 'mcpre',
            'compiled_date': 'Fri 16-Oct-20 19:08',
            'curr_config_register': '0x2102',
            'disks': {
                'bootflash:.': {
                    'disk_size': '7090175',
                    'type_of_disk': 'flash memory',
                },
                'harddisk:.': {
                    'disk_size': '585924608',
                    'type_of_disk': 'NVMe SSD',
                },
                'usb0:.': {
                    'disk_size': '16789568',
                    'type_of_disk': 'USB flash',
                },
            },
            'hostname': 'cEdge-P2',
            'image_id': 'X86_64_LINUX_IOSD-UNIVERSALK9-M',
            'image_type': 'developer image',
            'last_reload_reason': 'SMU Install',
            'main_mem': '3753847',
            'mem_size': {
                'non-volatile configuration': '32768',
                'physical': '8388608',
            },
            'number_of_intfs': {
                'Cellular': '2',
                'Gigabit Ethernet': '4',
                'Serial': '4',
            },
            'os': 'IOS-XE',
            'platform': 'c8000be',
            'processor_board_flash': '7203041280',
            'processor_type': '1RU',
            'returned_to_rom_by': 'SMU Install',
            'rom': 'PROM-20200723',
            'rtr_type': 'C8200-1N-4T',
            'system_image': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin',
            'uptime': '31 minutes',
            'uptime_this_cp': '32 minutes',
            'version': '17.5.20201016:181710',
            'version_short': '17.5',
        },
    }

    showDir = {
        'dir': {
            'bootflash:/': {
                'bytes_free': '2294001664',
                'bytes_total': '7203041280',
                'files': {
                    '.PATCH': {
                        'index': '362881',
                        'last_modified_date': 'Nov 18 2020 06:39:41     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.PATCH-backup': {
                        'index': '225793',
                        'last_modified_date': 'Nov 18 2020 06:35:08     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.cdb_backup': {
                        'index': '282241',
                        'last_modified_date': 'Jun 9 2020 20:11:42  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.dbpersist': {
                        'index': '290305',
                        'last_modified_date': 'Nov 16 2020 05:11:08     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.geo': {
                        'index': '137089',
                        'last_modified_date': 'Jun 21 2020 19:08:46     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.iox_dir_list': {
                        'index': '29',
                        'last_modified_date': 'Oct 30 2020 18:58:56     +00:00',
                        'permissions': '-rw-',
                        'size': '275',
                    },
                    '.prst_sync': {
                        'index': '411265',
                        'last_modified_date': 'Nov 18 2020 06:36:19     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.rollback_timer': {
                        'index': '8065',
                        'last_modified_date': 'Nov 18 2020 06:39:14     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.sdwaninstaller': {
                        'index': '298369',
                        'last_modified_date': 'Nov 18 2020 06:39:43     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.sdwaninstallerfs': {
                        'index': '18',
                        'last_modified_date': 'Nov 16 2020 05:11:48     +00:00',
                        'permissions': '-rw-',
                        'size': '419430400',
                    },
                    '.sdwaninternal': {
                        'index': '96769',
                        'last_modified_date': 'Jun 9 2020 20:03:48  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '.ssh': {
                        'index': '403201',
                        'last_modified_date': 'Jun 9 2020 19:37:47  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    '175_yang_kgv.cfg': {
                        'index': '41',
                        'last_modified_date': 'Nov 16 2020 22:02:30     +00:00',
                        'permissions': '-rw-',
                        'size': '6555',
                    },
                    'CSCvW14593_show_audit_log.txt': {
                        'index': '37',
                        'last_modified_date': 'Oct 30 2020 19:34:26     +00:00',
                        'permissions': '-rw-',
                        'size': '75919',
                    },
                    'CSCvv61331_audit_log.txt': {
                        'index': '31',
                        'last_modified_date': 'Sep 16 2020 18:09:02     +00:00',
                        'permissions': '-rw-',
                        'size': '283402',
                    },
                    'CSCvv61331_show_audit_log.txt': {
                        'index': '36',
                        'last_modified_date': 'Oct 16 2020 21:46:00     +00:00',
                        'permissions': '-rw-',
                        'size': '95734',
                    },
                    'CSCvv61331_show_audit_output.txt': {
                        'index': '35',
                        'last_modified_date': 'Oct 16 2020 20:48:33     +00:00',
                        'permissions': '-rw-',
                        'size': '371048',
                    },
                    'CSCvv82742_show_audit_log.txt': {
                        'index': '33',
                        'last_modified_date': 'Sep 28 2020 06:40:04     +00:00',
                        'permissions': '-rw-',
                        'size': '334666',
                    },
                    'HD_destroy_show_audit.txt': {
                        'index': '30',
                        'last_modified_date': 'Sep 3 2020 18:49:19  +00:00',
                        'permissions': '-rw-',
                        'size': '171680',
                    },
                    'PROM-20200723.pkg': {
                        'index': '25',
                        'last_modified_date': 'Jul 30 2020 22:00:45     +00:00',
                        'permissions': '-rw-',
                        'size': '7222220',
                    },
                    'SHARED-IOX': {
                        'index': '209665',
                        'last_modified_date': 'Jul 9 2020 06:05:39  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'System_Firmware_Info.txt': {
                        'index': '42',
                        'last_modified_date': 'Nov 18 2020 06:37:43     +00:00',
                        'permissions': '-rw-',
                        'size': '151',
                    },
                    'admin-tech_show_audit.log': {
                        'index': '27',
                        'last_modified_date': 'Aug 12 2020 04:39:25     +00:00',
                        'permissions': '-rw-',
                        'size': '1322755',
                    },
                    'admin-tech_show_audit_log.txt': {
                        'index': '32',
                        'last_modified_date': 'Sep 22 2020 22:15:46     +00:00',
                        'permissions': '-rw-',
                        'size': '2818976',
                    },
                    'c8000be-firmware_dreamliner.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80643',
                        'last_modified_date': 'Nov 7 2020 02:00:44  +00:00',
                        'permissions': '-rw-',
                        'size': '54360',
                    },
                    'c8000be-firmware_dreamliner.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314499',
                        'last_modified_date': 'Nov 6 2020 04:35:15  +00:00',
                        'permissions': '-rw-',
                        'size': '54356',
                    },
                    'c8000be-firmware_dsp_analogbri.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80644',
                        'last_modified_date': 'Nov 7 2020 02:00:45  +00:00',
                        'permissions': '-rw-',
                        'size': '6677592',
                    },
                    'c8000be-firmware_dsp_analogbri.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314500',
                        'last_modified_date': 'Nov 6 2020 04:35:15  +00:00',
                        'permissions': '-rw-',
                        'size': '6677592',
                    },
                    'c8000be-firmware_dsp_sp2700.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80645',
                        'last_modified_date': 'Nov 7 2020 02:00:45  +00:00',
                        'permissions': '-rw-',
                        'size': '1762392',
                    },
                    'c8000be-firmware_dsp_sp2700.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314501',
                        'last_modified_date': 'Nov 6 2020 04:35:15  +00:00',
                        'permissions': '-rw-',
                        'size': '1762388',
                    },
                    'c8000be-firmware_dsp_tilegx.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80646',
                        'last_modified_date': 'Nov 7 2020 02:00:45  +00:00',
                        'permissions': '-rw-',
                        'size': '17933400',
                    },
                    'c8000be-firmware_dsp_tilegx.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314502',
                        'last_modified_date': 'Nov 6 2020 04:35:16  +00:00',
                        'permissions': '-rw-',
                        'size': '17933396',
                    },
                    'c8000be-firmware_ngwic_t1e1.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80647',
                        'last_modified_date': 'Nov 7 2020 02:00:45  +00:00',
                        'permissions': '-rw-',
                        'size': '11310168',
                    },
                    'c8000be-firmware_ngwic_t1e1.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314503',
                        'last_modified_date': 'Nov 6 2020 04:35:16  +00:00',
                        'permissions': '-rw-',
                        'size': '11310164',
                    },
                    'c8000be-firmware_nim_async.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80648',
                        'last_modified_date': 'Nov 7 2020 02:00:46  +00:00',
                        'permissions': '-rw-',
                        'size': '12870740',
                    },
                    'c8000be-firmware_nim_async.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314504',
                        'last_modified_date': 'Nov 6 2020 04:35:17  +00:00',
                        'permissions': '-rw-',
                        'size': '9344084',
                    },
                    'c8000be-firmware_nim_bri_st_fw.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80649',
                        'last_modified_date': 'Nov 7 2020 02:00:46  +00:00',
                        'permissions': '-rw-',
                        'size': '4789336',
                    },
                    'c8000be-firmware_nim_bri_st_fw.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314505',
                        'last_modified_date': 'Nov 6 2020 04:35:17  +00:00',
                        'permissions': '-rw-',
                        'size': '4789336',
                    },
                    'c8000be-firmware_nim_cwan. BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80650',
                        'last_modified_date': 'Nov 7 2020 02:00:46  +00:00',
                        'permissions': '-rw-',
                        'size': '17650772',
                    },
                    'c8000be-firmware_nim_cwan. BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314506',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '17650768',
                    },
                    'c8000be-firmware_nim_ge.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80651',
                        'last_modified_date': 'Nov 7 2020 02:00:46  +00:00',
                        'permissions': '-rw-',
                        'size': '2933844',
                    },
                    'c8000be-firmware_nim_ge.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314507',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '2933840',
                    },
                    'c8000be-firmware_nim_shdsl.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80652',
                        'last_modified_date': 'Nov 7 2020 02:00:47  +00:00',
                        'permissions': '-rw-',
                        'size': '11523156',
                    },
                    'c8000be-firmware_nim_shdsl.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314508',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '11523156',
                    },
                    'c8000be-firmware_nim_ssd.  BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80653',
                        'last_modified_date': 'Nov 7 2020 02:00:47  +00:00',
                        'permissions': '-rw-',
                        'size': '5334100',
                    },
                    'c8000be-firmware_nim_ssd.  BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314509',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '5334096',
                    },
                    'c8000be-firmware_nim_xdsl. BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80654',
                        'last_modified_date': 'Nov 7 2020 02:00:47  +00:00',
                        'permissions': '-rw-',
                        'size': '6321236',
                    },
                    'c8000be-firmware_nim_xdsl. BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314510',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '6321232',
                    },
                    'c8000be-firmware_prince.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80655',
                        'last_modified_date': 'Nov 7 2020 02:00:48  +00:00',
                        'permissions': '-rw-',
                        'size': '10191956',
                    },
                    'c8000be-firmware_prince.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314511',
                        'last_modified_date': 'Nov 6 2020 04:35:18  +00:00',
                        'permissions': '-rw-',
                        'size': '10191952',
                    },
                    'c8000be-firmware_sm_10g.   BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80656',
                        'last_modified_date': 'Nov 7 2020 02:00:48  +00:00',
                        'permissions': '-rw-',
                        'size': '2475092',
                    },
                    'c8000be-firmware_sm_10g.   BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314512',
                        'last_modified_date': 'Nov 6 2020 04:35:19  +00:00',
                        'permissions': '-rw-',
                        'size': '2475088',
                    },
                    'c8000be-firmware_sm_1t3e3. BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80657',
                        'last_modified_date': 'Nov 7 2020 02:00:48  +00:00',
                        'permissions': '-rw-',
                        'size': '11093076',
                    },
                    'c8000be-firmware_sm_1t3e3. BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314513',
                        'last_modified_date': 'Nov 6 2020 04:35:19  +00:00',
                        'permissions': '-rw-',
                        'size': '11093072',
                    },
                    'c8000be-firmware_sm_async. BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80658',
                        'last_modified_date': 'Nov 7 2020 02:00:49  +00:00',
                        'permissions': '-rw-',
                        'size': '14259284',
                    },
                    'c8000be-firmware_sm_async. BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314514',
                        'last_modified_date': 'Nov 6 2020 04:35:19  +00:00',
                        'permissions': '-rw-',
                        'size': '10732624',
                    },
                    'c8000be-firmware_sm_dsp_sp2700.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80659',
                        'last_modified_date': 'Nov 7 2020 02:00:49  +00:00',
                        'permissions': '-rw-',
                        'size': '1897560',
                    },
                    'c8000be-firmware_sm_dsp_sp2700.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314515',
                        'last_modified_date': 'Nov 6 2020 04:35:19  +00:00',
                        'permissions': '-rw-',
                        'size': '1897560',
                    },
                    'c8000be-firmware_sm_nim_adpt.  BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80660',
                        'last_modified_date': 'Nov 7 2020 02:00:49  +00:00',
                        'permissions': '-rw-',
                        'size': '156760',
                    },
                    'c8000be-firmware_sm_nim_adpt.  BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314516',
                        'last_modified_date': 'Nov 6 2020 04:35:19  +00:00',
                        'permissions': '-rw-',
                        'size': '156756',
                    },
                    'c8000be-mono-universalk9.  BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80661',
                        'last_modified_date': 'Nov 7 2020 02:01:02  +00:00',
                        'permissions': '-rw-',
                        'size': '567600228',
                    },
                    'c8000be-mono-universalk9.  BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314517',
                        'last_modified_date': 'Nov 6 2020 04:35:30  +00:00',
                        'permissions': '-rw-',
                        'size': '555934816',
                    },
                    'c8000be-rpboot.    BLD_POLARIS_DEV_LATEST_20201103_212701.SSA.pkg': {
                        'index': '80662',
                        'last_modified_date': 'Nov 7 2020 02:01:50  +00:00',
                        'permissions': '-rw-',
                        'size': '41442704',
                    },
                    'c8000be-rpboot.    BLD_V174_THROTTLE_LATEST_20201104_PRD14.SSA.pkg': {
                        'index': '314518',
                        'last_modified_date': 'Nov 6 2020 04:36:17  +00:00',
                        'permissions': '-rw-',
                        'size': '41515430',
                    },
                    'c8000be-universalk9.17.04.01prd9.SPA.bin': {
                        'index': '40',
                        'last_modified_date': 'Nov 12 2020 22:50:31     +00:00',
                        'permissions': '-rw-',
                        'size': '727336014',
                    },
                    'c8000be-universalk9.   BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin': {
                        'index': '39',
                        'last_modified_date': 'Nov 12 2020 21:41:45     +00:00',
                        'permissions': '-rw-',
                        'size': '744614104',
                    },
                    'c8000be-universalk9.   BLD_POLARIS_DEV_LATEST_20201103_212.conf': {
                        'index': '80642',
                        'last_modified_date': 'Nov 7 2020 02:01:50  +00:00',
                        'permissions': '-rw-',
                        'size': '11388',
                    },
                    'c8000be-universalk9.   BLD_V174_THROTTLE_LATEST_20201104_P.conf': {
                        'index': '314498',
                        'last_modified_date': 'Nov 6 2020 04:36:17  +00:00',
                        'permissions': '-rw-',
                        'size': '11851',
                    },
                    'core': {
                        'index': '177409',
                        'last_modified_date': 'Jul 27 2020 05:13:21     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'format_audit_log.txt': {
                        'index': '28',
                        'last_modified_date': 'Aug 13 2020 21:17:17     +00:00',
                        'permissions': '-rw-',
                        'size': '3025023',
                    },
                    'fw_upgrade_sysinfo': {
                        'index': '217729',
                        'last_modified_date': 'Oct 30 2020 18:05:39     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'gs_script': {
                        'index': '419329',
                        'last_modified_date': 'Oct 30 2020 17:59:57     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'guest-share': {
                        'index': '104833',
                        'last_modified_date': 'Jun 9 2020 19:39:23  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'ios_core.p7b': {
                        'index': '14',
                        'last_modified_date': 'Jun 9 2020 19:38:21  +00:00',
                        'permissions': '-rw-',
                        'size': '20109',
                    },
                    'iox_host_data_share': {
                        'index': '193537',
                        'last_modified_date': 'Jun 9 2020 19:39:43  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'license_evlog': {
                        'index': '153217',
                        'last_modified_date': 'Nov 18 2020 06:36:27     +00:00',
                        'permissions': 'drwx',
                        'size': '8192',
                    },
                    'lost+found': {
                        'index': '11',
                        'last_modified_date': 'Jun 9 2020 19:37:10  +00:00',
                        'permissions': 'drwx',
                        'size': '16384',
                    },
                    'memleak.tcl': {
                        'index': '13',
                        'last_modified_date': 'Nov 18 2020 06:36:05     +00:00',
                        'permissions': '-rw-',
                        'size': '134808',
                    },
                    'mode_event_log': {
                        'index': '12',
                        'last_modified_date': 'Nov 18 2020 06:35:46     +00:00',
                        'permissions': '-rw-',
                        'size': '27299',
                    },
                    'olin_RootCert22.crt': {
                        'index': '17',
                        'last_modified_date': 'Jun 10 2020 05:45:44     +00:00',
                        'permissions': '-rw-',
                        'size': '1314',
                    },
                    'onep': {
                        'index': '322561',
                        'last_modified_date': 'Jun 9 2020 19:38:54  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'original-startup-config': {
                        'index': '24',
                        'last_modified_date': 'Jul 10 2020 18:32:00     +00:00',
                        'permissions': '-rw-',
                        'size': '1471',
                    },
                    'original-xe-config': {
                        'index': '19',
                        'last_modified_date': 'Nov 5 2020 20:59:12  +00:00',
                        'permissions': '-rw-',
                        'size': '6262',
                    },
                    'packages.conf': {
                        'index': '306434',
                        'last_modified_date': 'Nov 7 2020 02:04:21  +00:00',
                        'permissions': '-rw-',
                        'size': '11388',
                    },
                    'pki_certificates': {
                        'index': '22',
                        'last_modified_date': 'Nov 5 2020 21:03:46  +00:00',
                        'permissions': '-rw-',
                        'size': '107',
                    },
                    'pnp-info': {
                        'index': '161281',
                        'last_modified_date': 'Jun 9 2020 19:38:53  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'pnp-tech': {
                        'index': '201601',
                        'last_modified_date': 'Nov 16 2020 05:15:38     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'prev_packages.conf': {
                        'index': '26',
                        'last_modified_date': 'Nov 7 2020 02:03:18  +00:00',
                        'permissions': '-rw-',
                        'size': '11851',
                    },
                    'running-config': {
                        'index': '21',
                        'last_modified_date': 'Jun 11 2020 20:35:37     +00:00',
                        'permissions': '-rw-',
                        'size': '5222',
                    },
                    'sdwan': {
                        'index': '112897',
                        'last_modified_date': 'Nov 16 2020 05:13:47     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'show_audit_log.txt': {
                        'index': '34',
                        'last_modified_date': 'Nov 7 2020 02:24:28  +00:00',
                        'permissions': '-rw-',
                        'size': '371908',
                    },
                    'ss_disc': {
                        'index': '40321',
                        'last_modified_date': 'Oct 30 2020 17:59:57     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'ssd': {
                        'index': '38',
                        'last_modified_date': 'Oct 30 2020 17:59:57     +00:00',
                        'permissions': '-rw-',
                        'size': '5242880',
                    },
                    'startup-config': {
                        'index': '23',
                        'last_modified_date': 'Jun 11 2020 20:44:06     +00:00',
                        'permissions': '-rw-',
                        'size': '25',
                    },
                    'sysboot': {
                        'index': '354817',
                        'last_modified_date': 'Nov 18 2020 06:34:55     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'syslog': {
                        'index': '387073',
                        'last_modified_date': 'Nov 16 2020 04:32:19     +00:00',
                        'permissions': 'drwx',
                        'size': '12288',
                    },
                    'throughput_monitor_params': {
                        'index': '16',
                        'last_modified_date': 'Nov 18 2020 06:36:10     +00:00',
                        'permissions': '-rw-',
                        'size': '30',
                    },
                    'tracelogs': {
                        'index': '427393',
                        'last_modified_date': 'Nov 18 2020 07:06:07     +00:00',
                        'permissions': 'drwx',
                        'size': '176128',
                    },
                    'trustidrootx3_ca.ca': {
                        'index': '15',
                        'last_modified_date': 'Jun 9 2020 19:38:21  +00:00',
                        'permissions': '-rwx',
                        'size': '1314',
                    },
                    'virtual-instance': {
                        'index': '306433',
                        'last_modified_date': 'Sep 24 2020 21:31:22     +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                    'vmanage-admin': {
                        'index': '129025',
                        'last_modified_date': 'Nov 7 2020 02:21:56  +00:00',
                        'permissions': 'drwx',
                        'size': '4096',
                    },
                },
            },
            'dir': 'bootflash:/',
        },
    }

    showDirEmpty = {}

    showPlatform = {
        'slot': {
            '0': {
                'lc': {
                    'C8200-1N-4T': {
                        'insert_time': '00:32:26',
                        'name': 'C8200-1N-4T',
                        'slot': '0',
                        'state': 'ok',
                        'subslot': {
                            '0': {
                                '2x1G-2xSFP': {
                                    'insert_time': '00:31:12',
                                    'name': '2x1G-2xSFP',
                                    'state': 'ok',
                                    'subslot': '0',
                                },
                            },
                            '1': {
                                'NIM-4T': {
                                    'insert_time': '00:31:12',
                                    'name': 'NIM-4T',
                                    'state': 'ok',
                                    'subslot': '1',
                                },
                            },
                            '2': {
                                'P-LTE-GB': {
                                    'insert_time': '00:31:12',
                                    'name': 'P-LTE-GB',
                                    'state': 'ok',
                                    'subslot': '2',
                                },
                            },
                            '5': {
                                'SSD-M2NVME-600G': {
                                    'insert_time': '00:31:12',
                                    'name': 'SSD-M2NVME-600G',
                                    'state': 'ok',
                                    'subslot': '5',
                                },
                            },
                        },
                    },
                },
            },
            'F0': {
                'other': {
                    'C8200-1N-4T': {
                        'insert_time': '00:32:26',
                        'name': 'C8200-1N-4T',
                        'slot': 'F0',
                        'state': 'ok, active',
                    },
                },
            },
            'P0': {
                'other': {
                    'PWR-INT-90WAC': {
                        'insert_time': '00:31:47',
                        'name': 'PWR-INT-90WAC',
                        'slot': 'P0',
                        'state': 'ok',
                    },
                },
            },
            'P2': {
                'other': {
                    'C8200-FAN-1R': {
                        'insert_time': '00:31:47',
                        'name': 'C8200-FAN-1R',
                        'slot': 'P2',
                        'state': 'ok',
                    },
                },
            },
            'R0': {
                'rp': {
                    'C8200-1N-4T': {
                        'insert_time': '00:32:26',
                        'name': 'C8200-1N-4T',
                        'slot': 'R0',
                        'state': 'ok, active',
                    },
                },
            },
        },
    }

    showInventory = {
        'main': {
            'chassis': {
                'C8200-1N-4T': {
                    'descr': 'Cisco C8200-1N-4T Chassis',
                    'name': 'Chassis',
                    'pid': 'C8200-1N-4T',
                    'sn': 'FGL2420L6EE',
                    'vid': 'V01',
                },
            },
        },
        'slot': {
            '0': {
                'lc': {
                    'C8200-1N-4T': {
                        'descr': 'Cisco C8200-1N-4T Built-In NIM    controller',
                        'name': 'module 0',
                        'pid': 'C8200-1N-4T',
                        'sn': '',
                        'subslot': {
                            '0': {
                                '2x1G-2xSFP': {
                                    'descr': 'Front Panel 4 ports   Gigabitethernet Module',
                                    'name': 'NIM subslot 0/0',
                                    'pid': '2x1G-2xSFP',
                                    'sn': '',
                                    'vid': 'V01',
                                },
                            },
                            '0 transceiver 3': {
                                'SFP-GE-S': {
                                    'descr': 'GE SX',
                                    'name': 'subslot 0/0 transceiver    3',
                                    'pid': 'SFP-GE-S',
                                    'sn': 'FNS1047175F',
                                    'vid': 'V01',
                                },
                            },
                            '1': {
                                'NIM-4T': {
                                    'descr': 'sync serial NIM with 4    ports',
                                    'name': 'NIM subslot 0/1',
                                    'pid': 'NIM-4T',
                                    'sn': 'FOC230369RF',
                                    'vid': 'V01',
                                },
                            },
                            '2': {
                                'P-LTE-GB': {
                                    'descr': 'P-LTE-GB Module',
                                    'name': 'NIM subslot 0/2',
                                    'pid': 'P-LTE-GB',
                                    'sn': 'FOC22191PWY',
                                    'vid': 'V00',
                                },
                            },
                            '5': {
                                'SSD-M2NVME-600G': {
                                    'descr': 'NVME SSD Module',
                                    'name': 'NIM subslot 0/5',
                                    'pid': 'SSD-M2NVME-600G',
                                    'sn': 'INTELSSDPELKX010T8',
                                    'vid': 'V01',
                                },
                            },
                        },
                        'vid': '',
                    },
                },
            },
            'F0': {
                'other': {
                    'C8200-1N-4T': {
                        'descr': 'Cisco C8200-1N-4T Forwarding  Processor',
                        'name': 'module F0',
                        'pid': 'C8200-1N-4T',
                        'sn': '',
                        'vid': '',
                    },
                },
            },
            'Fan_Tray': {
                'other': {
                    'C8200-FAN-1R': {
                        'descr': 'Cisco C8200 1RU Fan Assembly',
                        'name': 'Fan Tray',
                        'pid': 'C8200-FAN-1R',
                        'sn': '',
                        'vid': '',
                    },
                },
            },
            'P0': {
                'other': {
                    'PWR-NOPI': {
                        'descr': '90W AC Internal Power Supply for  Cisco C8200',
                        'name': 'Power Supply Module 0',
                        'pid': 'PWR-NOPI',
                        'sn': '',
                        'vid': '',
                    },
                },
            },
            'R0': {
                'rp': {
                    'C8200-1N-4T': {
                        'descr': 'Cisco C8200-1N-4T Route Processor',
                        'name': 'module R0',
                        'pid': 'C8200-1N-4T',
                        'sn': 'FOC24143XF7',
                        'vid': 'V01',
                    },
                },
            },
        },
    }

    showRedundancy = {
        'red_sys_info': {
            'available_system_uptime': '31 minutes',
            'communications': 'Down',
            'communications_reason': 'Failure',
            'conf_red_mode': 'Non-redundant',
            'hw_mode': 'Simplex',
            'last_switchover_reason': 'none',
            'maint_mode': 'Disabled',
            'oper_red_mode': 'Non-redundant',
            'standby_failures': '0',
            'switchovers_system_experienced': '0',
        },
        'slot': {
            'slot 6': {
                'boot': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin,12;',
                'config_register': '0x2102',
                'curr_sw_state': 'ACTIVE',
                'image_ver': 'Cisco IOS Software [Bengaluru], c8000be Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.5.20201016:181710 [S2C-build-polaris_dev-124418-/nobackup/mcpre/BLD-BLD_POLARIS_DEV_LATEST_20201016_180855 217]',
                'uptime_in_curr_state': '31 minutes',
            },
        },
    }

    ShowIssuStateDetail = {
        'slot': {
            'R0': {
                'issu_in_progress': False,
            },
        },
    }

    ShowIssuRollbackTimer = {
        'rollback_timer_reason': 'no ISSU operation is in progress',
        'rollback_timer_state': 'inactive',
    }

    platform_all = {
        'chassis': 'C8200-1N-4T',
        'chassis_sn': 'FGL2420L6EE',
        'config_register': '0x2102',
        'dir': 'bootflash:/',
        'image': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin',
        'issu_rollback_timer_reason': 'no ISSU operation is in progress',
        'issu_rollback_timer_state': 'inactive',
        'main_mem': '3753847',
        'os': 'iosxe',
        'redundancy_communication': False,
        'redundancy_mode': 'Non-redundant',
        'rp_uptime': 1860,
        'rtr_type': 'C8200-1N-4T',
        'slot': {
            'lc': {
                '0': {
                    'name': 'C8200-1N-4T',
                    'sn': '',
                    'state': 'ok',
                    'subslot': {
                        '0': {
                            'name': '2x1G-2xSFP',
                            'sn': '',
                            'state': 'ok',
                        },
                        '0 transceiver 3': {
                            'name': 'SFP-GE-S',
                            'sn': 'FNS1047175F',
                        },
                        '1': {
                            'name': 'NIM-4T',
                            'sn': 'FOC230369RF',
                            'state': 'ok',
                        },
                        '2': {
                            'name': 'P-LTE-GB',
                            'sn': 'FOC22191PWY',
                            'state': 'ok',
                        },
                        '5': {
                            'name': 'SSD-M2NVME-600G',
                            'sn': 'INTELSSDPELKX010T8',
                            'state': 'ok',
                        },
                    },
                },
            },
            'oc': {
                'F0': {
                    'name': 'C8200-1N-4T',
                    'sn': '',
                    'state': 'ok, active',
                },
                'Fan_Tray': {
                    'sn': '',
                },
                'P0': {
                    'name': 'PWR-INT-90WAC',
                    'sn': '',
                    'state': 'ok',
                },
                'P2': {
                    'name': 'C8200-FAN-1R',
                    'state': 'ok',
                },
            },
            'rp': {
                'R0': {
                    'boot_image': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin,12;',
                    'config_register': '0x2102',
                    'issu': {
                        'in_progress': False,
                    },
                    'name': 'C8200-1N-4T',
                    'redundancy_state': 'ACTIVE',
                    'rp_uptime': '31 minutes',
                    'sn': 'FOC24143XF7',
                    'state': 'ok, active',
                    'system_image': 'Cisco IOS Software [Bengaluru], c8000be Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.5.20201016:181710 [S2C-build-polaris_dev-124418-/nobackup/mcpre/BLD-BLD_POLARIS_DEV_LATEST_20201016_180855 217]',
                },
            },
        },
        'switchover_reason': 'none',
        'version': '17.5.20201016:181710',
    }

    platform_all_empty_dir = {
        'chassis': 'C8200-1N-4T',
        'chassis_sn': 'FGL2420L6EE',
        'config_register': '0x2102',
        'dir': 'bootflash:/',
        'image': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin',
        'issu_rollback_timer_reason': 'no ISSU operation is in progress',
        'issu_rollback_timer_state': 'inactive',
        'main_mem': '3753847',
        'os': 'iosxe',
        'redundancy_communication': False,
        'redundancy_mode': 'Non-redundant',
        'rp_uptime': 1860,
        'rtr_type': 'C8200-1N-4T',
        'slot': {
            'lc': {
                '0': {
                    'name': 'C8200-1N-4T',
                    'sn': '',
                    'state': 'ok',
                    'subslot': {
                        '0': {
                            'name': '2x1G-2xSFP',
                            'sn': '',
                            'state': 'ok',
                        },
                        '0 transceiver 3': {
                            'name': 'SFP-GE-S',
                            'sn': 'FNS1047175F',
                        },
                        '1': {
                            'name': 'NIM-4T',
                            'sn': 'FOC230369RF',
                            'state': 'ok',
                        },
                        '2': {
                            'name': 'P-LTE-GB',
                            'sn': 'FOC22191PWY',
                            'state': 'ok',
                        },
                        '5': {
                            'name': 'SSD-M2NVME-600G',
                            'sn': 'INTELSSDPELKX010T8',
                            'state': 'ok',
                        },
                    },
                },
            },
            'oc': {
                'F0': {
                    'name': 'C8200-1N-4T',
                    'sn': '',
                    'state': 'ok, active',
                },
                'Fan_Tray': {
                    'sn': '',
                },
                'P0': {
                    'name': 'PWR-INT-90WAC',
                    'sn': '',
                    'state': 'ok',
                },
                'P2': {
                    'name': 'C8200-FAN-1R',
                    'state': 'ok',
                },
            },
            'rp': {
                'R0': {
                    'boot_image': 'bootflash:c8000be-universalk9.BLD_POLARIS_DEV_LATEST_20201016_180855.SSA.bin,12;',
                    'config_register': '0x2102',
                    'issu': {
                        'in_progress': False,
                    },
                    'name': 'C8200-1N-4T',
                    'redundancy_state': 'ACTIVE',
                    'rp_uptime': '31 minutes',
                    'sn': 'FOC24143XF7',
                    'state': 'ok, active',
                    'system_image': 'Cisco IOS Software [Bengaluru], c8000be Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.5.20201016:181710 [S2C-build-polaris_dev-124418-/nobackup/mcpre/BLD-BLD_POLARIS_DEV_LATEST_20201016_180855 217]',
                },
            },
        },
        'switchover_reason': 'none',
        'version': '17.5.20201016:181710',
    }

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* nxos
    * Added
        * support for platform mds in genie clean
        * support for platform n5k in genie clean

* iosxe
    * Added configure_umbrella_in_out API
        * Umbrella inside and outside configuration
    * Added unconfigure_umbrella_in_out API
        * Umbrella inside and outside unconfiguration
    * Added configure_umbrella_global_parameter_map API
        * Umbrella parameter-map configuration
    * Added unconfigure_umbrella_global_parameter_map API
        * Umbrella parameter-map unconfiguration
    * Added configure_umbrella_local_bypass API
        * Umbrella local bypass regex pattern configuration
    * Added unconfigure_umbrella_local_bypass API
        * Umbrella local bypass regex pattern unconfiguration
    * Added execute_clear_dns_statistics API
        * Umbrella statistics clear
    * Added execute_test_ngdns_lookup API
        * ngdns test cli execution
    * Added configure_ip_domain_lookup API
        * ip domain lookup configuration
    * Added unconfigure_ip_domain_lookup API
        * ip domain lookup unconfiguration
    * Added configure_ip_name_server API
        * ip name server configuration
    * Added unconfigure_ip_name_server API
        * ip name server unconfiguration
    * Added configure_nat_in_out API
        * configure nat inside outside over interface
    * Added unconfigure_nat_in_out API
        * unconfiguration nat inside outside over interface
    * Added configure_nat_overload_rule API
        * nat overload rule configuration
    * Added unconfigure_nat_overload_rule API
        * nat overload rule unconfiguration
    * Added execute_clear_nat_translation API
        * clear nat translation

* stages
    * nxos/n9k
        * Added clean stage InstallImage
    * nxos
        * Added UT for ChangeBootVariable nxos clean stage apis
    * common
        * Added UT for WriteErase common apis
        * Added UT for BackupFileOnDevice common apis
        * Added UT for DeleteFilesFromServer common apis
    * apic
        * Added UT for FabricClean clean stage apis
    * iosxe/sdwan
        * Added UT for ApplyConfiguration clean stage apis
        * Added UT for ExpandImage clean stage apis
        * Added UT for SetControllerMode clean stage apis
    * iosxe
        * Added UT for InstallImage clean stage apis
        * Added UT for InstallRemoveInactive clean stage apis
    * common
        * Added UT for ApplyConfiguration clean stage apis
    * apic
        * Added UT for FabricClean clean stage apis
        * Added UT for NodeRegistration clean stage apis
        * Added UT for ApplyConfiguration clean stage apis
    * iosxr
        * Added UT for LoadPies clean stage apis
        * Added UT for TftpBoot clean stage apis
    * common
        * Added UT for DeleteBackupFromDevice common apis
        * Added UT for PowerCycle common apis
        * Added UT for Pingserve common apis
    * nxos/aci
        * Added UT for FabricClean nxos clean stage apis
    * iosxe
        * Added UT for InstallPackages clean stage apis
    * iosxe/cat9k
        * Added UT for TftpBoot clean stage apis

* aireos
    * Added
        * Clean cli_boot


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified config_extended_acl API
        * Added line to configure policy permit any any
    * Removed pre requisite check for cat9k and cat 9500 from exec order.



--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* IOSXE
    * Added API clear_aaa_cache(device, server_grp, profile='all')
    * Added API configure_username(device, username, pwd, encryption=0)
    * Added API unconfigure_username(device, username)
    * Added API configure_radius_automate_tester(device, server_name, username, idle_time=None)
    * Added API unconfigure_radius_automate_tester(device, server_name, username)
    * Added API configure_eap_profile(device, profile_name,method='md5')
    * Added API unconfigure_eap_profile(device, profile_name)

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* IOSXE

    * Modified config_identity_ibns
        * Added port_control as an arg, and made 'auto' the default

    * Modified configure_authentication_host_mode
        * Added spaces between args for readability

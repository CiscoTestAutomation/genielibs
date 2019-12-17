| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v19.12      |


----------------------------------------------------------------------------
                        Fixed
----------------------------------------------------------------------------
* IOSXE
    * Updated prepare_issu
        * Added 'overwrite' option when copy file exists
    * Updated get_ntp_md5_peer
        * Updated verification criteria
    * Updated configure_tacacs_server
        * Updated configuration commands
    * Updated verify_ntp_time
        * Added tolerance 1 second
    * Updated remove_ntp_system_peer
        * to support various config pattern
    * Updated get_ntp_outgoing_interface
        * to support vrf argument
    * Updated remove_ntp_system_peer
        * to support vrf argument

* Libs
    * Updated processor reporting mechanism

----------------------------------------------------------------------------
                        New
----------------------------------------------------------------------------
* IOSXE
    * Added get_running_config_section
    * Added remove_tacacs_server
    * Added get_ntp_system_peer_vrf


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* conf
    * Added breakout interface support to IOSXE
    * Added ParsedInterface class


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * configure_interface
        * Add portsec
            * portsec_enable True
            * portsec_count '1025'
            * portsec_violation_mode 'restrict | protect | shutdown'
            * portsec_aging_type 'inactivity | absolute'
            * portsec_type 'static|sticky'
            * portsec_static_mac '001506000001'
            * portsec_static_vlan '1002'
            * portsec_aging_time '5'
        * Add vpc_id
            * port-channel12
                * vpc_id "12"
        * Add vpc_peerlink
            * port-channel10
                * vpc_peer_link True



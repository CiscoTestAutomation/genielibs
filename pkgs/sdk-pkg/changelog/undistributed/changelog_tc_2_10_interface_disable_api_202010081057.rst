--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* Junos
    * Modified get_rsvp_hello_sent
        * Returns a dictionary with last_changed_time and hello_sent value
    * Modified verify_log_exists
        * Added support for match in command

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* Junos
    * Added verify_chassis_fpc_slot_state
        * Checked if slot state is as expected
    * Added get_configuration_interface_family_bridge_vlan_id
        * Get vlan-id from configuration interface family-bridge
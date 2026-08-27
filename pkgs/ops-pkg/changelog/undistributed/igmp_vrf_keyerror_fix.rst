--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxr
    * Modified Igmp
        * Fixed KeyError raised during learn() when a vrf exists on the device but has no igmp-enabled interfaces, such a vrf now shows up

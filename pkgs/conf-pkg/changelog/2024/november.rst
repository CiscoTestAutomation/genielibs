--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* nxos
    * Added
        * neighbor <neighbor_id> \ bfd multihop
    * Added associate_vrf_name attributes under vlan
        * associate_vrf_name = 'vxlan-1001'
    * Added
        * enabled redistribute AM routes
        * router bgp <ASN> \ address-family ipv4|ipv6 unicast \ redistribute am route-map <user defined route map>


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* nxos
    * Modified ipv6addr.py
        * changed route_tag type to str from bool to read the route_tag values
    * Modified ipv4addr.py
        * Modified 'tag' to 'route_tag' for configuring route_tag
    * Modified route_policy.py
        * Reading 'match_tag' for configuring match_tag under route policy



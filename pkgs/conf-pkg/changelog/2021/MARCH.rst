--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* NXOS
    * Added in bgp conf
        * disable-peer-as-check
    * Added in bgp conf
        * nbr_af_rewrite_mvpn_rt_asn


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* Utils
    * Changed "from fractions import gcd" to "from math import gcd" due to deprecation in Python 3.9

* Device object
    * Removed 'role' attribute

* NXOS
    * Modified Interface Conf
        * Fixed a bug which unconfig doesn't work with attributes



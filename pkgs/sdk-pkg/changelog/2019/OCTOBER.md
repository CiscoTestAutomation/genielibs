| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v19.10      |


----------------------------------------------------------------------------
                       	mapping
----------------------------------------------------------------------------
* updated mapping for static keys to work properly when count key is provided

----------------------------------------------------------------------------
                       	segment_routing
----------------------------------------------------------------------------
* IOSXR
	* Fix compile errors

----------------------------------------------------------------------------
                       	Abstracted_libs
----------------------------------------------------------------------------
HA
    * Added enhancement for deleting debug plugin after process restart (N7K)
    * Added enhancement for connecting to VDCs after reload.switchover (N7K)

NTP & Segment Routing
    * New 41 apis under IOSXR

----------------------------------------------------------------------------
                       	mapping
----------------------------------------------------------------------------
* updated mapping for static keys to work properly when count key is provided

----------------------------------------------------------------------------
                       	apis
----------------------------------------------------------------------------
* updated some API's device args to work with latest device.api
* moved scapy import inside api functions and handled import error if not installed
* IOSXE
    * Added verify_segment_routing_traffic_eng_policies
    * Added verify_mpls_forwarding_table_has_prefix_in_subnet_range
    * Added verify_mpls_forwarding_table_local_label_for_subnet

----------------------------------------------------------------------------
                       	restore
----------------------------------------------------------------------------
* IOSXE
	* updated restore for old images where 'configure replace' is not supported
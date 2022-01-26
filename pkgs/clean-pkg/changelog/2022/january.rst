--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added ApplySelfSignedCert
        * Added new clean stage called apply self signed certificate

* common
    * Added
        * CopyRunToFlash Stage

* stages
    * IOSXE
        * CAT9K
            * Update the tftp boot to support stack devices
            * update the dailog.py for IOSXE devices
        * cat3k
            * Added dialog.py for cat3k
            * Added UT for TftpBoot clean stage apis
            * Added support for copy to device for stack devices
            * Added apis for change boot variable


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Connect to devices in rommon mode
    * Use reload service for install image stage



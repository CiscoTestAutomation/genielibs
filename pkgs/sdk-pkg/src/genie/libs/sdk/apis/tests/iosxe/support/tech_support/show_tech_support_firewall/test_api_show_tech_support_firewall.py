from unittest import TestCase
from genie.libs.sdk.apis.iosxe.support.tech_support import show_tech_support_firewall
from unittest.mock import Mock


class TestShowTechSupportFirewall(TestCase):

    def test_show_tech_support_firewall(self):
        self.device = Mock()
        results_map = {
            'show tech-support firewall': """
------------------ show clock ------------------


14:30:10.834 PST Mon Jan 3 2000

------------------ show version ------------------

Cisco IOS XE Software, Version 17.09.08prd1
Cisco IOS Software [Cupertino], ISR Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.9.8prd1, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2025 by Cisco Systems, Inc.
Compiled Wed 20-Aug-25 16:30 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2025 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: 16.12(2r)

analog-perf-uut1 uptime is 3 weeks, 2 days, 12 hours, 24 minutes
Uptime for this control processor is 3 weeks, 2 days, 12 hours, 26 minutes
System returned to ROM by Reload Command at 01:15:25 PDT Sat Jan 1 2000
System restarted at 02:05:17 PST Sat Dec 11 1999
System image file is "bootflash:isr4300-universalk9.17.09.08prd1.SPA.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.



Suite License Information for Module:'esg' 

--------------------------------------------------------------------------------
Suite                 Suite Current         Type           Suite Next reboot     
--------------------------------------------------------------------------------
FoundationSuiteK9     None                  Smart License  None                  
securityk9
appxk9

AdvUCSuiteK9          AdvUCSuiteK9          Smart License  AdvUCSuiteK9          
uck9
cme-srst
cube


Technology Package License Information: 

-----------------------------------------------------------------
Technology    Technology-package           Technology-package
              Current       Type           Next reboot  
------------------------------------------------------------------
appxk9           appxk9           Smart License    appxk9
uck9             None             Smart License    None
securityk9       None             Smart License    None
ipbase           ipbasek9         Smart License    ipbasek9

The current throughput level is 200000 kbps 


Smart Licensing Status: Smart Licensing Using Policy

cisco ISR4351/K9 (2RU) processor with 1653513K/3071K bytes of memory.
Processor board ID FLM2026W18H
Router operating mode: Autonomous
3 Gigabit Ethernet interfaces
4 ISDN Basic Rate interfaces
6 Voice FXO interfaces
18 Voice FXS interfaces
4 Voice E & M interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
3223551K bytes of flash memory at bootflash:.

Configuration register is 0x0


------------------ show running-config ------------------


Building configuration...

Current configuration : 8304 bytes
!
! Last configuration change at 01:01:09 PST Sat Jan 1 2000
!
version 17.9
service timestamps debug datetime msec localtime show-timezone
service timestamps log datetime msec localtime show-timezone
service internal
platform qfp utilization monitor load 80
platform punt-keepalive disable-kernel-core
!
hostname analog-perf-uut1
!
boot-start-marker
boot-end-marker
!
!
vrf definition Mgmt-intf
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
!
no logging buffered
no logging console
no aaa new-model
clock timezone PST -8 0
!
!
!
!
!
!
!
!
!
ip host sj20lab-tftp1 223.255.254.254
no ip domain lookup
!
!
!
login on-success log
!
!
!
!
!
!
!
subscriber templating
! 
! 
! 
! 
!
multilink bundle-name authenticated
!
!
!
!
!
!
isdn switch-type basic-net3
!
!
crypto pki trustpoint TP-self-signed-1357684700
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-1357684700
 revocation-check none
 rsakeypair TP-self-signed-1357684700
 hash sha256
!
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
 hash sha256
!
!
crypto pki certificate chain TP-self-signed-1357684700
 certificate self-signed 01
  30820330 30820218 A0030201 02020101 300D0609 2A864886 F70D0101 0B050030 
  31312F30 2D060355 04030C26 494F532D 53656C66 2D536967 6E65642D 43657274 
  69666963 6174652D 31333537 36383437 3030301E 170D3030 30313031 31333036 
  31345A17 0D303931 32333131 33303631 345A3031 312F302D 06035504 030C2649 
  4F532D53 656C662D 5369676E 65642D43 65727469 66696361 74652D31 33353736 
  38343730 30308201 22300D06 092A8648 86F70D01 01010500 0382010F 00308201 
  0A028201 01009EE1 19C98C9B 43D803DE 8A9772A4 6E82CF25 713418D9 B12BAF24 
  66825FC9 A760C3EC 7D5821F3 89F3FCB2 C8D2E6DC 7C2B3606 6900A582 754E1C20 
  F2F9CF10 98E7B1CB 7F64E2CD CB3845CC 540C1F89 CB57149C 0510C12B 961A8196 
  704D7E5B A6344996 670803B4 435470CD E15C457D 825250DD D4BF0ACA 568B144C 
  EAA60C31 03BAE8C7 666C747E 5107016B 9E32C3CF 68666055 DF49A39C 281AF61E 
  DC31AC24 7F868770 211FC6B1 3C89B9CC 5B18FDBF 3CEACCBC C6CC7624 876E12A4 
  B9274820 48DBB573 D37540C3 94A2F807 6EDEE0BB 0661BEB3 E27DEE78 29643688 
  0A957F6A 7CB7176E 403513C5 32EFFF3B 26D153EC 5DA61DAA 660E507A 7B22CA3F 
  C0A4E792 AFEB0203 010001A3 53305130 1D060355 1D0E0416 04149196 D61DE1B8 
  A8523F58 27D93256 01CBBC2E 9CC1301F 0603551D 23041830 16801491 96D61DE1 
  B8A8523F 5827D932 5601CBBC 2E9CC130 0F060355 1D130101 FF040530 030101FF 
  300D0609 2A864886 F70D0101 0B050003 82010100 4D2BA772 12249DE1 F04AF4C3 
  9970E601 93B9D06E 51BC36FC C8E3145A 18972B52 C79B7732 466CF3A1 122FA872 
  36695CDA 8F2E963F C82E3EED 650DD6F5 963C6587 888B83F6 7DB7E6FA DFAB1E2D 
  A9BFD447 C23A1914 5C98BA31 5ED52DC2 657D2694 2BDD7A23 61347D2A 4B8353F2 
  AE45D887 9C1463C8 544A54BB DF51E209 8FEEF308 0A3E8D45 97AA9969 723A1F19 
  598D213D 789E919B 5E8DE6DB 4B5F39F6 A304A7A0 7CD8B8C4 9CC76A3A A835E383 
  2760EB55 F0F6DD9D 5F7079EA F82BB422 3CFDDA1F AA1EC921 780F99A3 67B049BE 
  CBC26D22 0F23C0EE 51549C79 B2911809 BC4F2952 6DC853EB 19D60845 39C672F4 
  1B9E66B1 B1DAD06A A25CAF57 BA2C4461 7A09C427
  	quit
crypto pki certificate chain SLA-TrustPoint
 certificate ca 01
  30820321 30820209 A0030201 02020101 300D0609 2A864886 F70D0101 0B050030 
  32310E30 0C060355 040A1305 43697363 6F312030 1E060355 04031317 43697363 
  6F204C69 63656E73 696E6720 526F6F74 20434130 1E170D31 33303533 30313934 
  3834375A 170D3338 30353330 31393438 34375A30 32310E30 0C060355 040A1305 
  43697363 6F312030 1E060355 04031317 43697363 6F204C69 63656E73 696E6720 
  526F6F74 20434130 82012230 0D06092A 864886F7 0D010101 05000382 010F0030 
  82010A02 82010100 A6BCBD96 131E05F7 145EA72C 2CD686E6 17222EA1 F1EFF64D 
  CBB4C798 212AA147 C655D8D7 9471380D 8711441E 1AAF071A 9CAE6388 8A38E520 
  1C394D78 462EF239 C659F715 B98C0A59 5BBB5CBD 0CFEBEA3 700A8BF7 D8F256EE 
  4AA4E80D DB6FD1C9 60B1FD18 FFC69C96 6FA68957 A2617DE7 104FDC5F EA2956AC 
  7390A3EB 2B5436AD C847A2C5 DAB553EB 69A9A535 58E9F3E3 C0BD23CF 58BD7188 
  68E69491 20F320E7 948E71D7 AE3BCC84 F10684C7 4BC8E00F 539BA42B 42C68BB7 
  C7479096 B4CB2D62 EA2F505D C7B062A4 6811D95B E8250FC4 5D5D5FB8 8F27D191 
  C55F0D76 61F9A4CD 3D992327 A8BB03BD 4E6D7069 7CBADF8B DF5F4368 95135E44 
  DFC7C6CF 04DD7FD1 02030100 01A34230 40300E06 03551D0F 0101FF04 04030201 
  06300F06 03551D13 0101FF04 05300301 01FF301D 0603551D 0E041604 1449DC85 
  4B3D31E5 1B3E6A17 606AF333 3D3B4C73 E8300D06 092A8648 86F70D01 010B0500 
  03820101 00507F24 D3932A66 86025D9F E838AE5C 6D4DF6B0 49631C78 240DA905 
  604EDCDE FF4FED2B 77FC460E CD636FDB DD44681E 3A5673AB 9093D3B1 6C9E3D8B 
  D98987BF E40CBD9E 1AECA0C2 2189BB5C 8FA85686 CD98B646 5575B146 8DFC66A8 
  467A3DF4 4D565700 6ADF0F0D CF835015 3C04FF7C 21E878AC 11BA9CD2 55A9232C 
  7CA7B7E6 C1AF74F6 152E99B7 B1FCF9BB E973DE7F 5BDDEB86 C71E3B49 1765308B 
  5FB0DA06 B92AFE7F 494E8A9E 07B85737 F3A58BE1 1A48A229 C37C1E69 39F08678 
  80DDCD16 D6BACECA EEBC7CF9 8428787B 35202CDC 60E4616A B623CDBD 230E3AFB 
  418616A9 4093E049 4D10AB75 27E86F73 932E35B5 8862FDAE 0275156F 719BB2F0 
  D697DF7F 28
  	quit
!
!
!
!
!
!
!
!
!
!
!
!
!
!
voice-card 0/1
 no watchdog
!
voice-card 0/2
 no watchdog
!
voice-card 0/3
 no watchdog
!
voice-card 0/4
 no watchdog
!
voice-card 1/0
 no watchdog
!
license udi pid ISR4351/K9 sn FDO20220684
license boot suite AdvUCSuiteK9
license boot level appxk9
memory free low-watermark processor 61489
!
diagnostic bootup level minimal
!
spanning-tree extend system-id
!
!
!
redundancy
 mode none
!
!
!
!
!
!
!
! 
! 
!
!
interface GigabitEthernet0/0/0
 no ip address
 negotiation auto
!
interface GigabitEthernet0/0/1
 no ip address
 negotiation auto
!
interface GigabitEthernet0/0/2
 no ip address
 negotiation auto
!
interface Service-Engine0/1/4
!
interface Service-Engine0/2/0
!
interface Service-Engine0/3/0
!
interface Service-Engine0/4/0
!
interface Service-Engine1/0/0
!
interface GigabitEthernet0
 vrf forwarding Mgmt-intf
 ip address 1.43.36.3 255.255.0.0
 negotiation auto
!
interface BRI0/1/0:0
 isdn switch-type basic-qsig
 isdn point-to-point-setup
 isdn incoming-voice voice
 isdn sending-complete
!
interface BRI0/1/1:0
 shutdown
 isdn switch-type basic-net3
 isdn timer T310 120000
 isdn point-to-point-setup
 isdn incoming-voice voice
!
interface BRI0/1/2:0
 isdn switch-type basic-net3
 isdn point-to-point-setup
 isdn incoming-voice voice
!
interface BRI0/1/3:0
 isdn switch-type basic-net3
 isdn point-to-point-setup
 isdn incoming-voice voice
!
ip default-gateway 1.43.0.1
no ip http server
ip http authentication local
ip http secure-server
ip forward-protocol nd
ip pim rp-address 8.8.8.1
ip tftp source-interface GigabitEthernet0
ip tftp blocksize 8192
ip route 0.0.0.0 0.0.0.0 1.2.0.1
ip route 223.255.254.0 255.255.255.0 1.2.0.1
ip route vrf Mgmt-intf 223.255.254.254 255.255.255.255 1.43.0.1
ip ssh bulk-mode 131072
!
!
!
!
!
!
!
control-plane
!
!
voice-port 0/1/0
 no echo-cancel enable
!
voice-port 0/1/1
 no echo-cancel enable
!
voice-port 0/1/2
!
voice-port 0/1/3
!
voice-port 0/2/0
 no echo-cancel enable
 shutdown
!
voice-port 0/2/1
 no echo-cancel enable
 shutdown
!
voice-port 0/2/2
!
voice-port 0/2/3
!
voice-port 0/3/0
!
voice-port 0/3/1
!
voice-port 0/3/2
!
voice-port 0/3/3
 shutdown
!
voice-port 0/3/4
!
voice-port 0/3/5
!
voice-port 1/0/0
 cptone AU
 connection plar 650
 station-id name sanjose
 station-id number 0123456789
 caller-id enable
 caller-id alerting ring 2
!
voice-port 1/0/1
 cptone AU
 caller-id enable
 caller-id alerting ring 2
!
voice-port 1/0/2
 no echo-cancel enable
!
voice-port 1/0/3
!
voice-port 1/0/4
!
voice-port 1/0/5
!
voice-port 1/0/6
!
voice-port 1/0/7
!
voice-port 1/0/8
!
voice-port 1/0/9
!
voice-port 1/0/10
!
voice-port 1/0/11
!
voice-port 1/0/12
!
voice-port 1/0/13
!
voice-port 1/0/14
!
voice-port 1/0/15
!
voice-port 1/0/16
!
voice-port 1/0/17
!
mgcp behavior rsip-range tgcp-only
mgcp behavior comedia-role none
mgcp behavior comedia-check-media-src disable
mgcp behavior comedia-sdp-force disable
!
mgcp profile default
!
!
!
!
dial-peer voice 1001 pots
 destination-pattern 550
 port 1/0/0
!
dial-peer voice 2001 pots
 destination-pattern 650
 port 1/0/1
!
!
!
line con 0
 exec-timeout 0 0
 stopbits 1
line aux 0
line vty 0 4
 exec-timeout 0 0
 login
 transport input ssh
line vty 5 14
 login
 transport input ssh
!
!
!
!
!
!
!
end


------------------ show parameter-map type inspect ------------------



------------------ show parameter-map type inspect-global ------------------



------------------ show parameter-map type inspect-vrf ------------------



------------------ show parameter-map type inspect-zone ------------------



------------------ show policy-map type inspect ------------------



------------------ show policy-map type inspect zone-pair ------------------



------------------ show class-map type inspect ------------------



------------------ show zone security ------------------



------------------ show zone-pair security ------------------



------------------ show policy-firewall stats global ------------------



------------------ show policy-firewall stats vrf ------------------



------------------ show policy-firewall stats zone ------------------



------------------ show platform hardware qfp active feature firewall memory ------------------

FW not init


------------------ show platform hardware qfp standby feature firewall memory ------------------



------------------ show platform hardware qfp active feature firewall runtime ------------------

FW not init


------------------ show platform hardware qfp standby feature firewall runtime ------------------



------------------ show platform hardware qfp active feature firewall datapath rg 0 ------------------

rg 0, rg_state 0x00010000 (Transport Down, Flow Off, Allow New Sessions) 
	4 (Active Solo) ha_handle 0x00000000 rg_flags 0x0

==== HA general stat ====
Initial bulksync retry count                                               0
Allocated retry entries                                                    0
Current retry queue depth                                                  0
Maximum queued retries                                                     0
Max retries queued ever                                                    0
  Stats were all zero

==== HA active stat ====
  Stats were all zero

==== HA standby stat ====
  Stats were all zero


------------------ show platform hardware qfp standby feature firewall datapath rg 0 ------------------



------------------ show platform hardware qfp active feature firewall drop ------------------


FW not init


------------------ show platform hardware qfp standby feature firewall drop ------------------



------------------ show platform hardware qfp active feature firewall client stat ------------------

Zonepair table entry count: 0
Filler block count: 0
Action block count: 0
L7 params block count: 0
Statistics table count: 0
Statistics block count: 0
Class name table entry count: 0
Number of vrf interfaces with zone: 0
Number of zoned interfaces: 0
Number of zones: 0
Number of zone pairs with policy: 0
Number of AVC policy: 0
Inspect parameter map count: 0
Multi-tenancy: No
Pending Multi-tenancy: No
VRF related objects: 
	VRF-ParameterMap count: 0, 
	VRF-ParameterMap Binding count: 0, 
	VRF stats: 0, 
	VRF drop stats: 0
Zone related objects: 
	Zone-ParameterMap count: 0, 
	Zone-ParameterMap Binding count: 0
SCB pool: 
	number of entries: 0, 
	entry limit: 0, 
	size: 0, 
	number of additions: 0
Synflood Hostdb pool: 
	number of entries: 0, 
	entry limit: 0, size: 0, 
	number of additions: 0
Session Teardown pool: 
	number of entries: 0, 
	entry limit: 0, 
	size: 0, number of additions: 0
Syncookie Destination pool: 
	number of entries: 0, 
	entry limit: 0, 
	size: 0, number of additions: 0
Errors: 
	Failed to zero global drop stats: 0, 
	Failed to allocate drop stats: 0, 
	Failed to zero global resource stats: 0, 
	Failed to allocate resource stats: 0, 
	Failed to walk vrf domains: 0, 
	Failed to re-enable firewall: 0, 
	Failed to disable firewall: 0, 
	Failed to allocate clear command buffer: 0, 
	Failed to send clear session IPC: 0


------------------ show platform hardware qfp standby feature firewall client stat ------------------



------------------ show platform hardware qfp active feature firewall client l7 policy all ------------------


L7 policies summary
Table entry count: 0


------------------ show platform hardware qfp standby feature firewall client l7 policy all ------------------



------------------ show platform software firewall FP active bindings ------------------



------------------ show platform software firewall FP standby bindings ------------------



------------------ show platform software firewall FP active pairs ------------------



------------------ show platform software firewall FP standby pairs ------------------



------------------ show platform software firewall FP active parameter-maps ------------------



------------------ show platform software firewall FP standby parameter-maps ------------------



------------------ show platform software firewall FP active statistics ------------------


Forwarding Manager Firewall Statistics

Zones:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-pairs:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Inspect Parameter-Maps:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

PAMs(Port Application Mapping):
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

VRF Bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-vpn-bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)



------------------ show platform software firewall FP standby statistics ------------------



------------------ show platform software firewall FP active zones ------------------



------------------ show platform software firewall FP standby zones ------------------



------------------ show platform software firewall RP active bindings ------------------



------------------ show platform software firewall RP standby bindings ------------------



------------------ show platform software firewall RP active pairs ------------------



------------------ show platform software firewall RP standby pairs ------------------



------------------ show platform software firewall RP active parameter-maps ------------------



------------------ show platform software firewall RP standby parameter-maps ------------------



------------------ show platform software firewall RP active statistics ------------------


Forwarding Manager Firewall Statistics

Zones:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-pairs:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Inspect Parameter-Maps:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

PAMs(Port Application Mapping):
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

VRF Bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)

Zone-vpn-bindings:
  0 Adds (0 errors), 0 Mods (0 errors), 0 Deletes (0 errors)
  0 Downloads (0 errors)



------------------ show platform software firewall RP standby statistics ------------------



------------------ show platform software firewall RP active zones ------------------



------------------ show platform software firewall RP standby zones ------------------



------------------ show geo status ------------------



------------------ show platform hardware qfp active feature geo client info ------------------

Geo DB disabled



------------------ show platform hardware qfp active feature geo client stats ------------------

CPP client Geo DB stats
-----------------------
  Enable received            : 0
  Modify received            : 0
  Disable received           : 0
  Enable failed              : 0
  Modify failed              : 0
  Disable failed             : 0
  IPv4 table write failed    : 0
  Persona write failed       : 0
  Country table write failed : 0


------------------ show platform hardware qfp active feature geo client country all ------------------


Country code     ISO-3 code       Country name                              Continent code   Continent name   Ref count        
-----------------------------------------------------------------------------------------------------------------------------
0                ?                unknown                                   0                **               0                
4                afg              afghanistan                               4                as               0                
8                alb              albania                                   5                eu               0                
10               ata              antarctica                                2                an               0                
12               dza              algeria                                   1                af               0                
16               asm              american samoa                            3                oc               0                
20               and              andorra                                   5                eu               0                
24               ago              angola                                    1                af               0                
28               atg              antigua and barbuda                       6                na               0                
31               aze              azerbaijan                                4                as               0                
32               arg              argentina                                 7                sa               0                
36               aus              australia                                 3                oc               0                
40               aut              austria                                   5                eu               0                
44               bhs              bahamas                                   6                na               0                
48               bhr              bahrain                                   4                as               0                
50               bgd              bangladesh                                4                as               0                
51               arm              armenia                                   4                as               0                
52               brb              barbados                                  6                na               0                
56               bel              belgium                                   5                eu               0                
60               bmu              bermuda                                   6                na               0                
64               btn              bhutan                                    4                as               0                
68               bol              bolivia                                   7                sa               0                
70               bih              bosnia and herzegovina                    5                eu               0                
72               bwa              botswana                                  1                af               0                
74               bvt              bouvet island                             2                an               0                
76               bra              brazil                                    7                sa               0                
84               blz              belize                                    6                na               0                
86               iot              british indian ocean territory            4                as               0                
90               slb              solomon islands                           3                oc               0                
92               vgb              british virgin islands                    6                na               0                
96               brn              brunei darussalam                         4                as               0                
100              bgr              bulgaria                                  5                eu               0                
104              mmr              myanmar                                   4                as               0                
108              bdi              burundi                                   1                af               0                
112              blr              belarus                                   5                eu               0                
116              khm              cambodia                                  4                as               0                
120              cmr              cameroon                                  1                af               0                
124              can              canada                                    6                na               0                
132              cpv              cape verde                                1                af               0                
136              cym              cayman islands                            6                na               0                
140              caf              central african republic                  1                af               0                
144              lka              sri lanka                                 4                as               0                
148              tcd              chad                                      1                af               0                
152              chl              chile                                     7                sa               0                
156              chn              china                                     4                as               0                
158              twn              taiwan province of china                  4                as               0                
162              cxr              christmas island                          3                oc               0                
166              cck              cocos (keeling) islands                   3                oc               0                
170              col              colombia                                  7                sa               0                
174              com              comoros                                   1                af               0                
175              myt              mayotte                                   1                af               0                
178              cog              congo                                     1                af               0                
180              cod              democratic republic of the congo          1                af               0                
184              cok              cook islands                              3                oc               0                
188              cri              costa rica                                6                na               0                
191              hrv              croatia                                   5                eu               0                
192              cub              cuba                                      6                na               0                
196              cyp              cyprus                                    5                eu               0                
203              cze              czech republic                            5                eu               0                
204              ben              benin                                     1                af               0                
208              dnk              denmark                                   5                eu               0                
212              dma              dominica                                  6                na               0                
214              dom              dominican republic                        6                na               0                
218              ecu              ecuador                                   7                sa               0                

Country code     ISO-3 code       Country name                              Continent code   Continent name   Ref count        
-----------------------------------------------------------------------------------------------------------------------------
222              slv              el salvador                               6                na               0                
226              gnq              equatorial guinea                         1                af               0                
231              eth              ethiopia                                  1                af               0                
232              eri              eritrea                                   1                af               0                
233              est              estonia                                   5                eu               0                
234              fro              faroe islands                             5                eu               0                
238              flk              falkland islands (malvinas)               7                sa               0                
239              sgs              south georgia / south sandwich isl        7                sa               0                
242              fji              fiji                                      3                oc               0                
246              fin              finland                                   5                eu               0                
248              ala              aland islands                             5                eu               0                
250              fra              france                                    5                eu               0                
254              guf              french guiana                             7                sa               0                
258              pyf              french polynesia                          3                oc               0                
260              atf              french southern territories               2                an               0                
262              dji              djibouti                                  1                af               0                
266              gab              gabon                                     1                af               0                
268              geo              georgia                                   5                eu               0                
270              gmb              gambia                                    1                af               0                
275              pse              palestinian territories                   4                as               0                
276              deu              germany                                   5                eu               0                
288              gha              ghana                                     1                af               0                
292              gib              gibraltar                                 5                eu               0                
296              kir              kiribati                                  3                oc               0                
300              grc              greece                                    5                eu               0                
304              grl              greenland                                 6                na               0                
308              grd              grenada                                   6                na               0                
312              glp              guadeloupe                                6                na               0                
316              gum              guam                                      3                oc               0                
320              gtm              guatemala                                 6                na               0                
324              gin              guinea                                    1                af               0                
328              guy              guyana                                    7                sa               0                
332              hti              haiti                                     6                na               0                
334              hmd              heard and mc donald islands               3                oc               0                
336              vat              holy see (vatican city state)             5                eu               0                
340              hnd              honduras                                  6                na               0                
344              hkg              hong kong                                 4                as               0                
348              hun              hungary                                   5                eu               0                
352              isl              iceland                                   5                eu               0                
356              ind              india                                     4                as               0                
360              idn              indonesia                                 4                as               0                
364              irn              iran (islamic republic of)                4                as               0                
368              irq              iraq                                      4                as               0                
372              irl              ireland                                   5                eu               0                
376              isr              israel                                    4                as               0                
380              ita              italy                                     5                eu               0                
384              civ              cote d ivoire                             1                af               0                
388              jam              jamaica                                   6                na               0                
392              jpn              japan                                     4                as               0                
398              kaz              kazakhstan                                4                as               0                
400              jor              jordan                                    4                as               0                
404              ken              kenya                                     1                af               0                
408              prk              north korea                               4                as               0                
410              kor              south korea                               4                as               0                
414              kwt              kuwait                                    4                as               0                
417              kgz              kyrgyzstan                                4                as               0                
418              lao              lao peoples democratic republic           4                as               0                
422              lbn              lebanon                                   4                as               0                
426              lso              lesotho                                   1                af               0                
428              lva              latvia                                    5                eu               0                
430              lbr              liberia                                   1                af               0                
434              lby              libyan arab jamahiriya                    1                af               0                
438              lie              liechtenstein                             5                eu               0                
440              ltu              lithuania                                 5                eu               0                

Country code     ISO-3 code       Country name                              Continent code   Continent name   Ref count        
-----------------------------------------------------------------------------------------------------------------------------
442              lux              luxembourg                                5                eu               0                
446              mac              macau                                     4                as               0                
450              mdg              madagascar                                1                af               0                
454              mwi              malawi                                    1                af               0                
458              mys              malaysia                                  4                as               0                
462              mdv              maldives                                  4                as               0                
466              mli              mali                                      1                af               0                
470              mlt              malta                                     5                eu               0                
474              mtq              martinique                                6                na               0                
478              mrt              mauritania                                1                af               0                
480              mus              mauritius                                 1                af               0                
484              mex              mexico                                    6                na               0                
492              mco              monaco                                    5                eu               0                
496              mng              mongolia                                  4                as               0                
498              mda              moldova                                   5                eu               0                
499              mne              montenegro                                5                eu               0                
500              msr              montserrat                                6                na               0                
504              mar              morocco                                   1                af               0                
508              moz              mozambique                                1                af               0                
512              omn              oman                                      4                as               0                
516              nam              namibia                                   1                af               0                
520              nru              nauru                                     3                oc               0                
524              npl              nepal                                     4                as               0                
528              nld              netherlands                               5                eu               0                
530              ant              netherlands antilles                      6                na               0                
531              cuw              curacao                                   6                na               0                
533              abw              aruba                                     6                na               0                
534              sxm              sint maarten                              6                na               0                
535              bes              bonaire/sint eustatius/saba               6                na               0                
540              ncl              new caledonia                             3                oc               0                
548              vut              vanuatu                                   3                oc               0                
554              nzl              new zealand                               3                oc               0                
558              nic              nicaragua                                 6                na               0                
562              ner              niger                                     1                af               0                
566              nga              nigeria                                   1                af               0                
570              niu              niue                                      3                oc               0                
574              nfk              norfolk island                            3                oc               0                
578              nor              norway                                    5                eu               0                
580              mnp              northern mariana islands                  3                oc               0                
581              umi              us minor outlying islands                 3                oc               0                
583              fsm              federated states of micronesia            3                oc               0                
584              mhl              marshall islands                          3                oc               0                
585              plw              palau                                     3                oc               0                
586              pak              pakistan                                  4                as               0                
591              pan              panama                                    6                na               0                
598              png              papua new guinea                          3                oc               0                
600              pry              paraguay                                  7                sa               0                
604              per              peru                                      7                sa               0                
608              phl              philippines                               4                as               0                
612              pcn              pitcairn                                  3                oc               0                
616              pol              poland                                    5                eu               0                
620              prt              portugal                                  5                eu               0                
624              gnb              guinea-bissau                             1                af               0                
626              tls              timor-leste                               4                as               0                
630              pri              puerto rico                               6                na               0                
634              qat              qatar                                     4                as               0                
638              reu              reunion                                   1                af               0                
642              rou              romania                                   5                eu               0                
643              rus              russian federation                        5                eu               0                
646              rwa              rwanda                                    1                af               0                
652              blm              saint barthelemy                          6                na               0                
654              shn              st. helena                                1                af               0                
659              kna              saint kitts and nevis                     6                na               0                
660              aia              anguilla                                  6                na               0                

Country code     ISO-3 code       Country name                              Continent code   Continent name   Ref count        
-----------------------------------------------------------------------------------------------------------------------------
662              lca              saint lucia                               6                na               0                
663              maf              saint martin                              6                na               0                
666              spm              st. pierre and miquelon                   6                na               0                
670              vct              saint vincent and the grenadines          6                na               0                
674              smr              san marino                                5                eu               0                
678              stp              sao tome and principe                     1                af               0                
682              sau              saudi arabia                              4                as               0                
686              sen              senegal                                   1                af               0                
688              srb              serbia                                    5                eu               0                
690              syc              seychelles                                1                af               0                
694              sle              sierra leone                              1                af               0                
702              sgp              singapore                                 4                as               0                
703              svk              slovakia (slovak republic)                5                eu               0                
704              vnm              viet nam                                  4                as               0                
705              svn              slovenia                                  5                eu               0                
706              som              somalia                                   1                af               0                
710              zaf              south africa                              1                af               0                
716              zwe              zimbabwe                                  1                af               0                
724              esp              spain                                     5                eu               0                
728              ssd              south sudan                               1                af               0                
732              esh              western sahara                            1                af               0                
736              sdn              sudan                                     1                af               0                
740              sur              suriname                                  7                sa               0                
744              sjm              svalbard and jan mayen islands            5                eu               0                
748              swz              swaziland                                 1                af               0                
752              swe              sweden                                    5                eu               0                
756              che              switzerland                               5                eu               0                
760              syr              syrian arab republic                      4                as               0                
762              tjk              tajikistan                                4                as               0                
764              tha              thailand                                  4                as               0                
768              tgo              togo                                      1                af               0                
772              tkl              tokelau                                   3                oc               0                
776              ton              tonga                                     3                oc               0                
780              tto              trinidad and tobago                       6                na               0                
784              are              united arab emirates                      4                as               0                
788              tun              tunisia                                   1                af               0                
792              tur              turkey                                    5                eu               0                
795              tkm              turkmenistan                              4                as               0                
796              tca              turks and caicos islands                  6                na               0                
798              tuv              tuvalu                                    3                oc               0                
800              uga              uganda                                    1                af               0                
804              ukr              ukraine                                   5                eu               0                
807              mkd              macedonia                                 5                eu               0                
818              egy              egypt                                     1                af               0                
826              gbr              united kingdom                            5                eu               0                
831              ggy              guernsey                                  5                eu               0                
832              jey              jersey                                    5                eu               0                
833              imn              isle of man                               5                eu               0                
834              tza              tanzania                                  1                af               0                
840              usa              united states                             6                na               0                
850              vir              us virgin islands                         6                na               0                
854              bfa              burkina faso                              1                af               0                
858              ury              uruguay                                   7                sa               0                
860              uzb              uzbekistan                                4                as               0                
862              ven              venezuela                                 7                sa               0                
876              wlf              wallis and futuna islands                 3                oc               0                
882              wsm              samoa                                     3                oc               0                
887              yem              yemen                                     4                as               0                
894              zmb              zambia                                    1                af               0                
994              asi              asia (unknown country)                    4                as               0                
995              eur              europe (unknown country)                  5                eu               0                
999              ***              reserved/private                          0                **               0                


------------------ show platform hardware qfp active feature geo datapath memory ------------------


Table-Name   Address      Size     
-----------------------------------------
Country DB   0p0x0          0              
IPV4 DB      0p0x0          0              


------------------ show platform hardware qfp active feature geo datapath stats ------------------

GEO Stats:
	lookup hit: 0
	lookup miss: 0
	error ip table: 0
	error country table: 0
	country table hit: 0
	country table miss: 0


------------------ show platform hardware qfp active feature dns-snoop-agent datapath stats ------------------

DNS Snoop Agent Stats:
  parser unknown pkt: 0
  parser not needed: 0
  parser fmt error: 0
  parser pa error: 0
  parser non resp: 0
  parser multiple name: 0
  parser dns name err: 0
  parser matched ip: 0
  parser redirect: 0
  parser whitelist redirect: 0
  parser blacklist redirect: 0
  parser invalid redirect ip: 0
  parser skip: 0
  regex locked: 0
  regex not matched: 0
  pkt drop whitelist no redirect ip: 0
  pkt drop blacklist no redirect ip: 0
  entries in use: 0
  ip cache allocation fail: 0
  ip addr add: 0
  ip addr update: 0
  ip addr delete: 0
  ip addr cache hit: 0
  ip addr cache miss: 0
  ip addr bad param: 0
  ip addr delete not found: 0
  ip cache not initialized: 0


------------------ show platform hardware qfp active feature dns-snoop-agent datapath regexp-table ------------------

DSA not init


------------------ show platform hardware qfp active feature dns-snoop-agent datapath ip-cache all ------------------

DSA not initialized


------------------ show platform hardware qfp active feature dns-snoop-agent datapath memory ------------------

DSA not init


------------------ show platform hardware qfp active feature dns-snoop-agent client info ------------------


Number of patterns added/deleted/total: 0/0/0
Number of re_table rebuilt: 0
Number of str_table rebuilt: 0
Registered clients: 0x00000000
Number of transaction started/ended: 0/0
Memory pool size/limit: 0/0
Pending Deletion Pattern List:



------------------ show platform hardware qfp active feature dns-snoop-agent client pattern-list ------------------



------------------ show platform hardware qfp active feature dns-snoop-agent client hw-pattern-list ------------------



------------------ show platform hardware qfp active classification class-group-manager object-group all ------------------""",
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_firewall(self.device, '400')
        self.assertIn(
            'show tech-support firewall',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = True
        self.assertEqual(result, expected_output)

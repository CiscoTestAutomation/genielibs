"""Common verify functions for macsec"""

# Python
import logging
import re
import time

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)

def verify_mka_session(device, intf, status, ckn=None, timeout=160, status2=None):
    ''' To Verify MKA MACsec sessioN
        Args:
            device ('obj'): device to use
            intf   ('str'): interface details
            status ('str'): status of MKA
            ckn    ('str'): ckn of mka
            timeout('int'): timeout value
            status2('str'): expected status of MKA
        Returns:
            result (`bool`): Verified result
        Raises:
            SubCommandFailure
    '''
    timeout = Timeout(timeout, interval = 10, disable_log = False)
    result = 0
    while timeout.iterate():
        try:
            converted_interface = Common.convert_intf_name(intf)
            mka_out = device.parse('show mka sessions interface '
                '{interface} detail'.format(interface=converted_interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if mka_out['sessions']['status'].lower() == status.lower():
            if ckn is not None:
                if mka_out['sessions']['ckn'] == ckn:
                    log.info('Mka CKN is %s'%(ckn))
                    log.info('Mka CKN value matched')
                else:
                    log.info('Mka CKN should be %s'%(ckn))
                    log.info('Mka CKN is %s'%(mka_out['sessions']['ckn']))
                    log.error('Mka CKN verification failed')
                    result+=1    

            if status2:
                if mka_out['sessions']['status'].lower() == status.lower():
                    result=0
                else:
                    log.info('Mka status should be %s'%(status))
                    log.info('Mka status is %s'%(mka_out['sessions']['status']))
                    result+=1 

            if result==0:
                return True
        timeout.sleep()

    return False
   
def verify_macsec_session(device, intf1, intf2, cipher, vlan, access, conf, count):
    ''' To fetch and verify MACsec session details
        Args:
            device ('obj'): device to use
            intf1 ('str'): interface details
            intf2 ('str'): interface details
            cipher ('str'): cipher details
            Vlan ('str'): dot1q Vlan details
            access ('str'): Access control details
            conf ('int'): conf offset details
            count ('int'): Number of packets
        Returns:
            result (`bool`): Verified result
        Raises:
            SubCommandFailure
    '''

    result = 0
    if intf2:
       interface = [intf1,intf2]
    else:
       interface = [intf1]
    for intf in interface:
         try:
             out1 = device.parse(
                 'show macsec interface {}'.format(intf))
         except Exception as e:
             log.info('Macsec session verification failed. Error:\n{e}'.format(e))
             return False
         if out1['macsec-data']['cipher'].lower() == cipher.lower():
             log.info("MACsec cipher value  %s " %(cipher))
             log.info('Macsec cipher value is successfully verified')
         else:
             log.info("MACsec cipher value is not %s " %(cipher))
             log.error('Macsec cipher value verification failed')
             result+=1

         if int(out1['macsec-data']['confidentiality-offset']) == int(conf):
             log.info("MACsec confidentiality offset value %s " %(conf))
             log.info('Macsec confidentiality offset value is '
                         'successfully verified')
         else:
             log.info("MACsec confidentiality offset value is not %s " %(conf))
             log.error('Macsec confidentiality offset '
                      'value verification failed')
             result+=1

         if out1['access-control'].lower() == access.lower():
             log.info("MACsec access control  %s " %(access))
             log.info('Macsec access control value '
                      'is successfully verified')
         else:
             log.info("MACsec access control is not %s " %(access))
             log.error('Macsec access control value verification failed')
             result+=1

         if int(out1['transmit-secure-channels']['current-an']) >= 0 and int(
                 out1['transmit-secure-channels']['current-an']) <=3:
             log.info('Macsec current an value is successfully verified')
         else:
             log.error('Macsec current an value verification failed')
             result+=1

         if out1['transmit-secure-channels']['previous-an'] == '-' or \
                 int(out1['transmit-secure-channels']['previous-an']) >= 0:
             log.info('Macsec previous an value is successfully verified')
         else:
             log.error('Macsec previous an value verification failed')
             result+=1
         if int(out1['transmit-secure-channels']['sc-statistics'][
                 'encrypted-bytes']) >= 0:
             log.info('Macsec sc-encrypted-bytes value is '
                  'successfully verified')
         else:
             log.error('Macsec sc-encrypted-bytes value verification failed')
             result+=1

         if int(out1['transmit-secure-channels']['sc-statistics'][
                     'encrypted-pkts']) >= 0:
             log.info('Macsec sc-encrypted-pkts value is successfully verified')
         else:
             log.error('Macsec sc-encrypted-bytes value verification failed')
             result+=1

         if int(out1['transmit-secure-channels']['sc-statistics'][
                     'encrypted-pkts']) >= 0:
             log.info('Macsec sc-encrypted-pkts value is successfully verified')
         else:
             log.error('Macsec sc-encrypted-pkts value verification failed')
             result+=1
         sc_Tx_En_byte=int(out1['transmit-secure-channels']['sc-statistics'][
                     'encrypted-bytes'])
         log.info('Macsec TX sc-Enc-bytes value is %s'%(sc_Tx_En_byte))

         sa_Tx_En_byte=int(out1['transmit-secure-channels']['sa-statistics'][
                     'encrypted-bytes'])
         log.info('Macsec TX sa-Enc-bytes value is %s'%(sa_Tx_En_byte))

         TX_Enc_byte = sc_Tx_En_byte+sa_Tx_En_byte
         if TX_Enc_byte > 0:
             log.info('Macsec TX sc and sa-encrypted-bytes successfully verified %s'%(TX_Enc_byte))
         else:
             log.error('Macsec TX sc and sa-encrypted-bytes value verification failed %s'%(TX_Enc_byte))
             result+=1

         sc_Tx_En_pkt=int(out1['transmit-secure-channels']['sc-statistics'][
                     'encrypted-pkts'])

         sa_Tx_En_pkt=int(out1['transmit-secure-channels']['sa-statistics'][
                     'encrypted-pkts'])
         TX_Enc_pkt = sc_Tx_En_pkt+sa_Tx_En_pkt
         if TX_Enc_pkt > count:
             log.info('Macsec TX sc and sa-encrypted-pkts value is successfully verified %s'%(TX_Enc_pkt))
         else:
             log.error('Macsec TX sc and sa-encrypted-pkts value verification failed %s'%(TX_Enc_pkt))
             result+=1

         sci = [val for val in out1['receive-secure-channels'].keys()][0]
         sc_decrypted_bytes = int(out1['receive-secure-channels'][sci]['sc-statistics']['decrypted-bytes'])
         log.info('Macsec RX sc-decrypted_bytes value is %s'%(sc_decrypted_bytes))

         sa_decrypted_bytes = int(out1['receive-secure-channels'][sci]['sa-statistics']['decrypted-bytes'])
         log.info('Macsec RX sa-decrypted_bytes value is %s'%(sa_decrypted_bytes))


         Rx_decrypted_bytes = sc_decrypted_bytes+sa_decrypted_bytes
         if Rx_decrypted_bytes > count:
             log.info('Macsec RX sc and sa-decrypted-bytes successfully verified %s'%(Rx_decrypted_bytes))
         else:
             log.error('Macsec RX sc and sa-decrypted-bytes value verification failed %s'%(Rx_decrypted_bytes))
             result+=1

         Sc_value = int(out1['receive-secure-channels'][sci]['sc-statistics']['valid-pkts'])
         log.info('Macsec RX sc-Valid-pkts value is %s'%(Sc_value))
         Sa_value = int(out1['receive-secure-channels'][sci]['sa-statistics']['valid-pkts'])
         log.info('Macsec RX sa-Valid-pkts value is %s'%(Sa_value))
         RX_Valid = Sc_value+Sa_value
         if RX_Valid  > count:
             log.info('Macsec RX sc and sa-Valid-pkts value is successfully verified %s'%(RX_Valid))
         else:
             log.error('Macsec RX sc and sa-Valid-pkts value verification failed %s'%(RX_Valid))
             result+=1
         if result != 0:
             log.error('Macsec Traffic counters failed')
             return False
    return True

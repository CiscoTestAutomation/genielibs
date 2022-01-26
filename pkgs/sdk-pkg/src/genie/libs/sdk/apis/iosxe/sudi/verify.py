"""Common verify functions for sudi"""
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_cmca3_certificates(
    device, max_time=15, check_interval=5
):
    """ Verify cmca3 certificates in show platform sudi pki 
        Args:
            device ('obj'): Device object
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    out = None
    try:
        out = device.parse("show platform sudi pki")
    except SchemaEmptyParserError:
        pass
    if out:
        if (out.q.contains_key_value('.*certificate','Enab.*',value_regex=True,key_regex=True) 
            and out.q.contains_key_value('.*III','Valid',key_regex=True) 
            and out.q.contains_key_value('.*SHA2','Valid',key_regex=True)):
            return True
        else:
            log.error("Certificates validation failed")
            return False
    else:
        log.error("cli is not parsed")
        return False
            
def verify_crypto_entropy_status(
    device, status, max_time=15, check_interval=5
):
    """ Verify crypto entropy status in show crypto entropy status
        Args:
            device ('obj'): Device object
            status ('list'): Expected status #['ACT-2','randfill','getrandombytes']
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    out = None
    try:
        out = device.parse("show crypto entropy status")
    except SchemaEmptyParserError:
        pass
    if out:
        for i in range(1,len(status)+1):
            if (out.q.contains("entropies").contains(i).contains_key_value("source",status[i-1]) 
                and out.q.contains("entropies").contains(i).contains_key_value("status","Working")):
                return True
            else:
                log.error("Entropy {name} not working".format(name=status[i-1]))
                return False
    else:
        log.error("cli is not parsed")
        return False

def verify_crypto_pki_certificate(
    device, cert_status, max_time=15, check_interval=5
):
    """ Verify pki certificates in show crypto pki certificates 
        Args:
            device ('obj'): Device object
            cert_status('list'): Expected output #["Cisco Manufacturing CA III","Cisco Manufacturing CA SHA2"]
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    try:
        out2 = device.parse("show crypto pki certificates CISCO_IDEVID_SUDI_LEGACY")
        out1 = device.parse("show crypto pki certificates CISCO_IDEVID_SUDI")
    except SchemaEmptyParserError:
        pass
    if out1 and out2:
        if (out2.q.contains("trustpoints").contains("CISCO_IDEVID_SUDI_LEGACY").contains("certificate").contains("issuer").contains_key_value("cn",cert_status[1])
           and out1.q.contains("trustpoints").contains("CISCO_IDEVID_SUDI").contains("certificate").contains("issuer").contains_key_value("cn",cert_status[0])) :
            return True
        else:
            log.error("Primary and secondary certificate is not 2099 and 2037")
            return False
    else:
        log.error("cli is not parsed")
        return False
            
def verify_hw_auth_status(
    device, max_time=15, check_interval=5
):
    """ Verify hardware authentication status in show platform hardware authentication status 
        Args:
            device ('obj'): Device object
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    try:
        out = device.parse('show platform hardware authentication status')
    except SchemaEmptyParserError:
        pass
    if out:
        if out.q.contains_key_value(".*Authentication","pass|Not Available",key_regex=True,value_regex=True):
            return True
        else:
            log.error('The hardware authentication has failed')
            return False
    else:
        log.error("cli is not parsed")
        return False

def verify_sudi_cert(
    device, sign_nonce, max_time=15, check_interval=5
):
    """ Verify sudi certificate status in show platform sudi certificate or show platform sudi certificate sign nonce xxx
        Args:
            device ('obj'): Device object
            sign_nonce ('str'): input from user #"123"
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """

    try:
        if sign_nonce!="0":
            out = device.parse("show platform sudi certificate sign nonce {sign_nonce}".format(sign_nonce=sign_nonce))
        else:
            out = device.parse("show platform sudi certificate")
    except SchemaEmptyParserError:
        pass
    if out:
        if (out.q.contains("certificates").contains(1).contains("MIIDIT.*XbFg==",regex=True)
            and out.q.contains("certificates").contains(2).contains("MIIEZz.*PW2/U",regex=True)): 
            return True
        else:
            log.error("Primary certificate is not crca2099.pem and Secondary certificate is not hasudi.pem")
            return False
    else:
        log.error("cli is not parsed")  
        return False 

def verify_sudi_pki(
    device, status, max_time=15, check_interval=5
):
    """ Verify cert present  in show platform sudi pki
        Args:
            device ('obj'): Device object
            status ('str'): Expected output 
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """
    try:
        out = device.parse("show platform sudi pki")
    except SchemaEmptyParserError:
        pass
    if out:
        if (out.q.contains_key_value(".*certificate",status,key_regex=True)
           and out.q.contains_key_value("Cisco Manufacturing CA","Valid")
           and out.q.contains_key_value("Cisco Manufacturing CA III","Valid")
           and out.q.contains_key_value("Cisco Manufacturing CA SHA2","Valid")):
           return True
        else:
            log.error("Certificates validation failed")
            return False
    else:
        log.error("cli is not parsed")
        return False

def verify_Parser_Encrypt_decrypt_File_Status(
    device, status, max_time=15, check_interval=5
):
    """ Verify parser encryption decryption status in show parser encrypt file status
        Args:
            device ('obj'): Device object
            status ('list'): Expected output # ["Cipher text",True,"ver1"]
            max_time ('int'): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result (`bool`): Verified result
    """

    try:
        out = device.parse("show parser encrypt file status")
    except SchemaEmptyParserError:
        pass
    if out:
        res=[]
        res.extend(out.q.get_values("file_format"))
        res.extend(out.q.get_values("feature"))
        res.extend(out.q.get_values("encryption_version"))
        if set(res)==set(status):
            return True
        else:
            log.error("encrypt status failed")
            return False
    else:
        log.error("cli is not parsed")
        return False
        
def verify_hardware_slot(
    device, slot, max_time=300, check_interval=30
):
    """ Verify hardware slot exists

        Args:
            device (`obj`): Device object
            slot (`list`): hardware slot with LC and SUP # ["C9600X-SUP-2","C9600-LC-24C"]
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result (`bool`): Verified result
    """

    try:
        out = device.parse("show platform")
    except SchemaEmptyParserError:
        pass
    if out:
        if (out.q.contains("slot").contains(slot[0]).contains_key_value("state","ok, active") 
           and out.q.contains("slot").contains(slot[1]).contains_key_value("state","ok")):
           return True
        else:
            log.error("LC/SUP not available")
            return False
    else:
        log.error("cli is not parsed")
        return False


        
 
  

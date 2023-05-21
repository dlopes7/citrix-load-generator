import winreg


def create_registry_citrix_session(session_id: int,
                                   client_address: str,
                                   client_name: str,
                                   ctx_session_key: str,
                                   published_name: str,
                                   user_name: str):
    """
    Only used for testing purposes, creates a fake Citrix session in the registry
    """
    hkey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Citrix\Ica\Session\{session_id}\Connection")
    winreg.SetValueEx(hkey, "ClientAddress", 0, winreg.REG_SZ, client_address)
    winreg.SetValueEx(hkey, "ClientName", 0, winreg.REG_SZ, client_name)
    winreg.SetValueEx(hkey, "CtxSessionKey", 0, winreg.REG_SZ, ctx_session_key)
    winreg.SetValueEx(hkey, "PublishedName", 0, winreg.REG_SZ, published_name)
    winreg.SetValueEx(hkey, "UserName", 0, winreg.REG_SZ, user_name)
    winreg.CloseKey(hkey)


def delete_registry_citrix_session(session_id: int):
    """
    Only used for testing purposes, deletes a fake Citrix session in the registry
    """
    winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Citrix\Ica\Session\{session_id}\Connection")

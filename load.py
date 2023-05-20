import time

import wmi

from models import constants
from models.clientconnect import ClientConnect
from models.logontimings import LogonTimings
from models.session import Session
from models.clientstartup import ClientStartup
from registry import create_citrix_session, delete_citrix_session


def create_full_session():
    client_connect = ClientConnect.generate_random_client()
    session = Session.generate_random_session(client_connect)
    client_startup = ClientStartup.generate_random_client_startup(client_connect)
    logon_timings = LogonTimings(session)

    # Add the session details to the registry
    create_citrix_session(session.session_id,
                          client_connect.ip,
                          session.client_name,
                          session.session_key,
                          session.published_name,
                          client_connect.username
                          )

    # order is VERY important
    logon_timings.send()
    client_connect.send()
    session.send()
    client_startup.send()

    time.sleep(60)

    delete_citrix_session(session.session_id)
    session.delete()


def delete_all():
    namespaces = {
        r"root\citrix\euem": ["Citrix_Euem_ClientConnect", "Citrix_Euem_RoundTrip", "Citrix_Euem_ClientStartup"],
        r"root\citrix\hdx": ["Citrix_Sessions"],
        r"root\citrix\profiles\Metrics": ["LogonTimings"],
    }
    for namespace, classes in namespaces.items():
        try:
            wmi_connection = wmi.WMI(namespace=namespace)
            for wmi_class in classes:
                count = 0
                for instance in wmi_connection.query(f"SELECT * FROM {wmi_class}"):
                    instance.Delete_()
                    count += 1
                print(f"Deleted {count} instances of {namespace}/{wmi_class}")
        except:
            pass


def create_namespaces():
    import win32com

    # Need to do this to get root
    loc = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    svc = loc.ConnectServer(".", "root")
    root = wmi.WMI(wmi=svc)

    # Create citrix namespace
    citrix = root.new("__NAMESPACE")
    citrix.Name = "Citrix"
    citrix.put()

    # Create namespaces under citrix
    namespaces = ["Euem", "hdx", "Profiles", "VdaParameters"]
    citrix = wmi.WMI(namespace="root\Citrix")
    for namespace in namespaces:
        n = citrix.new("__NAMESPACE")
        n.Name = namespace
        n.put()

    # Create Metrics namespace
    profiles = wmi.WMI(namespace="root\Citrix\Profiles")
    m = profiles.new("__NAMESPACE")
    m.Name = "Metrics"
    m.put()

    # Create Euem classes
    euem = wmi.GetObject("winmgmts:root\citrix\EUEM")

    print("Creating Citrix_Euem_ClientConnect")
    cls = euem.Get()
    cls.Path_.Class = "Citrix_Euem_ClientConnect"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("ProcessId", constants.wbemCimtypeString)
    cls.Properties_("ProcessId").Qualifiers_.add("key", True)
    cls.Properties_.add("InstanceId", constants.wbemCimtypeString)
    cls.Properties_("InstanceId").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("UserName", constants.wbemCimtypeString)
    cls.Properties_.add("ClientMachineIP", constants.wbemCimtypeString)
    cls.Properties_.add("ClientMachineName", constants.wbemCimtypeString)
    cls.Properties_.add("WinstationName", constants.wbemCimtypeString)
    cls.Properties_.add("EUEMVersion", constants.wbemCimtypeString)
    cls.Properties_.add("PassthroughClientSessionId", constants.wbemCimtypeString)
    cls.Properties_.add("PassthroughClientSessionTimestamp", constants.wbemCimtypeString)
    cls.Put_()

    print("Creating Citrix_Euem_RoundTrip")
    cls = euem.Get()
    cls.Path_.Class = "Citrix_Euem_RoundTrip"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("ProcessId", constants.wbemCimtypeString)
    cls.Properties_("ProcessId").Qualifiers_.add("key", True)
    cls.Properties_.add("InstanceId", constants.wbemCimtypeString)
    cls.Properties_("InstanceId").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("RoundtripTime", constants.wbemCimtypeUint32)
    cls.Properties_.add("InputBandwidthAvailable", constants.wbemCimtypeUint32)
    cls.Properties_.add("InputBandwidthUsed", constants.wbemCimtypeUint32)
    cls.Properties_.add("OutputBandwidthAvailable", constants.wbemCimtypeUint32)
    cls.Properties_.add("OutputBandwidthUsed", constants.wbemCimtypeUint32)
    cls.Properties_.add("NetworkLatency", constants.wbemCimtypeUint32)
    cls.Properties_.add("TriggerRoundtripDuration", constants.wbemCimtypeUint32)
    cls.Properties_.add("FirstDrawRoundtripDuration", constants.wbemCimtypeUint32)
    cls.Properties_.add("FrameCutRoundtripDuration", constants.wbemCimtypeUint32)
    cls.Properties_.add("FrameSendRoundtripDuration", constants.wbemCimtypeUint32)
    cls.Properties_.add("WDTriggerRoundtripDuration", constants.wbemCimtypeUint32)
    cls.Put_()

    print("Creating Citrix_Euem_ClientStartup")
    cls = euem.Get()
    cls.Path_.Class = "Citrix_Euem_ClientStartup"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("ProcessId", constants.wbemCimtypeString)
    cls.Properties_("ProcessId").Qualifiers_.add("key", True)
    cls.Properties_.add("InstanceId", constants.wbemCimtypeString)
    cls.Properties_("InstanceId").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("ApplicationName", constants.wbemCimtypeString)
    cls.Properties_.add("LaunchType", constants.wbemCimtypeString)
    cls.Properties_.add("IsSharedSession", constants.wbemCimtypeBoolean)
    cls.Properties_.add("SCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("AECD", constants.wbemCimtypeSint32)
    cls.Properties_.add("COCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("RECD", constants.wbemCimtypeSint32)
    cls.Properties_.add("REWD", constants.wbemCimtypeSint32)
    cls.Properties_.add("NRCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("NRWD", constants.wbemCimtypeSint32)
    cls.Properties_.add("TRWD", constants.wbemCimtypeSint32)
    cls.Properties_.add("LPWD", constants.wbemCimtypeSint32)
    cls.Properties_.add("IFDCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("SLCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("SCCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("CFDCD", constants.wbemCimtypeSint32)
    cls.Properties_.add("BUCC", constants.wbemCimtypeSint32)
    cls.Properties_.add("WfIcaTimestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("ClientSendTimestamp", constants.wbemCimtypeDateTime)
    cls.Put_()

    print("Creating Citrix_Euem_ClientDisconnect")
    cls = euem.Get()
    cls.Path_.Class = "Citrix_Euem_ClientDisconnect"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("ProcessId", constants.wbemCimtypeString)
    cls.Properties_("ProcessId").Qualifiers_.add("key", True)
    cls.Properties_.add("InstanceId", constants.wbemCimtypeString)
    cls.Properties_("InstanceId").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("UserName", constants.wbemCimtypeString)
    cls.Properties_.add("WinstationName", constants.wbemCimtypeString)
    cls.Put_()

    print("Creating Citrix_Euem_ServerStartup")
    cls = euem.Get()
    cls.Path_.Class = "Citrix_Euem_ServerStartup"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("ProcessId", constants.wbemCimtypeString)
    cls.Properties_("ProcessId").Qualifiers_.add("key", True)
    cls.Properties_.add("InstanceId", constants.wbemCimtypeString)
    cls.Properties_("InstanceId").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("CASD", constants.wbemCimtypeUint32)
    cls.Properties_.add("CONSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("COSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("DMSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("EndTime", constants.wbemCimtypeDateTime)
    cls.Properties_.add("LESD", constants.wbemCimtypeUint32)
    cls.Properties_.add("PCSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("PLSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("PNCOSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("SCSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("SSSD", constants.wbemCimtypeUint32)
    cls.Properties_.add("StartTime", constants.wbemCimtypeDateTime)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Put_()

    hdx = wmi.GetObject("winmgmts:root\citrix\hdx")

    print("Creating Citrix_Sessions")
    cls = hdx.Get()
    cls.Path_.Class = "Citrix_Sessions"
    cls.Properties_.add("SessionID", constants.wbemCimtypeUint32)
    cls.Properties_("SessionID").Qualifiers_.add("key", True)
    cls.Properties_.add("SessionKey", constants.wbemCimtypeString)  # - String
    cls.Properties_("SessionKey").Qualifiers_.add("key", True)
    cls.Properties_.add("Timestamp", constants.wbemCimtypeDateTime)
    cls.Properties_.add("AppNames", constants.wbemCimtypeString, True)  # - String []
    cls.Properties_.add("AppState", constants.wbemCimtypeUint32)  # - UInt32
    cls.Properties_.add("ClientIP", constants.wbemCimtypeString)  # - String
    cls.Properties_.add("ClientName", constants.wbemCimtypeString)  # - String
    cls.Properties_.add("EncryptionLevel", constants.wbemCimtypeSint32)  # - SInt32
    cls.Properties_.add("IsBrokered", constants.wbemCimtypeBoolean)  # - Boolean
    cls.Properties_.add("IsHDXProtocolUDP", constants.wbemCimtypeBoolean)  # - Boolean
    cls.Properties_.add("IsPublishedApp", constants.wbemCimtypeBoolean)  # - Boolean
    cls.Properties_.add("LastError", constants.wbemCimtypeSint32)  # - String
    cls.Properties_.add("ProductID", constants.wbemCimtypeSint32)  # - SInt32
    cls.Properties_.add("PublishedName", constants.wbemCimtypeString)  # - String
    cls.Properties_.add("State", constants.wbemCimtypeSint32)  # - SInt32
    cls.Properties_.add("StationName", constants.wbemCimtypeString)  # - String
    cls.Properties_.add("Supported", constants.wbemCimtypeBoolean)  # - Boolean
    cls.Put_()

    print("Creating LogonTimings")
    metrics = wmi.GetObject("winmgmts:root\citrix\Profiles\Metrics")
    cls = metrics.Get()
    cls.Path_.Class = "LogonTimings"
    cls.Properties_.add("SessionId", constants.wbemCimtypeString)
    cls.Properties_("SessionId").Qualifiers_.add("key", True)
    cls.Properties_.add("DesktopReady", constants.wbemCimtypeDateTime)
    cls.Properties_.add("GroupPolicyComplete", constants.wbemCimtypeDateTime)
    cls.Properties_.add("GroupPolicyStart", constants.wbemCimtypeDateTime)
    cls.Properties_.add("LogonScriptsComplete", constants.wbemCimtypeDateTime)
    cls.Properties_.add("LogonScriptsStart", constants.wbemCimtypeDateTime)
    cls.Properties_.add("ProfileLoaded", constants.wbemCimtypeDateTime)
    cls.Properties_.add("ProfileLoadStart", constants.wbemCimtypeDateTime)
    cls.Properties_.add("UserInitComplete", constants.wbemCimtypeDateTime)
    cls.Properties_.add("UserInitStart", constants.wbemCimtypeDateTime)
    cls.Put_()


def main():
    delete_all()
    create_namespaces()
    create_full_session()


if __name__ == "__main__":
    main()

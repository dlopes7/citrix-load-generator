"""
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

class LogonTimings:

    def __init__(self, session: Session):
        self.session_id = session.session_key

        now = datetime.now()
        self.desktop_ready = now + timedelta(seconds=10)
        self.group_policy_complete = now + timedelta(seconds=9)
        self.group_policy_start = now + timedelta(seconds=1)
        self.logon_scripts_complete = now + timedelta(seconds=8)
        self.logon_scripts_start = now + timedelta(seconds=2)
        self.profile_loaded = now + timedelta(seconds=7)
        self.profile_load_start = now + timedelta(seconds=3)
        self.user_init_complete = now + timedelta(seconds=6)
        self.user_init_start = now + timedelta(seconds=4)

        self.namespace = wmi.WMI(namespace=r"root\citrix\Profiles\Metrics")
        self.wmi_instance = None

    def send(self):
        logon_timings_class = self.namespace.LogonTimings
        logon_timings_instance = logon_timings_class.SpawnInstance_()
        logon_timings_instance.SessionId = self.session_id

        logon_timings_instance.DesktopReady = self.desktop_ready.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.GroupPolicyComplete = self.group_policy_complete.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.GroupPolicyStart = self.group_policy_start.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.LogonScriptsComplete = self.logon_scripts_complete.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.LogonScriptsStart = self.logon_scripts_start.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.ProfileLoaded = self.profile_loaded.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.ProfileLoadStart = self.profile_load_start.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.UserInitComplete = self.user_init_complete.strftime(WMI_DATE_FORMAT)
        logon_timings_instance.UserInitStart = self.user_init_start.strftime(WMI_DATE_FORMAT)
        logon_timings_path = logon_timings_instance.Put_()
        print(f"Created LogonTimings: '{logon_timings_path.Path}'")
        self.wmi_instance = logon_timings_instance
"""
import random
from datetime import datetime, timedelta
from uuid import uuid4

import wmi

from models.constants import WMI_DATE_FORMAT
from models.session import Session


class ServerStartup:
    def __init__(self, session: Session):

        now = datetime.now()
        self.session_id: int = session.session_id
        self.process_id: str = f"{random.randint(1000, 2000)}"
        self.instance_id: str = f"{uuid4()}"
        self.start_time: datetime = now
        self.end_time: datetime = now + timedelta(seconds=random.randint(8, 10))
        self.timestamp: datetime = now
        self.casd: int = random.randint(1, 2)
        self.consd: int = random.randint(3, 4)
        self.cosd: int = random.randint(5, 6)
        self.dmsd: int = random.randint(7, 8)
        self.lesd: int = random.randint(9, 10)
        self.pcsd: int = random.randint(11, 12)
        self.plsd: int = random.randint(13, 14)
        self.pncosd: int = random.randint(15, 16)
        self.scsd: int = random.randint(17, 18)
        self.sssd: int = random.randint(19, 20)

        self.namespace = wmi.WMI(namespace=r"root\citrix\euem")

    def send(self):

        server_startup_class = self.namespace.Citrix_Euem_ServerStartup
        server_startup_instance = server_startup_class.SpawnInstance_()

        server_startup_instance.SessionId = self.session_id
        server_startup_instance.ProcessId = self.process_id
        server_startup_instance.InstanceId = self.instance_id
        server_startup_instance.StartTime = self.start_time.strftime(WMI_DATE_FORMAT)
        server_startup_instance.EndTime = self.end_time.strftime(WMI_DATE_FORMAT)
        server_startup_instance.Timestamp = self.timestamp.strftime(WMI_DATE_FORMAT)
        server_startup_instance.CASD = self.casd
        server_startup_instance.CONSD = self.consd
        server_startup_instance.COSD = self.cosd
        server_startup_instance.DMSD = self.dmsd
        server_startup_instance.LESD = self.lesd
        server_startup_instance.PCSD = self.pcsd
        server_startup_instance.PLSD = self.plsd
        server_startup_instance.PNCOSD = self.pncosd
        server_startup_instance.SCSD = self.scsd
        server_startup_instance.SSSD = self.sssd

        server_startup_path = server_startup_instance.Put_()
        print(f"Created ServerStartup: '{server_startup_path.Path}'")
        self.wmi_instance = server_startup_instance

    def delete(self):
        self.wmi_instance.Delete_()

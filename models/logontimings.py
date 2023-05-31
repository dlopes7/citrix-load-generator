from datetime import datetime, timedelta

import wmi

from models.constants import WMI_DATE_FORMAT
from models.session import Session


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

    def delete(self):
        self.wmi_instance.Delete_()


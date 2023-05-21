"""
import random
import uuid

import wmi

from models.clientconnect import ClientConnect


class Session:
    def __init__(self):
        self.app_names = None
        self.app_state = None
        self.client_ip = None
        self.client_name = None
        self.encryption_level = None
        self.is_brokered = None
        self.is_published_app = None
        self.last_error = None
        self.product_id = None
        self.published_name = None
        self.session_id = None
        self.session_key = None
        self.state = None
        self.station_name = None
        self.supported = None
        self.namespace = wmi.WMI(namespace="root\citrix\hdx")

    @staticmethod
    def generate_random_session(client: ClientConnect):
        s = Session()
        s.app_names = [""]
        s.app_state = 1
        s.client_ip = client.ip
        s.client_name = client.machine
        s.encryption_level = 0
        s.is_brokered = False
        s.is_published_app = False
        s.last_error = None
        s.product_id = None
        s.published_name = random.choice(["Notepad", "Firefox"])
        s.session_id = client.session_id
        s.session_key = str(uuid.uuid4())
        s.state = 0
        s.station_name = client.win_station
        s.supported = True

        return s

    def send(self):
        session_class = self.namespace.Citrix_Sessions
        session_instance = session_class.SpawnInstance_()

        session_instance.SessionID = self.session_id
        session_instance.SessionKey = self.session_key
        session_instance.StationName = self.station_name
        session_instance.State = self.state
        session_instance.ClientName = self.client_ip
        session_instance.ClientIP = self.client_ip
        session_instance.ProductID = self.product_id
        session_instance.EncryptionLevel = self.encryption_level
        session_instance.IsBrokered = self.is_brokered
        session_instance.IsPublishedApp = self.is_published_app
        session_instance.AppState = self.app_state
        session_instance.AppNames = self.app_names
        session_instance.PublishedName = self.published_name
        session_path = session_instance.Put_()
        print(f"Created Session: '{session_path.Path}'")
        self.wmi_instance = session_instance

    def delete(self):
        self.wmi_instance.Delete_()
"""
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


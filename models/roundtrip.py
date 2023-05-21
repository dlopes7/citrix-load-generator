"""
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

    def send(self):
        logon_timings_class = self.namespace.LogonTimings
        logon_timings_instance = logon_timings_class.SpawnInstance_()
        logon_timings_instance.SessionId = self.session_id

        print(self.desktop_ready.strftime(WMI_DATE_FORMAT))
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

import wmi

from models.constants import WMI_DATE_FORMAT
from models.session import Session


class Roundtrip:

    def __init__(self, session: Session):
        self.session_id = session.session_id

        self.timestamp = datetime.now()
        self.roundtrip_time = random.randint(80, 100)
        self.input_bandwidth_available = random.randint(200, 300)
        self.input_bandwidth_used = self.input_bandwidth_available * 0.3
        self.output_bandwidth_available = random.randint(200, 300)
        self.output_bandwidth_used = self.output_bandwidth_available * 0.3
        self.network_latency = random.randint(40, 80)
        self.trigger_roundtrip_duration = random.randint(20, 60)
        self.first_draw_roundtrip_duration = random.randint(20, 60)
        self.frame_cut_roundtrip_duration = random.randint(20, 60)
        self.frame_send_roundtrip_duration = random.randint(20, 60)
        self.wd_trigger_roundtrip_duration = random.randint(20, 60)

        self.namespace = wmi.WMI(namespace="root\\citrix\\euem")
        self.wmi_instance = None

    def send(self):
        roundtrip_class = self.namespace.Citrix_Euem_RoundTrip
        roundtrip_instance = roundtrip_class.SpawnInstance_()
        roundtrip_instance.SessionID = self.session_id
        roundtrip_instance.ProcessId = "1234"
        roundtrip_instance.InstanceId = "1234"
        roundtrip_instance.Timestamp = self.timestamp.strftime(WMI_DATE_FORMAT)
        roundtrip_instance.RoundtripTime = self.roundtrip_time
        roundtrip_instance.InputBandwidthAvailable = self.input_bandwidth_available
        roundtrip_instance.InputBandwidthUsed = self.input_bandwidth_used
        roundtrip_instance.OutputBandwidthAvailable = self.output_bandwidth_available
        roundtrip_instance.OutputBandwidthUsed = self.output_bandwidth_used
        roundtrip_instance.NetworkLatency = self.network_latency
        roundtrip_instance.TriggerRoundtripDuration = self.trigger_roundtrip_duration
        roundtrip_instance.FirstDrawRoundtripDuration = self.first_draw_roundtrip_duration
        roundtrip_instance.FrameCutRoundtripDuration = self.frame_cut_roundtrip_duration
        roundtrip_instance.FrameSendRoundtripDuration = self.frame_send_roundtrip_duration
        roundtrip_instance.WDTriggerRoundtripDuration = self.wd_trigger_roundtrip_duration
        roundtrip_path = roundtrip_instance.Put_()
        print(f"Created Roundtrip: '{roundtrip_path.Path}'")
        self.wmi_instance = roundtrip_instance




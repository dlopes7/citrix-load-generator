import random
from datetime import datetime

import wmi

from models.clientconnect import ClientConnect


class ClientStartup:
    def __init__(self):

        self.aecd = None
        self.application_name = None
        self.bucc = None
        self.cfdcd = None
        self.client_send_timestamp = None
        self.cocd = None
        self.ifdcd = None
        self.instance_id = None
        self.is_shared_session = None
        self.launch_type = None
        self.lpwd = None
        self.nrcd = None
        self.nrwd = None
        self.process_id = None
        self.recd = None
        self.rewd = None
        self.sccd = None
        self.scd = None
        self.session_id = None
        self.slcd = None
        self.timestamp = None
        self.trwd = None
        self.wflca_timestamp = None

        self.namespace = wmi.WMI(namespace="root\citrix\euem")

    @staticmethod
    def generate_random_client_startup(client: ClientConnect):
        c = ClientStartup()

        """
        AECD:0 ApplicationName:VLC media player BUCC:0 CFDCD:0
         ClientSendTimestamp:2020-06-02 17:15:35.928 +0000 UTC
          COCD:0 IFDCD:0 InstanceId:3848 IsSharedSession:false LaunchType:WI LPWD:110 NRCD:0 NRWD:63 
          ProcessId:3d067a2b-b316-450c-95ba-279c61c36faa 
          RECD:0 REWD:0 SCCD:1970 SCD:0 SessionID:4 SLCD:1 Timestamp:2020-06-02 17:15:48.434 +0000 UTC TRWD:1 WflcaTimestamp:2020-06-02 19:15:51.9811014 +0200 CEST m=+4747.835592501
        """
        c.aecd = 0
        c.application_name = random.choice(["Notepad", "Firefox", "SAP", "VSCode"])
        c.bucc = 0
        c.cfdcd = 0
        c.client_send_timestamp = datetime.now().strftime("%Y%m%d%H%M%S.000000")
        c.cocd = 0
        c.ifdcd = 0
        c.is_shared_session = False
        c.launch_type = "WI"
        c.lpwd = 110
        c.nrcd = 0
        c.nrwd = 6
        c.recd = 0
        c.rewd = 0
        c.sccd = 1970
        c.scd = 0
        c.session_id = client.session_id
        c.slcd = 1
        c.trwd = 1
        c.wflca_timestamp = datetime.now().strftime("%Y%m%d%H%M%S.000000")

        return c

    def send(self):
        client_startup_class = self.namespace.Citrix_Euem_ClientStartup
        client_startup_instance = client_startup_class.SpawnInstance_()

        client_startup_instance.SessionID = self.session_id
        client_startup_instance.ApplicationName = self.application_name
        client_startup_instance.LaunchType = self.launch_type
        client_startup_instance.IsSharedSession = self.is_shared_session
        client_startup_instance.SCD = self.scd
        client_startup_instance.AECD = self.aecd
        client_startup_instance.COCD = self.cocd
        client_startup_instance.RECD = self.recd
        client_startup_instance.REWD = self.rewd
        client_startup_instance.NRCD = self.nrcd
        client_startup_instance.NRWD = self.nrwd
        client_startup_instance.TRWD = self.trwd
        client_startup_instance.LPWD = self.lpwd
        client_startup_instance.IFDCD = self.ifdcd
        client_startup_instance.SLCD = self.slcd
        client_startup_instance.SCCD = self.sccd
        client_startup_instance.CFDCD = self.cfdcd
        client_startup_instance.BUCC = self.bucc
        client_startup_path = client_startup_instance.Put_()
        print(f"Created ClientStartup: '{client_startup_path.Path}'")
        self.wmi_instance = client_startup_instance

    def delete(self):
        self.wmi_instance.Delete_()

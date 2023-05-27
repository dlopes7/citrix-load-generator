import random
from datetime import datetime
from uuid import uuid4

import wmi

from models.clientconnect import ClientConnect
from models.constants import WMI_DATE_FORMAT


class ClientStartup:
    def __init__(self, client: ClientConnect):

        self.aecd = 0
        self.application_name = random.choice(["Notepad", "Firefox", "SAP", "VSCode"])
        self.bucc = 0
        self.cfdcd = 0
        self.client_send_timestamp = datetime.now()
        self.cocd = 0
        self.ifdcd = 0
        self.instance_id = str(uuid4())
        self.is_shared_session = False
        self.launch_type = random.choice(["WI", "RDP", "ICA"])
        self.lpwd = 110
        self.nrcd = 0
        self.nrwd = 63
        self.process_id = str(uuid4())
        self.recd = 0
        self.rewd = 0
        self.sccd = 1970
        self.scd = 0
        self.session_id = client.session_id
        self.slcd = 1
        self.timestamp = datetime.now()
        self.trwd = 1
        self.wflca_timestamp = datetime.now()

        self.namespace = wmi.WMI(namespace="root\citrix\euem")


    def send(self):
        client_startup_class = self.namespace.Citrix_Euem_ClientStartup
        client_startup_instance = client_startup_class.SpawnInstance_()

        client_startup_instance.SessionID = self.session_id
        client_startup_instance.ApplicationName = self.application_name
        client_startup_instance.LaunchType = self.launch_type
        client_startup_instance.IsSharedSession = self.is_shared_session
        client_startup_instance.Timestamp = self.timestamp.strftime(WMI_DATE_FORMAT)
        client_startup_instance.InstanceID = self.instance_id
        client_startup_instance.ProcessID = self.process_id
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

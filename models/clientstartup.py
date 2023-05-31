import random
from datetime import datetime
from uuid import uuid4

import wmi

from models.clientconnect import ClientConnect
from models.constants import WMI_DATE_FORMAT


class ClientStartup:
    def __init__(self, client: ClientConnect):
        self.session_id = client.session_id
        self.application_name = random.choice(["Notepad", "Firefox", "SAP", "VSCode"])
        self.client_send_timestamp = datetime.now()
        self.instance_id = str(uuid4())
        self.is_shared_session = False
        self.launch_type = random.choice(["WI", "RDP", "ICA"])
        self.timestamp = datetime.now()
        self.wflca_timestamp = datetime.now()
        self.process_id = str(uuid4())

        self.aecd = random.randint(1, 2)
        self.bucc = random.randint(3, 4)
        self.cfdcd = random.randint(5, 6)
        self.cocd = random.randint(7, 8)
        self.ifdcd = random.randint(9, 10)
        self.lpwd = random.randint(11, 12)
        self.nrcd = random.randint(13, 14)
        self.nrwd = random.randint(15, 16)
        self.recd = random.randint(17, 18)
        self.rewd = random.randint(19, 20)
        self.sccd = random.randint(21, 22)
        self.slcd = random.randint(23, 24)
        self.trwd = random.randint(25, 26)
        self.scd = random.randint(27, 28)

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

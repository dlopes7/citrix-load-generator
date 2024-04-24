from uuid import uuid4

import wmi
import random
from datetime import datetime, timedelta

from models.constants import WMI_DATE_FORMAT


class ClientConnect:
    def __init__(self):

        self.username = random.choice(["david", "mike", "jai", "diego"])
        self.ip = f"191.254.171.{random.randint(1, 254)}"
        self.machine = f"{self.username}-machine"
        self.win_station = f"{self.username}-win-station"
        self.euem_version = 3
        self.passthrough_client_session_id = 0
        self.passthrough_client_session_timestamp = 0
        self.session_id = random.randint(1, 5)
        self.timestamp = datetime.now() - timedelta(hours=1)

        self.wmi_instance = None

        self.namespace = wmi.WMI(namespace="root\citrix\EUEM")

    def send(self):
        client_connect_class = self.namespace.Citrix_Euem_ClientConnect
        client_connect_instance = client_connect_class.SpawnInstance_()
        client_connect_instance.InstanceId = f"{uuid4()}"
        client_connect_instance.ProcessId = f"{random.randint(1, 1000)}"
        client_connect_instance.SessionID = self.session_id
        client_connect_instance.UserName = self.username
        client_connect_instance.ClientMachineIP = self.ip
        client_connect_instance.ClientMachineName = self.machine
        client_connect_instance.WinstationName = self.win_station
        client_connect_instance.EUEMVersion = self.euem_version
        client_connect_instance.PassthroughClientSessionId = self.passthrough_client_session_id
        client_connect_instance.PassthroughClientSessionTimestamp = self.passthrough_client_session_timestamp
        client_connect_instance.Timestamp = self.timestamp.strftime(WMI_DATE_FORMAT)

        client_connect_path = client_connect_instance.Put_()
        print(f"Created ClientConnect: '{client_connect_path.Path}'")
        self.wmi_instance = client_connect_instance

    def delete(self):
        self.wmi_instance.Delete_()

import wmi
import random
from datetime import datetime
import uuid
import time


class ClientConnect:
    def __init__(self):

        self.ip = None
        self.machine = None
        self.euem_version = None
        self.InstanceId = None
        self.passthrough_client_session_id = None
        self.passthrough_client_session_timestamp = None
        self.process_id = None
        self.session_id = None
        self.timestamp = None
        self.username = None
        self.win_station = None

        self.wmi_instance = None

        self.namespace = wmi.WMI(namespace="root\citrix\EUEM")

    def send(self):
        client_connect_class = self.namespace.Citrix_Euem_ClientConnect
        client_connect_instance = client_connect_class.SpawnInstance_()
        client_connect_instance.SessionID = self.session_id
        client_connect_instance.UserName = self.username
        client_connect_instance.ClientMachineIP = self.ip
        client_connect_instance.ClientMachineName = self.machine
        client_connect_instance.WinstationName = self.win_station
        client_connect_instance.EUEMVersion = self.euem_version
        client_connect_instance.PassthroughClientSessionId = self.passthrough_client_session_id
        client_connect_instance.PassthroughClientSessionTimestamp = self.passthrough_client_session_timestamp
        client_connect_instance.Timestamp = self.timestamp

        client_connect_path = client_connect_instance.Put_()
        print(f"Created ClientConnect: '{client_connect_path.Path}'")
        self.wmi_instance = client_connect_instance

    @staticmethod
    def generate_random_client():
        c = ClientConnect()
        c.username = random.choice(["david", "mike", "jai", "diego"])
        c.ip = f"191.254.171.{random.randint(1, 254)}"
        c.machine = f"{c.username}-machine"
        c.win_station = f"{c.username}-win-station"
        c.euem_version = 3
        c.InstanceId = random.randint(1, 1000)
        c.passthrough_client_session_id = 0
        c.passthrough_client_session_timestamp = 0
        c.session_id = random.randint(1, 9000)
        # 2006 01 02 15 04 05 . 000000
        # c.timestamp = datetime.now().strftime("%Y%m%d%H%M%S.000000")

        return c

    def delete(self):
        self.wmi_instance.Delete_()

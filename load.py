import time

import wmi

from models.clientconnect import ClientConnect
from models.session import Session
from models.clientstartup import ClientStartup


def create_full_session():
    client_connect = ClientConnect.generate_random_client()
    session = Session.generate_random_session(client_connect)
    client_startup = ClientStartup.generate_random_client_startup(client_connect)

    client_connect.send()
    session.send()
    client_startup.send()

    time.sleep(1)

    session.delete()


def delete_all():
    namespaces = {
        "root\citrix\euem": ["Citrix_Euem_ClientConnect", "Citrix_Euem_RoundTrip", "Citrix_Euem_ClientStartup"],
        "root\citrix\hdx": ["Citrix_Sessions"],
    }
    for namespace, classes in namespaces.items():
        wmi_connection = wmi.WMI(namespace=namespace)
        for wmi_class in classes:
            count = 0
            for instance in wmi_connection.query(f"SELECT * FROM {wmi_class}"):
                instance.Delete_()
                count += 1
            print(f"Deleted {count} instances of {namespace}/{wmi_class}")


def main():
    delete_all()
    while True:
        create_full_session()
        time.sleep(10)


if __name__ == "__main__":
    main()

import random
import sys
import time

import logging
log = logging.getLogger(__name__)
st = logging.StreamHandler()
log.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s ")
st.setFormatter(fmt)
log.addHandler(st)


from models.serverstartup import ServerStartup
from state import delete_all, create_namespaces
from models.clientconnect import ClientConnect
from models.logontimings import LogonTimings
from models.roundtrip import Roundtrip
from models.session import Session
from models.clientstartup import ClientStartup
from models.vdaparameters import VDAParameters
from registry import create_registry_citrix_session, delete_registry_citrix_session


def create_vda_parameters():
    vda_parameters = VDAParameters()
    vda_parameters.send()


def create_full_session():

    log.info("--- Session Start ---")
    client_connect = ClientConnect()
    session = Session.generate_random_session(client_connect)
    client_startup = ClientStartup(client_connect)
    logon_timings = LogonTimings(session)
    server_startup = ServerStartup(session)

    # Add the session details to the registry
    create_registry_citrix_session(session.session_id,
                                   client_connect.ip,
                                   session.client_name,
                                   session.session_key,
                                   session.published_name,
                                   client_connect.username
                                   )

    # order is VERY important
    logon_timings.send()
    client_connect.send()
    server_startup.send()
    session.send()
    client_startup.send()

    roundtrip_measurements = []
    measurements_quantity = random.randint(1, 5)
    print(f"Creating {measurements_quantity} roundtrip measurements")
    for i in range(measurements_quantity):
        time.sleep(5)
        rt = Roundtrip(session)
        rt.send()
        roundtrip_measurements.append(rt)

    # Delete everything
    delete_registry_citrix_session(session.session_id)
    session.delete()
    client_connect.delete()
    client_startup.delete()
    logon_timings.delete()
    server_startup.delete()

    for rt in roundtrip_measurements:
        rt.delete()

    log.info("--- Session End ---")


def main():
    delete_all()
    create_namespaces()
    create_vda_parameters()
    while True:
        try:
            create_full_session()
        except KeyboardInterrupt:
            log.info("Exiting")
            sys.exit(0)

if __name__ == "__main__":
    main()

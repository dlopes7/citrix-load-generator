"""
    print("Creating CitrixVdaParameters")
    vda_params = wmi.GetObject("winmgmts:root\citrix\VdaParameters")
    cls = vda_params.Get()
    cls.Path_.Class = "CitrixVdaParameters"
    cls.Properties_.add("BrokerVersion", constants.wbemCimtypeString)
    cls.Properties_.add("DesktopCatalogName", constants.wbemCimtypeString)
    cls.Properties_.add("FarmName", constants.wbemCimtypeString)
    cls.Properties_.add("DesktopGroupName", constants.wbemCimtypeString)
    cls.Properties_.add("Desktopid", constants.wbemCimtypeString)
    cls.Put_()

"""
import wmi


class VDAParameters:

    def __init__(self):

        self.broker_version = "7.15"
        self.desktop_catalog_name = "Catalog 01"
        self.farm_name = "Citrix Lab"
        self.desktop_group_name = "Group 01"
        self.desktop_id = "Desktop 01"

        self.namespace = wmi.WMI(namespace=r"root\citrix\VdaParameters")
        self.wmi_instance = None

    def send(self):
        vda_params_class = self.namespace.CitrixVdaParameters
        vda_params_instance = vda_params_class.SpawnInstance_()
        vda_params_instance.BrokerVersion = self.broker_version
        vda_params_instance.DesktopCatalogName = self.desktop_catalog_name
        vda_params_instance.FarmName = self.farm_name
        vda_params_instance.DesktopGroupName = self.desktop_group_name
        vda_params_instance.Desktopid = self.desktop_id
        vda_params_path = vda_params_instance.Put_()
        print(f"Created VdaParameters: '{vda_params_path.Path}'")
        self.wmi_instance = vda_params_instance

    def delete(self):
        self.wmi_instance.Delete_()

import requests
import openpyxl
from config import Config


class nessus:
    def __init__(self):
        self.url = Config.URL
        self.request = requests.session()
        body = {"username": Config.Account, "password": Config.Password}
        res = self.request.post(f"{self.url}/session", json=body, verify=False)
        self.request.headers["X-Cookie"] = "token=" + res.json()["token"]
        self.uuid = "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66"

    def get_plugin_list(self):
        res = self.request.get(f"{self.url}/editor/scan/templates/{self.uuid}")
        plugin_list = list(res.json()["plugins"]["families"].keys())
        return plugin_list

    def get_plugin_id(self, plugin):
        res = self.request.get(f"{self.url}/editor/scan/templates/{self.uuid}")
        plugin_id = res.json()["plugins"]["families"][plugin]["id"]
        plugin_count = res.json()["plugins"]["families"][plugin]["count"]
        return plugin_id, plugin_count

    def get_subplugin_id(self, plugin):
        plugin_id, plugin_count = self.get_plugin_id(plugin)
        res = self.request.get(f"{self.url}/editor/scan/templates/{self.uuid}/families/{plugin_id}?")
        subplugin_id_list = []
        for i in range(plugin_count):
            subplugin_id_list.append(res.json()["plugins"][i]["id"])
        return plugin_id, subplugin_id_list

    def get_information(self, plugin):
        plugin_id, subplugin_id_list = self.get_subplugin_id(plugin)
        subplugin_name_list = []
        subplugin_synopsis_list = []
        subplugin_description_list = []
        subplugin_solution_list = []
        for i in subplugin_id_list:
            res = self.request.get(f"{self.url}/editor/scan/templates/{self.uuid}/families/{plugin_id}/plugins/{i}")
            subplugin_name_list.append(res.json()["plugindescription"]["pluginattributes"]["plugin_name"])
            subplugin_synopsis_list.append(res.json()["plugindescription"]["pluginattributes"]["synopsis"])
            subplugin_description_list.append(res.json()["plugindescription"]["pluginattributes"]["description"])
            subplugin_solution_list.append(res.json()["plugindescription"]["pluginattributes"]["solution"])

        workbook = openpyxl.Workbook()
        sheet = workbook.worksheets[0]
        sheet.column_dimensions["C"].width = 70.0
        sheet.column_dimensions["D"].width = 70.0
        sheet.column_dimensions["E"].width = 140.0
        sheet.column_dimensions["F"].width = 70.0
        sheet["A1"] = "Check"
        sheet["B1"] = "ID"
        sheet["C1"] = "Name"
        sheet["D1"] = "Synopsis"
        sheet["E1"] = "Description"
        sheet["F1"] = "Solution"
        for i in range(len(subplugin_id_list)):
            sheet[f"B{i+2}"] = subplugin_id_list[i]
        for i in range(len(subplugin_name_list)):
            sheet[f"C{i+2}"] = subplugin_name_list[i]
        for i in range(len(subplugin_synopsis_list)):
            sheet[f"D{i+2}"] = subplugin_synopsis_list[i]
        for i in range(len(subplugin_description_list)):
            sheet[f"E{i+2}"] = subplugin_description_list[i]
        for i in range(len(subplugin_solution_list)):
            sheet[f"F{i+2}"] = subplugin_solution_list[i]
        workbook.save(f"{plugin}.xlsx")


api = nessus()
# plugin_list = api.get_plugin_list()
api.get_information("MacOS X Local Security Checks")

import json
import glob
import csv
import pytz
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def parse_xml_file():
    xml_tree = ET.parse("test_payload1.xml")
    root = xml_tree.getroot()
    
    return xml_tree, root

def update_fields(xml_data, value:int, key:str):
    current_date = datetime.now().date()
    updated_date = current_date + timedelta(value)
    for i in xml_data.iter(key):
        i.text = str(updated_date).replace("-", "")

def update_depart_return(X:int, Y:int):
    xml_tree, xml_data = parse_xml_file()
    update_fields(xml_data, X, "DEPART")
    update_fields(xml_data, Y, "RETURN")
    xml_tree.write("updated_test_payload1.xml")

def load_json_file():
    with open("test_payload.json") as json_file:
        json_data = json.load(json_file)
        return json_data

def remove_json_element(element):
    json_data = load_json_file()
    fnc = lambda sub: { key1: fnc(val1) if isinstance(val1, dict) else val1
      for key1, val1 in sub.items() if key1 != element}
    result_json = fnc(json_data)
    with open("updated_test_payload.json", "w") as update_json_file:
        json.dump(result_json, update_json_file, indent=4)

def parse_jmeter_logs():
    jmeter_log_file = glob.glob("Jmeter_log*")
    for log_file in jmeter_log_file:
        with open(log_file) as _file:
            csv_data = csv.reader(_file)
            header = next(csv_data)
            for log in csv_data:
                if int(log[3]) != 200:
                    epoch_time = int(log[0]) / 1000 
                    converted_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch_time)))
                    print(converted_date, log[2], log[3], log[4], log[8])

def main():
    update_depart_return(5, 10)
    remove_json_element("appdate")
    parse_jmeter_logs()

if __name__ == "__main__":
    main()
import xml.etree.ElementTree as ET
import xlsxwriter

nsd = "http://www.tresos.de/_projects/DataModel2/06/data.xsd"
ns = "http://www.tresos.de/_projects/DataModel2/08/root.xsd" 
tree = ET.parse('smu.xdm')
root = tree.getroot()

workbook = xlsxwriter.Workbook('smu.xlsx')

titles = ["Alarm Name", 'FSP', "Internal"]
for set in root.findall(".//{{{0}}}ctr[@name='SmuAlarmGlobalConfig']/..".format(nsd)):
    set_name = set.attrib['name']
    worksheet = workbook.add_worksheet(name = set_name)
    row = column = 0
    worksheet.write_row(row,column, titles)
    row+=1
    print("--------------")
    for alm in set.findall(".//{{{0}}}ctr/{{{0}}}var[@name='SmuAlarmFSP']/..".format(nsd)):
        name, fsp, intbeh = alm.attrib['name'], alm.find(".//{{{0}}}var[@name='SmuAlarmFSP']".format(nsd)).attrib['value'],  alm.find(".//{{{0}}}var[@name='SmuAlarmIntBeh']".format(nsd)).attrib['value']
        worksheet.write_row(row, column, [name, fsp, intbeh])
        row+=1

        if fsp == 'SMU_ALARM_FSP_ENABLED':
            if intbeh != 'SMU_NMI_INT_ACTION':
                print(name, fsp, intbeh)
        if intbeh == 'SMU_NMI_INT_ACTION':
            if fsp != 'SMU_ALARM_FSP_ENABLED':
                print(name, fsp, intbeh)


workbook.close()

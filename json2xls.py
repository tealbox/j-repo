import pandas as pd

## json to excel conversion
import json
import xlsxwriter

############## Arg Parse
import argparse
parser = argparse.ArgumentParser(description ='CISCO ACI')
parser.add_argument("-if", "--inputFile")

args = parser.parse_args()
print(args.inputFile)

file0 = r'fvBD.json'

file0 = args.inputFile
file, extn = file0.split(".")

exlsFile = f'ACI_{file}.xlsx'
with open(file0, mode="r", encoding="utf-8") as jsonFile:
    data = json.load(jsonFile)

##print(json.dumps(data, indent=2))

totalCount = data['totalCount']
imdata = data['imdata']
key = list(data['imdata'][0].keys())[0]
l = []
for item in imdata:
    l.append(item[key].get("attributes","N/F"))

print(totalCount)
##
##
### Corrected the attribute name to dumps
##df_read_json = pd.read_json(json.dumps(data), orient='index')
##print("DataFrame using pd.read_json() method:")
##print(df_read_json)
##


col_names = sorted(item[key]["attributes"].keys())



df = pd.DataFrame(l, columns=col_names)
print("table in pandas dataframe:")
##print(df)


writer = pd.ExcelWriter(exlsFile, engine='xlsxwriter')
df.to_excel(writer, sheet_name=key)
# some modify in writer(the excel file)
##print("some manipulation")
# Get the xlsxwriter objects from the dataframe writer object.
# you can use it to manipulate the excel,
# for example, change a value, or add a photo, a chart, and formatting
# more information to check XlsxWriter
##workbook  = writer.book
##worksheet = writer.sheets[exlsFile]
### Add a bold format to use to highlight cells.
##bold = workbook.add_format({'bold': True})
##worksheet.write('F2', 'Manipulation', bold)
writer.close()
print(f"write to excel: {exlsFile}.xlsx")



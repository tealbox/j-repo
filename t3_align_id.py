#-------------------------------------------------------------------------------
# Name:        module1
#-------------------------------------------------------------------------------
from myXLS import *
from pathlib import Path
from pprint import pprint
from collections import OrderedDict
import json

def is_template_exist(gt, templateId):
    # gt is a list of dict
##    print("in TEst", templateId)
    for idx, item in enumerate(gt):
        if item.get('templateId', None) == templateId:
            return True, idx
    return False, None

def main():
    _ = Path(".")
    gs = _ / "gs_template.xlsx"
    t = OrderedDict("")
    t.setdefault("featureTemplateUidRange",[])
    t.setdefault("factoryDefault",False)
    wb = fast_openpyxl(gs)
    Sample = wb[1]["sheet_sandbox"]
    gt = []
    for line in Sample:
        templateName = line.get("TemplateName", None)
        if templateName == "None":
            templateName = ""
##        if str(templateName).lower == "false":
##            templateName = "false"
##        if str(templateName).lower == "true":
##            templateName = "true"

        if line["Section"] == "template" or line["Section"] == "Security Policy" or line["Section"] == "Policy":
                t.setdefault(line['Template'], templateName)
        else:
            # "templateType": "", "templateId": "" optional >> "subTemplates"
            if line['Sub-Template'] != 'None':
##                print("\t", line['Sub-Template'], line['SubTemplateName'])
                status, idx = is_template_exist(gt,templateName)
                if status:
                    if "subTemplates" in gt[idx]:
                        # add item
                        subt = gt[-1]['subTemplates']
                        subt.append({"templateType": line["Sub-Template"], "templateId": line["SubTemplateName"]})
                        gt[-1].update({'subTemplates':subt})
                        gt[-1].move_to_end("subTemplates", last = True)
                    else:
##                        print("GT[-1]", gt[-1])
                        gt[-1].setdefault("subTemplates", [{"templateType": line["Sub-Template"], "templateId": line["SubTemplateName"]}])
                        gt[-1].move_to_end("subTemplates", last = True)
##                        print("After GT[-1]", gt[-1])

            else:
                gt.append(OrderedDict({"templateType": line["Template"], "templateId": templateName}))

##    pprint(t)
##    pprint(gt)
    t.setdefault("generalTemplates", gt)
    pprint(t)
    print(json.dumps(t))

if __name__ == '__main__':
    main()

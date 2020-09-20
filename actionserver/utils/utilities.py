from datetime import datetime
import json
def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestampStr
def getJsonFileAsDict(filePath):
    with open(filePath,"r") as f:
        return json.load(f)
def saveDictAsJsonFile(dictData,filePath):
    with open("./../"+filePath,"w") as f:
        json.dump(dictData,f,indent = 4)
        return True

        
def product_info(product_name, category):
    with open(r'.\actionserver\custom_payload.json') as f:
        restaurant_menu =   json.load(f)
    
    menu = restaurant_menu['frendy']['product_menu']
    if menu[category]:
        temp = menu[category]
        for j in temp:
            if product_name.lower() == j['product'].lower():
                return {"product":j['product'],"price":j['price'],"image":j['image']}
        return {"none":-1}
    return {"none":-1}
    

    
    
    


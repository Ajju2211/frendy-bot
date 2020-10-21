from datetime import datetime
import json
import secrets
from word2number import w2n

INVALID_VALUE = str(secrets.token_hex(20))


def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestampStr


def getJsonFileAsDict(filePath):
    with open(filePath, "r") as f:
        return json.load(f)


def saveDictAsJsonFile(dictData, filePath):
    with open("./../"+filePath, "w") as f:
        json.dump(dictData, f, indent=4)
        return True


def product_info(product_name, category):
    with open(r'./actionserver/custom_payload.json') as f:
        frendy_menu = json.load(f)

    menu = frendy_menu['frendy']['product_menu']
    if menu[category]:
        temp = menu[category]
        for j in temp:
            if product_name.lower() == j['product'].lower():
                return {"product": j['product'], "price": j['price'], "image": j['image']}
        return {"none": -1}
    return {"none": -1}

def getWordToNum(word):
    try:
        num = w2n.word_to_num(word)
        return num
    except ValueError as ve:
        print(ve)
        return None


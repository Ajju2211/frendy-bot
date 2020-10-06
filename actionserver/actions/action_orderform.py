from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted, UserUttered,  FollowupAction
# from rasa_core.events import (UserUtteranceReverted, UserUttered,
#                               ActionExecuted, Event)
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa.core.constants import REQUESTED_SLOT
from rasa.core.slots import Slot
import pandas as pd
import json
from actionserver.utils import utilities as util
from actionserver.controllers.faqs.faq import FAQ
from actionserver.controllers.constants.orderForm import *
import logging
from actionserver.utils.utilities import INVALID_VALUE

product_list = []
quant_list = []  # takes quantity from user

logger = logging.getLogger(__name__)


with open(r'./actionserver/custom_payload.json') as f:
    frendy_product_menu = json.load(f)

# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
    #   "intent": {"confidence": 1.0, "name": "get_started"},
    #   "entities": []
    #  }), FollowupAction(name="utter_greet")]


def query_back(dispatcher):
    dispatcher.utter_message("Going back to queries!!!")
    greet_utter = UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    })

    query_utter = UserUttered(text="/query_init", parse_data={
        "intent": {"confidence": 1.0, "name": "query_init"},
        "entities": []
    })

    return [
        greet_utter,
        FollowupAction(name="utter_greet"),
        query_utter,
        FollowupAction(name="utter_query_type")
    ]


def greet_back(dispatcher):
    dispatcher.utter_message("Going back!!!")
    return [UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    }), FollowupAction(name="utter_greet")]


class ActionShowProductMenu(Action):
    def name(self) -> Text:
        return "action_show_product_menu"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        x = open('./actionserver/custom_payload.json', "r")
        data = json.load(x)
        data_frendy = data['frendy']
        for i in data['frendy']['product_menu_imgs']:
            url = str(i)
            dispatcher.utter_message("product_menu of that frendy is ")
            dispatcher.utter_message(image=url)
        return []


class OrderForm(FormAction):

    def name(self):
        return "order_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("quantity"):
            return [
                "proceed"
            ]
        elif tracker.get_slot("product_name"):
            return [
                "quantity"
            ]
        elif tracker.get_slot("product_category"):
            return [
                "product_name"
            ]
        else:
            return [
                "product_category",
                # "product_name",
                # "quantity",
                # "proceed"
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        # return {"product_category": self.from_intent("inform"),"product_name": self.from_entity("any_thing"),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}
        # return {"product_category": [self.from_intent("inform"),self.from_text()], "product_name": self.from_text(), "quantity": self.from_entity("quantity"), "proceed": self.from_intent("inform")}
        return {
            "product_category": [
                self.from_entity("product_category"),
                self.from_text()
            ],
            "product_name": [
                self.from_entity("product_name"),
                self.from_text()
            ],
            "quantity": [self.from_entity("quantity"), self.from_text()],
            "proceed": [self.from_entity("proceed"), self.from_text()]
        }

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ):
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug(f"Request next slot '{slot}'")
                if slot == "product_category":
                    dispatcher.utter_message(text="Please select the category")
                    button_resp = [
                        {
                            "title": "back",
                            "payload": '/inform{"product_category":"back"}'
                        }
                    ]
                    dispatcher.utter_message(
                        text="type back otherwise!",
                        buttons=button_resp)
                    self.askCategories(dispatcher)
                elif slot == 'product_name':
                    self.showProducts(tracker.get_slot(
                        "product_category"), dispatcher, tracker)
                else:
                    dispatcher.utter_message(
                        template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def askCategories(self, dispatcher):
        data = []
        for keys in frendy_product_menu['frendy']['product_menu'].keys():
            val = '\"{}\"'.format(keys)
            cat = {"label": f"{keys}",
                   "value": '/inform{\"product_category\":'+val+'}'}
            data.append(cat)

        message = {"payload": "dropDown", "data": data}

        dispatcher.utter_message(
            text="Please select a option", json_message=message)
    # To display productes of category

    def showProducts(self, category, dispatcher, tracker):
        dic = {}
        data = []
        print(f"cat:{category}")
        try:
            if frendy_product_menu['frendy']['product_menu'][category]:
                temp = frendy_product_menu['frendy']['product_menu'][category]
                for j in temp:

                    dic = {
                        "title": j['product'],
                        "price": j['price'],
                        "image": j['image']
                    }

                    data.append(dic)

            message = {"payload": "cartCarousels", "data": data}
            button_resp = [
                {
                    "title": "back",
                    "payload": '/inform{"product_name":"back1"}'
                }
            ]

            dispatcher.utter_message(
                text="Please type the product name", json_message=message, buttons=button_resp)

            # return {"product_category": category}

        except:
            dispatcher.utter_message(text="No such Category Found")
            raise Exception("No such Category")
            # return {"product_category":None}

    def showCart(self, dispatcher, tracker):
        data = []
        for x in product_list:
            image = util.product_info(x['product'], x['category'])['image']
            price = util.product_info(x['product'], x['category'])['price']
            cart = {
                "title": x['product'],
                "image": image,
                "quantity": x['quantity'],
                "price": price
            }

            data.append(cart)

        message = {"payload": "cartCarousels", "data": data}

        dispatcher.utter_message(text="Your Order", json_message=message)

    def validate_product_category(self,
                               value: Text,
                               dispatcher: CollectingDispatcher,
                               tracker: Tracker,
                               domain: Dict[Text, Any],
                               ) -> Dict[Text, Any]:

        data = []
        category = value
        if value:
            if value.lower() == 'back':
                return {
                    "product_category": INVALID_VALUE,
                    "product_name": INVALID_VALUE,
                    "quantity": INVALID_VALUE,
                    "proceed": INVALID_VALUE
                }
            else:
                try:
                    self.showProducts(category, dispatcher, tracker)
                    return {"product_category": category}
                except:
                    return {"product_category": None}
        else:
            return {"product_category": None}

        # message={"payload":"cartCarousels","data":data}

        # dispatcher.utter_message(text="Please type the product name",json_message=message)

        # return {"product_category": category}

    def validate_product_name(self,
                           value: Text,
                           dispatcher: CollectingDispatcher,
                           tracker: Tracker,
                           domain: Dict[Text, Any],
                           ) -> Dict[Text, Any]:
        if value:
            value = value.lower()
            if value == "back" or value == "back1":
                return {
                    "product_category": None,
                    "product_name": None,
                    "quantity": None,
                    "proceed": None,
                    REQUESTED_SLOT: "product_category"
                }
            else:

                category = tracker.get_slot("product_category")

                # to debug whether the slot is present
                print(category)

                product_name = value
                product_menu = frendy_product_menu['frendy']['product_menu']
                if product_menu[category]:
                    temp = product_menu[category]
                    for j in temp:
                        if product_name.lower() == j['product'].lower():
                            dispatcher.utter_message(
                                "it costs {}".format(j['price']))
                            return {"product_name": product_name}
                        else:
                            continue
                            # dispatcher.utter_template("utter_not_serving",tracker)
                            # return {"product_name":None}
                    dispatcher.utter_template("utter_not_serving", tracker)
                    return {"product_name": None}
                else:
                    dispatcher.utter_message(text="No such category found")

        # if product_name in dataset.keys():
        #     dispatcher.utter_message("it costs {}".format(dataset[product_name][0]))
        #     return {"product_name": product_name}
        # else:
        #     dispatcher.utter_template("utter_not_serving",tracker)
        #     return {"product_name":None}

    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        product_name = tracker.get_slot("product_name")
        quantity = 0
        if value.lower() == 'back':
            return {
                "product_name": None,
                "quantity": None,
                REQUESTED_SLOT: "product_name"
            }
        try:
            quantity = int(value)
            return {"product_name": product_name, "quantity": quantity}
        except:
            dispatcher.utter_message(text="Please Enter Valid Number")
            return {"product_name": product_name, "quantity": None}

    def validate_proceed(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        product_name = tracker.get_slot("product_name")
        proceed = value
        quant = int(tracker.get_slot("quantity"))
        cat = tracker.get_slot("product_category")
        if proceed:
            proceed = proceed.lower().strip()

            # check if the value exist in individual list
            if proceed in ADD_TO_CART:
                product_obj = {"product": product_name,
                            "quantity": quant, "category": cat}
                product_list.append(product_obj)
                self.showProducts(cat, dispatcher, tracker)
                print("quantity")
                return {"proceed": None, "product_name": None, "quantity": None, REQUESTED_SLOT: "product_name"}

            elif proceed in BUY_NOW:
                product_obj = {"product": product_name,
                            "quantity": quant, "category": cat}
                product_list.append(product_obj)
                return {"proceed": proceed}

            elif proceed in CHANGE_PRODUCT:
                self.showProducts(cat, dispatcher, tracker)
                return {"product_name": None, "proceed": None, "quantity": None, REQUESTED_SLOT: "product_name"}

            elif proceed in CHANGE_QUANTITY:
                return {"quantity": None, "proceed": None, REQUESTED_SLOT: "quantity"}

            elif proceed in SWITCH_CATEGORY:
                return {"product_category": None, "product_name": None, "proceed": None, "quantity": None, REQUESTED_SLOT: "product_category"}

            else:
                # Select other product
                dispatcher.utter_message(text="Please select a valid option")
                # self.showProducts(cat, dispatcher, tracker)
                return {"proceed": None, REQUESTED_SLOT: "proceed"}
        else:
            dispatcher.utter_message(text="Please select valid option")
            return {"proceed": None, REQUESTED_SLOT: "proceed"}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("product_category") == INVALID_VALUE:
            li = [
                SlotSet("product_category", None),
                SlotSet("product_name", None),
                SlotSet("quantity", None),
                SlotSet("proceed", None)
            ]
            li.extend(greet_back(dispatcher))
            return li

        else:

            amount = 0
            product_cat = tracker.get_slot("product_category")
            total = 0
            price = 0

            for x in product_list:
                prize = util.product_info(x['product'], x['category'])['price']
                total = float(prize)*int(x['quantity'])
                amount += total
                # dispatcher.utter_message("{} : {} : {}".format(x['product'],x["quantity"],total))
                # amount += total
            self.showCart(dispatcher, tracker)
            dispatcher.utter_message("Total Amount : {}".format(amount))
            dispatcher.utter_message("Thanks for ordering")
            return [AllSlotsReset()]

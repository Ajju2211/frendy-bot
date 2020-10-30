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
import traceback

product_list = []
quant_list = []  # takes quantity from user


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
    dispatcher.utter_message(json_message = {
    "platform":"whatsapp",
    "payload":"text",
    "text":"Welcome back to Frendy Shopping."
    })
    return [UserUttered(text="/greet", parse_data={
        "intent": {"confidence": 1.0, "name": "greet"},
        "entities": []
    }), FollowupAction(name="utter_greet")]


class ActionGreetBack(Action):
    def name(self) -> Text:
        return "action_greet_back"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        return greet_back(dispatcher)


class OrderRatingForm(FormAction):

    def name(self):
        return "order_rating_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("give_rating"):
            return [
                "order_rating"
            ]

        else:
            return [
                "give_rating"
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "order_rating": [
                self.from_entity("rating"),
                self.from_text()
            ],
            "give_rating": [
                self.from_entity("confirm"),
                self.from_text()
            ]
        }

    def validate_give_rating(self,
                             value: Text,
                             dispatcher: CollectingDispatcher,
                             tracker: Tracker,
                             domain: Dict[Text, Any]
                             ) -> Dict[Text, Any]:

        NO = ["no", "nope", "not", "n"]
        YES = ["yes", "s", "sure", "yeah", "y"]
        val = value

        if val.lower() in NO:
            return {"give_rating": "NO", "order_rating": "NO"}
        elif val.lower() in YES:
            return {"give_rating": "YES", "order_rating": None, REQUESTED_SLOT: "order_rating"}

    def validate_order_rating(self,
                        value: Text,
                        dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]
                        ) -> Dict[Text, Any]:

        val = value

        rating = ['1', '2', '3', '4', '5']
        try:
            if val:
                num = util.getWordToNum(val.strip())
                if num:
                    val = num
                else:
                    raise ValueError('Rating shoud be 1-5')
                # if not a number then raises valueError which is handled
                if str(val) in rating:

                    give_rate = tracker.get_slot("give_rating")

                    return {"give_rating": give_rate, "order_rating": str(val)}
                else:
                    raise ValueError('Rating shoud be 1-5')
            else:
                dispatcher.utter_message(
                    text='please type rating in between 1 to 5')
                dispatcher.utter_message(json_message = {
                "platform":"whatsapp",
                "payload":"text",
                "text":"Please type rating in between \x2A1-5\x2A"
                })
                return {"order_rating": None, REQUESTED_SLOT: "order_rating"}
        except ValueError as e:
            dispatcher.utter_message(
                text='please type rating in between 1 to 5')
            dispatcher.utter_message(json_message = {
            "platform":"whatsapp",
            "payload":"text",
            "text":"Please type rating in between \x2A1-5\x2A"
            })
            return {"order_rating": None, REQUESTED_SLOT: "order_rating"}

        # If some other error raises
        except Exception as ex:
            traceback.print_exc()
            print(ex)
            dispatcher.utter_message(
                text='please type rating in between 1 to 5')
            dispatcher.utter_message(json_message = {
            "platform":"whatsapp",
            "payload":"text",
            "text":"Please type rating from 1️⃣-5️⃣"
            })
            return {"order_rating": None, REQUESTED_SLOT: "order_rating"}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],
               ) -> List[Dict]:

        rating = tracker.get_slot("order_rating")
        give_rating = tracker.get_slot("give_rating")

        # Already filled its value in uppercase in validations
        if give_rating == 'YES':
            # implement saving order rating in DB
            dispatcher.utter_message(
                text='Thank you your review has been submitted')
            dispatcher.utter_message(json_message = {
            "platform":"whatsapp",
            "payload":"text",
            "text":"🙂 Thank you, your review has been submitted!"
            })
            # return {"give_rating": None, "order_rating": None}
            return [SlotSet("give_rating", None), SlotSet("order_rating", None)]
        else:
            dispatcher.utter_message(
                text='Thankyou for ordering from us Your order will be ready shortly')
            # return {"give_rating": None, "order_rating": None}
            dispatcher.utter_message(json_message = {
            "platform":"whatsapp",
            "payload":"text",
            "text":"🙂 Thanks for ordering with us Your order will be delivered shortly, \n \
                track your order from the Frendy App."
            })
            return [SlotSet("give_rating", None), SlotSet("order_rating", None)]

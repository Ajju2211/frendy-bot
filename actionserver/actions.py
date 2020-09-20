from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted , UserUttered ,  FollowupAction
# from rasa_core.events import (UserUtteranceReverted, UserUttered,
#                               ActionExecuted, Event)
from rasa_sdk.events import AllSlotsReset, SlotSet
import pandas as pd
from rasa.core.slots import Slot
import json
from actionserver.utils import utilities as util
from actionserver.controllers.faqs.faq import FAQ
import logging

# dataset = pd.read_csv('./actionserver/productes.csv')
# dataset = dataset.set_index('product').T.to_dict('list')
product_list = []
quant_list = [] #takes quantity from user
# frendy_dataset = pd.read_csv('./actionserver/frendy.csv')
# frendy_dataset = frendy_dataset.set_index('frendy').T.to_dict('list')

logger = logging.getLogger(__name__)


REQUESTED_SLOT = "requested_slot"


with open(r'.\actionserver\custom_payload.json') as f:
    frendy_menu = json.load(f)

# Code snippet for global back
# return [Restarted(), UserUttered(text="/get_started", parse_data={
                    #   "intent": {"confidence": 1.0, "name": "get_started"}, 
                    #   "entities": []
                    #  }), FollowupAction(name="utter_greet")]

class ActionGreetBack(Action):
    def name(self) -> Text:
        return "action_greet_back"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Going back!!!")
        return [UserUttered(text="/greet", parse_data={
                      "intent": {"confidence": 1.0, "name": "greet"}, 
                      "entities": []
                     }), FollowupAction(name="utter_greet")]

class InfoForm(FormAction):

    """Collects order information"""

    def name(self):
        return "info_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "username",
            "mailid",
            "phone_number",
            "confirm"
            ]

    @staticmethod
    def msg() -> List[Text]:
        return ["back1","back2","back3"]

    def validate_mailid(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"mailid": value}
        else:
            return {"mailid": None, "username": None}

    def validate_phone_number(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"phone_number": value}
        else:
            return {"phone_number": None,"mailid": None}

    def validate_confirm(
        self,
        value: Text,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() not in self.msg():
            return {"phone_number": value}
        else:
            return {"phone_number": None,"confirm": None}


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        username = tracker.get_slot("username")
        mailid = tracker.get_slot("mailid")
        phone_number=tracker.get_slot("phone_number")



        message="DETAILS:"+"\n\n"+"Name:"+username+"\n"+"Email:"+mailid+"\n"+"Phone Number:"+phone_number+"\n"+"\nThanks! for sharing information."
        saveFile = open("some.txt", 'a')
        saveFile.write(message)
        saveFile.close()
        dispatcher.utter_message(message)
        return []

class ActionShowProduct(Action):
    def name(self) -> Text:
        return "action_show_product"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        x = open('./actionserver/custom_payload.json',"r")
        data = json.load(x)
        data_frendy = data['frendy']
        for i in data['frendy']['product_imgs']:
                url = str(i)
                dispatcher.utter_message("Product of Frendy are ")
                dispatcher.utter_message(image = url)
        return []

class ActionAskProductCategory(Action):
    def name(self) -> Text:
        return "action_ask_product_category"
    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        data=[
			{"label":"starters1","value":"/inform{'product_category':'starters'}"},
			{"label":"meals1","value":"/inform{'product_category':'meals'}"}
			]

        message={"payload":"dropDown","data":data}
  
        dispatcher.utter_message(text="Please select a option",json_message=message)
        print("inside product_category")
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
        else:
            return [
                "product_category",
                "product_name",
                "quantity",
                "proceed"
            ]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        # return {"product_category": self.from_intent("inform"),"product_name": self.from_entity("any_thing"),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}
        return {"product_category": self.from_intent("inform"),"product_name": self.from_text(),"quantity": self.from_entity("quantity"),"proceed": self.from_intent("inform")}
    
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
                    self.askCategories(dispatcher)
                else:
                    dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def askCategories(self,dispatcher):
        li = []
        for keys in frendy_menu['frendy']['product_menu'].keys():
            val = '\"{}\"'.format(keys)
            cat = {"label":f"{keys}","value":'/inform{\"product_category\":'+val+'}'}
            li.append(cat)

                
        data = li

        message={"payload":"dropDown","data":data}
  
        dispatcher.utter_message(text="Please select a option",json_message=message)
    # To display productes of category
    def showProducts(self,category,dispatcher,tracker):
        dic = {}
        data = []
        print(f"cat:{category}")
        try:
            if frendy_menu['frendy']['product_menu'][category]:
                temp = frendy_menu['frendy']['product_menu'][category]
                for j in temp:


                    dic = {
                        "title" : j['product'],
                        "price" : j['price'],
                        "image" : j['image']
                    }
                    
                    data.append(dic)
            
            message={"payload":"cartCarousels","data":data}
  
            dispatcher.utter_message(text="Please type the product name",json_message=message)

            # return {"product_category": category}
        
        except :
            dispatcher.utter_message(text="No such Category Found")
            raise Exception("No such Category")
            # return {"product_category":None}

    def showCart(self,dispatcher,tracker):
        data = []
        for x in product_list:
            image = util.product_info(x['product'],x['category'])['image']
            price = util.product_info(x['product'],x['category'])['price']
            cart = {
                "title" : x['product'],
                "image" : image,
                "quantity" : x['quantity'],
                "price" : price
                }

            data.append(cart)

        message={"payload":"cartCarousels","data":data}

        dispatcher.utter_message(text="Your Order",json_message=message)  

            
        

    def validate_product_category(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        data = []
        category = tracker.get_slot("product_category")
        try:
            self.showProducts(category,dispatcher,tracker)
            return {"product_category": category}
        except:
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

        category = tracker.get_slot("product_category")

        # to debug whether the slot is present
        print(category)

        product_name = value
        menu = frendy_menu['frendy']['product_menu']
        if menu[category]:
            temp = menu[category]
            for j in temp:
                if product_name.lower() == j['product'].lower():
                    dispatcher.utter_message("it costs {}".format(j['price']))
                    return {"product_name": product_name}
                else:
                    continue
                    # dispatcher.utter_template("utter_not_serving",tracker)
                    # return {"product_name":None}
            dispatcher.utter_template("utter_not_serving",tracker)
            return {"product_name":None}
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
        quantity=0
        try:
            quantity = int(value)
            return {"product_name":product_name,"quantity":quantity}
        except:
            dispatcher.utter_message(text="Please Enter Valid Number")
            return {"product_name":product_name,"quantity":None}


    def validate_proceed(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        product_name = tracker.get_slot("product_name")
        proceed = tracker.get_slot("proceed")
        quant = int(tracker.get_slot("quantity"))
        cat = tracker.get_slot("product_category")
        if proceed =="Add to Cart":
            product_obj = {"product":product_name,"quantity":quant,"category":cat}
            product_list.append(product_obj)
            self.showProducts(cat,dispatcher,tracker)
            print("quantity")
            return {"proceed":None,"product_name":None,"quantity":None}

        elif proceed == "Buy Now":
            product_obj = {"product":product_name,"quantity":quant,"category":cat}
            product_list.append(product_obj)
            return {"proceed":proceed}

        else:
            # Select other food
            self.showProducts(cat,dispatcher,tracker)
            return {"product_name":None,"proceed":None,"quantity":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        amount = 0
        product_cat = tracker.get_slot("product_category")
        total = 0
        price=0
        
        for x in product_list:
            prize = util.product_info(x['product'],x['category'])['price']
            total = float(prize)*int(x['quantity'])
            amount += total
            # dispatcher.utter_message("{} : {} : {}".format(x['product'],x["quantity"],total))
            # amount += total
        self.showCart(dispatcher,tracker)
        dispatcher.utter_message("Total Amount : {}".format(amount))
        dispatcher.utter_message("Thanks for ordering")
        return [AllSlotsReset()]

class DefaultFallback(FormAction):
    """Default Fallback Action"""

    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any])-> List[Dict[Text, Any]]:
        queryText = tracker.latest_message.get('text')

        dispatcher.utter_message("Fallback Triggered bcoz u've typed something! "+queryText)
        return []

class ComplainForm(FormAction):

    def name(self):
        return "complain_form"

    @staticmethod
    def required_slots(tracker):

            if tracker.get_slot("complain_type"):
                return ["complain_type", "complain_text"]
            else:
                return ["complain_type"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"complain_type": [self.from_entity("complain_type"),self.from_text()],"complain_text": [self.from_entity(entity="navigation"),self.from_text()]}

        #return {"complain_type": self.from_entity("complain_type"),"complain_text": self.from_entity(entity="any_thing")}

    def validate_complain_type(
        self,
        value:Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        complaints = ["food quality","delivery","naaniz app","other"]
        value=value.strip().lower()
        if value=="back1" or value=="back":
            return {"complain_type":"-1","complain_text":"-1"}
        elif value in complaints:
            return {"complain_type":value}
        else:
            dispatcher.utter_message("please type valid option.")
            return {"complain_type":None}    
    def validate_complain_text(
        self,
        value:Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if value=="back2" or value.lower()=="back":
            return {"complain_type":None,"complain_text":None}
        else:
            return {"complain_text":value}
        

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot("complain_type")!="-1":
        # saving 
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                comp_type=tracker.get_slot("complain_type")
                comp = tracker.get_slot("complain_text")
                compObj = json.load(queriesRef)
                compObj["complaints"].append({
                    "createdOn":util.timestamp(),
                    "complaint_area":comp_type,
                    "complaint":comp
                })
                with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                    json.dump(compObj, queriesRefWrite, indent = 4)

            dispatcher.utter_message("Your Complaint :\n Complaint Area:{comp_type}\n Complaint: '{comp}' \n has been registered!".format(comp_type=comp_type,comp = comp))
        else:
            dispatcher.utter_message("Complaints Form is closed")


        return [SlotSet("complain_type",None), SlotSet("complain_text",None)]


class FeedbackForm(FormAction):

    def name(self):
        return "feedback_form"

    @staticmethod
    def required_slots(tracker):
        if tracker.get_slot("rating"):
            return ["rating","feedback_text"]
        else :
            return ["rating"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        # return {"rating": [self.from_entity("rating"),self.from_entity("any_thing")],"feedback_text": [self.from_entity(entity="any_thing"),self.from_entity(entity="navigation")]}
        return {"rating": [self.from_entity("rating"),self.from_text()],"feedback_text": [self.from_text(),self.from_entity(entity="navigation")]}


    def validate_rating(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        ratings=['1','2','3','4','5']
        try:
            value=value.strip()
            if value=="back1" or value.lower()=="back":
                return {"rating":"-1", "feedback_text":"-1"}
                # 1-5 it integer otherwise rating:None
            elif value in ratings:
                return {"rating":value,"feedback_text":None}
            else:
                dispatcher.utter_message("Please enter valid option.")
                return {"rating":None,"feedback_text":None}
        except Exception as e:
            print(e)
            dispatcher.utter_message("Please enter valid option.")
            return {"rating":None,"feedback_text":None}

    def validate_feedback_text(
    self,
    value: Text,
    dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value=="back2" or value.lower()=="back":
            return {"rating":None, "feedback_text":None}
        else:
            return {"feedback_text":value}


    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("rating")!="-1":
            with open("./actionserver/customer_queries.json", "r") as queriesRef:
                rating=tracker.get_slot("rating")
                feedback = tracker.get_slot("feedback_text")
                feedbackObj = json.load(queriesRef)
                feedbackObj["feedback"].append({
                    "createdOn":util.timestamp(),
                    "complaint_area":rating,
                    "complaint":feedback
                })
            with open("./actionserver/customer_queries.json", "w") as queriesRefWrite:
                json.dump(feedbackObj, queriesRefWrite, indent = 4)

            dispatcher.utter_message("Your Response :\n Rating :'{rate}' star \n Feedback: '{feedbk}' \n Submitted!Thank You!".format(rate=rating,feedbk=feedback))
        else:
            dispatcher.utter_message("Feedback form closed")


        return [SlotSet("rating", None), SlotSet("feedback_text", None)]
    

        
              

class FaqForm(FormAction):

    def name(self):
        return "faq_form"

    @staticmethod
    def required_slots(tracker):
        return ["faq_choice","faq_text"]
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        # return {"faq_choice": self.from_entity("faq_choice"), "faq_text": [self.from_entity(entity="any_thing"),self.from_entity(entity="navigation")] }
        return {"faq_choice": self.from_entity("faq_choice"), "faq_text": [self.from_text(),self.from_entity(entity="navigation")] }


    def validate_faq_choice(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        faq_choice = tracker.get_slot("faq_choice")
        print(faq_choice)

        if faq_choice == "back2":
            return {"faq_choice": "-1","faq_text":"-1"}
        elif faq_choice == "1":
            useNlp = False
            faq_data = pd.read_excel("./actionserver/controllers/faqs/test_faq.xlsx")

            button_resp = [
                {
                    "title":"Choose from our set of FAQs",
                    "payload": "/faq_choice{\"faq_choice\": \"1\"}"
                },
                {
                    "payload": "/faq_choice{\"faq_choice\": \"2\" }",
                    "title": "Type your own question."
                },{
                        "payload": "/faq_choice{\"faq_choice\": \"back2\"}",
                        "title": "Back"
                }
            ]
            dispatcher.utter_message(text="How should we get your FAQ?", buttons=button_resp)
            qa = []
            for i in range(len(faq_data)):
                obj = {
                "title":faq_data["Question"][i],
                "description":faq_data["Answer"][i]
                    }
                qa.append(obj)
            message={ "payload": "collapsible", "data": qa }
            dispatcher.utter_message(text="Faq's",json_message=message)

            return {"faq_choice":None}
        else:
            return {"faq_choice":value}

    def validate_faq_text(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        faq_choice = tracker.get_slot("faq_choice")
        try:
            navigation = tracker.get_slot("navigation")
        except:
            navigation = "NOBACK"
        print(value)


        if navigation == "back3":
            return {"faq_text": None,"faq_choice": None,"navigation":None}
        else:
            # dispatcher.utter_template("utter_not_serving",tracker)
            print(faq_choice)
            if faq_choice!="-1":
                ques= value
                useNlp = True

                f = FAQ("./actionserver/controllers/faqs/test_faq.xlsx")
                # NLP disabled coz morethan 100 sec
                ans = f.ask_faq(ques, NLP = False)
                if ans:
                    dispatcher.utter_message("Your Question :{}\n Answer:{}".format(ques, ans))
                else:
                    dispatcher.utter_message("Query not found !")               
                return {"faq_choice":faq_choice,"faq_text":None}
            else:
                {"faq_choice":faq_choice,"faq_text":"filled"}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
            # handle back2 logic here
            dispatcher.utter_message("Faq is closed")
            return [SlotSet("faq_choice", None),SlotSet("faq_text", None) ]




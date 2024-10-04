from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from mongo_connector import MongoConnector
import logging

logger = logging.getLogger(__name__)

class ActionSearchCar(Action):
    def name(self) -> Text:
        return "action_search_car"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        car_brand = tracker.get_slot("car_brand")
        mongo = MongoConnector()
        
        try:
            cars = mongo.search_cars(car_brand)
            if cars:
                car_list = "\n".join([f"- {car['model']}" for car in cars])
                dispatcher.utter_message(f"Here are the available {car_brand} models:\n{car_list}")
            else:
                dispatcher.utter_message(f"I'm sorry, we don't have any {car_brand} cars available at the moment.")
        except Exception as e:
            logger.error(f"Error searching for cars: {e}")
            dispatcher.utter_message("An error occurred while searching for cars. Please try again later.")

        return []

class ActionCarInfo(Action):
    def name(self) -> Text:
        return "action_car_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        car_model = tracker.get_slot("car_model")
        mongo = MongoConnector()
        
        try:
            car_info = mongo.get_car_info(car_model)
            if car_info:
                info = f"Here's information about the {car_model}:\n"
                info += f"Brand: {car_info['brand']}\n"
                info += f"Year: {car_info['year']}\n"
                info += f"Engine: {car_info['engine']}\n"
                info += f"Transmission: {car_info['transmission']}\n"
                dispatcher.utter_message(info)
            else:
                dispatcher.utter_message(f"I'm sorry, I couldn't find any information about the {car_model}.")
        except Exception as e:
            logger.error(f"Error retrieving car information: {e}")
            dispatcher.utter_message("An error occurred while retrieving car information. Please try again later.")

        return []

class ActionPriceInquiry(Action):
    def name(self) -> Text:
        return "action_price_inquiry"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        car_brand = tracker.get_slot("car_brand")
        car_model = tracker.get_slot("car_model")
        mongo = MongoConnector()
        
        try:
            price = mongo.get_car_price(car_brand, car_model)
            if price:
                dispatcher.utter_message(f"The price of {car_brand} {car_model} is ₱{price:,}.")
            else:
                dispatcher.utter_message(f"I'm sorry, I couldn't find the price for {car_brand} {car_model}.")
        except Exception as e:
            logger.error(f"Error retrieving car price: {e}")
            dispatcher.utter_message("An error occurred while retrieving the car price. Please try again later.")

        return []

class ActionBookTestDrive(Action):
    def name(self) -> Text:
        return "action_book_test_drive"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        car_brand = tracker.get_slot("car_brand")
        car_model = tracker.get_slot("car_model")

        if car_brand and car_model:
            dispatcher.utter_message(f"Great! I've scheduled a test drive for the {car_brand} {car_model}. Our team will contact you shortly to confirm the details.")
        else:
            dispatcher.utter_message("To book a test drive, please provide the car brand and model you're interested in.")

        return []
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

import yaml
from yaml.loader import SafeLoader

with open('data/enrollment_schedule.yml') as f:
    e_schedule = yaml.load(f, Loader=SafeLoader)

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        data_inicio = e_schedule[city]['data_inicio']

        dispatcher.utter_message(text=f"Hello World! {city} - {data_inicio}")

        return []

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

import yaml
from yaml.loader import SafeLoader
from unidecode import unidecode

def get_schedule(city: Text) -> Dict:
    # read the schedules file
    try:
        with open('data/enrollment_schedule.yml', encoding='latin1') as file:
            schedules = yaml.load(file, Loader=SafeLoader)
    except OSError:
        return None

    # pre-process the city parameter
    city = unidecode(city.lower())

    # query the data
    try:
        return (schedules['year'], schedules['semester'], schedules[city])
    except KeyError:
        return None

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        year, semester, schedule = get_schedule(city) or (None, None, None)

        if year is not None and semester is not None and schedule is not None:
            dispatcher.utter_message(text=f"Matrícula de veteranos do {semester}o semestre de {year} para a cidade {city}:\n" \
                + f"Início: {schedule['data_inicio']} a partir das {schedule['hora_inicio']} horas.\n" \
                + f"Término: {schedule['data_termino']} até às {schedule['hora_termino']} horas.")
        else:
            dispatcher.utter_message(text=f"Me desculpe, mas não consegui localizar o cronograma de matrícula para a cidade {city}.")

        return []

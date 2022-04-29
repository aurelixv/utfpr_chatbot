# Rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Other imports
import yaml
from yaml.loader import SafeLoader
from unidecode import unidecode

class ActionGetSchedule(Action):
    """
    Handles the action_get_schedule action
    """
    def name(self) -> Text:
        return "action_get_schedule"

    @staticmethod
    def get_schedule(city: Text) -> Dict:
        """
        Function that receives a city (key), pre-processes it and returns its values
        """
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

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        year, semester, schedule = self.get_schedule(city) or (None, None, None)

        if year and semester and schedule:
            dispatcher.utter_message(text=f"Matrícula de veteranos do {semester}o semestre de {year} para a cidade {city}:\n\n" \
                + f"- Início: {schedule['data_inicio']} a partir das {schedule['hora_inicio']} horas.\n" \
                + f"- Término: {schedule['data_termino']} até às {schedule['hora_termino']} horas.")
        else:
            dispatcher.utter_message(text=f"Me desculpe, mas não consegui localizar o cronograma de matrícula para a cidade {city}.")

        # clears the city slot
        return [SlotSet('city', None)]

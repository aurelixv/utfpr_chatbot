# Rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Other imports
import yaml
from yaml.loader import SafeLoader
from unidecode import unidecode
import psycopg2

def psql_connect():
    """
    Establishes a connection to postgres
    """
    try:
        # read credentials
        with open('endpoints.yml', encoding='utf-8') as file:
            endpoints = yaml.load(file, Loader=SafeLoader)

        # parse credentials
        credentials = endpoints['tracker_store']
        host = credentials['url']
        database = credentials['db']
        user = credentials['username']
        password = credentials['password']

        try:
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )

            print('--- Connection to Postgres established successfully ---')

            return conn
        except psycopg2.OperationalError:
            return None

    except OSError:
        return None

# starts postgres connection
CONN = psql_connect()

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
        if CONN:
            # pre-process the city parameter
            city = unidecode(city.upper())

            # query the data
            query = """
            SELECT B.CAMPUS_NAME,
                C.PHASE_NAME,
                A.YEAR,
                A.SEMESTER,
                A.START_TIMESTAMP,
                A.END_TIMESTAMP
            FROM ENROLLMENT_SCHEDULE A
            LEFT JOIN CAMPI B
                ON A.CAMPUS_ID = B.CAMPUS_ID
            LEFT JOIN PHASE C
                ON A.PHASE_ID = C.PHASE_ID
            WHERE B.CAMPUS_NAME = (%s)
                AND CONCAT(A.YEAR, A.SEMESTER) = 
                    (
                        SELECT CONCAT(A.YEAR, A.SEMESTER) 
                        FROM ENROLLMENT_SCHEDULE 
                        ORDER BY YEAR DESC, SEMESTER DESC 
                        LIMIT 1
                    )
            """
            with CONN.cursor() as cur:
                cur.execute(query, (city,))
                data = cur.fetchall()

            if len(data) > 0:
                schedule = {
                    'city': data[0][0].title(),
                    'year': data[0][2],
                    'semester': data[0][3]
                }
                for line in data:
                    schedule[line[1].lower()] = {
                        'start_date': line[4].strftime("%d/%m/%Y"), 
                        'start_hour': line[4].strftime("%H"),
                        'end_date': line[5].strftime("%d/%m/%Y"),
                        'end_hour': line[5].strftime("%H")
                    }
                return schedule

        return None

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('city')
        schedule = self.get_schedule(city)

        if schedule:
            dispatcher.utter_message(text=f"Matrícula de veteranos do {schedule['semester']}o semestre de {schedule['year']} para a cidade {schedule['city']}:\n\n" \
                + f"- Início: {schedule['requerimento']['start_date']} a partir das {schedule['requerimento']['start_hour']} horas.\n" \
                + f"- Término: {schedule['requerimento']['end_date']} até às {schedule['requerimento']['end_hour']} horas.")
        else:
            dispatcher.utter_message(text=f"Me desculpe, mas não consegui localizar o cronograma de matrícula para a cidade {city}.")

        # clears the city slot
        return [SlotSet('city', None)]

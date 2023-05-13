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

# For debugging code
import logging

logger = logging.getLogger(__name__)

class Credentials:
    """
    Parses the credentials from yaml file
    """
    def __init__(self, file_path: str):
        # open credentials file
        with open(file_path, encoding='utf-8') as file:
            endpoints = yaml.load(file, Loader=SafeLoader)
        # parse credentials
        credentials = endpoints['tracker_store']
        self.host = credentials['url']
        self.database = credentials['db']
        self.user = credentials['username']
        self.password = credentials['password']

def psql_connect(credentials: Credentials):
    """
    Establishes a connection to postgres
    """
    try:
        conn = psycopg2.connect(
            host = credentials.host,
            database = credentials.database,
            user = credentials.user,
            password = credentials.password
        )
        return conn
    except psycopg2.OperationalError:
        return None

class ActionGetSchedule(Action):
    """
    Handles the action_get_schedule action
    """
    def name(self) -> Text:
        return "action_get_schedule"

    @staticmethod
    def get_schedule(campus: Text) -> Dict:
        """
        Function that receives a campus (key), pre-processes it and returns its values
        """
        # connects to db
        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        if conn:
            # pre-process the campus parameter
            campus = unidecode(campus.upper())

            # query the data
            q_year_semester = """
                SELECT A.YEAR,
                    A.SEMESTER
                FROM ENROLLMENT_SCHEDULE A
                LEFT JOIN CAMPUS B
                    ON A.CAMPUS_ID = B.CAMPUS_ID
                WHERE B.CAMPUS_NAME = (%s)
                ORDER BY YEAR DESC, SEMESTER DESC 
                LIMIT 1
            """
            q_schedule = """
                SELECT B.CAMPUS_NAME,
                    C.ENROLLMENT_PHASE_NAME,
                    A.START_TIMESTAMP,
                    A.END_TIMESTAMP
                FROM ENROLLMENT_SCHEDULE A
                LEFT JOIN CAMPUS B
                    ON A.CAMPUS_ID = B.CAMPUS_ID
                LEFT JOIN ENROLLMENT_PHASE C
                    ON A.ENROLLMENT_PHASE_ID = C.ENROLLMENT_PHASE_ID
                WHERE B.CAMPUS_NAME = (%s)
                    AND A.YEAR = (%s)
                    AND A.SEMESTER = (%s)
            """
            with conn.cursor() as cur:
                cur.execute(q_year_semester, (campus,))
                year_semester = cur.fetchall()
                if len(year_semester) > 0:
                    year = year_semester[0][0]
                    semester = year_semester[0][1]
                    cur.execute(q_schedule, (campus, year, semester))
                    data = cur.fetchall()
                else:
                    data = []

            # close the connection to db
            conn.close()

            if len(data) > 0:
                schedule = {
                    'campus': data[0][0].title(),
                    'year': year,
                    'semester': semester,
                    'phases': {}
                }
                for line in data:
                    schedule['phases'][line[1].lower()] = {
                        'start_date': line[2].strftime("%d/%m/%Y"),
                        'start_hour': line[2].strftime("%H"),
                        'end_date': line[3].strftime("%d/%m/%Y"),
                        'end_hour': line[3].strftime("%H")
                    }
                return schedule

        return None

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        campus = tracker.get_slot('campus')
        schedule = self.get_schedule(campus)

        if schedule:

            response = f"Matrícula de veteranos do {schedule['semester']}.º semestre "\
                f"de {schedule['year']} para o campus {schedule['campus']}:\n\n"

            phases = schedule['phases']

            for phase in phases:
                response += f"{phase.upper()}\n"\
                    f"- Início: {phases[phase]['start_date']} a partir das "\
                    f"{phases[phase]['start_hour']} horas.\n" \
                    f"- Término: {phases[phase]['end_date']} até às "\
                    f"{phases[phase]['end_hour']} horas.\n\n"

            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Me desculpe, mas não consegui localizar o "\
                f"cronograma de matrícula de veteranos para o campus {campus.title()}.")

        # clears the campus slot
        return [SlotSet('campus', None)]

class ActionInformInternship(Action):
    """
    Handles the action_inform_internship action
    """
    def name(self) -> Text:
        return "action_inform_internship"

    @staticmethod
    def get_intent_name(tracker):
        """
        Function that receives a tracker object and returns the intent name
        """
        return tracker.latest_message['intent']['name']

    @staticmethod
    def get_slot_internship_type(tracker):
        """
        Function that receives a tracker object and returns the internship_type_slot
        """
        # retrieve slot
        internship_type = tracker.get_slot('internship_type')

        # pre process
        if internship_type:
            internship_type = unidecode(internship_type.upper())

        return internship_type

    @staticmethod
    def get_slot_internship_info(tracker):
        """
        Function that receives a tracker object and returns the internship_type_info
        """
        # retrieve slot
        internship_info = tracker.get_slot('internship_info')

        # pre process
        if internship_info:
            internship_info = unidecode(internship_info.upper())

        return internship_info

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        internship_type = self.get_slot_internship_type(tracker)
        internship_info = self.get_slot_internship_info(tracker)
        intent = self.get_intent_name(tracker)

        dispatcher.utter_message(text=f'Intent: {intent}\nInformações sobre: {internship_type}'\
            + f'\nInternship_info: {internship_info}')

        # clears the internship_type slot
        return [SlotSet('internship_type', None), SlotSet('internship_info', None)]

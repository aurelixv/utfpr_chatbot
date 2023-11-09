"""
Module docstring
"""
import logging
import re

# Rasa
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

# Other imports
import yaml
from yaml.loader import SafeLoader
from unidecode import unidecode
import psycopg2

# For debugging code
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

    def __repr__(self):
        return f'\nhost: {self.host}\ndatabase: {self.database}\n' \
            f'user: {self.user}\npassword: {self.password}'

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
    def get_campus_slot(tracker):
        """
        Function that receives a tracker object and returns the campus slot
        """
        # retrieve slot
        campus = tracker.get_slot('campus')

        # pre process
        if campus:
            campus = unidecode(campus.upper())

        return campus

    @staticmethod
    def get_schedule(campus: Text) -> Dict:
        """
        Function that receives a campus (key), pre-processes it and returns its values
        """
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

        # connects to db
        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        if conn:
            # query the data
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

        campus = self.get_campus_slot(tracker)
        schedule = self.get_schedule(campus)

        if schedule:

            response = f"Matrícula de veteranos do {schedule['semester']}.º semestre "\
                f"de {schedule['year']} para o campus {schedule['campus']}:\n\n"

            phases = schedule['phases']

            for phase in phases:
                response += f"{phase.upper()}\n"\
                    f"- Início: {phases[phase]['start_date']} a partir das "\
                    f"{phases[phase]['start_hour']} horas.\n"\
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

        logger.debug(tracker.latest_message)

        return tracker.latest_message['intent']['name']

    @staticmethod
    def get_internship_type_slot(tracker):
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
    def get_internship_info_slot(tracker):
        """
        Function that receives a tracker object and returns the internship_type_info
        """
        # retrieve slot
        internship_info = tracker.get_slot('internship_info')

        # pre process
        if internship_info:
            internship_info = unidecode(internship_info.upper())

        return internship_info

    @staticmethod
    def get_internship_type_id(internship_type: Text):
        """
        Function that receives an internship_type and queries the database to
        return the corresponding internship_type_id
        """
        q_internship_type = """
            SELECT A.INTERNSHIP_TYPE_ID,
                A.INTERNSHIP_TYPE_NAME
            FROM INTERNSHIP_TYPE A
            WHERE A.INTERNSHIP_TYPE_NAME = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        internship_type_id = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_internship_type, (internship_type,))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                internship_type_id = result[0][0]

        return internship_type_id

    @staticmethod
    def get_internship_info_id(internship_info: Text):
        """
        Function that receives an internship_info and queries the database to
        return the corresponding internship_info_id
        """
        q_internship_info = """
            SELECT A.INTERNSHIP_INFO_ID,
                A.INTERNSHIP_INFO_NAME,
                A.INTERNSHIP_DESCRIPTION
            FROM INTERNSHIP_INFO A
            WHERE A.INTERNSHIP_INFO_NAME = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        internship_info_id = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_internship_info, (internship_info,))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                internship_info_id = result[0][0]

        return internship_info_id

    @staticmethod
    def get_internship_text(internship_info_id, internship_type_id):
        """
        Function that receives an internship_info_id and internship_type_id and 
        queries the database to return the corresponding internship_text
        """
        q_internship_text = """
            SELECT A.INTERNSHIP_INFO_ID,
                A.INTERNSHIP_TYPE_ID,
                A.UPDATE_TIMESTAMP,
                A.INFO_TEXT
            FROM INTERNSHIP_TEXT A
            WHERE A.INTERNSHIP_INFO_ID = (%s)
                AND A.INTERNSHIP_TYPE_ID = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        internship_text = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_internship_text, (internship_info_id, internship_type_id))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                # pre-process to enable breaklines
                if result[0][3]:
                    internship_text = result[0][3].replace('\\n', '\n')

        return internship_text

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        internship_type = self.get_internship_type_slot(tracker)
        internship_type_id = self.get_internship_type_id(internship_type)
        internship_info = self.get_internship_info_slot(tracker)
        internship_info_id = self.get_internship_info_id(internship_info)
        internship_text = self.get_internship_text(internship_info_id, internship_type_id)
        intent = self.get_intent_name(tracker)

        # debug
        dispatcher.utter_message(text=f'intent: {intent}'\
            + f'\ninternship_type: {internship_type} id: {internship_type_id}'\
            + f'\ninternship_info: {internship_info} id: {internship_info_id}'\
            + f'\ninternship_text: {internship_text}')

        # clears the internship_info slot
        return [SlotSet('internship_info', None)]

class ActionExtractInternshipType(Action):
    """
    Handles the action_extract_internship_type action
    """
    def name(self) -> Text:
        return "action_extract_internship_type"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # retrieve last user message
        latest_message = tracker.latest_message['text']

        # retrieve previously defined internship_type slot
        old_internship_type = tracker.get_slot('internship_type')

        new_internship_type = None
        # regex to find entity
        if re.search('n[aã]o obrigat[oó]rio', latest_message):
            new_internship_type = 'nao obrigatorio'
        elif re.search('obrigat[oó]rio', latest_message):
            new_internship_type = 'obrigatorio'

        # pre process
        if new_internship_type:
            new_internship_type = unidecode(new_internship_type.upper())
            return [SlotSet('internship_type', new_internship_type)]

        return [SlotSet('internship_type', old_internship_type)]

class ActionInformAssistance(Action):
    """
    Handles the action_inform_assistance action
    """
    def name(self) -> Text:
        return "action_inform_assistance"

    @staticmethod
    def get_intent_name(tracker):
        """
        Function that receives a tracker object and returns the intent name
        """

        logger.debug(tracker.latest_message)

        return tracker.latest_message['intent']['name']

    @staticmethod
    def get_assistance_type_slot(tracker):
        """
        Function that receives a tracker object and returns the assistance_type_slot
        """
        # retrieve slot
        assistance_type = tracker.get_slot('assistance_type')

        # pre process
        if assistance_type:
            assistance_type = unidecode(assistance_type.upper())

        return assistance_type

    @staticmethod
    def get_assistance_info_slot(tracker):
        """
        Function that receives a tracker object and returns the assistance_type_info
        """
        # retrieve slot
        assistance_info = tracker.get_slot('assistance_info')

        # pre process
        if assistance_info:
            assistance_info = unidecode(assistance_info.upper())

        return assistance_info

    @staticmethod
    def get_assistance_type_id(assistance_type: Text):
        """
        Function that receives an assistance_type and queries the database to
        return the corresponding assistance_type_id
        """
        q_assistance_type = """
            SELECT A.ASSISTANCE_TYPE_ID,
                A.ASSISTANCE_TYPE_NAME
            FROM ASSISTANCE_TYPE A
            WHERE A.ASSISTANCE_TYPE_NAME = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        assistance_type_id = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_assistance_type, (assistance_type,))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                assistance_type_id = result[0][0]

        return assistance_type_id

    @staticmethod
    def get_assistance_info_id(assistance_info: Text):
        """
        Function that receives an assistance_info and queries the database to
        return the corresponding assistance_info_id
        """
        q_assistance_info = """
            SELECT A.ASSISTANCE_INFO_ID,
                A.ASSISTANCE_INFO_NAME,
                A.ASSISTANCE_DESCRIPTION
            FROM ASSISTANCE_INFO A
            WHERE A.ASSISTANCE_INFO_NAME = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        assistance_info_id = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_assistance_info, (assistance_info,))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                assistance_info_id = result[0][0]

        return assistance_info_id

    @staticmethod
    def get_assistance_text(assistance_info_id, assistance_type_id):
        """
        Function that receives an assistance_info_id and assistance_type_id and 
        queries the database to return the corresponding assistance_text
        """
        q_assistance_text = """
            SELECT A.ASSISTANCE_INFO_ID,
                A.ASSISTANCE_TYPE_ID,
                A.UPDATE_TIMESTAMP,
                A.INFO_TEXT
            FROM ASSISTANCE_TEXT A
            WHERE A.ASSISTANCE_INFO_ID = (%s)
                AND A.ASSISTANCE_TYPE_ID = (%s)
            LIMIT 1
        """

        credentials = Credentials('endpoints.yml')
        conn = psql_connect(credentials)

        assistance_text = None
        if conn:
            with conn.cursor() as cur:
                cur.execute(q_assistance_text, (assistance_info_id, assistance_type_id))
                result = cur.fetchall()

            conn.close()

            if len(result) > 0:
                # pre-process to enable breaklines
                if result[0][3]:
                    assistance_text = result[0][3].replace('\\n', '\n')

        return assistance_text

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        assistance_type = self.get_assistance_type_slot(tracker)
        assistance_type_id = self.get_assistance_type_id(assistance_type)
        assistance_info = self.get_assistance_info_slot(tracker)
        assistance_info_id = self.get_assistance_info_id(assistance_info)
        assistance_text = self.get_assistance_text(assistance_info_id, assistance_type_id)
        intent = self.get_intent_name(tracker)

        # debug
        dispatcher.utter_message(text=f'intent: {intent}'\
            + f'\nassistance_type: {assistance_type} id: {assistance_type_id}'\
            + f'\nassistance_info: {assistance_info} id: {assistance_info_id}'\
            + f'\nassistance_text: {assistance_text}')

        # clears the internship_info slot
        return [SlotSet('assistance_info', None)]

class ActionExtractAssistanceType(Action):
    """
    Handles the action_extract_internship_type action
    """
    def name(self) -> Text:
        return "action_extract_assistance_type"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # retrieve last user message
        latest_message = tracker.latest_message['text']

        # retrieve previously defined internship_type slot
        old_assistance_type = tracker.get_slot('assistance_type')

        new_assistance_type = None
        # regex to find entity
        if re.search('b[aá]sico', latest_message):
            new_assistance_type = 'basico'
        elif re.search('moradia', latest_message):
            new_assistance_type = 'moradia'
        elif re.search('alimenta[cç][aã]o', latest_message):
            new_assistance_type = 'alimentacao'

        # pre process
        if new_assistance_type:
            new_assistance_type = unidecode(new_assistance_type.upper())
            return [SlotSet('assistance_type', new_assistance_type)]

        return [SlotSet('assistance_type', old_assistance_type)]

class ActionClearSlots(Action):
    """
    Handles the action_clear_slots action
    """
    def name(self) -> Text:
        return "action_clear_slots"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]

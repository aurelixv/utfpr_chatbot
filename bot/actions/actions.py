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
    def get_schedule(campus: Text) -> Dict:
        """
        Function that receives a campus (key), pre-processes it and returns its values
        """
        global CONN
        # connects to db if expired
        if CONN.closed != 0:
            print('--- Reconnecting to Postgres... ---')
            CONN = psql_connect()

        if CONN.closed == 0:
            # pre-process the campus parameter
            campus = unidecode(campus.upper())

            # query the data
            q_year_semester = """
                SELECT A.YEAR,
                    A.SEMESTER
                FROM ENROLLMENT_SCHEDULE A
                LEFT JOIN CAMPI B
                    ON A.CAMPUS_ID = B.CAMPUS_ID
                WHERE B.CAMPUS_NAME = (%s)
                ORDER BY YEAR DESC, SEMESTER DESC 
                LIMIT 1
            """
            q_schedule = """
                SELECT B.CAMPUS_NAME,
                    C.PHASE_NAME,
                    A.START_TIMESTAMP,
                    A.END_TIMESTAMP
                FROM ENROLLMENT_SCHEDULE A
                LEFT JOIN CAMPI B
                    ON A.CAMPUS_ID = B.CAMPUS_ID
                LEFT JOIN PHASE C
                    ON A.PHASE_ID = C.PHASE_ID
                WHERE B.CAMPUS_NAME = (%s)
                    AND A.YEAR = (%s)
                    AND A.SEMESTER = (%s)
            """
            with CONN.cursor() as cur:
                cur.execute(q_year_semester, (campus,))
                year_semester = cur.fetchall()
                if len(year_semester) > 0:
                    year = year_semester[0][0]
                    semester = year_semester[0][1]
                    cur.execute(q_schedule, (campus, year, semester))
                    data = cur.fetchall()
                else:
                    return None

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

            response = f"Matrícula de veteranos do {schedule['semester']}o semestre "\
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

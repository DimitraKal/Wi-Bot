from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email, EmailNotValidError
from rasa_sdk.forms import FormAction
from datetime import datetime
import dateutil.parser

import announcements
import categories
import eduPeople
import sendEmail


class EmailForm(FormAction):
    def name(self) -> Text:
        return "email_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["email"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {

            "email": [self.from_entity(entity="email"),
                      self.from_text(intent="send_email")],
        }

    def validate_email(self, value, dispatcher, tracker, domain):

        if any(tracker.get_latest_entity_values("email")):
            try:
                valid = validate_email(value)
                email = valid.email
                return {"email": value}
            except EmailNotValidError as e:
                dispatcher.utter_message(template="utter_no_email")
                return {"email": None}

        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_message(template="utter_no_email")
            return {"email": None}


class ActionResetEmailSlots(Action):
    def name(self) -> Text:
        return "action_reset_email_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("email", None), SlotSet("subject", None), SlotSet("message", None)]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict", ) -> List[Dict[Text, Any]]:
        smail = sendEmail.send_email("wichatbotinfo@gmail.com", tracker.get_slot("email"), tracker.get_slot("subject"),
                                     tracker.get_slot("message"))
        if smail:
            SlotSet("email", None)
            dispatcher.utter_message(smail)
        else:
            dispatcher.utter_message(
                "???? ???? email ???????? ?????????????????? ???????? ??????????????????: {}".format(tracker.get_slot("email")))
            dispatcher.utter_message(response="utter_help_new")

        return [SlotSet("email", None), SlotSet("subject", None), SlotSet("message", None)]


class ActionSubmitWithFile(Action):
    def name(self) -> Text:
        return "action_submit_email_with_file"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict", ) -> List[Dict[Text, Any]]:
        subject = "???????????? Pdf"
        message = "???????????????? ???? ???????????? ???? ?????????????? ????????????"
        if file_to_send:
            smail = sendEmail.send_email_with_file("wichatbotinfo@gmail.com", tracker.get_slot("email"),
                                                   subject, message, file_to_send)

        if smail:
            SlotSet("email", None)
            dispatcher.utter_message(smail)
        else:
            dispatcher.utter_message(
                "???? ???? email ???????? ?????????????????? ???????? ??????????????????: {}".format(tracker.get_slot("email")))
            dispatcher.utter_message(response="utter_help_new")

        return [SlotSet("email", None)]


class ActionReadFile(Action):
    def name(self):
        return "action_read_file"

    async def run(self, dispatcher, tracker, domain):

        from tika import parser
        if tracker.latest_message['intent'].get('name') == "semester_program":
            file = "files/2021_22_????????????????????_????????????????????.pdf"
            parsed_pdf = parser.from_file(file)
            data = parsed_pdf['content']
            data = data.replace("\n\n", "\n\r")
        elif tracker.latest_message['intent'].get('name') == "year_program":
            file = "files/2021_22_????????_????_??????????????????????_??????????????????.pdf"
            parsed_pdf = parser.from_file(file)
            data = parsed_pdf['content']
           #data = data.replace("\n\n", "\n")
            data = data.replace("\n\n", "\n\r")

        dispatcher.utter_message(data)
        global file_to_send
        file_to_send = file
        message = "???? ???????????? ???? ?????? ???????????? ???? email ???? ???????????????????? ????????????;"
        buttons = [{'title': "?????? ???",
                    'payload': '/send_email_with_file'},
                   {'title': "?????? ???",
                    'payload': '/cancel_email'}]
        dispatcher.utter_message(message, buttons=buttons)
        return []


class ActionProfessorInfo(Action):

    def name(self) -> Text:
        return "action_professor_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # professor_name = "???????????????????? ??????????????????????????"

        professor_name = tracker.get_slot('professor_name')
        print("professor: ", professor_name)
        professor = eduPeople.professor_info(professor_name)
        dispatcher.utter_message(professor["title;lang-el"] + ' - ' + professor[
            "displayName;lang-el"] + "  \n ?????? " + professor["telephoneNumber"] + "  \n  ???? " +
                                 professor[
                                     "labeledURI"] + "  \n " + professor["socialMedia"][
                                     "researchGate"] + "  \n ", image=professor["secondarymail"])
        return [SlotSet("professor_name", None)]


class ActionEduPeople(Action):

    def name(self) -> Text:
        return "action_edu_people"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        temp = eduPeople.edu_people()

        length = len(temp)
        for i in range(length):
            dispatcher.utter_message('???? ' + temp[i]["title"] + " | " +
                                     temp[i]["name"] + '  \n ?????? ' + temp[i][
                                         "telephoneNumber"] + "  \n ???? " + temp[i][
                                         "Uri"] + "  \n  ", image=temp[i]["mail"])
        return []


class ActionAnnouncementsApi(Action):

    def name(self) -> Text:
        return "action_announcements_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        temp = announcements.announcements()

        length = len(temp)

        for i in range(length):
            print(temp[i]["publisher"] + "????????????: " + temp[i]["title"])

            dispatcher.utter_message(
                format(temp[i]["title"]) + "  \n" + temp[i]["publisher"] + "  \n" + dateutil.parser.parse(
                    temp[i]["date"]).strftime(
                    '%d/%m/%Y') + "  \n ????" + "https://apps.iee.ihu.gr/announcements/announcement/" +
                temp[i][
                    "id"])
        return []


class ActionCategoriesAll(Action):

    def name(self) -> Text:
        return "action_categories_all"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        temp = categories.categories_all()
        buttons = []
        length = len(temp)
        for i in range(length):
            buttons.append(
                {"title": temp[i]["name"], "payload": '/category{"category_id":"' + temp[i]["id"] + '"}'})

        message = "???????????????? ???????????????? ?????? ?????? ?????? ???????????????????? ????????????????????: "
        dispatcher.utter_message(message, buttons=buttons)

        print("category_id: ", tracker.get_slot('category_id'))
        # dispatcher.utter_message(response="utter_category")
        return [SlotSet("category_id", tracker.get_slot('category_id'))]


class ActionAnnouncementPerCat(Action):

    def name(self) -> Text:
        return "action_announcement_per_cat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category_id = tracker.get_slot('category_id')

        if category_id:
            temp = announcements.announcements_category(category_id)
            length = len(temp)
            for i in range(length):
                print(temp[i]["publisher"], temp[i]["title"])

                dispatcher.utter_message(
                    temp[i]["publisher"] + "  \n" + dateutil.parser.parse(temp[i]["date"]).strftime(
                        '%d/%m/%Y') + "   \n " + format(
                        temp[i]["title"]) + "  \n ????" + "https://apps.iee.ihu.gr/announcements/announcement/" +
                    temp[i][
                        "id"])
        else:
            print("No category id")

        tracker.slots["category_id"] = None
        print(tracker.slots["category_id"])
        return [SlotSet("category_id", None)]


class ActionCourses(Action):
    def name(self) -> Text:
        return "action_courses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        semester = next(tracker.get_latest_entity_values('semester'), None)
        if str(semester) == '1' or str(semester) == '1??' or str(semester) == '??????????????????':
            dispatcher.utter_message(response="utter_courses_1")
            dispatcher.utter_message(response="utter_help_new")
        elif str(semester) == '2' or str(semester) == '2??' or str(semester) == '????????????':
            dispatcher.utter_message(response="utter_courses_2")
            dispatcher.utter_message(response="utter_help_new")
        elif str(semester) == '3' or str(semester) == '3??' or str(semester) == '??????????':
            dispatcher.utter_message(response="utter_courses_3")
            dispatcher.utter_message(response="utter_help_new")
        else:
            dispatcher.utter_message(text="???? ???????????????????????? ???????????????????????? ???????? (3) ?????????????????? ??????????????")
            dispatcher.utter_message(response="utter_ask_courses")

        return []

# class ActionCheckAmExams(Action):
#    def name(self) -> Text:
#        return "action_check_am_exams"
#
#    def run(self, dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#        # am = next(tracker.get_latest_entity_values('am'), None)
#        am = tracker.get_slot('am')
#
#        if str(am) == '72020':
#            strg = '???????????????????????????? ??????????????!'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(response="utter_septemberExams")
#
#            dispatcher.utter_message(response="utter_help_new")
#        elif str(am) != '72020':
#            strg = '?????????? ????.\n\n?????????????????? ????????!'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(str(am))
#        elif str(am) == '':
#            strg = '???????? ???????? ???????????? :/ ?????? ?????????? ????'
#            dispatcher.utter_message(strg)
#        return []

# class ActionCheckAm(Action):
#    def name(self) -> Text:
#        return "action_check_am"
#
#    def run(self, dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#        am = next(tracker.get_latest_entity_values('am'), None)
#        if str(am) == '72020':
#            strg = '???????????????????????????? ??????????????.'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(response="utter_contactInfo")
#
#            dispatcher.utter_message(response="utter_help_new")
#        elif str(am) != '72020':
#            strg = '?????????? ????.\n\n?????????????????? ????????!'
#            dispatcher.utter_message(strg)
#        else:
#            strg = '???????? ???????? ???????????? :/'
#            dispatcher.utter_message(strg)
#        return []

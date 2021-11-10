from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import announcements
import categories
import eduPeople
import sendEmail


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict", ) -> List[Dict[Text, Any]]:
        sendEmail.send_email("wichatbotinfo@gmail.com", tracker.get_slot("email"), tracker.get_slot("subject"),
                             tracker.get_slot("message"))
        dispatcher.utter_message(
            "Το email έχει αποσταλεί στην διεύθυνση: {}".format(tracker.get_slot("email")))
        dispatcher.utter_message(response="utter_help_new")
        return [SlotSet("email", None), SlotSet("subject", None), SlotSet("message", None)]


class ActionReadFile(Action):
    def name(self):
        return "action_read_file"

    async def run(self, dispatcher, tracker, domain):
        if tracker.latest_message['intent'].get('name') == "semester_program":
            file = "files/2021_22_Χειμ_Εξ_Εβδομαδιαίο_Πρόγραμμα.pdf"
        elif tracker.latest_message['intent'].get('name') == "year_program":
            file = "files/2021_22_Ακαδημαϊκό_Ημερολόγιο.pdf"
        from tika import parser

        parsed_pdf = parser.from_file(file)
        data = parsed_pdf['content']

        dispatcher.utter_message(data)
        return []


class ActionProfessorInfo(Action):

    def name(self) -> Text:
        return "action_professor_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # professor_name = "Παναγιώτης Σαρηγιαννίδης"

        professor_name = tracker.get_slot('professor_name')
        print("professor: ", professor_name)
        professor = eduPeople.professor_info(professor_name)
        dispatcher.utter_message(
            professor["title;lang-el"] + ' - ' + professor[
                "displayName;lang-el"])  # TODO: check for values !=0 || !=""
        dispatcher.utter_message(professor["telephoneNumber"])
        dispatcher.utter_message(image=professor["secondarymail"])  # TODO: base64 way to display
        dispatcher.utter_message(professor["labeledURI"])
        dispatcher.utter_message(professor["socialMedia"]["researchGate"])

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
            dispatcher.utter_message(
                temp[i]["title"] + ' - ' + temp[i]["name"] + ' - ' + temp[i][
                    "telephoneNumber"])  # TODO: check for values !=0 || !=""
            dispatcher.utter_message(image=temp[i]["mail"])  # TODO: base64 way to display
            dispatcher.utter_message(temp[i]["Uri"])
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
            print(temp[i]["publisher"])
            print(temp[i]["title"])
            dispatcher.utter_message(temp[i]["publisher"])
            dispatcher.utter_message(temp[i]["date"])
            dispatcher.utter_message(format(temp[i]["title"]))
            dispatcher.utter_message("https://apps.iee.ihu.gr/announcements/announcement/" + temp[i]["id"])

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
        # buttons.append(
        #     {"title": "Όλες", "payload": ''})

        message = "Παρακαλώ επιλέξτε μια από τις διαθέσιμες κατηγορίες: "
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
                print(temp[i]["publisher"])
                print(temp[i]["title"])
                dispatcher.utter_message(temp[i]["publisher"])
                dispatcher.utter_message(temp[i]["date"])
                dispatcher.utter_message(format(temp[i]["title"]))
                dispatcher.utter_message("https://apps.iee.ihu.gr/announcements/announcement/" + temp[i]["id"])
        else:
            print("No category id")
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
#            strg = 'Ταυτοποιημενος Χρήστης!'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(response="utter_septemberExams")
#
#            dispatcher.utter_message(response="utter_help_new")
#        elif str(am) != '72020':
#            strg = 'Λάθος ΑΜ.\n\nΔοκιμάστε πάλι!'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(str(am))
#        elif str(am) == '':
#            strg = 'Κάτι πήγε στραβά :/ Δεν βρήκα ΑΜ'
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
#            strg = 'Ταυτοποιημενος Χρήστης.'
#            dispatcher.utter_message(strg)
#            dispatcher.utter_message(response="utter_contactInfo")
#
#            dispatcher.utter_message(response="utter_help_new")
#        elif str(am) != '72020':
#            strg = 'Λάθος ΑΜ.\n\nΔοκιμάστε πάλι!'
#            dispatcher.utter_message(strg)
#        else:
#            strg = 'κάτι πήγε στραβά :/'
#            dispatcher.utter_message(strg)
#        return []

class ActionCourses(Action):
    def name(self) -> Text:
        return "action_courses"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        semester = next(tracker.get_latest_entity_values('semester'), None)
        if str(semester) == '1' or str(semester) == 'χειμερινό':
            dispatcher.utter_message(response="utter_courses_1")
            dispatcher.utter_message(response="utter_help_new")
        elif str(semester) == '2' or str(semester) == 'εαρινό':
            dispatcher.utter_message(response="utter_courses_2")
            dispatcher.utter_message(response="utter_help_new")

        return []

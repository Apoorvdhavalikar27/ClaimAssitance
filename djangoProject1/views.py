# from django.http import JsonResponse, HttpResponse
# import spacy
# import re
# import pyttsx3
# import openai
# import json
# from dateutil import parser
# from datetime import datetime
#
# # API key
# # openai.api_key = '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'
# # openai.api_key = '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'
#
# nlp = spacy.load("en_core_web_sm")
# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)
#
#
# def remove_quotes_around_numbers(text):
#     # Use regular expression to match numbers within quotes
#     pattern = re.compile(r'"(\d+)"')
#
#     # Replace matched patterns with the numbers inside the quotes
#     result = pattern.sub(r'\1', text)
#
#     return result
#
#
# def validate_date_format(text):
#     date_patterns = [
#         r'(\d{1,2})[^\d]*(\d{1,2})[^\d]*(\d{2,4})',
#         r'(\d{1,2})(?:st|nd|rd|th)[^\w]*(\w+)[^\w]*(\d{2,4})',
#         r'(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})',
#         r'(\d{1,2})[^\w]*(\w+)[^\w]*(\d{2,4})'
#     ]
#
#     for pattern in date_patterns:
#         match = re.search(pattern, text)
#         if match:
#             groups = match.groups()
#
#             try:
#                 if len(groups) == 3:
#                     return int(groups[0]), datetime.strptime(groups[1], "%B").month, int(groups[2])
#                 elif len(groups) == 2:
#                     return None, datetime.strptime(groups[1], "%B").month, datetime.now().year
#                 else:
#                     return tuple(map(int, groups))
#             except ValueError:
#                 pass
#
#     return "Invalid"
#
#
# def convert_text_to_date(text_date):
#     try:
#         if re.search(r'\b\d{4}\b', text_date) and re.search(r'\b\d{1,2}\b', text_date):
#             date_object = parser.parse(text_date)
#             return date_object.date()
#         else:
#             return "Invalid Date:"
#     except ValueError:
#         return "Invalid Date"
#
#
# def convert_to_month(result):
#     if result != 'Invalid':
#         date_object = datetime(result[2], result[1], result[0])
#         formatted_month = date_object.strftime('%b')
#         new_tuple = (result[0], formatted_month, result[2])
#         return new_tuple
#     else:
#         return "Invalid"
#
#
# def claim_date(text):
#     doc = nlp(text)
#     try:
#         dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
#         return convert_text_to_date(dates[0])
#     except:
#         return "Invalid"
#
#
# def is_substring_present(word, substring):
#     return substring in word and word.index(substring) == 0
#
#
# def extract_expenses(text):
#     expenses = {"travel": 0, "lodging": 0, "food": 0, "maintenance": 0, "laundry": 0, "local": 0}
#
#     matches = re.findall(r'(\d+)\s*(?:rupees?|₹)?\s*(?:on|for|in)\s*(\b\w+\b)', text, re.IGNORECASE)
#
#     for amount, category in matches:
#         if category.lower() in expenses:
#             expenses[category.lower()] += int(amount)
#
#     return expenses
#
#
# def extract_locations(text):
#     doc = nlp(text)
#
#     start_location = None
#     end_location = None
#     try:
#         for token in doc:
#             if token.text.lower() == 'from' and token.i < len(doc) - 1:
#                 start_location = doc[token.i + 1].text
#             elif token.text.lower() == 'to' and token.i < len(doc) - 1:
#                 end_location = doc[token.i + 1].text
#     except:
#         return None, None
#
#     return start_location, end_location
#
# #
# # def claim_expenses(request, value):
# #     if len(value) >= 25:
# #
# #         prompt2 = ("Parse the expenses in category lodging, food, travel, maintenance, laundry, phone/xerox,local "
# #                    f"from the following sentence and all the expenses should be in Integer format without quotes. "
# #                    f"and finally give the output in the JSON format comma seperated with curly brackets "
# #                    f"and keys in double quotes not the values,use json keys as "
# #                    f"LODGING:,FOOD:,TRAVEL:,MAINTENANCE:,LAUNDRY:PHONE: "
# #                    f"and write \"none\" if expenses,locations and date are not mentioned\n\n\"{value}\"")
# #
# #         response = openai.Completion.create(
# #             engine="text-davinci-003",
# #             prompt=prompt2,
# #             max_tokens=140,
# #             temperature=0.7,
# #         )
# #         start, end = extract_locations(value)
# #         result = validate_date_format(value)
# #         date = convert_to_month(result)
# #         parsed_data = response['choices'][0]['text']
# #         filter_string = parsed_data.replace('\n', '')
# #         pattern = r'{[^}]*}'
# #         match = re.search(pattern, filter_string)
# #         if match:
# #             result = match.group()
# #             result = remove_quotes_around_numbers(result)
# #             data = json.loads(result)
# #             response_data = {"START": start, "END": end, "DATE": date, "expenses": data}
# #             # Extract key-value pairs
# #             return JsonResponse(response_data)
# #         else:
# #             return voice_assistant(value)
# #     else:
# #         return HttpResponse("Insufficient data, please specify more details")Claim
#
#
# def voice_assistant(request, value):
#     claim_txt = value
#     # claim_txt = "I have traveled from Mumbai to Pune on 10th of March 2023
#     # and spend 500 for traveling, 3000 on lodging and 300 in food"
#     start_location, end_location = extract_locations(claim_txt)
#     result = validate_date_format(value)
#     date = convert_to_month(result)
#     expenses = extract_expenses(claim_txt)
#     expenses_list = list(expenses.values())
#     traveling = expenses_list[0]
#     lodging = expenses_list[1]
#     food = expenses_list[2]
#     maintenance = expenses_list[3]
#     laundry = expenses_list[4]
#     entertainment = expenses_list[5]
#
#     return JsonResponse({'START': start_location,
#                          'END': end_location,
#                          'DATE': date,
#                          "EXPENSES": {
#                              'TRAVEL': traveling,
#                              'LODGING': lodging,
#                              'FOOD': food,
#                              'MAINTENANCE': maintenance,
#                              "LAUNDRY": laundry,
#                          }
#                          })
from django.http import JsonResponse
import spacy
import re
import pyttsx3
import openai
import json
from dateutil import parser
from datetime import datetime, timedelta

# Free_API_key
openai.api_key = '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'
# openai.api_key = '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'

# chatbot model key
# openai.api_key = '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'

# TextGenration model key
# openai.api_key = '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'

nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init('sapi5')


def remove_quotes_around_numbers(text):
    pattern = re.compile(r'"(\d+)"')
    result = pattern.sub(r'\1', text)
    return result


def extract_date(text):
    doc = nlp(text)

    current_date = datetime.now().date()
    previous_date = current_date - timedelta(days=1)

    extracted_dates = []

    for ent in doc.ents:
        if ent.label_ == "DATE":

            if ent.text.lower() == "today" or ent.text.lower() == "Today":
                extracted_date = current_date
            elif ent.text.lower() == "yesterday" or ent.text.lower() == "Yesterday":
                extracted_date = current_date - timedelta(days=1)
            else:

                extracted_date = parser.parse(ent.text).date()

            if extracted_date == current_date:
                extracted_dates.append(str(current_date))
            elif extracted_date == previous_date:
                extracted_dates.append(str(previous_date))
            else:
                extracted_dates.append(str(extracted_date))

    return extracted_dates[0]


def decide_mode(mode_of_travel):

    mode_of_travel = mode_of_travel.lower()
    if mode_of_travel in ["car", "four wheeler", "4 wheeler"]:
        return "4 wheeler", "vehicle"
    elif mode_of_travel in ["airplane", "aeroplane", "plane", "flight"]:
        return "none", "airplane"
    elif mode_of_travel in ["bike", "two wheeler", "2 wheeler", "scooty"]:
        return "2 wheeler", "vehicle"
    else:
        return "none", mode_of_travel


def validate_date_format(text):
    date_patterns = [
        r'(\d{1,2})[^\d]*(\d{1,2})[^\d]*(\d{2,4})',
        r'(\d{1,2})(?:st|nd|rd|th)[^\w]*(\w+)[^\w]*(\d{2,4})',
        r'(\d{4})[^\d]*(\d{1,2})[^\d]*(\d{1,2})',
        r'(\d{1,2})[^\w]*(\w+)[^\w]*(\d{2,4})'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()

            try:
                if len(groups) == 3:
                    return int(groups[0]), datetime.strptime(groups[1], "%B").month, int(groups[2])
                elif len(groups) == 2:
                    return None, datetime.strptime(groups[1], "%B").month, datetime.now().year
                else:
                    return tuple(map(int, groups))
            except ValueError:
                pass

    return "Invalid"


def convert_text_to_date(text_date):
    try:
        if re.search(r'\b\d{4}\b', text_date) and re.search(r'\b\d{1,2}\b', text_date):
            date_object = parser.parse(text_date)
            return date_object.date()
        else:
            return "Invalid Date:"
    except ValueError:
        return "Invalid Date"


def convert_to_month(result):
    if result != 'Invalid':
        date_object = datetime(result[2], result[1], result[0])
        formatted_month = date_object.strftime('%b')
        new_tuple = (result[0], formatted_month, result[2])
        return new_tuple
    else:
        return "Invalid"


def extract_locations(text):
    doc = nlp(text)

    start_location = None
    end_location = None
    try:
        for token in doc:
            if token.text.lower() == 'from' and token.i < len(doc) - 1:
                start_location = doc[token.i + 1].text
            elif token.text.lower() == 'to' and token.i < len(doc) - 1:
                end_location = doc[token.i + 1].text
    except:
        return None, None

    return start_location, end_location


def claim_expenses(request, value):
    empty_data = {
        "start_location": 'none',
        "end_location": 'none',
        "date": 'none',
        "travelling": 'none',
        "lodging": 'none',
        "food": 'none',
        "maintenance": 'none',
        "laundry": 'none',
        "entertainment": 'none',
        "mode": 'none',
        "local": 'none'
    }

    try:
        if len(value) >= 25:

            prompt2 = ("Parse the expenses in category lodging, food, travel, maintenance, laundry, phone/xerox,local "
                       f"from the following sentence and all the expenses should be in Integer format without quotes. "
                       f"also fetch the start and end location of journey "
                       f"also fetch the date of journey "
                       f"also fetch the mode of journey "
                       f"also fetch the local expenses "
                       f"and finally give the output in the JSON format comma seperated with curly brackets "
                       f"and keys in double quotes not the values,use json keys as "
                       f"START:, END:, DATE:, LODGING:, MODE:, FOOD:, TRAVEL:, MAINTENANCE:, LAUNDRY:, PHONE:, LOCAL: "
                       f"and write \"none\" if expenses,locations and date are not mentioned\n\n\"{value}\"")

            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt2,
                max_tokens=140,
                temperature=0.7,
            )
            start, end = extract_locations(value)
            result = validate_date_format(value)
            date = convert_to_month(result)
            parsed_data = response['choices'][0]['text']
            filter_string = parsed_data.replace('\n', '')
            pattern = r'{[^}]*}'
            match = re.search(pattern, filter_string)
            if match:
                result = match.group()
                result = remove_quotes_around_numbers(result)
                data = json.loads(result)
                vehicle_type, mode_of_journey = decide_mode(data['MODE'])
                response_data = {
                    "start_location": data['START'],
                    "end_location": data['END'],
                    "date": extract_date(value),
                    "travelling": data['TRAVEL'],
                    "lodging": data['LODGING'],
                    "food": data['FOOD'],
                    "maintenance": data['MAINTENANCE'],
                    "laundry": data['LAUNDRY'],
                    "ph/f/x": data['PHONE'],
                    "local": data['LOCAL'],
                    "mode": mode_of_journey,
                    "vehicle": vehicle_type
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse(empty_data)
        else:
            return JsonResponse(empty_data)
    except:
        return JsonResponse(empty_data)

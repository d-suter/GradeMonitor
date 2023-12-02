import requests
import json
import logging

def load_sent_grades():
    try:
        with open('sent_grades.json', 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_sent_grades(sent_grades):
    with open('sent_grades.json', 'w') as file:
        json.dump(list(sent_grades), file)

def send_discord_message(webhook_url, new_grades):
    sent_grades = load_sent_grades()
    embeds = []

    for grade in new_grades:
        grade_id = '-'.join(grade)
        if grade_id not in sent_grades:
            embed = {
                "title": "Neue Note!",
                "description": f"Fach: `{grade[0]}`\nTest: `{grade[1]}`\nDatum: `{grade[2]}`\nNote `{grade[3]}`",
                "color": 3224376,
                "author": {
                    "name": "Grade-Monitor",
                    "url": "https://github.com/d-suter/grade-monitor",
                    "icon_url": "https://avatars.githubusercontent.com/u/93440331?s=400&u=a05cbca990d5ecce2a4be5de46181b8bebf8291f&v=4"
                }
            }
            embeds.append(embed)
            sent_grades.add(grade_id)
            logging.info("New Grade found. Successfully sent the Webhook")

    if embeds:
        data = {
            "content": "@everyone",
            "embeds": embeds,
            "username": "Grade Monitor",
            "avatar_url": "https://avatars.githubusercontent.com/u/93440331?s=400&u=a05cbca990d5ecce2a4be5de46181b8bebf8291f&v=4"
        }
        
        response = requests.post(webhook_url, json=data)
        try:
            response.raise_for_status()
            save_sent_grades(sent_grades)
        except requests.exceptions.HTTPError as err:
            print(f"Error sending message: {err}")

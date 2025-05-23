import base64
import hashlib
import os

import requests

from translator import Translator


class AnkiConnector:
    def __init__(self, audio_dir, deck_name="Default", add_tag_question=False):
        self.deck_name = deck_name
        self.api_url = "http://localhost:8765"
        self.audio_dir = audio_dir
        self.add_tag_question = add_tag_question

    def upload_audio_to_anki(self, filename):
        path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return False

        with open(path, "rb") as f:
            file = f.read()
            b64_data = base64.b64encode(file).decode("utf-8")
            sha1_hash = hashlib.sha1(file).hexdigest()

        new_filename = f"google-{sha1_hash}.mp3"
        payload = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": new_filename,
                "data": b64_data,
                "skipHash": sha1_hash,
            },
        }

        response = requests.post(self.api_url, json=payload)
        result = response.json()
        if result["error"]:
            print(f"Error uploading {filename}: {result['error']}")
            return False

        return new_filename

    def _add_notes(self, cards):
        if not cards:
            print("No cards to add.")
            return

        payload = {"action": "addNotes", "version": 6, "params": {"notes": cards}}
        response = requests.post(self.api_url, json=payload)
        result = response.json()
        if result.get("error"):
            print(f"Error adding cards: {result['error']}")
        else:
            print("Cards added successfully to Anki.")

    def add_cards(self, phrases, tags=None):
        if not phrases:
            print("No phrases to add.")
            return

        if tags is None:
            tags = []

        translator = Translator(self.audio_dir)

        add_tag = []
        if tags and self.add_tag_question:
            add_tag = ["Question"]

        cards = []
        index = 0
        for phrase in phrases:
            index += 1
            audio_filename = f"audio_{index}.mp3"
            translator.generate_audio(phrase, f"{self.audio_dir}/{audio_filename}")
            audio_new_name = self.upload_audio_to_anki(audio_filename)

            if not audio_new_name:
                continue

            translation = translator.translate_to_spanish(phrase)
            cards.append(
                {
                    "deckName": self.deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": f"{phrase}<br>[sound:{audio_new_name}]",
                        "Back": f"{translation}<br>[sound:{audio_new_name}]",
                    },
                    "tags": tags + add_tag if "?" in phrase else tags,
                }
            )

        self._add_notes(cards)

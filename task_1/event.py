import argparse
import datetime
import enum
import json
import random
import string
from collections import defaultdict


class EventType(enum.Enum):
    PRIVATE = "private"
    MEETING = "meeting"
    CORPORATE = "corporate"
    OTHER = "other"


class EventLocation(enum.Enum):
    ZOOM = "zoom"
    TELEGRAM = "telegram"
    OFFICE = "office"
    SKYPE = "skype"
    DISCORD = "discord"


class Event:
    NAMES = ["Alex", "Vova", "Sergey", "Roma", "Polina"]

    def __init__(self, datetime_utc, event_type, name, attendees, location):
        self.datetime_utc = datetime_utc
        self.event_type = EventType(event_type)
        self.name = name
        self.attendees = attendees
        self.location = EventLocation(location)

    def to_dict(self):
        return {
            "datetime_utc": self.datetime_utc.isoformat(),
            "event_type": self.event_type.value,
            "name": self.name,
            "attendees": self.attendees,
            "location": self.location.value,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            datetime.datetime.fromisoformat(data["datetime_utc"]),
            data["event_type"],
            data["name"],
            data["attendees"],
            data["location"],
        )


class EventFactory:
    @classmethod
    def random_string(cls, max_length=20):
        return "".join(random.choices(string.ascii_letters + string.digits, k=max_length))

    @classmethod
    def generate_event(cls, date_from, date_to, event_type=None):
        delta = date_to - date_from
        random_days = random.randint(0, delta.days)
        random_time = datetime.time(random.randint(0, 23), random.randint(0, 59))
        datetime_utc = datetime.datetime.combine(date_from + datetime.timedelta(days=random_days), random_time)
        event_type = event_type or random.choice(list(EventType)).value
        name = cls.random_string()
        attendees = random.sample(Event.NAMES, random.randint(1, len(Event.NAMES)))
        location = random.choice(list(EventLocation)).value

        return Event(datetime_utc, event_type, name, attendees, location)


class EventProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        events = self.load_events()
        grouped_events = self.group_events(events)
        self.save_grouped_events(grouped_events)

    def load_events(self):
        with open(self.input_file, "r") as f:
            data = json.load(f)
        return [Event.from_dict(item) for item in data]

    def group_events(self, events):
        grouped = defaultdict(list)
        for event in events:
            if event.event_type != EventType.OTHER:
                date = event.datetime_utc.date().isoformat()
                grouped[date].append(event.to_dict())

        for date in grouped:
            grouped[date].sort(key=lambda x: x["datetime_utc"])

        return dict(grouped)

    def save_grouped_events(self, grouped_events):
        with open(self.output_file, "w") as f:
            json.dump(grouped_events, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Group events by date.")
    parser.add_argument("-i", "--input", help="Input JSON file", default="input.json")
    parser.add_argument("-o", "--output", help="Output JSON file", default="output.json")
    args = parser.parse_args()

    processor = EventProcessor(args.input, args.output)
    processor.process()

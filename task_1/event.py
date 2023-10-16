import argparse
import datetime
import enum
import json
import random
import string


class EventType(enum.Enum):
    PRIVATE = "private"
    MEETING = "meeting"
    CORPORATE = "corporate"
    OTHER = "other"


class Event:
    NAMES = ["Alex", "Vova", "Sergey", "Roma", "Polina"]

    def __init__(self, datetime_utc, event_type, name, attendees, location):
        self.datetime_utc = datetime_utc
        self.event_type = EventType(event_type)
        self.name = name
        self.attendees = attendees
        self.location = location

    def to_dict(self):
        return {
            "datetime_utc": self.datetime_utc.isoformat(),
            "event_type": self.event_type.value,
            "name": self.name,
            "attendees": self.attendees,
            "location": self.location,
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
    LOCATIONS = ["zoom", "telegram", "office", "skype", "discord"]

    @classmethod
    def random_string(cls, max_length):
        length = random.randint(1, max_length)
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @classmethod
    def generate_event(cls, date_from, date_to):
        datetime_utc = datetime.datetime.combine(
            random.choice([date for date in cls.date_range(date_from, date_to)]),
            datetime.time(random.randint(0, 23), random.randint(0, 59)),
        )
        event_type = random.choice(list(EventType)).value
        name = " ".join(cls.random_string(20) for _ in range(random.randint(1, 5)))
        attendees = random.sample(Event.NAMES, random.randint(1, len(Event.NAMES)))
        location = random.choice(cls.LOCATIONS)
        return Event(datetime_utc, event_type, name, attendees, location)

    @staticmethod
    def date_range(date_from, date_to):
        return [date_from + datetime.timedelta(days=x) for x in range(0, (date_to - date_from).days + 1)]


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
        grouped = {}
        for event in events:
            if event.event_type != EventType.OTHER:
                date = event.datetime_utc.date().isoformat()
                if date not in grouped:
                    grouped[date] = []
                grouped[date].append(event.to_dict())
        for date, events_for_date in grouped.items():
            grouped[date] = sorted(events_for_date, key=lambda x: x["datetime_utc"])
        return grouped

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

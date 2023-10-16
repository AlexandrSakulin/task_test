import json
from datetime import datetime, timedelta

import pytest

from task_test.task_1.event import EventFactory, EventProcessor


@pytest.fixture(scope="module")
def random_event():
    return EventFactory.generate_event(datetime.utcnow() - timedelta(days=7), datetime.utcnow())


@pytest.fixture(scope="function")
def events_list():
    return [EventFactory.generate_event(datetime.utcnow() - timedelta(days=7), datetime.utcnow()) for _ in range(10)]


@pytest.mark.grouping
def test_grouping(events_list):
    """Проверка, что события для каждой даты в группированном списке упорядочены по времени"""
    processor = EventProcessor("dummy_input.json", "dummy_output.json")
    grouped = processor.group_events(events_list)
    for _, events in grouped.items():
        assert all(
            events[i]["datetime_utc"] <= events[i + 1]["datetime_utc"] for i in range(len(events) - 1)
        ), "События не упорядочены по времени"


@pytest.mark.loading
def test_loading_invalid_event_type():
    """Проверяет, что при попытке загрузить событие с недействительным типом события возникает исключение"""
    with open("temp.json", "w") as f:
        json.dump(
            [
                {
                    "datetime_utc": datetime.utcnow().isoformat(),
                    "event_type": "invalid_type",
                    "name": "Test Event",
                    "attendees": ["Egor"],
                    "location": "zoom",
                }
            ],
            f,
        )

    processor = EventProcessor("temp.json", "dummy_output.json")
    with pytest.raises(ValueError):
        processor.load_events()


@pytest.mark.output
def test_output(events_list):
    """Проверка, что события для каждой даты в группированном списке упорядочены по времени."""
    processor = EventProcessor("dummy_input.json", "temp_output.json")
    grouped = processor.group_events(events_list)
    processor.save_grouped_events(grouped)

    with open("temp_output.json", "r") as f:
        saved_data = json.load(f)

    assert grouped == saved_data, "События не упорядоточенны по времени"


@pytest.mark.random_event
def test_random_event_creation(random_event):
    """Проверка корректности создания случайного события."""
    assert random_event.datetime_utc is not None, "Поле datetime_utc пустое"
    assert random_event.event_type is not None, "Поле event_type пустое"
    assert random_event.name is not None, "Поле name пустое"
    assert random_event.attendees is not None, "Поле attendees пустое"
    assert random_event.location is not None, "Поле location пустое"

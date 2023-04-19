import datetime
import uuid
from dataclasses import dataclass

import dateutil.parser
from ics import Event as IcsEvent
from sqlmodel import Field, SQLModel


@dataclass
class Date:
    date: datetime.date

    @staticmethod
    def from_gibberish(s):
        return Date(date=dateutil.parser.parse(s, fuzzy=True).date())

    def to_str(self):
        return self.date.isoformat()


class EventBase(SQLModel):
    name: str
    start: str
    end: str


class Event(EventBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    @staticmethod
    def from_gibberish(s):
        date = Date.from_gibberish(s)
        return Event(name=s, start=date.to_str(), end=date.to_str())

    def to_ics(self):
        e = IcsEvent()
        e.name = self.name
        e.begin = datetime.date.fromisoformat(self.start)
        e.end = datetime.date.fromisoformat(self.end)
        e.make_all_day()
        return e

    def __eq__(self, other):
        return self.name == other.name

import functools
import os
import threading

import uvicorn as uvicorn
from fastapi import Depends, FastAPI
from ics import Calendar
from sqlmodel import Session, SQLModel, create_engine, select

from discord_client import HangoutsClient
from events import Event

app = FastAPI()


@functools.cache
def get_engine():
    return create_engine(
        os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///tmp.db"),
        echo=True,
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    with Session(get_engine()) as session:
        yield session


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/calendar.ics")
def read_root(
    *,
    s: Session = Depends(get_session),
):
    statement = select(Event)
    results = s.exec(statement).all()

    c = Calendar()
    for event in results:
        c.events.add(event.to_ics())
    return c.serialize()


def sync_events(new_events):
    print(f"writing {len(new_events)} to events")
    with Session(get_engine()) as s:
        print(get_engine().table_names)
    for event in new_events:
        s.add(event)
    s.commit()


def start_discord_client():
    client = HangoutsClient(
        text_channel_id=int(os.environ["DISCORD_TEXT_CHANNEL_ID"]), on_sync=sync_events
    )
    client.run(os.environ["DISCORD_TOKEN"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    threading.Thread(target=start_discord_client).start()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("UVICORN_PORT", "80")),
    )

from aiogram.fsm.state import State, StatesGroup


class PrsGeneration(StatesGroup):
    selecting_topic = State()
    selecting_language = State()
    selecting_requirements = State()
    generating = State()

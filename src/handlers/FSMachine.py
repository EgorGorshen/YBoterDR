from aiogram.fsm.state import State, StatesGroup


class FindTrack(StatesGroup):
    get_request = State()
    set_track = State()

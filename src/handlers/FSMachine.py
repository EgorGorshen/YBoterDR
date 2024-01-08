from aiogram.fsm.state import State, StatesGroup


class FindTrack(StatesGroup):
    get_request = State()
    choose_track = State()
    set_track = State()


class Toast(StatesGroup):
    toast = State()
    finish_toast = State()


class BlockUser(StatesGroup):
    choose_delta_time = State()
    add_to_db = State()

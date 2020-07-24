from aiogram.utils.helper import Helper, HelperMode, ListItem

class TestStates(Helper):
    mode = HelperMode.snake_case

    STATE_ADD_TOKEN = ListItem()
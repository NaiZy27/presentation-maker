from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
        InlineKeyboardButton(text="Английский 🇬🇧", callback_data="lang_en"),
    ]]
)

no_requirements_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Без особых требований")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

remove_keyboard = ReplyKeyboardRemove()

document_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Готово ✅", callback_data="done_finish"),
        InlineKeyboardButton(text="Перегенерировать 🔄", callback_data="regenerate"),
    ]]
)

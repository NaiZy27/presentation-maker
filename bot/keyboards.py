from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

slides_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="10 слайдов", callback_data="slides_10"),
        InlineKeyboardButton(text="15 слайдов", callback_data="slides_15"),
    ]]
)

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

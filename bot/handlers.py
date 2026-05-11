import os
import re
import tempfile

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import PrsGeneration
from bot.keyboards import (
    language_keyboard,
    no_requirements_keyboard,
    remove_keyboard,
    document_keyboard,
)
from services.gemini import generate_content
from services.pptx_builder import build_presentation
from core.logger import get_logger

logger = get_logger(__name__)

router = Router()

_START_TEXT = (
    "Привет! Я помогу создать презентацию для РЭУ им. Г.В. Плеханова.\n\n"
    "Введи тему презентации:"
)

_LANG_CALLBACKS = {
    "lang_ru": ("русский", "🇷🇺"),
    "lang_en": ("английский", "🇬🇧"),
}


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_START_TEXT, reply_markup=remove_keyboard)
    await state.set_state(PrsGeneration.selecting_topic)


@router.message(PrsGeneration.selecting_topic, F.text)
async def handle_topic(message: types.Message, state: FSMContext) -> None:
    topic = message.text.strip()
    if len(topic) < 3:
        await message.answer("Тема слишком короткая - минимум 3 символа. Попробуй ещё раз:")
        return
    await state.update_data(topic=topic.capitalize())
    await message.answer("Выбери язык презентации:", reply_markup=language_keyboard)
    await state.set_state(PrsGeneration.selecting_language)


@router.callback_query(PrsGeneration.selecting_language, F.data.in_({"lang_ru", "lang_en"}))
async def handle_language(callback: types.CallbackQuery, state: FSMContext) -> None:
    language, flag = _LANG_CALLBACKS[callback.data]
    await callback.answer(f"Язык выбран {flag}")
    await state.update_data(language=language)
    await callback.message.answer(
        "Есть особые требования к презентации?\n"
        "Напиши их или нажми кнопку ниже:",
        reply_markup=no_requirements_keyboard,
    )
    await state.set_state(PrsGeneration.selecting_requirements)


@router.message(PrsGeneration.selecting_language)
async def delete_language_state_message(message: types.Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass


@router.message(PrsGeneration.selecting_requirements, F.text)
async def handle_requirements(message: types.Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    topic = user_data["topic"]
    language = user_data["language"]
    requirements = message.text.strip()

    await state.set_state(PrsGeneration.generating)
    await _run_generation(message, state, topic, language, requirements, user_id=message.from_user.id)


@router.message(PrsGeneration.generating)
async def handle_during_generation(message: types.Message) -> None:
    await message.answer("Презентация генерируется... 🔍")


@router.callback_query(F.data == "done_finish")
async def handle_done_finish(callback: types.CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == "regenerate")
async def handle_regenerate(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == PrsGeneration.generating:
        await callback.answer("Презентация генерируется...")
        return

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    user_data = await state.get_data()
    await state.set_state(PrsGeneration.generating)
    await _run_generation(
        callback.message,
        state,
        topic=user_data["regen_topic"],
        language=user_data["regen_language"],
        requirements=user_data["regen_requirements"],
        user_id=callback.from_user.id,
    )


async def _run_generation(
    message: types.Message,
    state: FSMContext,
    topic: str,
    language: str,
    requirements: str,
    user_id: int,
) -> None:
    progress = await message.answer("✏️ Генерация текста...", reply_markup=remove_keyboard)

    try:
        content = await generate_content(topic, language, requirements)

        await progress.delete()
        progress = await message.answer("🔍 Поиск картинок...")

        safe_topic = re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_")[:40]
        output_path = os.path.join(tempfile.gettempdir(), f"{safe_topic}_{user_id}.pptx")

        try:
            await progress.delete()
            progress = await message.answer("🧱 Собираю презентацию...")
            await build_presentation(content, output_path)

            await message.answer_document(
                types.FSInputFile(output_path, filename=f"{safe_topic}_{user_id}.pptx"),
                caption=f"Презентация на тему: {topic}. Титульный слайд заполняется вручную.",
                reply_markup=document_keyboard,
            )
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

        await progress.delete()

        await state.update_data(regen_topic=topic, regen_language=language, regen_requirements=requirements)
        await state.set_state(None)
        await message.answer("Для новой презентации напиши /start 🚀")

    except Exception as e:
        logger.error("Generation failed for user %d: %s", user_id, e, exc_info=True)
        try:
            await progress.delete()
        except Exception:
            pass
        await message.answer("Произошла ошибка при генерации презентации. Попробуй ещё раз — /start")
        await state.clear()


@router.message(~F.text)
async def delete_non_text(message: types.Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass

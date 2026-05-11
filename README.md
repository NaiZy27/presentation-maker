# Presentation Maker Bot

Telegram-бот, генерирующий академические презентации (.pptx) на основе темы. Текст - через Gemini, картинки - через Unsplash, вставка в заранее размеченный шаблон PowerPoint.

## Быстрый старт (macOS)

### 1. Установить Redis
```bash
brew install redis
brew services start redis
```

### 2. Получить ключи
- **Telegram Bot Token** - [@BotFather](https://t.me/BotFather)
- **Gemini API Key** - [ai.google.dev](https://ai.google.dev)
- **Unsplash Access Key** - [unsplash.com/developers](https://unsplash.com/developers) (создать приложение)

### 3. Настроить окружение
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# заполнить .env своими ключами
```

### 4. Запуск
```bash
python main.py
```

## Использование

1. В Telegram: `/start`
2. Ввести тему презентации
3. Выбрать язык (Русский / Английский)
4. Ввести требования или нажать «Без особых требований»
5. Получить готовый `.pptx`
6. Открыть в PowerPoint, заполнить титульный слайд (Группа, ФИО)

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("bot")

# Developed by Hamid Yarali
# GitHub: https://github.com/HamidYaraliOfficial
# Instagram: https://www.instagram.com/hamidyaraliofficial?igsh=MWpxZjhhMHZuNnlpYQ==
# Telegram: @Hamid_Yarali

BOT_TOKEN = "" #توکن جایگزین بشه
ADMIN_ID = 1111111 #ایدی عددی ادمین 

user_keyboard_en = ReplyKeyboardMarkup([
    ["🆘 Support", "📋 My Info"],
    [KeyboardButton("📱 Share My Number", request_contact=True)]
], resize_keyboard=True)

user_keyboard_zh = ReplyKeyboardMarkup([
    ["🆘 支持", "📋 我的信息"],
    [KeyboardButton("📱 分享我的号码", request_contact=True)]
], resize_keyboard=True)

user_keyboard_ru = ReplyKeyboardMarkup([
    ["🆘 Поддержка", "📋 Моя информация"],
    [KeyboardButton("📱 Поделиться номером", request_contact=True)]
], resize_keyboard=True)

admin_keyboard_en = ReplyKeyboardMarkup([
    ["📊 Bot Stats", "👥 Bot Users"],
    ["📢 Broadcast Message", "📨 Send Message to User"],
    ["🚫 Block User", "✅ Unblock User"],
    ["📞 Users' Phone Numbers", "📋 My Info"]
], resize_keyboard=True)

admin_keyboard_zh = ReplyKeyboardMarkup([
    ["📊 机器人统计", "👥 机器人用户"],
    ["📢 广播消息", "📨 给用户发送消息"],
    ["🚫 屏蔽用户", "✅ 解除屏蔽用户"],
    ["📞 用户电话号码", "📋 我的信息"]
], resize_keyboard=True)

admin_keyboard_ru = ReplyKeyboardMarkup([
    ["📊 Статистика бота", "👥 Пользователи бота"],
    ["📢 Рассылка сообщений", "📨 Отправить сообщение пользователю"],
    ["🚫 Заблокировать пользователя", "✅ Разблокировать пользователя"],
    ["📞 Номера телефонов пользователей", "📋 Моя информация"]
], resize_keyboard=True)

awaiting_broadcast = {}
awaiting_support = {}
reply_targets = {}
awaiting_direct_id = {}
awaiting_direct_message = {}
awaiting_block_id = {}
awaiting_unblock_id = {}

def ensure_file(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")

def save_user(user_id, name):
    ensure_file("users.txt")
    with open("users.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    ids = [line.split(" - ")[0] for line in lines]
    if str(user_id) not in ids:
        lines.append(f"{user_id} - {name}")
        with open("users.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write(str(len(lines)))

def is_blocked(user_id):
    if not os.path.exists("blocked.txt"):
        return False
    with open("blocked.txt", "r", encoding="utf-8") as f:
        return str(user_id) in [ln.strip() for ln in f if ln.strip()]

def block_user(user_id):
    ensure_file("blocked.txt")
    with open("blocked.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if str(user_id) not in lines:
        lines.append(str(user_id))
        with open("blocked.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

def unblock_user(user_id):
    if not os.path.exists("blocked.txt"):
        return
    with open("blocked.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    lines = [ln for ln in lines if ln != str(user_id)]
    with open("blocked.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

def save_phone(user_id, name, phone):
    ensure_file("phones.txt")
    updated = False
    with open("phones.txt", "r", encoding="utf-8") as f:
        rows = [ln.strip() for ln in f if ln.strip()]
    new_rows = []
    for row in rows:
        parts = [p.strip() for p in row.split(" - ")]
        if len(parts) >= 3 and parts[0] == str(user_id):
            new_rows.append(f"{user_id} - {name} - {phone}")
            updated = True
        else:
            new_rows.append(row)
    if not updated:
        new_rows.append(f"{user_id} - {name} - {phone}")
    with open("phones.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(new_rows) + "\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.full_name)
    if is_blocked(user.id) and user.id != ADMIN_ID:
        await update.message.reply_text({
            "fa": "⛔ شما بلاک شده‌اید.",
            "en": "⛔ You are blocked.",
            "zh": "⛔ 您已被屏蔽。",
            "ru": "⛔ Вы заблокированы."
        }.get(context.user_data.get("lang", "fa")))
        return
    if user.id == ADMIN_ID:
        await update.message.reply_text({
            "fa": "🎛️ خوش آمدی ادمین!",
            "en": "🎛️ Welcome Admin!",
            "zh": "🎛️ 欢迎管理员！",
            "ru": "🎛️ Добро пожаловать, администратор!"
        }.get(context.user_data.get("lang", "fa")), 
        reply_markup={
            "fa": admin_keyboard,
            "en": admin_keyboard_en,
            "zh": admin_keyboard_zh,
            "ru": admin_keyboard_ru
        }.get(context.user_data.get("lang", "fa")))
    else:
        await update.message.reply_text({
            "fa": "سلام به ربات پیامرسان شخصی من خیلی خوش آمدید!:",
            "en": "Hello, welcome to my personal messaging bot!",
            "zh": "您好，欢迎体验我的个人消息机器人！",
            "ru": "Привет, добро пожаловать в мой личный мессенджер!"
        }.get(context.user_data.get("lang", "fa")), 
        reply_markup={
            "fa": user_keyboard,
            "en": user_keyboard_en,
            "zh": user_keyboard_zh,
            "ru": user_keyboard_ru
        }.get(context.user_data.get("lang", "fa")))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message
    text = msg.text or ""
    contact = msg.contact

    if is_blocked(user.id) and user.id != ADMIN_ID:
        await msg.reply_text({
            "fa": "⛔ شما بلاک شده‌اید.",
            "en": "⛔ You are blocked.",
            "zh": "⛔ 您已被屏蔽。",
            "ru": "⛔ Вы заблокированы."
        }.get(context.user_data.get("lang", "fa")))
        return

    if contact:
        phone = contact.phone_number
        save_phone(user.id, user.full_name, phone)
        await msg.reply_text({
            "fa": "✅ شماره شما ذخیره شد.",
            "en": "✅ Your number has been saved.",
            "zh": "✅ 您的号码已保存。",
            "ru": "✅ Ваш номер сохранен."
        }.get(context.user_data.get("lang", "fa")))
        await context.bot.send_message(chat_id=ADMIN_ID,
            text=f"📱 {'شماره جدید' if context.user_data.get('lang', 'fa') == 'fa' else 'New number' if context.user_data.get('lang', 'fa') == 'en' else '新号码' if context.user_data.get('lang', 'fa') == 'zh' else 'Новый номер'}:\n"
                 f"{'نام' if context.user_data.get('lang', 'fa') == 'fa' else 'Name' if context.user_data.get('lang', 'fa') == 'en' else '姓名' if context.user_data.get('lang', 'fa') == 'zh' else 'Имя'}: {user.full_name}\n"
                 f"{'آیدی' if context.user_data.get('lang', 'fa') == 'fa' else 'ID' if context.user_data.get('lang', 'fa') == 'en' else 'ID' if context.user_data.get('lang', 'fa') == 'zh' else 'ID'}: {user.id}\n"
                 f"{'شماره' if context.user_data.get('lang', 'fa') == 'fa' else 'Number' if context.user_data.get('lang', 'fa') == 'en' else '号码' if context.user_data.get('lang', 'fa') == 'zh' else 'Номер'}: {phone}")
        return

    if reply_targets.get(user.id):
        target_id = reply_targets.pop(user.id)
        try:
            await context.bot.copy_message(chat_id=target_id, from_chat_id=msg.chat_id, message_id=msg.message_id)
            await msg.reply_text({
                "fa": "✅ پیام شما برای کاربر ارسال شد.",
                "en": "✅ Your message was sent to the user.",
                "zh": "✅ 您的消息已发送给用户。",
                "ru": "✅ Ваше сообщение отправлено пользователю."
            }.get(context.user_data.get("lang", "fa")))
        except Exception as e:
            logger.error(f"{'ارسال پاسخ به کاربر' if context.user_data.get('lang', 'fa') == 'fa' else 'Sending response to user' if context.user_data.get('lang', 'fa') == 'en' else '发送回复给用户' if context.user_data.get('lang', 'fa') == 'zh' else 'Отправка ответа пользователю'} {target_id} {'ناکام' if context.user_data.get('lang', 'fa') == 'fa' else 'failed' if context.user_data.get('lang', 'fa') == 'en' else '失败' if context.user_data.get('lang', 'fa') == 'zh' else 'не удалась'}: {e}")
            await msg.reply_text({
                "fa": "❌ ارسال پیام به کاربر ناموفق بود.",
                "en": "❌ Sending message to user failed.",
                "zh": "❌ 发送消息给用户失败。",
                "ru": "❌ Отправка сообщения пользователю не удалась."
            }.get(context.user_data.get("lang", "fa")))
        return

    if user.id == ADMIN_ID:
        if text == "📊 آمار ربات" or text == "📊 Bot Stats" or text == "📊 机器人统计" or text == "📊 Статистика бота":
            if os.path.exists("stats.txt"):
                with open("stats.txt", "r", encoding="utf-8") as f:
                    count = f.read().strip() or "0"
                await msg.reply_text({
                    "fa": f"📈 تعداد کاربران: {count}",
                    "en": f"📈 Number of users: {count}",
                    "zh": f"📈 用户数量: {count}",
                    "ru": f"📈 Количество пользователей: {count}"
                }.get(context.user_data.get("lang", "fa")))
            else:
                await msg.reply_text({
                    "fa": "📈 هیچ کاربری ثبت نشده.",
                    "en": "📈 No users registered.",
                    "zh": "📈 没有注册用户。",
                    "ru": "📈 Пользователи не зарегистрированы."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "👥 کاربران ربات" or text == "👥 Bot Users" or text == "👥 机器人用户" or text == "👥 Пользователи бота":
            if os.path.exists("users.txt"):
                with open("users.txt", "r", encoding="utf-8") as f:
                    users = f.read().strip()
                await msg.reply_text({
                    "fa": f"👥 لیست کاربران:\n{users or 'خالی'}",
                    "en": f"👥 List of users:\n{users or 'Empty'}",
                    "zh": f"👥 用户列表:\n{users or '空'}",
                    "ru": f"👥 Список пользователей:\n{users or 'Пусто'}"
                }.get(context.user_data.get("lang", "fa")))
            else:
                await msg.reply_text({
                    "fa": "👥 لیست خالی است.",
                    "en": "👥 List is empty.",
                    "zh": "👥 列表为空。",
                    "ru": "👥 Список пуст."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "📢 پیام همگانی" or text == "📢 Broadcast Message" or text == "📢 广播消息" or text == "📢 Рассылка сообщений":
            awaiting_broadcast[user.id] = True
            await msg.reply_text({
                "fa": "📝 پیام خود را بفرستید:",
                "en": "📝 Send your message:",
                "zh": "📝 发送您的消息：",
                "ru": "📝 Отправьте ваше сообщение:"
            }.get(context.user_data.get("lang", "fa")))
        elif awaiting_broadcast.get(user.id):
            awaiting_broadcast.pop(user.id)
            if os.path.exists("users.txt"):
                with open("users.txt", "r", encoding="utf-8") as f:
                    lines = [ln.strip() for ln in f if ln.strip()]
                for line in lines:
                    try:
                        uid = int(line.split(" - ")[0])
                        if not is_blocked(uid):
                            await context.bot.copy_message(chat_id=uid, from_chat_id=msg.chat_id, message_id=msg.message_id)
                    except Exception as e:
                        logger.warning(f"{'ارسال همگانی به' if context.user_data.get('lang', 'fa') == 'fa' else 'Broadcast to' if context.user_data.get('lang', 'fa') == 'en' else '广播至' if context.user_data.get('lang', 'fa') == 'zh' else 'Рассылка для'} {line} {'ناکام' if context.user_data.get('lang', 'fa') == 'fa' else 'failed' if context.user_data.get('lang', 'fa') == 'en' else '失败' if context.user_data.get('lang', 'fa') == 'zh' else 'не удалась'}: {e}")
            await msg.reply_text({
                "fa": "✅ پیام همگانی ارسال شد.",
                "en": "✅ Broadcast message sent.",
                "zh": "✅ 广播消息已发送。",
                "ru": "✅ Рассылка сообщений отправлена."
            }.get(context.user_data.get("lang", "fa")))
        elif text == "📨 ارسال پیام به کاربر" or text == "📨 Send Message to User" or text == "📨 给用户发送消息" or text == "📨 Отправить сообщение пользователю":
            awaiting_direct_id[user.id] = True
            await msg.reply_text({
                "fa": "🔢 آیدی عددی کاربر را وارد کنید:",
                "en": "🔢 Enter the user's numeric ID:",
                "zh": "🔢 输入用户的数字ID：",
                "ru": "🔢 Введите числовой ID пользователя:"
            }.get(context.user_data.get("lang", "fa")))
        elif awaiting_direct_id.get(user.id):
            awaiting_direct_id.pop(user.id)
            try:
                target_id = int(text.strip())
                awaiting_direct_message[user.id] = target_id
                await msg.reply_text({
                    "fa": "✉️ حالا پیام خود را برای کاربر ارسال کن:",
                    "en": "✉️ Now send your message to the user:",
                    "zh": "✉️ 现在向用户发送您的消息：",
                    "ru": "✉️ Теперь отправьте сообщение пользователю:"
                }.get(context.user_data.get("lang", "fa")))
            except Exception:
                await msg.reply_text({
                    "fa": "❌ آیدی عددی نامعتبر بود.",
                    "en": "❌ Invalid numeric ID.",
                    "zh": "❌ 无效的数字ID。",
                    "ru": "❌ Недействительный числовой ID."
                }.get(context.user_data.get("lang", "fa")))
        elif awaiting_direct_message.get(user.id):
            target_id = awaiting_direct_message.pop(user.id)
            try:
                await context.bot.copy_message(chat_id=target_id, from_chat_id=msg.chat_id, message_id=msg.message_id)
                await msg.reply_text({
                    "fa": "✅ پیام برای کاربر ارسال شد.",
                    "en": "✅ Message sent to the user.",
                    "zh": "✅ 消息已发送给用户。",
                    "ru": "✅ Сообщение отправлено пользователю."
                }.get(context.user_data.get("lang", "fa")))
            except Exception as e:
                logger.error(f"{'ارسال پیام به کاربر' if context.user_data.get('lang', 'fa') == 'fa' else 'Sending message to user' if context.user_data.get('lang', 'fa') == 'en' else '发送消息给用户' if context.user_data.get('lang', 'fa') == 'zh' else 'Отправка сообщения пользователю'} {target_id} {'ناموفق بود' if context.user_data.get('lang', 'fa') == 'fa' else 'failed' if context.user_data.get('lang', 'fa') == 'en' else '失败' if context.user_data.get('lang', 'fa') == 'zh' else 'не удалась'}: {e}")
                await msg.reply_text({
                    "fa": "❌ ارسال پیام به کاربر ناموفق بود.",
                    "en": "❌ Sending message to user failed.",
                    "zh": "❌ 发送消息给用户失败。",
                    "ru": "❌ Отправка сообщения пользователю не удалась."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "🚫 بلاک کاربر" or text == "🚫 Block User" or text == "🚫 屏蔽用户" or text == "🚫 Заблокировать пользователя":
            awaiting_block_id[user.id] = True
            await msg.reply_text({
                "fa": "🔒 آیدی عددی کاربر را وارد کنید:",
                "en": "🔒 Enter the user's numeric ID:",
                "zh": "🔒 输入用户的数字ID：",
                "ru": "🔒 Введите числовой ID пользователя:"
            }.get(context.user_data.get("lang", "fa")))
        elif awaiting_block_id.get(user.id):
            awaiting_block_id.pop(user.id)
            try:
                target_id = int(text.strip())
                block_user(target_id)
                await msg.reply_text({
                    "fa": f"🚫 کاربر {target_id} بلاک شد.",
                    "en": f"🚫 User {target_id} blocked.",
                    "zh": f"🚫 用户 {target_id} 已被屏蔽。",
                    "ru": f"🚫 Пользователь {target_id} заблокирован."
                }.get(context.user_data.get("lang", "fa")))
            except Exception:
                await msg.reply_text({
                    "fa": "❌ آیدی عددی نامعتبر بود.",
                    "en": "❌ Invalid numeric ID.",
                    "zh": "❌ 无效的数字ID。",
                    "ru": "❌ Недействительный числовой ID."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "✅ آنبلاک کاربر" or text == "✅ Unblock User" or text == "✅ 解除屏蔽用户" or text == "✅ Разблокировать пользователя":
            awaiting_unblock_id[user.id] = True
            await msg.reply_text({
                "fa": "🔓 آیدی عددی کاربر را وارد کنید:",
                "en": "🔓 Enter the user's numeric ID:",
                "zh": "🔓 输入用户的数字ID：",
                "ru": "🔓 Введите числовой ID пользователя:"
            }.get(context.user_data.get("lang", "fa")))
        elif awaiting_unblock_id.get(user.id):
            awaiting_unblock_id.pop(user.id)
            try:
                target_id = int(text.strip())
                unblock_user(target_id)
                await msg.reply_text({
                    "fa": f"✅ کاربر {target_id} آنبلاک شد.",
                    "en": f"✅ User {target_id} unblocked.",
                    "zh": f"✅ 用户 {target_id} 已解除屏蔽。",
                    "ru": f"✅ Пользователь {target_id} разблокирован."
                }.get(context.user_data.get("lang", "fa")))
            except Exception:
                await msg.reply_text({
                    "fa": "❌ آیدی عددی نامعتبر بود.",
                    "en": "❌ Invalid numeric ID.",
                    "zh": "❌ 无效的数字ID。",
                    "ru": "❌ Недействительный числовой ID."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "📞 شماره موبایل کاربران" or text == "📞 Users' Phone Numbers" or text == "📞 用户电话号码" or text == "📞 Номера телефонов пользователей":
            if os.path.exists("phones.txt"):
                with open("phones.txt", "r", encoding="utf-8") as f:
                    phones = f.read().strip()
                await msg.reply_text({
                    "fa": f"📞 شماره‌ها:\n{phones or 'خالی'}",
                    "en": f"📞 Numbers:\n{phones or 'Empty'}",
                    "zh": f"📞 号码:\n{phones or '空'}",
                    "ru": f"📞 Номера:\n{phones or 'Пусто'}"
                }.get(context.user_data.get("lang", "fa")))
            else:
                await msg.reply_text({
                    "fa": "📞 هیچ شماره‌ای ثبت نشده.",
                    "en": "📞 No numbers registered.",
                    "zh": "📞 没有注册的号码。",
                    "ru": "📞 Номера не зарегистрированы."
                }.get(context.user_data.get("lang", "fa")))
        elif text == "📋 اطلاعات من" or text == "📋 My Info" or text == "📋 我的信息" or text == "📋 Моя информация":
            info = {
                "fa": f"🆔 آیدی عددی شما: {user.id}\n👤 نام شما: {user.full_name}",
                "en": f"🆔 Your numeric ID: {user.id}\n👤 Your name: {user.full_name}",
                "zh": f"🆔 您的数字ID: {user.id}\n👤 您的名字: {user.full_name}",
                "ru": f"🆔 Ваш числовой ID: {user.id}\n👤 Ваше имя: {user.full_name}"
            }.get(context.user_data.get("lang", "fa"))
            phone = None
            if os.path.exists("phones.txt"):
                with open("phones.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(" - ")
                        if len(parts) >= 3 and parts[0] == str(user.id):
                            phone = parts[2]
                            break
            if phone:
                info += {
                    "fa": f"\n📱 شماره ثبت‌شده: {phone}",
                    "en": f"\n📱 Registered number: {phone}",
                    "zh": f"\n📱 已注册号码: {phone}",
                    "ru": f"\n📱 Зарегистрированный номер: {phone}"
                }.get(context.user_data.get("lang", "fa"))
            await msg.reply_text(info)
        else:
            await msg.reply_text({
                "fa": "از دکمه‌های پنل مدیریت استفاده کن.",
                "en": "Use the buttons in the admin panel.",
                "zh": "请使用管理面板中的按钮。",
                "ru": "Используйте кнопки в панели администратора."
            }.get(context.user_data.get("lang", "fa")))
    else:
        if text == "🆘 پشتیبانی" or text == "🆘 Support" or text == "🆘 支持" or text == "🆘 Поддержка":
            awaiting_support[user.id] = True
            await msg.reply_text({
                "fa": "📝 پیام خود را برای پشتیبانی ارسال کنید:",
                "en": "📝 Send your message to support:",
                "zh": "📝 向支持团队发送您的消息：",
                "ru": "📝 Отправьте ваше сообщение в поддержку:"
            }.get(context.user_data.get("lang", "fa")))
        elif text == "📋 اطلاعات من" or text == "📋 My Info" or text == "📋 我的信息" or text == "📋 Моя информация":
            info = {
                "fa": f"🆔 آیدی عددی شما: {user.id}\n👤 نام شما: {user.full_name}",
                "en": f"🆔 Your numeric ID: {user.id}\n👤 Your name: {user.full_name}",
                "zh": f"🆔 您的数字ID: {user.id}\n👤 您的名字: {user.full_name}",
                "ru": f"🆔 Ваш числовой ID: {user.id}\n👤 Ваше имя: {user.full_name}"
            }.get(context.user_data.get("lang", "fa"))
            phone = None
            if os.path.exists("phones.txt"):
                with open("phones.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(" - ")
                        if len(parts) >= 3 and parts[0] == str(user.id):
                            phone = parts[2]
                            break
            if phone:
                info += {
                    "fa": f"\n📱 شماره ثبت‌شده: {phone}",
                    "en": f"\n📱 Registered number: {phone}",
                    "zh": f"\n📱 已注册号码: {phone}",
                    "ru": f"\n📱 Зарегистрированный номер: {phone}"
                }.get(context.user_data.get("lang", "fa"))
            await msg.reply_text(info)
        elif awaiting_support.get(user.id):
            awaiting_support.pop(user.id)
            await msg.reply_text({
                "fa": "✅ پیام شما ارسال شد. منتظر پاسخ باشید.",
                "en": "✅ Your message was sent. Please wait for a response.",
                "zh": "✅ 您的消息已发送，请等待回复。",
                "ru": "✅ Ваше сообщение отправлено. Ожидайте ответа."
            }.get(context.user_data.get("lang", "fa")))
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton({
                    "fa": "📩 پاسخ",
                    "en": "📩 Reply",
                    "zh": "📩 回复",
                    "ru": "📩 Ответить"
                }.get(context.user_data.get("lang", "fa")), callback_data=f"reply_{user.id}")]
            ])
            try:
                await context.bot.copy_message(chat_id=ADMIN_ID, from_chat_id=msg.chat_id, message_id=msg.message_id)
                await context.bot.send_message(chat_id=ADMIN_ID,
                    text={
                        "fa": f"👤 از: {user.full_name} ({user.id})",
                        "en": f"👤 From: {user.full_name} ({user.id})",
                        "zh": f"👤 来自: {user.full_name} ({user.id})",
                        "ru": f"👤 От: {user.full_name} ({user.id})"
                    }.get(context.user_data.get("lang", "fa")),
                    reply_markup=keyboard)
            except Exception as e:
                logger.error(f"{'ارسال پیام پشتیبانی به ادمین ناموفق بود' if context.user_data.get('lang', 'fa') == 'fa' else 'Sending support message to admin failed' if context.user_data.get('lang', 'fa') == 'en' else '发送支持消息给管理员失败' if context.user_data.get('lang', 'fa') == 'zh' else 'Отправка сообщения поддержки администратору не удалась'}: {e}")
        else:
            await msg.reply_text({
                "fa": "از دکمه‌ها استفاده کن 🙂",
                "en": "Use the buttons 🙂",
                "zh": "请使用按钮 🙂",
                "ru": "Используйте кнопки 🙂"
            }.get(context.user_data.get("lang", "fa")))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("reply_"):
        user_id = int(query.data.split("_")[1])
        reply_targets[ADMIN_ID] = user_id
        await query.message.reply_text({
            "fa": "✉️ پیام خود را برای کاربر بفرستید:",
            "en": "✉️ Send your message to the user:",
            "zh": "✉️ 向用户发送您的消息：",
            "ru": "✉️ Отправьте ваше сообщение пользователю:"
        }.get(context.user_data.get("lang", "fa")))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print({
        "fa": "ربات اجرا شد...",
        "en": "Bot started...",
        "zh": "机器人已启动...",
        "ru": "Бот запущен..."
    }.get("fa"))
    app.run_polling()
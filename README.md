# Telegram Bot Documentation

## Persian (فارسی)

### معرفی پروژه
این پروژه یک ربات تلگرام پیشرفته است که با استفاده از کتابخانه python-telegram-bot توسعه یافته است. این ربات قابلیت‌های متعددی از جمله مدیریت کاربران، ارسال پیام‌های همگانی، بلاک و آنبلاک کاربران، ذخیره شماره‌های تماس و پشتیبانی از کاربران را فراهم می‌کند. ربات برای ادمین و کاربران عادی رابط‌های کاربری متفاوتی ارائه می‌دهد و از چندزبانگی (فارسی، انگلیسی، چینی و روسی) پشتیبانی می‌کند.

### ویژگی‌ها
- **مدیریت کاربران**: ذخیره اطلاعات کاربران (نام و آیدی) و شماره‌های تماس آن‌ها.
- **پنل ادمین**: امکان مشاهده آمار، لیست کاربران، ارسال پیام همگانی، ارسال پیام به کاربر خاص، بلاک و آنبلاک کاربران.
- **پشتیبانی چندزبانه**: رابط کاربری به زبان‌های فارسی، انگلیسی، چینی و روسی.
- **ذخیره‌سازی داده‌ها**: استفاده از فایل‌های متنی برای ذخیره اطلاعات کاربران و شماره‌های تماس.
- **سیستم پشتیبانی**: امکان ارسال پیام به ادمین برای پشتیبانی و پاسخ‌دهی توسط ادمین.
- **امنیت**: قابلیت بلاک کردن کاربران برای جلوگیری از دسترسی غیرمجاز.

### پیش‌نیازها
- Python 3.8 یا بالاتر
- کتابخانه python-telegram-bot (نسخه 20.0 یا بالاتر)
- یک توکن معتبر تلگرام از BotFather

### نصب و راه‌اندازی
1. نصب کتابخانه مورد نیاز:
   ```
   pip install python-telegram-bot
   ```
2. جایگزینی توکن ربات:
   - در فایل `bot.py`، مقدار `BOT_TOKEN` را با توکن دریافت‌شده از BotFather جایگزین کنید.
3. تنظیم آیدی ادمین:
   - در فایل `bot.py`، مقدار `ADMIN_ID` را با آیدی عددی ادمین تنظیم کنید.
4. اجرای ربات:
   ```
   python bot.py
   ```

### ساختار فایل‌ها
- `bot.py`: فایل اصلی ربات که شامل منطق اصلی و عملکردهای آن است.
- `users.txt`: ذخیره اطلاعات کاربران (آیدی و نام).
- `phones.txt`: ذخیره شماره‌های تماس کاربران.
- `blocked.txt`: ذخیره آیدی کاربران بلاک‌شده.
- `stats.txt`: ذخیره تعداد کاربران ثبت‌شده.

### توسعه‌دهنده
توسعه‌یافته توسط حمید یارعلی  
- گیت‌هاب: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)  
- اینستاگرام: [hamidyaraliofficial](https://www.instagram.com/hamidyaraliofficial?igsh=MWpxZjhhMHZuNnlpYQ==)  
- تلگرام: [@Hamid_Yarali](https://t.me/Hamid_Yarali)

---

## English

### Project Overview
This project is an advanced Telegram bot developed using the python-telegram-bot library. It offers a range of features, including user management, broadcasting messages, blocking/unblocking users, storing contact numbers, and providing user support. The bot provides distinct interfaces for admins and regular users and supports multilingual functionality (Persian, English, Chinese, and Russian).

### Features
- **User Management**: Stores user information (ID and name) and their contact numbers.
- **Admin Panel**: Allows viewing statistics, user lists, broadcasting messages, sending messages to specific users, and blocking/unblocking users.
- **Multilingual Support**: User interface available in Persian, English, Chinese, and Russian.
- **Data Storage**: Uses text files to store user data and contact numbers.
- **Support System**: Enables users to send messages to the admin for support and receive responses.
- **Security**: Ability to block users to prevent unauthorized access.

### Requirements
- Python 3.8 or higher
- python-telegram-bot library (version 20.0 or higher)
- A valid Telegram bot token from BotFather

### Installation and Setup
1. Install the required library:
   ```
   pip install python-telegram-bot
   ```
2. Replace the bot token:
   - In the `bot.py` file, replace the `BOT_TOKEN` value with the token obtained from BotFather.
3. Set the admin ID:
   - In the `bot.py` file, set the `ADMIN_ID` to the admin’s numeric ID.
4. Run the bot:
   ```
   python bot.py
   ```

### File Structure
- `bot.py`: The main bot file containing its logic and functionalities.
- `users.txt`: Stores user information (ID and name).
- `phones.txt`: Stores users’ contact numbers.
- `blocked.txt`: Stores IDs of blocked users.
- `stats.txt`: Stores the count of registered users.

### Developer
Developed by Hamid Yarali  
- GitHub: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)  
- Instagram: [hamidyaraliofficial](https://www.instagram.com/hamidyaraliofficial?igsh=MWpxZjhhMHZuNnlpYQ==)  
- Telegram: [@Hamid_Yarali](https://t.me/Hamid_Yarali)

---

## Chinese (中文)

### 项目简介
该项目是一个使用 python-telegram-bot 库开发的先进 Telegram 机器人。它提供了多种功能，包括用户管理、广播消息、屏蔽/解除屏蔽用户、存储联系电话以及用户支持。机器人为管理员和普通用户提供不同的界面，并支持多语言功能（波斯语、英语、中文和俄语）。

### 功能
- **用户管理**：存储用户信息（ID 和姓名）及其联系电话。
- **管理员面板**：允许查看统计数据、用户列表、广播消息、向特定用户发送消息以及屏蔽/解除屏蔽用户。
- **多语言支持**：用户界面支持波斯语、英语、中文和俄语。
- **数据存储**：使用文本文件存储用户数据和联系电话。
- **支持系统**：允许用户向管理员发送支持消息并接收回复。
- **安全性**：能够屏蔽用户以防止未经授权的访问。

### 要求
- Python 3.8 或更高版本
- python-telegram-bot 库（版本 20.0 或更高）
- 从 BotFather 获取的有效 Telegram 机器人令牌

### 安装和设置
1. 安装所需库：
   ```
   pip install python-telegram-bot
   ```
2. 替换机器人令牌：
   - 在 `bot.py` 文件中，将 `BOT_TOKEN` 值替换为从 BotFather 获取的令牌。
3. 设置管理员 ID：
   - 在 `bot.py` 文件中，将 `ADMIN_ID` 设置为管理员的数字 ID。
4. 运行机器人：
   ```
   python bot.py
   ```

### 文件结构
- `bot.py`：机器人主文件，包含其逻辑和功能。
- `users.txt`：存储用户信息（ID 和姓名）。
- `phones.txt`：存储用户联系电话。
- `blocked.txt`：存储被屏蔽用户的 ID。
- `stats.txt`：存储注册用户的数量。

### 开发者
由 Hamid Yarali 开发  
- GitHub: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)  
- Instagram: [hamidyaraliofficial](https://www.instagram.com/hamidyaraliofficial?igsh=MWpxZjhhMHZuNnlpYQ==)  
- Telegram: [@Hamid_Yarali](https://t.me/Hamid_Yarali)
import pyttsx3
import subprocess
import os
import psutil
import time
from datetime import datetime
import webbrowser

class TextVoiceAssistant:
    def __init__(self):
        # Инициализация синтеза речи
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        print("Голосовой помощник с текстовым вводом запущен!")
        self.speak("Привет! Я ваш голосовой помощник. Вводите команды текстом, а я буду отвечать голосом!")
        
        self.running = True

    def setup_tts(self):
        """Настройка синтеза речи для русского языка"""
        voices = self.tts_engine.getProperty('voices')
        
        # Поиск русского голоса
        russian_voice = None
        for voice in voices:
            if voice and hasattr(voice, 'name') and hasattr(voice, 'id'):
                if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                    russian_voice = voice.id
                    break
        
        if russian_voice:
            self.tts_engine.setProperty('voice', russian_voice)
        
        # Настройка скорости и громкости
        self.tts_engine.setProperty('rate', 150)  # Скорость речи
        self.tts_engine.setProperty('volume', 0.9)  # Громкость

    def speak(self, text):
        """Произнести текст"""
        print(f"Помощник: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Ошибка синтеза речи: {e}")

    def get_input(self):
        """Получить команду от пользователя"""
        try:
            command = input("\nВведите команду: ").lower().strip()
            return command
        except KeyboardInterrupt:
            return "выход"

    def open_application(self, app_name):
        """Открыть приложение по имени"""
        app_paths = {
            'блокнот': 'notepad.exe',
            'калькулятор': 'calc.exe',
            'браузер': 'msedge.exe',
            'проводник': 'explorer.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'paint': 'mspaint.exe',
            'командная строка': 'cmd.exe',
            'диспетчер задач': 'taskmgr.exe',
            'настройки': 'ms-settings:',
            'панель управления': 'control.exe'
        }
        
        app_name = app_name.lower()
        
        # Поиск приложения в словаре
        for key, path in app_paths.items():
            if key in app_name:
                try:
                    if path.startswith('ms-settings:'):
                        subprocess.run(['start', path], shell=True)
                    else:
                        subprocess.Popen(path)
                    self.speak(f"Открываю {key}")
                    return True
                except FileNotFoundError:
                    self.speak(f"Не удалось найти {key}")
                    return False
        
        # Попытка открыть по прямому имени
        try:
            subprocess.Popen(app_name)
            self.speak(f"Открываю {app_name}")
            return True
        except:
            self.speak(f"Не удалось открыть {app_name}")
            return False

    def open_website(self, site_name):
        """Открыть веб-сайт"""
        sites = {
            'гугл': 'https://google.com',
            'яндекс': 'https://yandex.ru',
            'ютуб': 'https://youtube.com',
            'вк': 'https://vk.com',
            'почта': 'https://mail.ru',
            'github': 'https://github.com',
            'википедия': 'https://ru.wikipedia.org'
        }
        
        for key, url in sites.items():
            if key in site_name:
                webbrowser.open(url)
                self.speak(f"Открываю {key}")
                return True
        
        return False

    def get_system_info(self):
        """Получить информацию о системе"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:')
            
            info = f"Загрузка процессора: {cpu_percent} процентов. "
            info += f"Использование памяти: {memory.percent} процентов. "
            info += f"Свободно на диске C: {disk.free // (1024**3)} гигабайт."
            
            return info
        except Exception as e:
            return "Не удалось получить информацию о системе"

    def process_command(self, command):
        """Обработать команду пользователя"""
        if not command:
            return
        
        # Команды для открытия приложений
        if any(word in command for word in ['открой', 'запусти', 'включи']):
            app_name = command
            for word in ['открой', 'запусти', 'включи']:
                app_name = app_name.replace(word, '').strip()
            
            # Проверяем, не сайт ли это
            if any(site in app_name for site in ['гугл', 'яндекс', 'ютуб', 'вк', 'почта', 'github', 'википедия']):
                self.open_website(app_name)
            else:
                self.open_application(app_name)
        
        # Команды времени
        elif any(word in command for word in ['время', 'час', 'сколько времени']):
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"Сейчас {current_time}")
        
        # Команды даты
        elif any(word in command for word in ['дата', 'число', 'какое сегодня']):
            current_date = datetime.now().strftime("%d %B %Y года")
            months = {
                'January': 'января', 'February': 'февраля', 'March': 'марта',
                'April': 'апреля', 'May': 'мая', 'June': 'июня',
                'July': 'июля', 'August': 'августа', 'September': 'сентября',
                'October': 'октября', 'November': 'ноября', 'December': 'декабря'
            }
            for eng, rus in months.items():
                current_date = current_date.replace(eng, rus)
            self.speak(f"Сегодня {current_date}")
        
        # Информация о системе
        elif any(word in command for word in ['система', 'компьютер', 'производительность']):
            info = self.get_system_info()
            self.speak(info)
        
        # Команды выключения компьютера
        elif any(word in command for word in ['выключи компьютер', 'завершение работы']):
            self.speak("Выключаю компьютер через 30 секунд. Введите 'отмена' чтобы отменить.")
            # subprocess.run(['shutdown', '/s', '/t', '30'])
        
        # Команда остановки помощника
        elif any(word in command for word in ['стоп', 'выход', 'завершить', 'пока']):
            self.speak("До свидания!")
            self.running = False
        
        # Приветствие
        elif any(word in command for word in ['привет', 'здравствуй', 'добро пожаловать']):
            self.speak("Привет! Как дела? Чем могу помочь?")
        
        # Помощь
        elif any(word in command for word in ['помощь', 'что ты умеешь', 'команды']):
            help_text = """Я умею:
- Открывать приложения: 'открой блокнот', 'запусти калькулятор'
- Открывать сайты: 'открой гугл', 'запусти ютуб'
- Сообщать время: 'сколько времени?'
- Сообщать дату: 'какое сегодня число?'
- Показывать информацию о системе: 'информация о системе'
- Для выхода: 'стоп' или 'выход'"""
            print(help_text)
            self.speak("Список команд выведен на экран")
        
        else:
            self.speak("Извините, я не понял команду. Введите 'помощь' для списка доступных команд.")

    def run(self):
        """Основной цикл работы помощника"""
        while self.running:
            command = self.get_input()
            if command:
                self.process_command(command)

def main():
    try:
        assistant = TextVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()

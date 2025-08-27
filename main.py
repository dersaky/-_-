import speech_recognition as sr
import pyttsx3
import subprocess
import os
import psutil
import threading
import time
from datetime import datetime

class RussianVoiceAssistant:
    def __init__(self):
        # Инициализация распознавания речи
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Инициализация синтеза речи
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Настройка микрофона
        self.setup_microphone()
        
        # Флаг для остановки помощника
        self.running = True
        
        print("Голосовой помощник инициализирован!")
        self.speak("Привет! Я ваш голосовой помощник. Чем могу помочь?")

    def setup_tts(self):
        """Настройка синтеза речи для русского языка"""
        voices = self.tts_engine.getProperty('voices')
        
        # Поиск русского голоса
        russian_voice = None
        for voice in voices:
            if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                russian_voice = voice.id
                break
        
        if russian_voice:
            self.tts_engine.setProperty('voice', russian_voice)
        
        # Настройка скорости и громкости
        self.tts_engine.setProperty('rate', 150)  # Скорость речи
        self.tts_engine.setProperty('volume', 0.9)  # Громкость

    def setup_microphone(self):
        """Настройка микрофона для лучшего распознавания"""
        with self.microphone as source:
            print("Калибровка микрофона...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Микрофон настроен!")

    def speak(self, text):
        """Произнести текст"""
        print(f"Помощник: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Слушать команду пользователя"""
        try:
            with self.microphone as source:
                print("Слушаю...")
                # Увеличиваем timeout для русской речи
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Распознаю речь...")
            # Используем Google Speech Recognition с русским языком
            command = self.recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Извините, я не расслышал. Повторите, пожалуйста.")
            return None
        except sr.RequestError as e:
            self.speak("Ошибка сервиса распознавания речи")
            print(f"Ошибка: {e}")
            return None

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
            'диспетчер задач': 'taskmgr.exe'
        }
        
        app_name = app_name.lower()
        
        # Поиск приложения в словаре
        for key, path in app_paths.items():
            if key in app_name:
                try:
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

    def get_system_info(self):
        """Получить информацию о системе"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"Загрузка процессора: {cpu_percent}%. "
        info += f"Использование памяти: {memory.percent}%. "
        info += f"Свободно на диске: {disk.free // (1024**3)} гигабайт."
        
        return info

    def process_command(self, command):
        """Обработать голосовую команду"""
        if not command:
            return
        
        # Команды для открытия приложений
        if any(word in command for word in ['открой', 'запусти', 'включи']):
            app_name = command
            for word in ['открой', 'запусти', 'включи']:
                app_name = app_name.replace(word, '').strip()
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
        
        # Команды выключения
        elif any(word in command for word in ['выключи компьютер', 'завершение работы']):
            self.speak("Выключаю компьютер через 30 секунд. Скажите 'отмена', чтобы отменить.")
            # Здесь можно добавить логику выключения
        
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
            - Открывать приложения: скажите 'открой блокнот' или 'запусти калькулятор'
            - Сообщать время: спросите 'сколько времени?'
            - Сообщать дату: спросите 'какое сегодня число?'
            - Показывать информацию о системе: скажите 'информация о системе'
            - Для выхода скажите 'стоп' или 'выход'"""
            self.speak(help_text)
        
        else:
            self.speak("Извините, я не понял команду. Скажите 'помощь' для списка доступных команд.")

    def run(self):
        """Основной цикл работы помощника"""
        while self.running:
            command = self.listen()
            if command:
                self.process_command(command)
            time.sleep(0.1)

def main():
    try:
        assistant = RussianVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
import subprocess
import os
import time
from datetime import datetime
import webbrowser

class SimpleVoiceAssistant:
    def __init__(self):
        print("Простой голосовой помощник запущен!")
        print("Введите команды текстом (пока без голоса)")
        self.running = True
        self.speak("Привет! Я ваш помощник. Введите 'помощь' для списка команд.")

    def speak(self, text):
        """Вывод текста и озвучивание через Windows SAPI"""
        print(f"Помощник: {text}")
        try:
            # Используем встроенную команду Windows для озвучивания
            subprocess.run([
                'powershell', '-Command', 
                f'Add-Type -AssemblyName System.Speech; '
                f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$speak.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::NotSet, [System.Speech.Synthesis.VoiceAge]::NotSet, 0, [System.Globalization.CultureInfo]"ru-RU"); '
                f'$speak.Speak("{text}")'
            ], capture_output=True, text=True, timeout=10)
        except:
            # Если не получается озвучить, просто выводим текст
            pass

    def get_input(self):
        """Получить команду от пользователя"""
        try:
            command = input("Введите команду: ").lower().strip()
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
        
        self.speak(f"Не знаю как открыть {app_name}")
        return False

    def open_website(self, site_name):
        """Открыть веб-сайт"""
        sites = {
            'гугл': 'https://google.com',
            'яндекс': 'https://yandex.ru',
            'ютуб': 'https://youtube.com',
            'вк': 'https://vk.com',
            'почта': 'https://mail.ru',
            'github': 'https://github.com'
        }
        
        for key, url in sites.items():
            if key in site_name:
                webbrowser.open(url)
                self.speak(f"Открываю {key}")
                return True
        
        return False

    def get_system_info(self):
        """Получить базовую информацию о системе"""
        try:
            # Получаем информацию о системе через wmic
            result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage', '/value'], 
                                  capture_output=True, text=True)
            cpu_info = "Информация о системе получена"
            
            # Получаем информацию о памяти
            mem_result = subprocess.run(['wmic', 'OS', 'get', 'TotalVisibleMemorySize,FreePhysicalMemory', '/value'], 
                                      capture_output=True, text=True)
            
            return "Система работает нормально"
        except:
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
            if any(site in app_name for site in ['гугл', 'яндекс', 'ютуб', 'вк', 'почта', 'github']):
                self.open_website(app_name)
            else:
                self.open_application(app_name)
        
        # Команды времени
        elif any(word in command for word in ['время', 'час', 'сколько времени']):
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"Сейчас {current_time}")
        
        # Команды даты
        elif any(word in command for word in ['дата', 'число', 'какое сегодня']):
            current_date = datetime.now().strftime("%d.%m.%Y")
            self.speak(f"Сегодня {current_date}")
        
        # Информация о системе
        elif any(word in command for word in ['система', 'компьютер', 'производительность']):
            info = self.get_system_info()
            self.speak(info)
        
        # Команда остановки помощника
        elif any(word in command for word in ['стоп', 'выход', 'завершить', 'пока']):
            self.speak("До свидания!")
            self.running = False
        
        # Приветствие
        elif any(word in command for word in ['привет', 'здравствуй']):
            self.speak("Привет! Как дела? Чем могу помочь?")
        
        # Помощь
        elif any(word in command for word in ['помощь', 'что ты умеешь', 'команды']):
            help_text = """Доступные команды:
- 'открой блокнот/калькулятор/браузер/проводник'
- 'запусти word/excel/paint'
- 'открой гугл/яндекс/ютуб'
- 'сколько времени?'
- 'какое сегодня число?'
- 'информация о системе'
- 'выход' - завершить работу"""
            print(help_text)
            self.speak("Список команд выведен на экран")
        
        else:
            self.speak("Не понял команду. Введите 'помощь' для списка команд.")

    def run(self):
        """Основной цикл работы помощника"""
        while self.running:
            command = self.get_input()
            if command:
                self.process_command(command)

def main():
    try:
        assistant = SimpleVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена")

if __name__ == "__main__":
    main()

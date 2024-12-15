import threading
import time

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Window, BufferControl, HSplit, Layout
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea

from app.analytics import Analytics
from app.queue import Queue
from app.worker import worker


def start(initial_number):
    command_buffer, layout, log_area, style, data_display = make_ui()
    default_priority = 99
    logs = []
    logger = get_logger(logs, log_area)
    analitics = Analytics(logger)
    queue = Queue(analitics)

    # Функция обновления данных на экране
    def update_data_display():
        data_str = "Current data:\n" + "\n".join(map(str, calculate_analysis(analitics)))
        data_display.text = data_str

    # Изначально обновим
    update_data_display()

    stop_refresh_event = threading.Event()

    # Функция, которая будет выполняться в потоке и раз в секунду обновлять экран
    def refresh_loop():
        while not stop_refresh_event.is_set():
            # Каждую секунду обновляем отображение
            # invalidate() заставляет приложение перерисовать экран
            update_data_display()
            app.invalidate()
            time.sleep(1)

    # KeyBindings не обязательны, но можно добавить, чтобы Ctrl+D - выход
    kb = KeyBindings()

    @kb.add("c-d")
    def exit_(event):
        event.app.exit()

    # Обработчик ввода команд
    def accept(buff):
        command = buff.text.strip()
        buff.text = ""  # очищаем поле ввода после команды
        if command.startswith("add "):
            parts = command.split(" ")
            if len(parts) == 3:
                try:
                    num = int(parts[1])
                    if num > 200:
                        logger("отказ, время слишком велико, максимум 200сек")
                        return
                    if num < 1:
                        logger("отказ, время слишком мало, минимум 1 сек")
                        return
                    priority = int(parts[2])
                    if priority > 200:
                        logger("отказ, значение приоритета слишком велико максимум 200")
                        return
                    if priority < 0:
                        logger("отказ, значение приоритета слишком мало минимум 0")
                        return
                    queue.push(priority, num)
                    update_data_display()
                except ValueError:
                    pass
            elif len(parts) == 2:
                try:
                    num = int(parts[1])
                    if num > 200:
                        logger("отказ, время слишком велико, максимум 200сек")
                        return
                    if num < 1:
                        logger("отказ, время слишком мало, минимум 1 сек")
                        return
                    queue.push(default_priority, num)
                    update_data_display()
                except ValueError:
                    pass
        elif command == "exit":
            app.exit()

    command_buffer.accept_handler = accept
    app = Application(
        layout=layout,
        full_screen=True,
        key_bindings=kb,
        style=style
    )
    # Запускаем поток для периодической перерисовки
    t = threading.Thread(target=refresh_loop, daemon=True)
    t.start()
    threads = []
    stop_events = []
    for workerId in range(0, initial_number):
        stop_event = threading.Event()
        tw = threading.Thread(target=worker, args=(workerId, queue, analitics, stop_event))
        tw.start()
        threads.append(tw)
        stop_events.append(stop_event)

    app.run()
    # graceful shutdown
    queue.set_shutdown()
    for stop_event in stop_events:
        stop_event.set()

    for thread in threads:
        thread.join()

    stop_refresh_event.set()
    t.join()


def make_ui():
    # Создаем текстовое поле для отображения данных
    data_display = TextArea(
        text="",
        read_only=True,
        style="class:data-area"
    )
    # Создаем буфер для ввода команд
    command_buffer = Buffer(multiline=False)
    # Нижняя строка ввода
    command_line = Window(
        height=1,
        content=BufferControl(buffer=command_buffer, lexer=SimpleLexer("class:input")),
        style="class:input-line"
    )
    # Верхняя часть: окно с данными
    top_window = Window(content=data_display.control, style="class:data-window")
    log_area = TextArea(
        text='',
        read_only=True,
        wrap_lines=False,
        height=8,  # показываем только 4 строки
        style='class:log-area'
    )
    # Собираем layout
    root_container = HSplit([
        top_window,
        log_area,
        command_line
    ])
    layout = Layout(root_container, focused_element=command_line)
    # Стили (необязательно, просто пример)
    style = Style.from_dict({
        "data-area": "bg:#202020 #ffffff",
        "data-window": "bg:#303030",
        "input": "#00ff00",
        "input-line": "bg:#000000 #00ff00"
    })
    return command_buffer, layout, log_area, style, data_display


def calculate_analysis(analytics: Analytics):
    data, queue_size = analytics.get_data()

    result = []
    for worker_id in sorted(data.keys()):
        info = data[worker_id]
        if not info["done"]:
            elapsed = info["number"] - (time.time() - info["timestamp"])
            s = f"сервер {worker_id}: выполняет задание (осталось {elapsed:.2f} сек.)"
            result.append(s)
        else:
            s1 = f"сервер {worker_id}: пусто"
            result.append(s1)
    result.append(f"в очереди {queue_size} элементов\n")
    return result


def get_logger(logs, log_area):
    return lambda line: add_log_line(logs, log_area, line)


def add_log_line(logs, log_area, line: str):
    logs.append(line)
    # Сохраняем не более 4 последних строк
    if len(logs) > 8:
        logs.pop(0)
    # Обновляем содержимое log_area
    log_area.text = "\n".join(logs)

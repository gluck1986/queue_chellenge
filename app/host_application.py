import threading
import time

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Window, BufferControl, HSplit, Layout
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea


def start(initial_number):
    data = [initial_number]
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
    # Собираем layout
    root_container = HSplit([
        top_window,
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

    # Функция обновления данных на экране
    def update_data_display():
        data_str = "Current data:\n" + "\n".join(map(str, data))
        data_display.text = data_str

    # Изначально обновим
    update_data_display()

    # Функция, которая будет выполняться в потоке и раз в секунду обновлять экран
    def refresh_loop():
        while True:
            # Каждую секунду обновляем отображение
            # invalidate() заставляет приложение перерисовать экран
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
            # извлекаем число
            try:
                num = int(command.split(" ", 1)[1])
                data.append(num)
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
    app.run()

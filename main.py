import flet as ft
import datetime as dt
from db import main_db

def main(page: ft.Page):
    page.title = "todo list"
    page.theme_mode = ft.ThemeMode.DARK

    task_list = ft.Column(spacing=10)
    filter_type = "completed"
    
    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, time, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text,completed=completed , time=time))
        page.update()

    load_tasks()

    def create_task_row(task_id , task_text, completed, time):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)
        task_time = ft.TextField(value=time, read_only=True, width=185)
        chekbox = ft.Checkbox(value=bool(completed), on_change=lambda e: togle_task(task_id=task_id, is_completed=completed))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        def delete_task(_):
            main_db.delete_task(id=task_id) 

            load_tasks()
        def save_task(_):
            new_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_time.value = new_time
            main_db.update_task(id=task_id, task=task_field.value, completed=int(), time=task_time.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED , on_click=delete_task)

        return ft.Row([chekbox, task_field, task_time, edit_button, save_button, delete_button])

    def togle_task(task_id, is_completed):
        main_db.update_task(id=task_id, completed=int(is_completed))


    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_id = main_db.add_task(task=task, time=task_time)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task,completed=None, time=task_time))
            print(task_id)
            task_input.value = None
            page.update()

    def set_filter(filter_value: str):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()
    
    filter_buttons = ft.Row([
        ft.ElevatedButton("все задачи", icon=ft.Icons.ALL_INBOX, on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("невыполненные", icon=ft.Icons.STOP_OUTLINED, on_click=lambda e: set_filter("uncompleted"), color=ft.Colors.PURPLE),
        ft.ElevatedButton("выполеннные", icon=ft.Icons.CHECK_BOX, on_click=lambda e: set_filter("completed"), color=ft.Colors.BLUE)
    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    task_input = ft.TextField(label="Введите задачу", expand=True, on_submit=add_task)
    task_button = ft.IconButton(icon=ft.Icons.SEND, on_click=add_task)

    page.add(ft.Row([task_input, task_button]), filter_buttons, task_list)

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
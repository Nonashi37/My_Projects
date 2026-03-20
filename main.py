import flet as ft 
from db import main_db
import os
import datetime

def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.DARK

    # edit theme
    def edit_theme(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.Icons.DARK_MODE 
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.Icons.LIGHT_MODE
        page.update()

    # button to change the theme
    theme_icon = ft.IconButton(icon=ft.Icons.LIGHT_MODE, on_click=edit_theme)

    # in appbar addint the icon
    page.appbar = ft.AppBar(
        title=ft.Text("My Tasks"),
        actions=[theme_icon]
    )
    

    

    task_list = ft.Column(spacing=22)
    filter_type = 'all'

    def load_task():
        task_list.controls.clear()
        for task_id, task, completed in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task, completed=completed))
        page.update()

    def view_tasks(task_id, task_text, completed=None):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        checkbox_task = ft.Checkbox(
            value=bool(completed), 
            on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value)
        )

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        # Функция Удаления
        def delete_task_click(_):
            # Удаляем из Базы
            main_db.delete_task(task_id=task_id)
            # Перезагрущим список
            load_task()

        delete_botton = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED,
            on_click=delete_task_click
        )
        # Добовляем кнопку в концу строки
        return ft.Row([checkbox_task, task_field, edit_button, save_button, delete_botton])
    
    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        page.update()

    # Время записи задачи
    def add_task_db(_):
        if task_input.value:
            now = datetime.datetime.now()
            time_string = now.strftime("%Y:%m:%d - %H:%M:%S")
            task = task_input.value + " (Created: " + time_string + ")"
            
            task_id = main_db.add_task(task=task)
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task))
            task_input.value = None
            page.update()

    

    task_input = ft.TextField(label='Write a Task', expand=True, on_submit=add_task_db)
    send_button = ft.ElevatedButton('SEND', on_click=add_task_db)
    main_objects = ft.Row([task_input, send_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_task()

    filter_buttons = ft.Row([
        ft.ElevatedButton("All to do's", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('In Progress', on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton("Done ✅", on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(main_objects, filter_buttons, task_list)
    load_task()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)

import flet as ft
from db import main_db
from datetime import datetime  # ✅ cleaner import, removed unused `os`

def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.DARK

    def edit_theme(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.Icons.LIGHT_MODE
        page.update()

    theme_icon = ft.IconButton(icon=ft.Icons.LIGHT_MODE, on_click=edit_theme)
    page.appbar = ft.AppBar(title=ft.Text("My Tasks"), actions=[theme_icon])

    task_list = ft.Column(spacing=22)
    filter_state = {'type': 'all'}  # ✅ dict instead of nonlocal — cleaner pattern

    def load_tasks():
        task_list.controls.clear()
        for task_id, task, completed in main_db.get_tasks(filter_state['type']):
            task_list.controls.append(build_task_row(task_id, task, completed))
        page.update()

    def build_task_row(task_id, task_text, completed=0):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: (
                main_db.update_task(task_id, completed=e.control.value),
                page.update()
            )
        )

        def toggle_edit(_):
            task_field.read_only = not task_field.read_only
            page.update()

        def save(_):
            main_db.update_task(task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()

        def delete(_):
            main_db.delete_task(task_id)
            load_tasks()

        return ft.Row([
            checkbox,
            task_field,
            ft.IconButton(ft.Icons.EDIT, on_click=toggle_edit),
            ft.IconButton(ft.Icons.SAVE, on_click=save),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=delete),
        ])

    def add_task(_):
        if not task_input.value:
            return
        # ✅ Cleaner timestamp formatting
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_text = f"{task_input.value} (Created: {timestamp})"
        task_id = main_db.add_task(task_text)
        task_list.controls.append(build_task_row(task_id, task_text))
        task_input.value = ""
        page.update()

    task_input = ft.TextField(label='Write a Task', expand=True, on_submit=add_task)

    def set_filter(value):
        filter_state['type'] = value
        load_tasks()

    page.add(
        ft.Row([task_input, ft.Button('SEND', on_click=add_task)]),  # ✅ ft.Button fixes deprecation
        ft.Row([
            ft.OutlinedButton("All", on_click=lambda e: set_filter('all')),
            ft.OutlinedButton("In Progress", on_click=lambda e: set_filter('uncompleted')),
            ft.OutlinedButton("Done ✅", on_click=lambda e: set_filter('completed')),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        task_list,
    )
    load_tasks()

if __name__ == '__main__':
    main_db.init_db()
    ft.app(main)  # ✅ `target=` is deprecated


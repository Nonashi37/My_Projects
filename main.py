import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'Shoppy Buy'
    page.theme_mode = ft.ThemeMode.DARK

    # edit theme I just like editing themes
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

    # counter text for purchased items
    purchased_counter = ft.Text(value='', size=14)

    # in appbar adding the icon and counter
    page.appbar = ft.AppBar(
        title=ft.Text("Shopping List"),
        actions=[purchased_counter, theme_icon]
    )

    shopping_list = ft.Column(spacing=22)
    filter_type = 'all Goods '

    def update_counter():
        count = main_db.get_purchased_count()
        purchased_counter.value = f'Purchased: {count}'
        page.update()

    def load_items():
        shopping_list.controls.clear()
        for item_id, item, quantity, purchased in main_db.get_items(filter_type=filter_type):
            shopping_list.controls.append(
                view_item(item_id=item_id, item_text=item, quantity=quantity, purchased=purchased)
            )
        update_counter()
        page.update()

    def view_item(item_id, item_text, quantity, purchased=None):
        # show item name (read only) (read only in not execute them all)
        item_field = ft.TextField(value=item_text, read_only=True, expand=True)

        # show quantity (read only)
        quantity_field = ft.TextField(value=quantity, read_only=True, width=70)

        # checkbox to mark as purchased
        checkbox_item = ft.Checkbox(
            value=bool(purchased),
            on_change=lambda e: toggle_purchased(item_id=item_id, is_purchased=e.control.value)
        )

        # delete function
        def delete_item_click(_):
            # delete from base
            main_db.delete_item(item_id=item_id)
            # update the list
            load_items()

        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            icon_color=ft.Colors.RED,
            on_click=delete_item_click
        )

        # add all to the Row
        return ft.Row([checkbox_item, item_field, quantity_field, delete_button])

    def toggle_purchased(item_id, is_purchased):
        main_db.mark_purchased(item_id=item_id, is_purchased=is_purchased)
        update_counter()
        page.update()


    def add_item_db(_):
        if item_input.value:
            # if Qty is empty - default is 1
            qty = quantity_input.value if quantity_input.value else '1'

            item_id = main_db.add_item(item=item_input.value, quantity=qty)
            shopping_list.controls.append(
                view_item(item_id=item_id, item_text=item_input.value, quantity=qty)
            )
            item_input.value = None
            quantity_input.value = None
            update_counter()
            page.update()


    item_input = ft.TextField(label='Item name', expand=True, on_submit=add_item_db)
    quantity_input = ft.TextField(label='Qty', width=80)
    send_button = ft.ElevatedButton('ADD', on_click=add_item_db)
    main_objects = ft.Row([item_input, quantity_input, send_button])

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_items()

    filter_buttons = ft.Row([
        ft.ElevatedButton("All", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Unpurchased", on_click=lambda e: set_filter('unpurchased')),
        ft.ElevatedButton("Purchased ", on_click=lambda e: set_filter('purchased'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(main_objects, filter_buttons, shopping_list)
    load_items()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)  #  originale
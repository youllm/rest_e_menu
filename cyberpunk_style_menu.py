import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        self.add_widget(layout)

        conn = sqlite3.connect('menu.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        menu_items = cursor.fetchall()
        for item in menu_items:
            item_label = Label(text=f"{item[0]}: {item[1]}$", size_hint=(1, None), height=50)
            layout.add_widget(item_label)


class AddItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        self.add_widget(layout)

        name_label = Label(text="Name:")
        self.name_input = TextInput()
        price_label = Label(text="Price:")
        self.price_input = TextInput()
        add_button = Button(text="Add Item")
        add_button.bind(on_press=self.add_item)

        layout.add_widget(name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(price_label)
        layout.add_widget(self.price_input)
        layout.add_widget(add_button)

    def add_item(self, instance):
        conn = sqlite3.connect('menu.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO menu (name, price) VALUES ('{self.name_input.text}', '{self.price_input.text}')")
        conn.commit()
        conn.close()
        self.name_input.text = ""
        self.price_input.text = ""


class DeleteItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        self.add_widget(layout)

        conn = sqlite3.connect('menu.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        menu_items = cursor.fetchall()
        for item in menu_items:
            item_label = Label(text=f"{item[0]}: {item[1]}$", size_hint=(1, None), height=50)
            item_button = Button(text="Delete")
            item_button.bind(on_press=self.delete_item)
            item_layout = BoxLayout()
            item_layout.add_widget(item_label)
            item_layout.add_widget(item_button)
            layout.add_widget(item_layout)

    def delete_item(self, instance):
        conn = sqlite3.connect('menu.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM menu WHERE name='{instance.parent.children[0].text[:-2]}'")
        conn.commit()
        conn.close()
        self.manager.current = "menu"


class RestaurantMenuApp(App):
    def build(self):
        screen_manager = ScreenManager()

        menu_screen = MenuScreen(name="menu")
        add_item_screen = AddItemScreen(name="add_item")
        delete_item_screen = DeleteItemScreen(name="delete_item")

        screen_manager.add_widget(menu_screen)
        screen_manager.add_widget(add_item_screen)
        screen_manager.add_widget(delete_item_screen)

        layout = BoxLayout(orientation="vertical")

        menu_button = Button(text="Menu", on_press=lambda x: screen_manager.current("menu"))
        add_item_button = Button(text="Add Item", on_press=lambda x: screen_manager.current("add_item"))
        delete_item_button = Button(text="Delete Item", on_press=lambda x: screen_manager.current("delete_item"))

    layout.add_widget(menu_button)
    layout.add_widget(add_item_button)
    layout.add_widget(delete_item_button)

    root_widget = BoxLayout(orientation="vertical")
    root_widget.add_widget(screen_manager)
    root_widget.add_widget(layout)

    return root_widget
   if name == 'main':
   RestaurantMenuApp().run()
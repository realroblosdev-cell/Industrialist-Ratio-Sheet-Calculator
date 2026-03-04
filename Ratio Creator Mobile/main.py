import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.core.audio import SoundLoader

from core import RatioCore

KV = """
<RootUI>:
    orientation: "vertical"
    padding: 10
    spacing: 8

    TextInput:
        id: search
        hint_text: "Search item..."
        multiline: False
        on_text: root.filter_items(self.text)
        size_hint_y: None
        height: 50

    ScrollView:
        size_hint_y: 0.4
        GridLayout:
            id: item_list
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            row_default_height: 44
            row_force_default: True

    TextInput:
        id: rate
        hint_text: "Target rate (/s)"
        input_filter: "float"
        multiline: False
        size_hint_y: None
        height: 50

    Button:
        text: "CALCULATE"
        size_hint_y: None
        height: 60
        on_release: root.calculate()

    ScrollView:
        Label:
            text: root.output_text
            text_size: self.width - 20, None
            size_hint_y: None
            height: self.texture_size[1]
"""

class RootUI(BoxLayout):
    output_text = StringProperty("Ready.")
    all_items = ListProperty([])
    selected_item = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        base = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base, "Dictionary.json")

        self.core = RatioCore(json_path)
        self.all_items = self.core.get_all_items()

        self.populate_items(self.all_items)

        # optional sound
        sound_path = os.path.join(base, "Transition.mp3")
        self.sound = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

    # --------------------------
    # UI helpers
    # --------------------------
    def populate_items(self, items):
        grid = self.ids.item_list
        grid.clear_widgets()

        from kivy.uix.button import Button

        for name in items:
            btn = Button(text=name)
            btn.bind(on_release=self.select_item)
            grid.add_widget(btn)

    def filter_items(self, text):
        t = text.lower().strip()
        filtered = [i for i in self.all_items if t in i.lower()]
        self.populate_items(filtered)

    def select_item(self, btn):
        self.selected_item = btn.text
        self.output_text = f"Selected: {btn.text}"

        if self.sound:
            self.sound.play()

    # --------------------------
    # Calculation
    # --------------------------
    def calculate(self):
        if not self.selected_item:
            self.output_text = "Select an item first."
            return

        rate_text = self.ids.rate.text.strip()

        if not rate_text:
            self.output_text = "Enter a rate."
            return

        rate = float(rate_text)

        result = self.core.calculate(self.selected_item, rate)
        self.output_text = result


class RatioApp(App):
    def build(self):
        Builder.load_string(KV)
        return RootUI()


if __name__ == "__main__":
    RatioApp().run()
import os
import datetime as dt

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from PIL import Image as PILImage, ImageDraw, ImageFont

class WatermarkApp(App):
    def build(self):
        self.title = "Watermark GUI"
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Logo image
        self.logo = Image(source='images/logo.png', size_hint=(1, 0.3))
        layout.add_widget(self.logo)
        
        # Text input for watermark
        self.text_input = TextInput(hint_text="Enter watermark text", size_hint=(1, 0.3))
        layout.add_widget(self.text_input)
        
        # Checkbox for B&W
        bw_layout = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.bw_checkbox = CheckBox(active=True)
        bw_label = Label(text="B&W")
        bw_layout.add_widget(self.bw_checkbox)
        bw_layout.add_widget(bw_label)
        layout.add_widget(bw_layout)
        
        # Checkbox for Hide ID
        hide_layout = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.hide_checkbox = CheckBox(active=True)
        hide_label = Label(text="Hide ID")
        hide_layout.add_widget(self.hide_checkbox)
        hide_layout.add_widget(hide_label)
        layout.add_widget(hide_layout)

        # Button to generate watermark
        self.generate_button = Button(text="Generate Watermark", size_hint=(1, 0.2))
        self.generate_button.bind(on_press=self.generate_watermark)
        layout.add_widget(self.generate_button)

        return layout

    def generate_watermark(self, instance):
        watermark_text = self.text_input.text.strip()
        if not watermark_text:
            self.show_popup("Error", "Please enter some text for the watermark.")
            return

        input_image_path = 'images/test.webp'
        if not os.path.exists(input_image_path):
            self.show_popup("Error", f"The input image {input_image_path} was not found.")
            return

        # Modify image
        try:
            with PILImage.open(input_image_path) as img:
                # Convert image to B&W
                if self.bw_checkbox.active:
                    img = img.convert("L").convert("RGB")
                
                # Add watermark text
                draw = ImageDraw.Draw(img)
                font_size = int(img.size[1] * 0.075)  # Font size proportional to image height
                font = ImageFont.truetype("font/Arial.ttf", font_size)
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                mult = [0.95, 0.32]
                position = [(img.size[0]-text_width) * mult[0], (img.size[1]-text_height) * mult[1]]
                draw.text(position, watermark_text, (255, 0, 0), font=font)
                
                # Hide ID
                if self.hide_checkbox.active:
                    # eyes
                    mult1 = [0.1, 0.45]
                    mult2 = [0.3, 0.55]
                    position1 = (img.size[0] * mult1[0], img.size[1] * mult1[1])
                    position2 = (img.size[0] * mult2[0], img.size[1] * mult2[1])
                    draw.rectangle([position1, position2], fill="black")

                    # signature
                    mult1 = [0.4, 0.77]
                    mult2 = [0.75, 0.88]
                    position1 = (img.size[0] * mult1[0], img.size[1] * mult1[1])
                    position2 = (img.size[0] * mult2[0], img.size[1] * mult2[1])
                    draw.rectangle([position1, position2], fill="black")

        except Exception as e:
            self.show_popup("Error", f"Failed to create watermark: {e}")
            return

        self.show_save_dialog(img)

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Button(text=message, size_hint=(1, 0.7)))
        close_button = Button(text="Close", size_hint=(1, 0.3))
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def show_save_dialog(self, img):
        filechooser = FileChooserListView(path=os.getcwd(), dirselect=True)

        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(filechooser)

        save_button = Button(text="Save", size_hint=(1, 0.1))
        popup_layout.add_widget(save_button)

        popup = Popup(title="Save Image", content=popup_layout, size_hint=(0.9, 0.9))

        def save_image(instance):
            output_name = f"Watermark_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            selected_path = filechooser.selection[0] if filechooser.selection else None
            if selected_path:
                try:
                    # Check if the selection is a directory
                    if os.path.isdir(selected_path):
                        output_image_path = os.path.join(selected_path, output_name)
                        img.save(output_image_path)
                        popup.dismiss()
                        self.show_popup("Success", f"Image saved to {output_image_path}")
                    else:
                        self.show_popup("Error", "Please select a directory.")
                except Exception as e:
                    self.show_popup("Error", f"Failed to save image: {e}")

        save_button.bind(on_press=save_image)
        popup.open()

if __name__ == '__main__':
    WatermarkApp().run()

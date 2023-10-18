import kivy
import speech_recognition as sr
import openai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

kivy.require("1.11.1")

class VoiceAssistantApp(App):
    def build(self):
        self.title = "Voice Assistant"
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.chat_history = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_history.bind(minimum_height=self.chat_history.setter("height"))

        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.chat_history)

        self.message_label = Label(text="Say a command or type it here...")
        self.listen_button = Button(text="Listen")
        self.listen_button.bind(on_press=self.listen_to_voice)
        self.input_text = TextInput(hint_text="Type your message here and press Enter")
        self.input_text.bind(on_text_validate=self.process_text_command)

        self.layout.add_widget(self.scroll_view)
        self.layout.add_widget(self.message_label)
        self.layout.add_widget(self.listen_button)
        self.layout.add_widget(self.input_text)

        self.recognizer = sr.Recognizer()
        openai.api_key = "YOUR_OPENAI_API_KEY"

        return self.layout

    def listen_to_voice(self, instance):
        self.message_label.text = "Listening..."
        Clock.schedule_once(self.process_voice_command, 0.1)

    def process_voice_command(self, dt):
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                self.process_command("Voice", command)
            except sr.WaitTimeoutError:
                self.message_label.text = "No command heard. Say a command..."
            except sr.UnknownValueError:
                self.message_label.text = "Sorry, I couldn't understand that. Say a command..."

    def process_text_command(self, instance):
        command = self.input_text.text
        self.input_text.text = ""
        self.process_command("Text", command)

    def process_command(self, sender, command):
        self.add_message(sender, command)
        if sender == "Voice":
            response = self.get_ai_response(command)
            self.add_message("AI", response)

    def get_ai_response(self, command):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=command,
                max_tokens=50
            )
            return response.choices[0].text
        except Exception as e:
            return f"AI Error: {str(e)}"

    def add_message(self, sender, message):
        label = Label(text=f"[{sender}]: {message}")
        self.chat_history.add_widget(label)

if __name__ == "__main__":
    VoiceAssistantApp().run()

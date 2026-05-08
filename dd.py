import os
import csv
import math
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.resources import resource_add_path
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from kivy.uix.button import Button

# ==========================================
# 📱 PC पर मोबाइल स्क्रीन साइज सेट करें
# ==========================================
Window.size = (360, 640)

# ==========================================
# 🌍 UNIVERSAL FONT SETUP
# ==========================================
curr_dir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(curr_dir)

U_FONT = "UniversalFont"
FONT_FILE = "devanagari.ttf" 

if os.path.exists(os.path.join(curr_dir, FONT_FILE)):
    LabelBase.register(name=U_FONT, fn_regular=FONT_FILE)
    print("✅ Universal Font Loaded!")
else:
    U_FONT = "Roboto"
    print("⚠️ Warning: Font not found. Using default.")

# ==========================================
# 🧠 APP LOGIC (SCREENS)
# ==========================================

class HomeScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class QuizScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.questions = []
        self.current_index = 0
        self.timer_event = None
        self.time_limit = 7.0  
        self.last_tick_sec = 7 
        
        # 🎵 साउंड फाइल्स लोड करें
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        tick_path = os.path.join(curr_dir, 'tick.wav')
        correct_path = os.path.join(curr_dir, 'correct.wav')
        
        self.tick_snd = SoundLoader.load(tick_path) if os.path.exists(tick_path) else None
        self.correct_snd = SoundLoader.load(correct_path) if os.path.exists(correct_path) else None
        
        if self.correct_snd:
            print("✅ correct.wav loaded successfully!")

    def start_quiz(self, data):
        # CSV Header चेक
        if data and data[0][0].lower() in ['q', 'question', 'प्रश्न', 'सवाल']:
            self.questions = data[1:]
        else:
            self.questions = data
        self.current_index = 0
        self.load_question()

    def load_question(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.ids.q_text.text = str(q[0])
            self.ids.opt1.text = f"A: {q[1]}"
            self.ids.opt2.text = f"B: {q[2]}"
            self.ids.opt3.text = f"C: {q[3]}"
            self.ids.opt4.text = f"D: {q[4]}"
            self.correct_ans = str(q[5]).strip().upper()
            
            # प्रोग्रेस ट्रैकर
            total_q = len(self.questions)
            curr_q = self.current_index + 1
            self.ids.q_tracker.text = f"प्रश्न: {curr_q} / {total_q}"
            
            self.reset_buttons()
            self.counter = self.time_limit
            self.last_tick_sec = int(self.time_limit) 
            self.ids.timer_lbl.text = str(int(self.time_limit))
            self.ids.prog_bar.value = 100
            
            if self.timer_event: 
                self.timer_event.cancel()
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.05)
        else:
            self.ids.q_text.text = "🎉 क्विज़ समाप्त! 🎉"
            self.ids.q_tracker.text = "All Done!"
            self.ids.timer_lbl.text = "0"
            self.ids.prog_bar.value = 0

    def update_timer(self, dt):
        if self.counter > 0:
            self.counter -= dt
            current_sec = int(math.ceil(self.counter))
            self.ids.timer_lbl.text = str(max(0, current_sec))
            self.ids.prog_bar.value = (self.counter / self.time_limit) * 100
            
            # हर सेकंड टिक साउंड
            if current_sec < self.last_tick_sec:
                if self.tick_snd:
                    self.tick_snd.play()
                self.last_tick_sec = current_sec
        else:
            self.ids.prog_bar.value = 0
            self.reveal_correct() # टाइमर खत्म होने पर ऑटो-रिवील
            return False

    def check_answer(self, choice):
        if self.timer_event: self.timer_event.cancel()
        if self.tick_snd: self.tick_snd.stop()
            
        mapping = {"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}
        
        # गलत जवाब को लाल करें
        if choice != self.correct_ans:
            self.ids[mapping[choice]].md_bg_color = (0.8, 0, 0, 1)
            
        # सही जवाब को हमेशा ग्रीन करें और साउंड बजाएं
        if self.correct_ans in mapping:
            self.ids[mapping[self.correct_ans]].md_bg_color = (0, 0.8, 0, 1)
            if self.correct_snd:
                self.correct_snd.stop()
                self.correct_snd.play()
            
        Clock.schedule_once(lambda dt: self.next_q(), 2)

    def reveal_correct(self):
        if self.tick_snd: self.tick_snd.stop()
        mapping = {"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}
        
        # ऑटोमैटिक ग्रीन और साउंड
        if self.correct_ans in mapping:
            self.ids[mapping[self.correct_ans]].md_bg_color = (0, 0.8, 0, 1)
            if self.correct_snd:
                self.correct_snd.stop()
                self.correct_snd.play()
                
        Clock.schedule_once(lambda dt: self.next_q(), 2)

    def next_q(self):
        self.current_index += 1
        self.load_question()

    def reset_buttons(self):
        for i in range(1, 5):
            self.ids[f'opt{i}'].md_bg_color = (0.15, 0.25, 0.45, 1)
            self.ids[f'opt{i}'].disabled = False

    def stop_quiz(self):
        if self.timer_event: self.timer_event.cancel()
        if self.tick_snd: self.tick_snd.stop()

# ==========================================
# 🎨 UI DESIGN (KV)
# ==========================================
KV = f'''
<HomeScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.1, 1
        
        MDTopAppBar:
            title: "LikeStudy PRO"
            elevation: 4
            md_bg_color: 0, 0.5, 0.8, 1
            right_action_items: [["account-cog-outline", lambda x: app.go_profile()]]
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(15)
            
            MDRectangleFlatIconButton:
                icon: "plus-circle"
                text: "ADD NEW CSV FILE"
                pos_hint: {{"center_x": .5}}
                width: dp(250)
                font_name: "{U_FONT}"
                line_color: 0, 1, 1, 1
                text_color: 0, 1, 1, 1
                on_release: app.open_file_manager()
                
            MDLabel:
                text: "UPLOADED QUIZZES:"
                halign: "center"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 1, 0, 1, 1
                size_hint_y: None
                height: dp(30)
                font_name: "{U_FONT}"
                
            MDScrollView:
                MDBoxLayout:
                    id: file_list
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(10)

<ProfileScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.1, 1
        
        MDTopAppBar:
            title: "Settings & Profile"
            md_bg_color: 0.1, 0.1, 0.2, 1
            elevation: 0
            
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(20)
            
            MDIcon:
                icon: "account-circle"
                font_size: "100sp"
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0, 1, 1, 1
                
            MDLabel:
                text: "Guest User"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                
            MDCard:
                orientation: "vertical"
                padding: dp(15)
                spacing: dp(15)
                md_bg_color: 0.1, 0.1, 0.25, 1
                radius: [15,]
                size_hint_y: None
                height: dp(150)
                
                MDLabel:
                    text: "App Settings"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 0, 1, 1
                    
                MDBoxLayout:
                    MDLabel:
                        text: "Sound Effects"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                    MDSwitch:
                        active: True
                        
                MDBoxLayout:
                    MDLabel:
                        text: "Dark Mode"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                    MDSwitch:
                        active: True
            Widget:
            MDFillRoundFlatIconButton:
                icon: "home"
                text: "BACK TO HOME"
                font_name: "{U_FONT}"
                pos_hint: {{"center_x": .5}}
                md_bg_color: 0, 0.5, 0.8, 1
                on_release: app.go_home()

<QuizScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0, 0, 0, 1
        padding: dp(15), dp(10), dp(15), dp(15)
        spacing: dp(10)

        MDLabel:
            id: timer_lbl
            text: "10"
            halign: "center"
            font_style: "H3"
            text_color: 1, 0, 1, 1
            theme_text_color: "Custom"
            size_hint_y: None
            height: dp(40)

        MDProgressBar:
            id: prog_bar
            value: 100
            color: 1, 0, 1, 1
            size_hint_y: None
            height: dp(6)

        MDLabel:
            id: q_tracker
            text: "प्रश्न: 0 / 0"
            halign: "center"
            font_name: "{U_FONT}"
            theme_text_color: "Custom"
            text_color: 0, 1, 1, 1
            size_hint_y: None
            height: dp(20)

        MDCard:
            size_hint: 1, 0.4
            md_bg_color: 0.1, 0.1, 0.25, 1
            radius: [15,]
            line_color: 0, 1, 1, 1
            padding: dp(15)
            MDLabel:
                id: q_text
                text: "Loading..."
                halign: "center"
                font_name: "{U_FONT}"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: 0.45
            
            MDRaisedButton:
                id: opt1
                text: "Option A"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                font_size: "16sp"
                on_release: root.check_answer("A")
                
            MDRaisedButton:
                id: opt2
                text: "Option B"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                font_size: "16sp"
                on_release: root.check_answer("B")

            MDRaisedButton:
                id: opt3
                text: "Option C"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                font_size: "16sp"
                on_release: root.check_answer("C")

            MDRaisedButton:
                id: opt4
                text: "Option D"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                font_size: "16sp"
                on_release: root.check_answer("D")

        # सीक्रेट पारदर्शी एग्जिट बटन
        Button:
            text: ""
            size_hint: 1, None
            height: dp(50)
            background_color: 0, 0, 0, 0  
            background_normal: ''
            background_down: ''
            on_release: app.go_home_from_quiz()
'''

# ==========================================
# ⚙️ MAIN APP CLASS
# ==========================================

class LikeStudyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        # कस्टम फॉन्ट स्टाइल्स
        self.theme_cls.font_styles["H3"] = [U_FONT, 48, False, 0.15]
        self.theme_cls.font_styles["H5"] = [U_FONT, 24, False, 0.15]
        self.theme_cls.font_styles["H6"] = [U_FONT, 20, False, 0.15]
        
        Builder.load_string(KV)
        self.manager = ScreenManager()
        self.manager.add_widget(HomeScreen(name='home'))
        self.manager.add_widget(QuizScreen(name='quiz'))
        self.manager.add_widget(ProfileScreen(name='profile')) 
        
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path
        )
        return self.manager

    def open_file_manager(self):
        path = os.getenv('EXTERNAL_STORAGE', os.getcwd())
        self.file_manager.show(path)

    def select_path(self, path):
        self.close_file_manager()
        if path.endswith('.csv'):
            filename = os.path.basename(path)
            home_screen = self.manager.get_screen('home')
            
            # लिस्ट में नया क्विज़ कार्ड जोड़ें
            card = MDCard(size_hint_y=None, height=dp(60), md_bg_color=(0.1, 0.1, 0.25, 1),
                          radius=[10,], line_color=(0, 1, 1, 1), padding=dp(10))
            lbl = MDLabel(text=filename, theme_text_color="Custom", text_color=(1, 1, 1, 1), font_name=U_FONT)
            play_btn = MDIconButton(icon="play-circle", theme_text_color="Custom", 
                                    text_color=(0, 1, 0, 1), pos_hint={"center_y": .5})
            
            play_btn.bind(on_release=lambda x, p=path: self.play_selected_quiz(p))
            card.add_widget(lbl); card.add_widget(play_btn)
            home_screen.ids.file_list.add_widget(card)

    def play_selected_quiz(self, path):
        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                data = list(csv.reader(f))
                self.manager.get_screen('quiz').start_quiz(data)
                self.manager.current = 'quiz'
        except Exception as e:
            print(f"Error: {e}")

    def close_file_manager(self, *args):
        self.file_manager.close()

    def go_home(self):
        self.manager.current = 'home'

    def go_home_from_quiz(self):
        self.manager.get_screen('quiz').stop_quiz()
        self.manager.current = 'home'
        
    def go_profile(self):
        self.manager.current = 'profile'

if __name__ == '__main__':
    LikeStudyApp().run()

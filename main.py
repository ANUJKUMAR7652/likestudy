import os
import csv
import math
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivy.resources import resource_add_path
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from kivy.utils import platform

# ==========================================
# 🌍 DIRECTORY & FONT SETUP
# ==========================================
curr_dir = os.path.dirname(os.path.abspath(__file__))
resource_add_path(curr_dir)

U_FONT = "HindiFont"
FONT_FILE = "hindi.ttf"  # Nayi Noto Sans file

if os.path.exists(os.path.join(curr_dir, FONT_FILE)):
    LabelBase.register(name=U_FONT, fn_regular=FONT_FILE)
else:
    # Fallback logic
    alt_fonts = ["universal.ttf", "devanagari.ttf"]
    found = False
    for f in alt_fonts:
        if os.path.exists(os.path.join(curr_dir, f)):
            LabelBase.register(name=U_FONT, fn_regular=f)
            found = True
            break
    if not found:
        U_FONT = "Roboto"

# ==========================================
# 🧠 SCREENS LOGIC
# ==========================================
class HomeScreen(Screen): pass
class ProfileScreen(Screen): pass

class QuizScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.questions = []
        self.current_index = 0
        self.timer_event = None
        self.time_limit = 7.0
        self.last_tick_sec = 7
        
        tick_p = os.path.abspath(os.path.join(curr_dir, 'tick.wav'))
        corr_p = os.path.abspath(os.path.join(curr_dir, 'correct.wav'))
        
        self.tick_snd = SoundLoader.load(tick_p) if os.path.exists(tick_p) else None
        self.correct_snd = SoundLoader.load(corr_p) if os.path.exists(corr_p) else None
        
        if self.tick_snd: self.tick_snd.volume = 1.0
        if self.correct_snd: self.correct_snd.volume = 1.0

    def start_quiz(self, data):
        if data and str(data[0][0]).lower() in ['q', 'question', 'प्रश्न', 'सवाल']:
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
            self.ids.q_tracker.text = f"प्रश्न: {self.current_index + 1} / {len(self.questions)}"
            
            self.reset_buttons()
            self.counter = self.time_limit
            self.last_tick_sec = int(self.time_limit)
            self.ids.timer_lbl.text = str(int(self.time_limit))
            self.ids.prog_bar.value = 100
            
            if self.timer_event: self.timer_event.cancel()
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.05)
        else:
            self.ids.q_text.text = "🎉 क्विज़ समाप्त! 🎉"

    def update_timer(self, dt):
        if self.counter > 0:
            self.counter -= dt
            sec = int(math.ceil(self.counter))
            self.ids.timer_lbl.text = str(max(0, sec))
            self.ids.prog_bar.value = (self.counter / self.time_limit) * 100
            if sec < self.last_tick_sec:
                if self.tick_snd: self.tick_snd.play()
                self.last_tick_sec = sec
        else:
            self.reveal_correct()
            return False

    def check_answer(self, choice):
        if self.timer_event: self.timer_event.cancel()
        mapping = {"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}
        if choice != self.correct_ans and choice in mapping:
            self.ids[mapping[choice]].md_bg_color = (0.8, 0, 0, 1)
        if self.correct_ans in mapping:
            self.ids[mapping[self.correct_ans]].md_bg_color = (0, 0.8, 0, 1)
            if self.correct_snd: self.correct_snd.play()
        Clock.schedule_once(lambda dt: self.next_q(), 2)

    def reveal_correct(self):
        mapping = {"A": "opt1", "B": "opt2", "C": "opt3", "D": "opt4"}
        if self.correct_ans in mapping:
            self.ids[mapping[self.correct_ans]].md_bg_color = (0, 0.8, 0, 1)
            if self.correct_snd: self.correct_snd.play()
        Clock.schedule_once(lambda dt: self.next_q(), 2)

    def next_q(self):
        self.current_index += 1
        self.load_question()

    def reset_buttons(self):
        for i in range(1, 5):
            self.ids[f'opt{i}'].md_bg_color = (0.15, 0.25, 0.45, 1)

    def stop_quiz(self):
        if self.timer_event: self.timer_event.cancel()

# ==========================================
# 🎨 UI DESIGN (KV)
# ==========================================
KV = f'''
<HomeScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.1, 1
        MDTopAppBar:
            title: "StudyLike PRO"
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
                size_hint_x: 0.9
                font_name: "{U_FONT}"
                on_release: app.open_file_manager()
            MDLabel:
                text: "UPLOADED QUIZZES:"
                halign: "center"
                font_name: "{U_FONT}"
                theme_text_color: "Custom"
                text_color: 1, 0, 1, 1
            MDScrollView:
                MDBoxLayout:
                    id: file_list
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: dp(10)

<QuizScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0, 0, 0, 1
        padding: dp(15)
        MDLabel:
            id: timer_lbl
            text: "7"
            halign: "center"
            font_style: "H3"
            theme_text_color: "Custom"
            text_color: 1, 0, 1, 1
        MDProgressBar:
            id: prog_bar
            value: 100
        MDLabel:
            id: q_tracker
            text: ""
            halign: "center"
            font_name: "{U_FONT}"
        MDCard:
            size_hint: 1, 0.4
            md_bg_color: 0.1, 0.1, 0.25, 1
            radius: [15,]
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
            MDRaisedButton:
                id: opt1
                text: "Option A"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                on_release: root.check_answer("A")
            MDRaisedButton:
                id: opt2
                text: "Option B"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                on_release: root.check_answer("B")
            MDRaisedButton:
                id: opt3
                text: "Option C"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                on_release: root.check_answer("C")
            MDRaisedButton:
                id: opt4
                text: "Option D"
                size_hint: 1, 1
                font_name: "{U_FONT}"
                on_release: root.check_answer("D")
        MDIconButton:
            icon: "home-circle"
            pos_hint: {{"center_x": .5}}
            on_release: app.go_home_from_quiz()

<ProfileScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.1, 1
        MDLabel:
            text: "Settings"
            halign: "center"
            font_name: "{U_FONT}"
        MDFillRoundFlatButton:
            text: "BACK"
            on_release: app.go_home()
'''

class LikeStudyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
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
            select_path=self.select_path,
            ext=[".csv"]
        )
        return self.manager

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            from android import api_version
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            
            if api_version >= 30:
                from jnius import autoclass
                Environment = autoclass('android.os.Environment')
                if not Environment.isExternalStorageManager():
                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Intent = autoclass('android.content.Intent')
                    Settings = autoclass('android.provider.Settings')
                    Uri = autoclass('android.net.Uri')
                    uri = Uri.parse("package:" + PythonActivity.mActivity.getPackageName())
                    intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION, uri)
                    PythonActivity.mActivity.startActivity(intent)

    def open_file_manager(self):
        path = '/storage/emulated/0/' if platform == 'android' else os.getcwd()
        self.file_manager.show(path)

    def select_path(self, path):
        self.close_file_manager()
        if path.endswith('.csv'):
            home_screen = self.manager.get_screen('home')
            card = MDCard(size_hint_y=None, height=dp(60), md_bg_color=(0.1, 0.1, 0.25, 1), padding=dp(10))
            lbl = MDLabel(text=os.path.basename(path), font_name=U_FONT, theme_text_color="Custom", text_color=(1,1,1,1))
            play_btn = MDIconButton(icon="play-circle", text_color=(0, 1, 0, 1), theme_text_color="Custom")
            play_btn.bind(on_release=lambda x, p=path: self.play_quiz(p))
            card.add_widget(lbl); card.add_widget(play_btn)
            home_screen.ids.file_list.add_widget(card)

    def play_quiz(self, path):
        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                data = list(csv.reader(f))
                self.manager.get_screen('quiz').start_quiz(data)
                self.manager.current = 'quiz'
        except Exception as e: print(f"Error: {e}")

    def close_file_manager(self, *args): self.file_manager.close()
    def go_home(self): self.manager.current = 'home'
    def go_profile(self): self.manager.current = 'profile'
    def go_home_from_quiz(self):
        self.manager.get_screen('quiz').stop_quiz()
        self.manager.current = 'home'

if __name__ == '__main__':
    LikeStudyApp().run()

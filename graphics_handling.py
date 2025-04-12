from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup

class SymbolsWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Wprowadzanie unitermów'
        self.size_hint = (0.8,0.8)
        self.separator_color=(24/255,123/255,205/255,1)
        self.background_color=(0,0,0,1)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(3/255,37/255,76/255,1)
            self.rect = Rectangle(size=layout.size,pos=layout.pos)
        layout.bind(size=self.update_rect,pos=self.update_rect)
        text1 = Label(text='Dla poziomej operacji sekwencjonowania',pos_hint={'center_x':0.5,'center_y':0.85},font_size='39')
        text2 = Label(text='Dla pionowej operacji sekwencjonowania',pos_hint={'center_x':0.5,'center_y':0.54},font_size='39')
        symbol1 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.3,'center_y':0.72})
        symbol2 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.7,'center_y':0.72})
        symbol3 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.3,'center_y':0.41})
        symbol4 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.7,'center_y':0.41})
        button1 = Button(text='Zatwierdź',size_hint=(0.32,0.1),pos_hint={'center_x':0.25,'center_y':0.17},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button2 = Button(text='Cofnij',size_hint=(0.32,0.1),pos_hint={'center_x':0.75,'center_y':0.17},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        layout.add_widget(text1)
        layout.add_widget(text2)
        layout.add_widget(symbol1)
        layout.add_widget(symbol2)
        layout.add_widget(symbol3)
        layout.add_widget(symbol4)
        layout.add_widget(button1)
        layout.add_widget(button2)
        self.content = layout
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class ApplicationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = [None,None,None,None]
        self.orientation = 'horizontal'
        left_side = Widget()
        with left_side.canvas.before:
            Color(1,1,1,1)
            self.rect_l = Rectangle(size=left_side.size,pos=left_side.pos)
        left_side.bind(size=self.update_rect_l,pos=self.update_rect_l)
        right_side = FloatLayout(size_hint=(0.3, 1))
        with right_side.canvas.before:
            Color(3/255,37/255,76/255,1)
            self.rect_r = Rectangle(size=right_side.size,pos=right_side.pos)
        right_side.bind(size=self.update_rect_r,pos=self.update_rect_r)
        button1 = Button(text='Wprowadź',size_hint=(0.72,0.1),pos_hint={'center_x':0.5,'center_y':0.76},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button2 = Button(text='Zamień',size_hint=(0.72,0.1),pos_hint={'center_x':0.5,'center_y':0.59},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button3 = Button(text='Wczytaj',size_hint=(0.72,0.1),pos_hint={'center_x':0.5,'center_y':0.42},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button4 = Button(text='Zapisz',size_hint=(0.72,0.1),pos_hint={'center_x':0.5,'center_y':0.25},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button1.bind(on_release=self.show_symbols_window)
        right_side.add_widget(button1)
        right_side.add_widget(button2)
        right_side.add_widget(button3)
        right_side.add_widget(button4)
        self.add_widget(left_side)
        self.add_widget(right_side)
    def update_rect_l(self, instance,value):
        self.rect_l.pos = instance.pos
        self.rect_l.size = instance.size
    def update_rect_r(self,instance,value):
        self.rect_r.pos = instance.pos
        self.rect_r.size = instance.size
    def show_symbols_window(self,instance):
        popup = SymbolsWindow()
        popup.open()

class UnitermGUI(App):
    def build(self):
        self.title = 'MASI Uniterm'
        return ApplicationLayout()  
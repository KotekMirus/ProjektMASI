from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class ApplicationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

class UnitermGUI(App):
    def build(self):
        self.title = 'MASI Uniterm'
        return ApplicationLayout()
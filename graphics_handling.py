from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Line
import database_handling as dbh

symbols = ['','','','']
position = 0
saved = True

class SymbolsWindow(Popup):
    def __init__(self,parent_ref,**kwargs):
        super(SymbolsWindow,self).__init__(**kwargs)
        self.parent_ref = parent_ref
        self.title = 'Wprowadzanie unitermów'
        self.size_hint = (0.8,0.8)
        self.separator_color=(24/255,123/255,205/255,1)
        self.background_color=(0,0,0,1)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(3/255,37/255,76/255,1)
            self.rect = Rectangle(size=layout.size,pos=layout.pos)
        layout.bind(size=self.update_rect,pos=self.update_rect)
        text1 = Label(text='Dla pionowej operacji sekwencjonowania',pos_hint={'center_x':0.5,'center_y':0.85},font_size='39')
        text2 = Label(text='Dla poziomej operacji sekwencjonowania',pos_hint={'center_x':0.5,'center_y':0.54},font_size='39')
        self.symbol1 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.3,'center_y':0.72},font_size='40')
        self.symbol2 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.7,'center_y':0.72},font_size='40')
        self.symbol3 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.3,'center_y':0.41},font_size='40')
        self.symbol4 = TextInput(multiline=False,size_hint=(0.28,0.1),pos_hint={'center_x':0.7,'center_y':0.41},font_size='40')
        button1 = Button(text='Zatwierdź',size_hint=(0.32,0.1),pos_hint={'center_x':0.25,'center_y':0.17},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button2 = Button(text='Cofnij',size_hint=(0.32,0.1),pos_hint={'center_x':0.75,'center_y':0.17},background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
        button1.bind(on_release=self.save_symbols_and_exit)
        button2.bind(on_release=self.exit)
        layout.add_widget(text1)
        layout.add_widget(text2)
        layout.add_widget(self.symbol1)
        layout.add_widget(self.symbol2)
        layout.add_widget(self.symbol3)
        layout.add_widget(self.symbol4)
        layout.add_widget(button1)
        layout.add_widget(button2)
        self.content = layout
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def save_symbols_and_exit(self,instance):
        global saved
        global symbols
        global position
        if self.symbol1.text != '' and self.symbol2.text != '' and self.symbol3.text != '' and self.symbol4.text != '':
            symbols[0] = self.symbol1.text
            symbols[1] = self.symbol2.text
            symbols[2] = self.symbol3.text
            symbols[3] = self.symbol4.text
            position = 0
            saved = False
            self.parent_ref.draw_operations()
            self.dismiss()
    def exit(self,instance):
        self.dismiss()

class LoadWindow(Popup):
    def __init__(self,parent_ref,**kwargs):
        super(LoadWindow,self).__init__(**kwargs)
        self.parent_ref = parent_ref
        self.title = 'Wczytywanie danych operacji'
        self.size_hint = (0.8,0.8)
        self.separator_color=(24/255,123/255,205/255,1)
        self.background_color=(0,0,0,1)
        layout = BoxLayout()
        layout.orientation = 'vertical'
        with layout.canvas.before:
            Color(3/255,37/255,76/255,1)
            self.rect = Rectangle(size=layout.size,pos=layout.pos)
        layout.bind(size=self.update_rect,pos=self.update_rect)
        database = dbh.load_all_entries()
        scroll = ScrollView()
        entries_list = GridLayout(cols=1,spacing=14,size_hint_y=None,padding=(130,20,130,20))
        entries_list.bind(minimum_height=entries_list.setter('height'))
        for date in database.keys():
            text = date[:19]+'\n'+(database[date]['symbol1']+' ; '+database[date]['symbol2']+' ; '+database[date]['symbol3']+' ; '+database[date]['symbol4'])[:39]
            button = Button(text=text,height=86,size_hint_y=None,background_normal='',background_color=(24/255,123/255,205/255,1),font_size='35')
            button.bind(on_release=lambda instance,d=date: self.load_uniterms(d))
            entries_list.add_widget(button)
        scroll.add_widget(entries_list)
        layout.add_widget(scroll)
        self.content = layout
    def update_rect(self,instance,value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def load_uniterms(self,date):
        global symbols
        global position
        database = dbh.load_all_entries()
        symbols[0] = database[date]['symbol1']
        symbols[1] = database[date]['symbol2']
        symbols[2] = database[date]['symbol3']
        symbols[3] = database[date]['symbol4']
        position = database[date]['position']
        if position == 0:
            self.parent_ref.draw_operations()
        elif position == 1:
            position = 2
            self.parent_ref.draw_operations(True)
        elif position == 2:
            position = 1
            self.parent_ref.draw_operations(True)
        self.dismiss()

class ApplicationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.left_side = Widget()
        with self.left_side.canvas.before:
            Color(1,1,1,1)
            self.rect_l = Rectangle(size=self.left_side.size,pos=self.left_side.pos)
        self.left_side.bind(size=self.update_rect_l,pos=self.update_rect_l)
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
        button2.bind(on_release=self.make_swap_operation)
        button3.bind(on_release=self.show_load_window)
        button4.bind(on_release=self.save_uniterms)
        right_side.add_widget(button1)
        right_side.add_widget(button2)
        right_side.add_widget(button3)
        right_side.add_widget(button4)
        self.add_widget(self.left_side)
        self.add_widget(right_side)
    def update_rect_l(self, instance,value):
        self.rect_l.pos = instance.pos
        self.rect_l.size = instance.size
    def update_rect_r(self,instance,value):
        self.rect_r.pos = instance.pos
        self.rect_r.size = instance.size
    def show_symbols_window(self,*args):
        popup = SymbolsWindow(parent_ref=self)
        popup.open()
    def show_load_window(self,*args):
        popup = LoadWindow(parent_ref=self)
        popup.open()
    def save_uniterms(self,instance):
        global saved
        global position
        global symbols
        if not saved:
            dbh.save_entry(symbols,position)
            saved = True
    def make_swap_operation(self,instance):
        if symbols[0] != '' and symbols[1] != '' and symbols[2] != '' and symbols[3] != '':
            self.draw_operations(True)
    def draw_operations(self,with_swap=False):
        global symbols
        global position
        canvas_width = self.left_side.width
        canvas_height = self.left_side.height
        size_sample = canvas_height+canvas_width
        curve_width = 2
        if size_sample >= 2200:
            curve_width = 6
        elif size_sample >= 1800:
            curve_width = 5
        elif size_sample >= 1400:
            curve_width = 4
        elif size_sample >= 1000:
            curve_width = 3
        else:
            curve_width = 2
        symbol1 = CoreLabel(text=symbols[0],font_size=int(canvas_height*0.06444))
        symbol1.refresh()
        symbol1_texture = symbol1.texture
        symbol2 = CoreLabel(text=symbols[1],font_size=int(canvas_height*0.06444))
        symbol2.refresh()
        symbol2_texture = symbol2.texture
        symbol3 = CoreLabel(text=symbols[2],font_size=int(canvas_height*0.06444))
        symbol3.refresh()
        symbol3_texture = symbol3.texture
        symbol4 = CoreLabel(text=symbols[3],font_size=int(canvas_height*0.06444))
        symbol4.refresh()
        symbol4_texture = symbol4.texture
        separator = CoreLabel(text=";",font_size=int(canvas_height*0.06444))
        separator.refresh()
        separator_texture = separator.texture
        self.left_side.canvas.clear()
        with self.left_side.canvas:
            Color(0,0,0,1)
            Line(bezier=[
                canvas_width*0.196,canvas_height*0.967,
                canvas_width*0.016,canvas_height*0.822,
                canvas_width*0.016,canvas_height*0.678,
                canvas_width*0.196,canvas_height*0.533
            ],width=curve_width)
            Line(bezier=[
                canvas_width*0.522,canvas_height*0.683,
                canvas_width*0.674,canvas_height*0.867,
                canvas_width*0.826,canvas_height*0.867,
                canvas_width*0.978,canvas_height*0.683
            ],width=curve_width)
            Rectangle(texture=symbol1_texture,pos=(canvas_width*0.114,canvas_height*0.811),size=symbol1_texture.size)
            Rectangle(texture=separator_texture,pos=(canvas_width*0.114,canvas_height*0.720),size=separator_texture.size)
            Rectangle(texture=symbol2_texture,pos=(canvas_width*0.114,canvas_height*0.617),size=symbol2_texture.size)
            Rectangle(texture=symbol3_texture,pos=(canvas_width*0.598,canvas_height*0.678),size=symbol3_texture.size)
            Rectangle(texture=separator_texture,pos=(canvas_width*0.745,canvas_height*0.686),size=separator_texture.size)
            Rectangle(texture=symbol4_texture,pos=(canvas_width*0.786,canvas_height*0.678),size=symbol4_texture.size)
            if with_swap:
                if position == 0 or position == 2:
                    position = 1
                elif position == 1:
                    position = 2
                Line(bezier=[
                    canvas_width*0.272,canvas_height*0.328,
                    canvas_width*0.435,canvas_height*0.511,
                    canvas_width*0.598,canvas_height*0.511,
                    canvas_width*0.761,canvas_height*0.328
                ],width=curve_width)
                if position == 1:
                    Line(bezier=[
                        canvas_width*0.397,canvas_height*0.417,
                        canvas_width*0.283,canvas_height*0.317,
                        canvas_width*0.283,canvas_height*0.217,
                        canvas_width*0.397,canvas_height*0.117
                    ],width=curve_width)
                    Rectangle(texture=symbol1_texture,pos=(canvas_width*0.358,canvas_height*0.308),size=symbol1_texture.size)
                    Rectangle(texture=symbol2_texture,pos=(canvas_width*0.358,canvas_height*0.165),size=symbol2_texture.size)
                    Rectangle(texture=separator_texture,pos=(canvas_width*0.358,canvas_height*0.241),size=separator_texture.size)
                    Rectangle(texture=symbol4_texture,pos=(canvas_width*0.552,canvas_height*0.329),size=symbol4_texture.size)
                elif position == 2:
                    Line(bezier=[
                        canvas_width*0.637,canvas_height*0.417,
                        canvas_width*0.523,canvas_height*0.317,
                        canvas_width*0.523,canvas_height*0.217,
                        canvas_width*0.637,canvas_height*0.117
                    ],width=curve_width)
                    Rectangle(texture=symbol1_texture,pos=(canvas_width*0.598,canvas_height*0.308),size=symbol1_texture.size)
                    Rectangle(texture=symbol2_texture,pos=(canvas_width*0.598,canvas_height*0.165),size=symbol2_texture.size)
                    Rectangle(texture=separator_texture,pos=(canvas_width*0.598,canvas_height*0.241),size=separator_texture.size)
                    Rectangle(texture=symbol3_texture,pos=(canvas_width*0.349,canvas_height*0.329),size=symbol3_texture.size)
                Rectangle(texture=separator_texture,pos=(canvas_width*0.511,canvas_height*0.342),size=separator_texture.size)

class UnitermGUI(App):
    def build(self):
        self.title = 'MASI - Operacje na unitermach'
        return ApplicationLayout()  
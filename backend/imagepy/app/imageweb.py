import os, sys
import time, threading
sys.path.append('../../../')
from skimage.data import camera
from sciapp import App, Source
from sciapp.object import Image, Table, Scene, Mesh
from imagepy import root_dir
from .startup import load_plugins, load_plugins_for_json, load_tools, load_widgets, load_document, load_dictionary
from .manager import ConfigManager, DictManager, ShortcutManager, DocumentManager

class ImageWeb(App):
    def __init__(self):
        App.__init__(self)
        
        logopath = os.path.join(root_dir, 'data/logo.ico')

        self.init_canvas()
        self.init_table()

        self.load_menu()
        # self.load_menu_for_json()

        self.source()

    def source(self):
        self.manager('color').add('front', (255, 255, 255))
        self.manager('color').add('back', (0, 0, 0))


    def flatten(self, plgs, lst=None):
        if lst is None: lst = []
        if isinstance(plgs, tuple):
            if callable(plgs[1]): lst.append((plgs))
            else: self.flatten(plgs[1], lst)
        if isinstance(plgs, list):
            for i in plgs: self.flatten(i, lst)
        return lst

    def load_menu(self):
        lang = ConfigManager.get('language')
        ls = DictManager.gets(tag=lang)
        short = ShortcutManager.gets()

        plgs, errplg = load_plugins()
        self.plugin_manager.remove()       
        for name, plg in self.flatten(plgs): 
            self.add_plugin(name, plg, 'plugin')
        # print(plgs)
        return plgs

    def load_menu_for_json(self):
        lang = ConfigManager.get('language')
        ls = DictManager.gets(tag=lang)
        short = ShortcutManager.gets()

        plgs, errplg = load_plugins_for_json()

        return plgs

    def load_tool(self, data, default=None):
        lang = ConfigManager.get('language')
        ls = DictManager.gets(tag=lang)
        dic = dict([(i,j[i]) for i,j,_ in ls])
        for i, (name, tols) in enumerate(data[1]):
            name = dic[name] if name in dic else name
        default = dic[default] if default in dic else default

    def load_widget(self, data):
        pass
        
    def init_canvas(self):
        pass

    def init_table(self):
        pass

    def add_task(self, task):
        self.task_manager.add(task.title, task)
        tasks = self.task_manager.gets()
        tasks = [(p.title, lambda t=p:p.prgs) for n,p,t in tasks]
        # self.pro_bar.SetValue(tasks)

    def remove_task(self, task):
        self.task_manager.remove(obj=task)
        tasks = self.task_manager.gets()
        tasks = [(p.title, lambda t=p:p.prgs) for n,p,t in tasks]
        # self.pro_bar.SetValue(tasks)

    def alert(self, cont, title='ImagePy'):
        raise Exception(cont)

    def show_para(self, title, para, view, on_handle=None, on_ok=None, 
        on_cancel=None, on_help=None, preview=False, modal=True):
        for i in view:
            if i[0]==str: para[i[1]] = input(i[2]+': ? '+i[3]+' <str> ')
            if i[0]==int: para[i[1]] = int(input(i[4]+': ? '+i[5]+' <int> '))
            if i[0]==float: para[i[1]] = float(input(i[4]+': ? '+i[5]+' <float> '))
            if i[0]=='slide': para[i[1]] = float(input(i[4]+': ? <float> '))
            if i[0]==bool: para[i[1]] = bool(input(i[2]+': <True/False> '))
            if i[0]==list: para[i[1]] = i[3](input('%s %s: %s'%(i[4],i[5],i[2])+' <single choice> '))
            if i[0]=='chos':para[i[1]] = input('%s:%s <multi choices> '%(i[3],i[2])).split(',')
            if i[0]=='color': para[i[1]] = eval(input(i[2]+': ? '+i[3]+' <rgb> '))
        return para

    def translate(self, dic):
        dic = dic or {}
        if isinstance(dic, list):
            dic = dict(j for i in dic for j in i.items())
        def lang(x): return dic[x] if x in dic else x
        def trans(frame):
            if hasattr(frame, 'GetChildren'):
                for i in frame.GetChildren(): trans(i)
            if isinstance(frame, wx.MenuBar):
                for i in frame.GetMenus(): trans(i[0])
                for i in range(frame.GetMenuCount()):
                    frame.SetMenuLabel(i, lang(frame.GetMenuLabel(i)))
                return 'not set title'
            if isinstance(frame, wx.Menu):
                for i in frame.GetMenuItems(): trans(i)
                return 'not set title'
            if isinstance(frame, wx.MenuItem):
                frame.SetItemLabel(lang(frame.GetItemLabel()))
                trans(frame.GetSubMenu())
            if isinstance(frame, wx.Button):
                frame.SetLabel(lang(frame.GetLabel()))
            if isinstance(frame, wx.CheckBox):
                frame.SetLabel(lang(frame.GetLabel()))
            if isinstance(frame, wx.StaticText):
                frame.SetLabel(lang(frame.GetLabel()))
            if hasattr(frame, 'SetTitle'):
                frame.SetTitle(lang(frame.GetTitle()))
            if isinstance(frame, wx.MessageDialog):
                frame.SetMessage(lang(frame.GetMessage()))
            if hasattr(frame, 'SetPageText'):
                for i in range(frame.GetPageCount()):
                    frame.SetPageText(i, lang(frame.GetPageText(i)))
            if hasattr(frame, 'Layout'): frame.Layout()
        return trans

if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    app = wx.App(False)
    frame = ImagePy(None)
    frame.Show()
    frame.show_img([np.zeros((512, 512), dtype=np.uint8)], 'zeros')
    #frame.show_img(None)
    frame.show_table(pd.DataFrame(np.arange(100).reshape((10,10))), 'title')
    '''
    frame.show_md('abcdefg', 'md')
    frame.show_md('ddddddd', 'md')
    frame.show_txt('abcdefg', 'txt')
    frame.show_txt('ddddddd', 'txt')
    '''
    app.MainLoop()
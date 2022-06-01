import wx,os,sys
from skimage.io import imread

from urllib.request import urlopen
from io import BytesIO as StringIO

from sciapp.action import Free
from sciapp.action import dataio


class OpenFile(dataio.Reader):
    title = 'Open'

    def load(self):
        self.filt = [i for i in sorted(dataio.ReaderManager.names())]
        return True

class OpenUrl(Free):
    title = 'Open Url'
    # para = {'url':'http://data.imagepy.org/testdata/yxdragon.jpg'}
    # view = [('lab', None, 'Input the URL, eg. http://data.imagepy.org/testdata/yxdragon.jpg'),
    #         (str, 'url', 'Url', '')]

    para = {'name':'yxdragon', 'age':10, 'h':1.72, 'w':70, 'sport':True, 'sys':'Mac', 'lan':['C/C++', 'Python'], 'c':(255,0,0), 'path': ' '}

    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'),
            (int, 'age', (0,150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 2.5), 2, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight','kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows','Mac','Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++','Java','Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like'),
            ('path', 'path', 'Select the image', ['jpg', 'jpeg', 'png'])]
    
    def run(self, para = None):
        try:
            fp, fn = os.path.split(para['url'])
            fn, fe = os.path.splitext(fn) 
            response = urlopen(para['url'])
            ## TODO: Fixme!
            stream = StringIO(response.read())
            img = imread(stream)
            self.app.show_img([img], fn)
        except Exception as e:
            print(self.app)
            self.app.show_txt('Open url failed!\tErrof:%s'%sys.exc_info()[1])
        
plgs = [OpenFile, OpenUrl]
    
if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()
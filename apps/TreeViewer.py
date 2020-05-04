from core import Window
import imgui
import os


class TreeViewer(Window):

    def __init__(self, path='./'):
        self.cwd = path
        self.path = None
        # self.updateG()
        super(TreeViewer, self).__init__()

    def render(self, *args):
        imgui.columns(2, 'fileLlist')
        imgui.separator()

        pathlist = os.listdir(os.curdir)
        pathlist.insert(0, os.pardir)
        pathlist.insert(0, os.curdir)
        length = len(pathlist)
        selected = [False] * length
        for i in range(length):
            _, selected[i] = imgui.selectable(pathlist[i], selected[i])
            imgui.next_column()
            size = os.path.getsize(pathlist[i])
            imgui.text(str(size)+' byte')
            imgui.next_column()
            if(selected[i] is True):
                self.path = os.path.abspath(pathlist[i])
                print('clicked ' + pathlist[i])
                if os.path.isdir(self.path):
                    os.chdir(self.path)
                    break

        imgui.next_column()

        imgui.columns(1)
        return {'path': self.path}

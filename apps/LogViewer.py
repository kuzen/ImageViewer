from core import Window
import imgui


class LogViewer(Window):
    def __init__(self):
        self.info = {}
        super(LogViewer, self).__init__()

    def render(self, *args):
        if 'fileInfo' in args[0][0][0]:
            self.info = args[0][0][0]['fileInfo'][0]
        imgui.columns(2, 'info')
        imgui.separator()
        for name in self.info:
            imgui.text(name)
            imgui.next_column()
            imgui.text(self.info[name])
            imgui.next_column()
        imgui.columns(1)
        return {}

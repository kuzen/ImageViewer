"""Misc apps that are too small to need their own file
"""
import imgui
from core import Window


class DemoWindow(Window):
    def _render(self):
        if not imgui.show_demo_window(True):
            # windowClosed.send(self)

# class MetricsWindow(Window):
#     def _render(self):
#         if not imgui.show_metrics_window(True): windowClosed.send(self)


class about(Window):
    def render(self, *args):
        imgui.text('Chen Sijie')
        imgui.text('GDUT')
        return {}

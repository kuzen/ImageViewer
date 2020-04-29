from core import Window, alerts, Widget
import imgui
from utils import singleton


@singleton
class ExceptionAlert(Widget):
    def __init__(self, exception, traceinfo):
        self.exception = exception
        self.traceinfo = traceinfo

    def render(self):
        expanded, visible = imgui.collapsing_header(self.exception)
        if expanded:
            imgui.text(self.traceinfo)

    def __str__(self):
        return self.exception


def render_alert(alertItem):
    alert, count = alertItem
    imgui.text(str(count))
    imgui.next_column()
    alert.render()
    imgui.next_column()
    imgui.separator()


class AlertViewer(Window):

    def render(self):
        imgui.columns(2, 'alertList')
        imgui.set_column_offset(1, 45)
        imgui.text("Count")
        imgui.next_column()
        imgui.text("Alert")
        imgui.next_column()
        imgui.separator()
        # ToDo: In the future dont revert this, and simple have it lock scroll
        # to bottom like a terminal? Might be more effort than it's worth.
        list(map(render_alert, reversed(alerts.items())))
        imgui.text("Count")
        imgui.next_column()
        imgui.text("Alert")
        imgui.next_column()
        imgui.columns(1)

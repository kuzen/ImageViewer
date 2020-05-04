from collections import Counter, OrderedDict

import glfw
import OpenGL.GL as gl
import operator
import imgui
import collections
import blinker

windowClosed = blinker.signal("windowClosed")


def render_all(iterable, *args):
    """Quickly calls the _render method on an iterable
    of renderables.
    """
    ret = map(operator.methodcaller('_render', args), iterable)
    # print(collections.deque(ret))

    retLists = list(ret)
    # print(retLists)
    result = collections.defaultdict(list)

    # convert to dict
    for i in range(len(retLists)):
        for name, value in retLists[i].items():
            result[name].append(value)
    return dict(result)


class Desktop:
    def __init__(self):
        self.running = set()
        self.to_add = set()
        self.to_remove = set()
        self.pubData = None
        windowClosed.connect(self.remove)

    def render(self):
        # We need to batch all changes to the beggining of the
        # render call, or the iterables size can change mid-stream
        if self.to_remove:
            self.running.difference_update(self.to_remove)
            self.to_remove.clear()
        if self.to_add:
            self.running.update(self.to_add)
            self.to_add.clear()
        self.pubData = render_all(self.running, self.pubData)

    def add(self, item):
        self.to_add.add(item)

    def remove(self, item):
        self.to_remove.add(item)


# class Widget:
#     def __init__(self):
#         pass

#     @property
#     def tickrate(self): return getattr(self, "_tickrate", None)

#     @tickrate.setter
#     def tickrate(self, tickrate):
#         # ToDo, this holds a reference to closed windows
#         self._tickrate = tickrate
#         pyglet.clock.unschedule(self.update)
#         if tickrate is None:
#             return
#         if type(tickrate) == bool and tickrate:
#             pyglet.clock.schedule_interval(self.update)
#             return
#         pyglet.clock.schedule_interval(self.update, tickrate)

#     def _render(self, *args):
#         return self.render(args)

#     def render(self):
#         pass

#     def update(self, dt):
#         pass


windowCount = collections.Counter()


class Window():
    # Set to false if you want the app not to show up in app the "start menu".
    inAppMenu = True

    def __init__(self):
        # Get a unique name for this window
        self.name = getattr(self, 'name', self.__class__.__name__)
        self._id = windowCount[self.name]
        self._idStr = "{}: {}".format(self._id, self.name)
        windowCount.update((self.name,))
        super().__init__()

    def __enter__(self):
        expanded, opened = imgui.begin(self._idStr, closable=True)
        if not opened:
            windowClosed.send(self)
        return expanded

    def __exit__(self, type, value, traceback):
        imgui.end()

    def _render(self, *args):
        with self as running:
            if running:
                ret = self.render(args)
        # print(ret)
        return ret


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "IMG Viewer"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


ignoredAlerts = set()


class OrderedAlertCounter(Counter, OrderedDict):
    pass


alerts = OrderedAlertCounter()


# class GenericPythonWidget(Widget, wrapt.ObjectProxy):
#     def render(self):
#         imgui.text(str(self))

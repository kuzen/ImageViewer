# -*- coding: utf-8 -*-
from __future__ import absolute_import

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
import core
import OpenGL.GL as gl
from core import Desktop
from plugins import get_app_list


def main():
    desktop = Desktop()
    imgui.create_context()
    window = core.impl_glfw_init()
    impl = GlfwRenderer(window)
    imgui.core.style_colors_light()

    app_list = list(get_app_list())
    # figure = plt.figure()
    # img = Image.open('./test.png')
    # texture, width, height = readImage(img)

    def update():
        imgui.new_frame()
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("System", True):
                for app in app_list:
                    clicked, selected = imgui.menu_item(
                        app.__name__, '', False, True)
                    if clicked:
                        desktop.add(app())
                imgui.separator()
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", '', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        desktop.render()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        update()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        data = imgui.get_draw_data()
        impl.render(data)

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        pass

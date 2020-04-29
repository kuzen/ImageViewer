"""
Semantic theme/colors.

The basic idea is that when you want a color/attribute you pass a list of possible
theme variable names. For example, a map application could do something like

waterC = theme.color("myApp_lake","lake","water","blue") or (0.5,0.5,0.8,1)
"""

import functools

class ColorDict(dict):
    def color(self, *args):
        """Supply it with a list of color names, it will
        return the first color that matches your name, trying each
        fallback in order. If it can't find any color, returns None.
        """
        return next((self[item] for item in args if item in self), None)

theme = ColorDict(**{
    'primary': (0.0,0.1,0.7,1),
    'secondary': (0.7,0.1,0,1),
    'success': (0.4,0.9,0.2,1),
    'warning': (0.85,0.8,0.2,1),
    'danger': (0.9,0.2,0,1),
    'info': (0.0,0.75,0.9,1),
})
#Have opinions on this default color scheme? I don't! Do a pull request.

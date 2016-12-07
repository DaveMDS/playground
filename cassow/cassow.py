#!/usr/bin/env python3
# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

# import os
# import sys
from cassowary import SimplexSolver, Variable, WEAK, STRONG

from efl import evas
# from efl import ecore
# from efl import edje
from efl import elementary as elm

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, EXPAND_BOTH, FILL_BOTH


# setup efl logging
import logging
logger = logging.getLogger('efl')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

solver = None
win = None

class Point(object):
    def __init__(self, canvas, identifier, x, y, color):
        self.x = Variable('x' + identifier, x)
        self.y = Variable('y' + identifier, y)
        self.r = evas.Rectangle(canvas, size=(10, 10), color=color)
        self.r.on_mouse_down_add(self._on_mouse_down)
        self.r.on_mouse_up_add(self._on_mouse_up)
        self.r.show()

    def __repr__(self):
        return u'(%s, %s)' % (self.x.value, self.y.value)

    def update(self):
        self.r.pos = self.x.value - 5, self.y.value - 5

    def _on_mouse_down(self, obj, event):
        print(event)
        solver.add_edit_var(self.x)
        solver.add_edit_var(self.y)
        obj.on_mouse_move_add(self._on_mouse_move)

    def _on_mouse_up(self, obj, event):
        print(event)
        solver.remove_edit_var(self.x)
        solver.remove_edit_var(self.y)
        obj.on_mouse_move_del(self._on_mouse_move)

    def _on_mouse_move(self, obj, event):
        # print(dir(event))#.output)
        print(event.position)

        # with solver.edit():
            # solver.suggest_value(self.x, event.position.canvas.x)
            # solver.suggest_value(self.y, event.position.canvas.y)

        solver.begin_edit()
        solver.suggest_value(self.x, event.position.canvas.x)
        solver.suggest_value(self.y, event.position.canvas.y)
        solver.resolve()

        win.update_all_points()

class Icon(object):
    def __init__(self, parent, identifier, standard):
        self.x = Variable('x' + identifier)
        self.y = Variable('y' + identifier)
        self.w = Variable('w' + identifier)
        self.icon = elm.Icon(parent, standard=standard)
        self.icon.show()

    def update(self):
        w2 = self.w.value / 2
        self.icon.pos = self.x.value - w2, self.y.value - w2
        # self.icon.pos = self.x.value, self.y.value
        # self.icon.size = w2, w2
        self.icon.size = self.w.value, self.w.value

class CassoWin(elm.StandardWindow):
    def __init__(self, app):
        self.app = app

        elm.StandardWindow.__init__(self, 'CassoW', 'CassoW',
                                    size=(500, 500), autodel=True)
        self.callback_delete_request_add(lambda o: elm.exit())

        # ly = Layout(self, file=(args.theme, 'pigreco/layout'))
        # ly.signal_callback_add('autoscroll,toggle', '',
                               # lambda a,s,d: self.autoscroll_toggle())
        # self.resize_object_add(ly)
        # ly.show()

        self.show()


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        global solver
        global win

        win = self
        solver = SimplexSolver()

        # ICON
        icon = Icon(self, 'icon0', 'user-home')
        self.icon = icon

        # LINES
        self.lines = [
            evas.Line(self.evas, anti_alias=True, pass_events=True),
            evas.Line(self.evas, anti_alias=True, pass_events=True),
            evas.Line(self.evas, anti_alias=True, pass_events=True),
            evas.Line(self.evas, anti_alias=True, pass_events=True),
            evas.Line(self.evas, color=(51, 153, 255, 255), anti_alias=True, pass_events=True),
            evas.Line(self.evas, color=(51, 153, 255, 255), anti_alias=True, pass_events=True),
            evas.Line(self.evas, color=(51, 153, 255, 255), anti_alias=True, pass_events=True),
            evas.Line(self.evas, color=(51, 153, 255, 255), anti_alias=True, pass_events=True),
        ]
        for l in self.lines:
            l.show()

        # POINTS
        points = [
            Point(self.evas, '0', 10, 10, color=(255, 0, 0, 255)),
            Point(self.evas, '1', 10, 200, color=(255, 0, 0, 255)),
            Point(self.evas, '2', 200, 200, color=(255, 0, 0, 255)),
            Point(self.evas, '3', 200, 10, color=(255, 0, 0, 255)),
            Point(self.evas, 'm0', 0, 0, color=(0, 255, 0, 255)),
            Point(self.evas, 'm1', 0, 0, color=(0, 255, 0, 255)),
            Point(self.evas, 'm2', 0, 0, color=(0, 255, 0, 255)),
            Point(self.evas, 'm3', 0, 0, color=(0, 255, 0, 255)),
        ]
        midpoints = points[4:]


        # "stay" for the 4 corners (WEAK)
        weight = 1.0
        multiplier = 2.0
        for point in points[:4]:
            solver.add_stay(point.x, strength=WEAK, weight=weight)
            solver.add_stay(point.y, strength=WEAK, weight=weight)
            weight = weight * multiplier

        # constrain for the 4 centers (REQUIRED)
        for start, end in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            cle = (points[start].x + points[end].x) / 2
            cleq = midpoints[start].x == cle
            solver.add_constraint(cleq)

            cle = (points[start].y + points[end].y) / 2
            cleq = midpoints[start].y == cle
            solver.add_constraint(cleq)

        # more constrains
        solver.add_constraint(points[0].x + 20 <= points[2].x)
        solver.add_constraint(points[0].x + 20 <= points[3].x)

        solver.add_constraint(points[1].x + 20 <= points[2].x)
        solver.add_constraint(points[1].x + 20 <= points[3].x)

        solver.add_constraint(points[0].y + 20 <= points[1].y)
        solver.add_constraint(points[0].y + 20 <= points[2].y)

        solver.add_constraint(points[3].y + 20 <= points[1].y)
        solver.add_constraint(points[3].y + 20 <= points[2].y)

        # stay in canvas
        for point in points:
            solver.add_constraint(point.x >= 10)
            solver.add_constraint(point.y >= 10)

            solver.add_constraint(point.x <= 490)
            solver.add_constraint(point.y <= 490)


        self.points = points


        # ICON constrains
        solver.add_constraint(icon.x == (points[4].x + points[6].x) / 2)
        solver.add_constraint(icon.y == (points[5].y + points[7].y) / 2)
        solver.add_constraint(icon.w == (points[6].x - points[4].x) / 2)


        # MORE POINTS
        anchor = icon
        for i in range(20):
            p = Point(self.evas, 'm'+str(i), 0, 0, color=(50, 0, 0, 50))
            solver.add_constraint(p.x - 3 == anchor.x)
            solver.add_constraint(p.y - 3 == anchor.y)

            self.points.append(p)
            anchor = p


        self.update_all_points()
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def update_all_points(self):
        for p in self.points:
            p.update()

        self.icon.update()

        # line 1 (left)
        self.lines[0].xy = \
            self.points[0].x.value, self.points[0].y.value, \
            self.points[1].x.value, self.points[1].y.value

        # line 2 (bottom)
        self.lines[1].xy = \
            self.points[1].x.value, self.points[1].y.value, \
            self.points[2].x.value, self.points[2].y.value

        # line 3 (right)
        self.lines[2].xy = \
            self.points[2].x.value, self.points[2].y.value, \
            self.points[3].x.value, self.points[3].y.value

        # line 4 (top)
        self.lines[3].xy = \
            self.points[3].x.value, self.points[3].y.value, \
            self.points[0].x.value, self.points[0].y.value

        # line 1b ()
        self.lines[4].xy = \
            self.points[4].x.value, self.points[4].y.value, \
            self.points[5].x.value, self.points[5].y.value

        # line 2b ()
        self.lines[5].xy = \
            self.points[5].x.value, self.points[5].y.value, \
            self.points[6].x.value, self.points[6].y.value

        # line 3b ()
        self.lines[6].xy = \
            self.points[6].x.value, self.points[6].y.value, \
            self.points[7].x.value, self.points[7].y.value

        # line 4b ()
        self.lines[7].xy = \
            self.points[7].x.value, self.points[7].y.value, \
            self.points[4].x.value, self.points[4].y.value




class CassoApp(object):
    def __init__(self):

        self.win = CassoWin(self)

        elm.run()

        
if __name__ == '__main__':
    CassoApp()

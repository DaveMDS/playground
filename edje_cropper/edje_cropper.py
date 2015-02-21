#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

from efl import elementary
from efl.elementary.photocam import Photocam
from efl.elementary.window import StandardWindow
from efl.elementary.scroller import Scrollable

from efl.ecore import Animator, ECORE_CALLBACK_RENEW
from efl.edje import Edje
from efl.evas import Rectangle, EXPAND_BOTH, EVAS_CALLBACK_MOUSE_WHEEL, \
    EVAS_EVENT_FLAG_ON_HOLD


SHADER_COLOR = (0, 0, 0, 100)

def clamp(low, val, high):
    if val < low: return low
    if val > high: return high
    return val

class ScrollablePhotocam(Photocam, Scrollable):
    def __init__(self, *args, **kargs):
        Photocam.__init__(self, paused=True, *args, **kargs)
        self.on_mouse_wheel_add(self._on_mouse_wheel)
        self.on_mouse_down_add(self._on_mouse_down)
        self.on_mouse_up_add(self._on_mouse_up)

    # mouse wheel: zoom
    def _on_mouse_wheel(self, obj, event):
        event.event_flags |= EVAS_EVENT_FLAG_ON_HOLD
        obj.zoom *= 1.1 if event.z == 1 else 0.9

    # mouse drag: pan
    def _on_mouse_down(self, obj, event):
        self._drag_start_region = obj.region
        self._drag_start_x, self._drag_start_y = event.position.canvas
        obj.on_mouse_move_add(self._on_mouse_move)

    def _on_mouse_up(self, obj, event):
        obj.on_mouse_move_del(self._on_mouse_move)

    def _on_mouse_move(self, obj, event):
        x, y = event.position.canvas
        dx, dy = self._drag_start_x - x, self._drag_start_y - y
        x, y, w, h = self._drag_start_region
        obj.region_show(x + dx, y + dy, w, h)

    # region selector stuff
    def region_selector_show(self):
        self.sel = Edje(self.evas, file='theme.edj', group='sel')
        self.sel.data['rel1'] = (0.2, 0.2)
        self.sel.data['rel2'] = (0.8, 0.8)
        self.sel.show()

        self.sel_shader1 = Rectangle(self.evas, color=SHADER_COLOR, pass_events=True)
        self.sel_shader1.show()
        self.sel_shader2 = Rectangle(self.evas, color=SHADER_COLOR, pass_events=True)
        self.sel_shader2.show()
        self.sel_shader3 = Rectangle(self.evas, color=SHADER_COLOR, pass_events=True)
        self.sel_shader3.show()
        self.sel_shader4 = Rectangle(self.evas, color=SHADER_COLOR, pass_events=True)
        self.sel_shader4.show()

        self.internal_image.on_move_add(self._internal_on_move_resize)
        self.internal_image.on_resize_add(self._internal_on_move_resize)
        self._internal_on_move_resize(self.internal_image)

        for part in ('h1','h2','h3','h4','h5','h6','h7','h8','hm'):
            h = self.sel.part_object_get(part)
            h.on_mouse_down_add(self._on_handler_mouse_down, part)
            h.on_mouse_up_add(self._on_handler_mouse_up, part)

    def _internal_on_move_resize(self, obj):
        self._update_selection()

    def _update_selection(self):
        px, py, pw, ph = self.internal_image.geometry

        rel1x, rel1y = self.sel.data['rel1']
        rel2x, rel2y = self.sel.data['rel2']
        x1 = int((pw * rel1x) + px)
        y1 = int((ph * rel1y) + py)
        x2 = int((pw * rel2x) + px)
        y2 = int((ph * rel2y) + py)

        # selection geometry
        sx, sy, sw, sh = x1, y1, x2-x1, y2-y1
        self.sel.move(sx, sy)
        self.sel.resize(sw, sh)

        # shaders geometry
        self.sel_shader1.move(px, py)
        self.sel_shader1.resize(pw, sy - py)
        self.sel_shader2.move(px, sy + sh)
        self.sel_shader2.resize(pw, (py + ph) - (sy + sh))
        self.sel_shader3.move(px, sy)
        self.sel_shader3.resize(sx - px, sh)
        self.sel_shader4.move(sx + sw, sy)
        self.sel_shader4.resize((px + pw) - (sx + sw), sh)

    def _on_handler_mouse_down(self, obj, event, part):
        self._drag_start_x, self._drag_start_y = event.position.canvas
        self._drag_start_geom = self.sel.geometry
        self._drag_animator = Animator(self._drag_animator_cb, obj, part)

    def _on_handler_mouse_up(self, obj, event, part):
        self._drag_animator.delete()

    def _drag_animator_cb(self, obj, part):
        x, y = obj.evas.pointer_canvas_xy_get()
        dx, dy = x - self._drag_start_x, y - self._drag_start_y
        x, y, w, h = self._drag_start_geom
        px, py, pw, ph = self.internal_image.geometry

        # calc new selection gemetry
        if part == 'hm':
            x, y = x + dx, y + dy
        elif part == 'h1':
            x, y = x + dx, y + dy
            w, h = w - dx, h - dy
        elif part == 'h2':
            y = y + dy
            h = h - dy
        elif part == 'h3':
            y = y + dy
            w, h = w + dx, h - dy
        elif part == 'h4':
            w = w + dx
        elif part == 'h5':
            w, h = w + dx, h + dy
        elif part == 'h6':
            h = h + dy
        elif part == 'h7':
            x, y = x + dx, y
            w, h = w - dx, h + dy
        elif part == 'h8':
            x = x + dx
            w = w - dx

        # calc relative pos
        rel1x = float(x - px) / pw
        rel1y = float(y - py) / ph
        rel2x = float(x + w - px) / pw
        rel2y = float(y + h - py) / ph

        # constrain inside photo geometry
        rel1x = clamp(0.0, rel1x, 1.0)
        rel1y = clamp(0.0, rel1y, 1.0)
        rel2x = clamp(0.0, rel2x, 1.0)
        rel2y = clamp(0.0, rel2y, 1.0)

        # update
        self.sel.data['rel1'] = (rel1x, rel1y)
        self.sel.data['rel2'] = (rel2x, rel2y)
        self._update_selection()

        return ECORE_CALLBACK_RENEW

class MainWin(StandardWindow):
    def __init__(self):
        StandardWindow.__init__(self, 'edje_cropper', 'Edje Cropper',
                                autodel=True, size=(800,600))
        self.callback_delete_request_add(lambda o: elementary.exit())

        img = ScrollablePhotocam(self, file='photo.jpg')
        img.callback_clicked_double_add(self._img_clicked_cb)
        self.resize_object_add(img)
        img.show()

        self.show()

    def _img_clicked_cb(self, img):
        img.region_selector_show()


if __name__ == '__main__':
    elementary.init()
    MainWin()
    elementary.run()
    elementary.shutdown()

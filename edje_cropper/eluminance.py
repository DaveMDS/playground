#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import os
import re

from efl.evas import EXPAND_BOTH, EXPAND_HORIZ, FILL_BOTH, FILL_HORIZ, \
    EVAS_EVENT_FLAG_ON_HOLD
from efl.edje import Edje

from efl import elementary
from efl.elementary.button import Button
from efl.elementary.background import Background
from efl.elementary.box import Box
from efl.elementary.label import Label
from efl.elementary.menu import Menu
from efl.elementary.thumb import Thumb
from efl.elementary.toolbar import Toolbar
from efl.elementary.photocam import Photocam, ELM_PHOTOCAM_ZOOM_MODE_AUTO_FIT, \
    ELM_PHOTOCAM_ZOOM_MODE_AUTO_FILL, ELM_PHOTOCAM_ZOOM_MODE_AUTO_FIT_IN, \
    ELM_PHOTOCAM_ZOOM_MODE_MANUAL
from efl.elementary.window import StandardWindow
from efl.elementary.scroller import Scrollable
from efl.elementary.panes import Panes
from efl.elementary.genlist import Genlist, GenlistItemClass, \
    ELM_GENLIST_ITEM_TREE
from efl.elementary.gengrid import Gengrid, GengridItemClass, \
    ELM_OBJECT_SELECT_MODE_ALWAYS
from efl.elementary.icon import Icon
from efl.elementary.notify import Notify
from efl.elementary.hoversel import Hoversel
from efl.elementary.image import Image
from efl.elementary.spinner import Spinner
from efl.elementary.slideshow import Slideshow, SlideshowItemClass


IMG_EXTS = ('.jpg', '.jpeg', '.png')
THEME_FILE = os.path.abspath('theme.edj')

def clamp(low, val, high):
    if val < low: return low
    if val > high: return high
    return val

def file_hum_size(file_path):
    bytes = float(os.path.getsize(file_path))
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.1fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.1fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.1fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.1fK' % kilobytes
    else:
        size = '%.1fb' % bytes
    return size

def natural_sort(l): 
   convert = lambda text: int(text) if text.isdigit() else text.lower() 
   alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
   return sorted(l, key=alphanum_key)


class StdButton(Button):
    """ A Button with a standard fdo icon """
    def __init__(self, parent, icon, *args, **kargs):
        Button.__init__(self, parent, *args, **kargs)
        # self.content = Icon(self, standard=icon, resizable=(False, False))
        self.icon = icon
        self.show()

    @property
    def icon(self):
        return self.content

    @icon.setter
    def icon(self, name):
        self.content = Icon(self, standard=name, resizable=(False, False))


class TreeView(Genlist):
    def __init__(self, app, *args, **kargs):
        self.app = app

        Genlist.__init__(self, *args, **kargs)
        self.callback_selected_add(self._item_selected_cb)
        self.callback_expand_request_add(self._item_expand_request_cb)
        self.callback_expanded_add(self._item_expanded_cb)
        self.callback_contract_request_add(self._item_contract_request_cb)
        self.callback_contracted_add(self._item_contracted_cb)
        self.callback_clicked_double_add(self._item_expand_request_cb)

        self.itc = GenlistItemClass('one_icon',
                                    text_get_func=self._gl_text_get,
                                    content_get_func=self._gl_content_get)

    def _gl_text_get(self, gl, part, item_data):
        return os.path.basename(item_data)

    def _gl_content_get(self, gl, part, item_data):
        return Icon(gl, standard='folder')

    def _item_selected_cb(self, gl, item):
        self.app.grid.populate(item.data)
        self.app.status.update()

    def _item_expand_request_cb(self, gl, item):
        item.expanded = True

    def _item_expanded_cb(self, gl, item):
        self.populate(item.data, item)

    def _item_contract_request_cb(self, gl, item):
        item.expanded = False

    def _item_contracted_cb(self, gl, item):
        item.subitems_clear()
        
    def populate(self, path, parent=None):
        for f in natural_sort(os.listdir(path)):
            if f[0] == '.': continue
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                self.item_append(self.itc, fullpath, parent,
                                 flags=ELM_GENLIST_ITEM_TREE)


class PhotoGrid(Gengrid):
    def __init__(self, app, parent):
        self.app = app

        Gengrid.__init__(self, parent, select_mode=ELM_OBJECT_SELECT_MODE_ALWAYS,
                         item_size=(128, 128), align=(0.5, 0.0))
        self.callback_selected_add(self._item_selected_cb)

        self.itc = GengridItemClass('default',
                                    text_get_func=self._gg_text_get,
                                    content_get_func=self._gg_content_get)

    def _gg_content_get(self, gg, part, item_data):
        if part == 'elm.swallow.icon':
            return Thumb(gg, file=item_data)

    def _gg_text_get(self, gg, part, item_data):
        return os.path.basename(item_data)

    def _item_selected_cb(self, gg, item):
        self.app.photo.file_set(item.data)
        self.app.status.update()

    def populate(self, path):
        self.clear()
        for f in natural_sort(os.listdir(path)):
            if os.path.splitext(f)[-1].lower() in IMG_EXTS:
                self.item_append(self.itc, os.path.join(path, f))
        if self.first_item:
            self.first_item.selected = True
            self.first_item.show()

    def next_select(self):
        it = self.selected_item or self.first_item
        if it: it = it.next
        if it: it.selected = True

    def prev_select(self):
        it = self.selected_item or self.last_item
        if it: it = it.prev
        if it: it.selected = True


class ScrollablePhotocam(Photocam, Scrollable):
    def __init__(self, app, *args, **kargs):
        self.app = app
        Photocam.__init__(self, paused=True,
                          zoom_mode=ELM_PHOTOCAM_ZOOM_MODE_AUTO_FIT,
                          *args, **kargs)
        self.on_mouse_wheel_add(self._on_mouse_wheel)
        self.on_mouse_down_add(self._on_mouse_down)
        self.on_mouse_up_add(self._on_mouse_up)
        self.on_del_add(self._on_del)
        self._drag_start_geom = None
        self.sel = None

    def file_set(self, file):
        self.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_AUTO_FIT
        Photocam.file_set(self, file)

    def _on_del(self, obj):
        if self.sel: self.sel.delete()

    # mouse wheel: zoom
    def _on_mouse_wheel(self, obj, event):
        event.event_flags |= EVAS_EVENT_FLAG_ON_HOLD
        self.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_MANUAL
        obj.zoom *= 1.1 if event.z == 1 else 0.9

    # mouse drag: pan
    def _on_mouse_down(self, obj, event):
        self._drag_start_region = obj.region
        self._drag_start_x, self._drag_start_y = event.position.canvas
        obj.on_mouse_move_add(self._on_mouse_move)

    def _on_mouse_up(self, obj, event):
        obj.on_mouse_move_del(self._on_mouse_move)

    def _on_mouse_move(self, obj, event):
        if self._drag_start_geom is None:
            x, y = event.position.canvas
            dx, dy = self._drag_start_x - x, self._drag_start_y - y
            x, y, w, h = self._drag_start_region
            obj.region_show(x + dx, y + dy, w, h)

    # region selector stuff
    def region_selector_show(self):
        self.sel = Edje(self.evas, file=THEME_FILE, group='sel')
        self.sel.show()

        internal = self.internal_image
        internal.on_move_add(self._internal_on_move_resize)
        internal.on_resize_add(self._internal_on_move_resize)
        self._internal_on_move_resize(internal)

        for part in ('h1','h2','h3','h4','h5','h6','h7','h8','hm'):
            h = self.sel.part_object_get(part)
            h.on_mouse_down_add(self._on_handler_mouse_down, part)
            h.on_mouse_up_add(self._on_handler_mouse_up, part)

    def _internal_on_move_resize(self, obj):
        self.sel.geometry = obj.geometry

    def _on_handler_mouse_down(self, obj, event, part):
        self._drag_start_x, self._drag_start_y = event.position.canvas
        self._drag_start_geom = self.sel.part_object_get('selector').geometry
        obj.on_mouse_move_add(self._on_handler_mouse_move, part)

    def _on_handler_mouse_up(self, obj, event, part):
        obj.on_mouse_move_del(self._on_handler_mouse_move)
        self._drag_start_geom = None

    def _on_handler_mouse_move(self, obj, event, part):
        x, y = event.position.canvas
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

        w, h = max(50, w), max(50, h)

        # calc new relative pos
        rel1x = float(x - px) / pw
        rel1y = float(y - py) / ph
        rel2x = float(x + w - px) / pw
        rel2y = float(y + h - py) / ph

        # constrain inside photo geometry
        rel1x = clamp(0.0, rel1x, 1.0)
        rel1y = clamp(0.0, rel1y, 1.0)
        rel2x = clamp(0.0, rel2x, 1.0)
        rel2y = clamp(0.0, rel2y, 1.0)

        # send signal to edje with new rels
        self.sel.message_send(1, (rel1x, rel1y, rel2x, rel2y))


class StatusBar(Box):
    def __init__(self, app, parent):
        self.app = app
        Box.__init__(self, parent, horizontal=True,
                     size_hint_expand=EXPAND_HORIZ,
                     size_hint_fill=FILL_HORIZ)

        self.lb_name = Label(self, ellipsis=True,
                            size_hint_expand=EXPAND_HORIZ,
                            size_hint_fill=FILL_HORIZ)
        self.pack_end(self.lb_name)
        self.lb_name.show()
        
        self.lb_info = Label(self)
        self.pack_end(self.lb_info)
        self.lb_info.show()

        # prev button
        bt = StdButton(self, icon='go-previous')
        bt.callback_clicked_add(lambda b: self.app.grid.prev_select())
        self.pack_end(bt)
        self.btn_prev = bt

        # next button
        bt = StdButton(self, icon='go-next')
        bt.callback_clicked_add(lambda b: self.app.grid.next_select())
        self.pack_end(bt)
        self.btn_next = bt

        # zoom button
        bt = StdButton(self, icon='zoom')
        bt.callback_clicked_add(self._zoom_btn_cb)
        self.pack_end(bt)
        self.btn_zoom = bt

        # slideshow button
        bt = StdButton(self, icon='media-playback-start')
        bt.callback_clicked_add(lambda b: SlideShow(self.app))
        self.pack_end(bt)
        self.btn_slideshow = bt

        # edit button
        bt = StdButton(self, icon='edit')
        bt.callback_clicked_add(lambda b: ImageEditor(self.app))
        self.pack_end(bt)
        self.btn_edit = bt

    def update(self):
        image_path = self.app.photo.file
        if image_path is None:
            self.btn_zoom.hide()
            self.btn_edit.hide()
            self.lb_name.text = '<align=left>{}</>'.format('No image selected')
            self.lb_info.text = ''
        else:
            self.btn_zoom.show()
            self.lb_name.text = '<align=left><b>{0}:</b> {1}</align>'.format(
                                'Name', os.path.basename(image_path))
            self.lb_info.text = \
                '    <b>{0}:</b> {1}x{2}    <b>{3}:</b> {4}    '.format(
                    'Resolution',
                    self.app.photo.image_size[0], self.app.photo.image_size[1],
                    'Size', file_hum_size(image_path)
                )
        if self.app.grid.items_count > 1:
            self.btn_next.show()
            self.btn_prev.show()
            self.btn_slideshow.show()
            self.btn_edit.show()
        else:
            self.btn_next.hide()
            self.btn_prev.hide()
            self.btn_slideshow.hide()
            self.btn_edit.hide()
    
    def _zoom_btn_cb(self, btn):
        m = Menu(self.app.main_win)
        m.item_add(None, 'Zoom In', 'zoom-in', self._zoom_set, -0.3)
        m.item_add(None, 'Zoom Out', 'zoom-out', self._zoom_set, +0.3)
        m.item_separator_add()
        m.item_add(None, 'Zoom Fit', 'zoom-fit-best', self._zoom_fit_set)
        m.item_add(None, 'Zoom Fill', 'zoom-fit-best', self._zoom_fill_set)
        m.item_add(None, 'Zoom 1:1', 'zoom-original', self._zoom_orig_set)
        m.move(*btn.pos)
        m.show()

    def _zoom_set(self, menu, item, val):
        self.app.photo.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_MANUAL
        self.app.photo.zoom += val

    def _zoom_fit_set(self, menu, item):
        self.app.photo.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_AUTO_FIT

    def _zoom_fill_set(self, menu, item):
        self.app.photo.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_AUTO_FILL

    def _zoom_orig_set(self, menu, item):
        self.app.photo.zoom_mode = ELM_PHOTOCAM_ZOOM_MODE_MANUAL
        self.app.photo.zoom = 1.0


class SlideShow(Slideshow):
    NOTIFY_TIMEOUT = 3.0
    def __init__(self, app):
        Slideshow.__init__(self, app.main_win, timeout=5.0,
                           size_hint_expand=EXPAND_BOTH)
        app.main_win.resize_object_add(self)
        self.show()

        itc = SlideshowItemClass(self._item_get_func)
        grid_item = app.grid.first_item
        while grid_item:
            self.item_add(itc, grid_item.data)
            grid_item = grid_item.next

        box = Box(self, horizontal=True)

        notify = Notify(self, align=(0.5, 1.0), content=box,
                        timeout=self.NOTIFY_TIMEOUT,
                        size_hint_expand=EXPAND_BOTH)
        notify.on_mouse_in_add(self._notify_mouse_in_cb)
        notify.on_mouse_out_add(self._notify_mouse_out_cb)
        self.on_mouse_move_add(self._sshow_mouse_move_cb, notify)

        bt = StdButton(box, icon='go-previous')
        bt.callback_clicked_add(lambda b: self.previous())
        box.pack_end(bt)

        bt = StdButton(box, icon='go-next')
        bt.callback_clicked_add(lambda b: self.next())
        box.pack_end(bt)

        hv = Hoversel(box, hover_parent=app.main_win, text=self.transitions[0])
        for t in list(self.transitions) + [None]:
            hv.item_add(t or "None", None, 0, self._transition_cb, t)
        box.pack_end(hv)
        hv.show()

        spinner = Spinner(box, label_format="%2.0f secs.", step=1,
                          min_max=(3, 60), value=3)
        spinner.callback_changed_add(lambda s: setattr(self, 'timeout', s.value))
        box.pack_end(spinner)
        spinner.show()

        bt = StdButton(box, icon='media-playback-pause', text='Pause')
        bt.callback_clicked_add(self._play_pause_cb)
        box.pack_end(bt)

        bt = StdButton(box, icon='close', text='Close')
        bt.callback_clicked_add(lambda b: self.delete())
        box.pack_end(bt)

    def _item_get_func(self, obj, file_path):
        return Image(obj, file=file_path)

    def _sshow_mouse_move_cb(self, obj, event, notify):
        notify.timeout = self.NOTIFY_TIMEOUT
        notify.show()

    def _notify_mouse_in_cb(self, notify, event):
        notify.timeout = 0.0
        notify.show()

    def _notify_mouse_out_cb(self, notify, event):
        notify.timeout = self.NOTIFY_TIMEOUT

    def _transition_cb(self, hoversel, item, transition):
        self.transition = transition
        hoversel.text = transition or "None"

    def _play_pause_cb(self, btn):
        if self.timeout == 0:
            self.timeout = 3 # TODO FIXME
            btn.text = 'Pause'
            btn.icon = 'media-playback-pause'
        else:
            self.timeout = 0
            btn.text = 'Play'
            btn.icon = 'media-playback-start'


class ImageEditor(object):
    def __init__(self, app):
        self.bg = Background(app.main_win, size_hint_expand=EXPAND_BOTH)
        app.main_win.resize_object_add(self.bg)
        self.bg.show()

        box = Box(self.bg, size_hint_expand=EXPAND_BOTH,
                  size_hint_fill=FILL_BOTH)
        app.main_win.resize_object_add(box)
        box.show()

        tb = Toolbar(app.main_win, homogeneous=True, menu_parent=app.main_win,
                     size_hint_expand=EXPAND_HORIZ,
                     size_hint_fill=FILL_HORIZ)

        item = tb.item_append('rotate', 'Rotate')
        item.menu = True
        item.menu.item_add(None, 'Rotate Right', 'object-rotate-right')
        item.menu.item_add(None, 'Rotate Left', 'object-rotate-left')
        item.menu.item_add(None, 'Mirror', 'object-flip-horizontal')
        item.menu.item_add(None, 'Flip', 'object-flip-vertical')

        tb.item_append('edit-cut', 'Crop', self._crop_item_cb)
        tb.item_append('resize', 'Resize')

        sep = tb.item_append(None, None)
        sep.separator = True

        tb.item_append('document-save', 'Save')
        tb.item_append('document-save-as', 'Save as')
        tb.item_append('document-close', 'Close', self._close_item_cb)

        box.pack_end(tb)
        tb.show()

        self.photo = ScrollablePhotocam(app, box, file=app.photo.file,
                                        size_hint_expand=EXPAND_BOTH,
                                        size_hint_fill=FILL_BOTH)
        box.pack_end(self.photo)
        self.photo.show()

    def _crop_item_cb(self, tb, item):
        self.photo.region_selector_show()

    def _close_item_cb(self, tb, item):
        self.bg.delete()


class MainWin(StandardWindow):
    def __init__(self, app):
        self.app = app
        StandardWindow.__init__(self, 'edje_cropper', 'eluminance',
                                autodel=True, size=(800,600))
        self.callback_delete_request_add(lambda o: elementary.exit())

        hpanes = Panes(self, content_left_size=0.0, content_left_min_size=200,
                       size_hint_expand=EXPAND_BOTH)
        self.resize_object_add(hpanes)
        hpanes.show()

        vbox = Box(hpanes, size_hint_expand=EXPAND_BOTH)
        hpanes.part_content_set('right', vbox)
        vbox.show()

        vpanes = Panes(hpanes, horizontal=True, size_hint_expand=EXPAND_BOTH,
                       size_hint_fill=FILL_BOTH)
        vbox.pack_end(vpanes)
        vpanes.show()

        self.status = StatusBar(app, vbox)
        vbox.pack_end(self.status)
        self.status.show()

        self.tree = TreeView(app, hpanes)
        hpanes.part_content_set('left', self.tree)
        self.tree.show()

        self.grid = PhotoGrid(app, hpanes)
        vpanes.part_content_set('left', self.grid)
        self.grid.show()

        self.photo = ScrollablePhotocam(app, self)
        self.photo.callback_clicked_double_add(lambda b: ImageEditor(self.app))
        vpanes.part_content_set('right', self.photo)
        self.photo.show()

        self.show()


class EphotoApp(object):
    def __init__(self):
        self.main_win = MainWin(self)
        self.tree = self.main_win.tree
        self.grid = self.main_win.grid
        self.photo = self.main_win.photo
        self.status = self.main_win.status

        self.tree.populate(os.path.expanduser("~"))
        self.status.update()


if __name__ == '__main__':
    elementary.init()
    elementary.need_ethumb()
    elementary.theme.theme_extension_add(THEME_FILE)
    EphotoApp()
    elementary.run()
    elementary.shutdown()

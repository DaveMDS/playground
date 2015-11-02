#!/usr/bin/env python
# -*- coding: <utf-8> -*-
# Author: davemds <dave@gurumeditation.it>
# Copyright 2015 Davide Andreoli
# License: GPL v3+
# Version 0.1
# GIMP compatibilty 2.8.x
# GIMP plugin to export layers as Second Life textures (jpg)

from gimpfu import *


W_ALL = 1
W_SEL = 2
W_VIS = 3


def get_layers(layers, only_visible, only_current):
    result = []
    for layer in layers:
        if pdb.gimp_item_is_group(layer):
            result += get_layers(layer.children, only_visible, only_current)
        else:
            if only_current and only_current != layer.name:
                continue
            if layer.name.endswith('.jpg'):
                if only_visible:
                    if layer.visible:
                        result.append(layer)
                else:
                    result.append(layer)
        
    return result


def export_layers(img, drw, path, what=W_SEL,
                  comp=90, width=512, height=512):

    if what == W_SEL:
        only_current = img.active_layer.name
    else:
        only_current = False

    if what == W_VIS:
        only_visible = True
    else:
        only_visible = False

    dupe = img.duplicate()
    layers = get_layers(dupe.layers, only_visible, only_current)

    for layer in layers:
        layer.visible = 1
        layer.scale(width, height, 0)

        filename = layer.name.decode('utf-8')
        fullpath = os.path.join(path, filename);
        pdb.file_jpeg_save(dupe, layer, fullpath, filename,
                           float(comp) / 100, 0, 1, 1, "", 0, 1, 0, 0)


register(
    proc_name=("python-fu-export-layers"),
    blurb=("Export Layers as SecondLife Textures"),
    help=("Export Layers as SecondLife Textures"),
    author=("DaveMDS <dave@gurumeditation.it>"),
    copyright=("Davide Andreoli"),
    date=("2015"),
    label=("SecondLife Texture Exporter"),
    imagetypes=("*"),
    params=[
        (PF_IMAGE, "img", "Image", None),
        (PF_DRAWABLE, "drw", "Drawable", None),
        (PF_DIRNAME, "path", "Save PNGs here", os.getcwd()),
        (PF_RADIO, "what", "Layers to export", W_SEL,
            (("Selected layer",W_SEL),
             ("Visible layers", W_VIS),
             ("All layers", W_ALL),
            )),
        (PF_SLIDER, "comp", "JPEG Quality", 90, (10, 100, 5)),
        (PF_INT, "width", "Texture width", 512),
        (PF_INT, "height", "Texture height", 512),
        ],
    results=[],
    function=(export_layers), 
    menu=("<Image>/File"), 
    domain=("gimp20-python", gimp.locale_directory)
    )

main()

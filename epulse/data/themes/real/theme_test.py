#!/usr/bin/env python
# encoding: utf-8

import os

from efl.ecore import Timer, ECORE_CALLBACK_RENEW
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, EXPAND_BOTH, FILL_BOTH, FILL_VERT
from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.scroller import Scroller
from efl.elementary.background import Background
from efl.elementary.box import Box
from efl.elementary.frame import Frame
from efl.elementary.icon import Icon
from efl.elementary.label import Label
from efl.elementary.separator import Separator
from efl.elementary.slider import Slider
from efl.elementary.theme import theme_extension_add

from lib_pulseaudio import *

# from ctypes import POINTER, c_ubyte, c_void_p, c_ulong, cast
from ctypes import c_void_p, cast
from Queue import Queue


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
THEME_FILE = os.path.join(SCRIPT_PATH, 'real.edj')

class PulseClient(object):
    def __init__(self, index):
        self.index = index
        self.name = None
        self.application_name = None
        self.media_role = None
        self.icon_name = None
    
    def __repr__(self):
        return '<PulseClient idx:  {s.index}\n' \
               '             name: "{s.name}"\n' \
               '             application_name: "{s.application_name}"\n' \
               '             icon_name: "{s.icon_name}"\n' \
               '             media_role: "{s.media_role}"\n' \
               '>'.format(s=self)


class PulseChannel(object):
    def __init__(self, index):
        self.index = index
        self.name = None
        self.description = None
        self.volume = []
        self.mute = None
        self.client = None

    def __repr__(self):
        name = self.__class__.__name__
        return '<'+name+' idx:  {s.index}\n' \
               '      name: "{s.name}"\n' \
               '      description: "{s.description}"\n' \
               '      volume: {s.volume}\n' \
               '      mute: {s.mute}\n' \
               '      client: {s.client}\n' \
               '>'.format(s=self)

class PulseOutput(PulseChannel):
    pass

class PulseInput(PulseChannel):
    pass

class PulsePlayback(PulseChannel):
    pass


class PulseMonitor(object):
    def __init__(self):#, sink_name, rate):
        
        self._queue = Queue()
        self._clients = {}    # key: client_index      val: PulseClient instance
        self._outputs = {}    # key: output_index      val: PulseOutput instance
        self._inputs = {}     # key: input_index       val: PulseInput instance
        self._playbacks = {}  # key: sink_input_index  val: PulsePlayback instance

        self._queue_timer = Timer(0.2, self._queue_timer_cb)
        # Wrap callback methods in appropriate ctypefunc instances so
        # that the Pulseaudio C API can call them
        self._context_notify_cb = pa_context_notify_cb_t(self.context_notify_cb)
        self._context_subscribe_cb = pa_context_subscribe_cb_t(self.context_subscribe_cb)
        
        self._sink_info_cb = pa_sink_info_cb_t(self.sink_info_cb)
        self._sink_input_info_cb = pa_sink_input_info_cb_t(self.sink_input_info_cb)
        
        self._source_info_cb = pa_source_info_cb_t(self.source_info_cb)
        self._source_output_info_cb = pa_source_output_info_cb_t(self.source_output_info_cb)
        
        # self._stream_read_cb = pa_stream_request_cb_t(self.stream_read_cb)
        self._client_info_cb = pa_client_info_cb_t(self.client_info_cb)
        # self._sample_info_cb = pa_sample_info_cb_t(self.sample_info_cb)
        
        # stream_read_cb() puts peak samples into this Queue instance
        # self._samples = Queue()
        
        # Create the mainloop thread and set our context_notify_cb
        # method to be called when there's updates relating to the
        # connection to Pulseaudio
        _mainloop = pa_threaded_mainloop_new()
        _mainloop_api = pa_threaded_mainloop_get_api(_mainloop)
        context = pa_context_new(_mainloop_api, 'peak_demo')
        pa_context_set_state_callback(context, self._context_notify_cb, None)
        pa_context_set_subscribe_callback(context, self._context_subscribe_cb, None)
        
        pa_context_connect(context, None, 0, None)
        pa_threaded_mainloop_start(_mainloop)
    
    def _queue_timer_cb(self):
        print("QUEUE")
        while not self._queue.empty():
            item = self._queue.get()
            if isinstance(item, PulseClient):
                if item.index in self._clients:
                    self._clients[item.index] = item
                    self.client_changed(item)
                else:
                    self._clients[item.index] = item
                    self.client_added(item)
            if isinstance(item, PulseOutput):
                if item.index in self._outputs:
                    self._outputs[item.index] = item
                    self.channel_changed(item)
                else:
                    self._outputs[item.index] = item
                    self.channel_added(item)
            elif isinstance(item, PulseInput):
                if item.index in self._inputs:
                    self._inputs[item.index] = item
                    self.channel_changed(item)
                else:
                    self._inputs[item.index] = item
                    self.channel_added(item)
            elif isinstance(item, PulsePlayback):
                if item.index in self._playbacks:
                    self._playbacks[item.index] = item
                    self.channel_changed(item)
                else:
                    self._playbacks[item.index] = item
                    self.channel_added(item)
            else:
                print("ITEM", item)

        return ECORE_CALLBACK_RENEW

    def context_notify_cb(self, context, _):
        state = pa_context_get_state(context)

        if state == PA_CONTEXT_READY:
            print "Pulseaudio connection ready..."
            
            # Connected to Pulseaudio. Now request infos...
            
            # clients
            o = pa_context_get_client_info_list(context, self._client_info_cb, None)
            pa_operation_unref(o)

            
            # sinks (outputs)
            o = pa_context_get_sink_info_list(context, self._sink_info_cb, None)
            pa_operation_unref(o)
            
            # sink inputs (playback)
            o = pa_context_get_sink_input_info_list(context, self._sink_input_info_cb, None)
            pa_operation_unref(o)
            
            # sources (inputs)
            o = pa_context_get_source_info_list(context, self._source_info_cb, None)
            pa_operation_unref(o)
            
            # source outputs (recording???)
            # o = pa_context_get_source_output_info_list(context, self._source_output_info_cb, None)
            # pa_operation_unref(o)

            # o = pa_context_get_sample_info_list(context, self._sample_info_cb, None)
            # pa_operation_unref(o)
            
            o = pa_context_subscribe(context, PA_SUBSCRIPTION_MASK_ALL,
                # PA_SUBSCRIPTION_MASK_SINK | PA_SUBSCRIPTION_MASK_SOURCE |
                # PA_SUBSCRIPTION_MASK_SINK_INPUT | PA_SUBSCRIPTION_MASK_SOURCE_OUTPUT, 
                cast(None, pa_context_success_cb_t), None)
            pa_operation_unref(o)

        elif state == PA_CONTEXT_FAILED :
            print "Connection failed"

        elif state == PA_CONTEXT_TERMINATED:
            print "Connection terminated"

    def context_subscribe_cb(self, context, event, index, _):
        # print("SUBSCRIBE")
        facility = event & PA_SUBSCRIPTION_EVENT_FACILITY_MASK
        event_type = event & PA_SUBSCRIPTION_EVENT_TYPE_MASK
        
        if facility == PA_SUBSCRIPTION_EVENT_SINK:
            print("SINK", index)
        
        elif facility == PA_SUBSCRIPTION_EVENT_SOURCE:
            print("SOURCE", index)
        
        elif facility == PA_SUBSCRIPTION_EVENT_SINK_INPUT:
            print("SINK_INPUT", index)
            if event_type == PA_SUBSCRIPTION_EVENT_REMOVE:
                print("remove SINK_INPUT", index)
            else:
                o = pa_context_get_sink_input_info(context, index, self._sink_input_info_cb, None)
                pa_operation_unref(o)
        
        elif facility == PA_SUBSCRIPTION_EVENT_SOURCE_OUTPUT:
            print("SOURCE_OUTPUT", index)
        
        elif facility == PA_SUBSCRIPTION_EVENT_CLIENT:
            if event_type == PA_SUBSCRIPTION_EVENT_REMOVE:
                print("remove CLIENT", index)
            else:
                o = pa_context_get_client_info(context, index, self._client_info_cb, None)
                pa_operation_unref(o)

        elif facility == PA_SUBSCRIPTION_EVENT_SERVER:
            print("SERVER", index)
        
        elif facility ==  PA_SUBSCRIPTION_EVENT_CARD:
            print("CARD", index)

    def _norm_volume(self, val):
        return float(val) / 65536

    ## Outputs (Sinks)
    def sink_info_cb(self, context, sink_info_p, _, __):
        if not sink_info_p:
            return

        sink_info = sink_info_p.contents
        output = PulseOutput(sink_info.index)
        output.name = sink_info.name
        output.description = sink_info.description
        output.mute = bool(sink_info.mute)
        output.volume = [ self._norm_volume(sink_info.volume.values[i])
                          for i in range(sink_info.volume.channels) ]
        self._queue.put(output)

    ## Playbacks (Sink inputs)
    def sink_input_info_cb(self, context, sink_info_p, _, __):
        if not sink_info_p:
            return

        sink_info = sink_info_p.contents
        playback = PulsePlayback(sink_info.index)
        playback.name = sink_info.name
        playback.mute = bool(sink_info.mute)
        playback.volume = [ self._norm_volume(sink_info.volume.values[i])
                            for i in range(sink_info.volume.channels) ]
        if sink_info.client in self._clients:
            playback.client = self._clients[sink_info.client]
        self._queue.put(playback)
        
        # print '-'* 60
        # print 'index:', sink_info.index
        # print 'name:', sink_info.name
        # print 'client:', sink_info.client
        # print 'channels:', sink_info.volume.channels, sink_info.volume.values[0], sink_info.volume.values[1]
        # print 'muted:', sink_info.mute

    
    ## Inputs (Sources)
    def source_info_cb(self, context, source_info_p, _, __):
        if not source_info_p:
            return

        source_info = source_info_p.contents
        input = PulseInput(source_info.index)
        input.name = source_info.name
        input.description = source_info.description
        input.mute = bool(source_info.mute)
        input.volume = [ self._norm_volume(source_info.volume.values[i])
                          for i in range(source_info.volume.channels) ]
        self._queue.put(input)


    ## Recordings ????
    def source_output_info_cb(self, context, sink_info_p, _, __):
        if not sink_info_p:
            return

        sink_info = sink_info_p.contents
        print '-'* 60
        print 'index:', sink_info.index
        print 'name:', sink_info.name
        print 'channels:', sink_info.volume.channels, sink_info.volume.values[0]
        print 'muted:', sink_info.mute
    
    # def sample_info_cb(self, context, sink_info_p, _, __):
        # if not sink_info_p:
            # return
        # sink_info = sink_info_p.contents
        # print '-'* 60
        # print 'index:', sink_info.index
        # print 'name:', sink_info.name
        # print 'channels:', sink_info.volume.channels, sink_info.volume.values[0]
        
    ## Client
    def client_info_cb(self, context, client_info_p, _, __):
        if not client_info_p:
            return

        client_info = client_info_p.contents
        client = PulseClient(client_info.index)
        client.name = client_info.name

        data = c_void_p()
        while 1:
            prop_name = pa_proplist_iterate(client_info.proplist, data)
            if not prop_name:
                break
            # print('prop:', prop_name, ' val:', pa_proplist_gets(client_info.proplist, prop_name))
            if prop_name == 'application.name':
                client.application_name = pa_proplist_gets(client_info.proplist, prop_name)
            elif prop_name == 'application.icon_name':
                client.icon_name = pa_proplist_gets(client_info.proplist, prop_name)
            elif prop_name == 'media.role':
                client.media_role = pa_proplist_gets(client_info.proplist, prop_name)
        
        self._queue.put(client)


    """
    def stream_read_cb(self, stream, length, index_incr):
        data = c_void_p()
        pa_stream_peek(stream, data, c_ulong(length))
        data = cast(data, POINTER(c_ubyte))
        for i in xrange(length):
            # When PA_SAMPLE_U8 is used, samples values range from 128
            # to 255 because the underlying audio data is signed but
            # it doesn't make sense to return signed peaks.
            self._samples.put(data[i] - 128)
        pa_stream_drop(stream)
    """
    # API #

    def client_added(self, client):
        raise(NotImplementedError)

    def client_changed(self, client):
        raise(NotImplementedError)

    def client_removed(self, client):
        raise(NotImplementedError)

    def channel_added(self, channel):
        raise(NotImplementedError)

    def channel_changed(self, channel):
        raise(NotImplementedError)

    def channel_removed(self, channel):
        raise(NotImplementedError)
        


class PulseAudio(PulseMonitor):
    
    def __init__ (self, win):
        self.win = win
        PulseMonitor.__init__(self)
        
    def client_added(self, client):
        print("ADDED")
        print(client)
    
    def client_changed(self, client):
        print("CHANGED")
        print(client)
    
    def client_removed(self, client):
        print("REMOVED")
        print(client)

    def channel_added(self, channel):
        print("ADDED")
        print(channel)
        self.win.channel_add(channel)

    def channel_changed(self, channel):
        print("CHANGED")
        print(channel)

    def channel_removed(self, channel):
        print("REMOVED")
        print(channel)


class MixerWin(StandardWindow):
    def __init__(self):
        StandardWindow.__init__(self, "E Pulse Mixer", "epulsemixer", 
                                autodel=True, size=(600, 300))
        self.callback_delete_request_add(lambda o: elementary.exit())

        bg = Background(self, style='pulse', size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(bg)
        bg.show()
        
        box = Box(self, horizontal=True, size_hint_weight=EXPAND_BOTH)
        box.padding = (25, 0) # TODO REMOVEME
        self.resize_object_add(box)

        theme_extension_add(THEME_FILE)

        # frame TEST
        fr = Frame(box, style='pulse', text="TEST2",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        fr.show()
        
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        
        sep = None
        for label in ("Stereo", "(HDMI)"):
            sl1 = Slider(sbox, style='pulse_double_left', text=label,
                        horizontal=False, inverted=True, 
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl1)
            sl1.show()

            sl2 = Slider(sbox, style='pulse_double_right', text='',
                        horizontal=False, inverted=True, 
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl2)
            sl2.show()
            
            sl1.callback_changed_add(lambda sl: setattr(sl2, 'value', sl.value))
            
            if sep is None:
                sep = Separator(sbox)
                sbox.pack_end(sep)
                sep.show()

        # Blaybacks frame
        fr = Frame(box, style='pulse', text="PLAYBACK",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        self.playbacks_box = sbox
        fr.show()

        # Inputs frame
        fr = Frame(box, style='pulse', text="INPUTS",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        self.inputs_box = sbox
        fr.show()

        # Outputs frame
        fr = Frame(box, style='pulse', text="OUTPUTS",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        self.outputs_box = sbox
        fr.show()


        box.show()
        self.show()

    
    def channel_add(self, channel):
        if isinstance(channel, PulsePlayback):
            box = self.playbacks_box
        elif isinstance(channel, PulseInput):
            box = self.inputs_box
        elif isinstance(channel, PulseOutput):
            box = self.outputs_box
        
        if len(channel.volume) == 2:
            sl1 = Slider(box, style='pulse_double_left',
                         horizontal=False, inverted=True,
                         text=channel.description or channel.name,
                         value=channel.volume[0],
                         size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            box.pack_end(sl1)
            sl1.show()
            sl2 = Slider(box, style='pulse_double_right',
                         horizontal=False, inverted=True,
                         text='',
                         value=channel.volume[1],
                         size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            box.pack_end(sl2)
            sl2.show()
            
        else:
            sl = Slider(box, style='pulse',
                        horizontal=False, inverted=True,
                        text=channel.description or channel.name,
                        value=channel.volume[0],
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            box.pack_end(sl)
            sl.show()
    
    
    
if __name__ == "__main__":

    win = MixerWin()
    
    pulse = PulseAudio(win)
    
    
    elementary.run()

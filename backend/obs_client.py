from fastapi import WebSocket
import threading
import time
from obswebsocket import obsws, events, requests
from data import CONFIG

def on_connect(obs):
    CONFIG.recording = obs_ws.call(requests.GetRecordStatus()).getOutputActive()
    if CONFIG.recording:
        pause_check_thread = threading.Thread(target=check_recording_paused)
        pause_check_thread.start()
    CONFIG.recording_paused = obs_ws.call(requests.GetRecordStatus()).getOutputPaused()
    CONFIG.streaming = obs_ws.call(requests.GetStreamStatus()).getOutputActive()
    CONFIG.replay_buffer = obs_ws.call(requests.GetReplayBufferStatus()).getOutputActive()

obs_ws = obsws("localhost", 4455, "Gccody_2010", authreconnect=1, on_connect=on_connect)

def on_record_state_changed(message):
    CONFIG.recording = message.getOutputActive()

def on_stream_state_changed(message):
    CONFIG.streaming = message.getOutputActive()

def on_replay_buffer_state_changed(message):
    CONFIG.replay_buffer = message.getOutputActive()

def check_recording_paused():
    while CONFIG.recording:
        CONFIG.recording_paused = obs_ws.call(requests.GetRecordStatus()).getOutputPaused()
        time.sleep(.5)


obs_ws.register(on_record_state_changed, events.RecordStateChanged)
obs_ws.register(on_stream_state_changed, events.StreamStateChanged)
from fastapi import WebSocket
from obs_client import obs_ws

class StartRecording:
    __commandname__ = 'Start Recording'

    @staticmethod
    async def execute():
        obs_ws.start_record()

class StopRecording:
    __commandname__ = 'Stop Recording'

    @staticmethod
    async def execute():
        obs_ws.stop_record()

class ToggleRecording:
    __commandname__ = 'Toggle Recording'

    @staticmethod
    async def execute():
        obs_ws.toggle_record()

class PauseRecording:
    __commandname__ = 'Pause Recording'

    @staticmethod
    async def execute():
        obs_ws.pause_record()

class ResumeRecording:
    __commandname__ = 'Resume Recording'

    @staticmethod
    async def execute():
        obs_ws.resume_record()

class TogglePauseRecording:
    __commandname__ = 'Togglepause Recording'

    @staticmethod
    async def execute():
        obs_ws.toggle_record_pause()

class StartStream:
    __commandname__ = 'Start Stream'

    @staticmethod
    async def execute():
        obs_ws.start_stream()


class EndStream:
    __commandname__ = 'End Stream'

    @staticmethod
    async def execute():
        obs_ws.stop_stream()

class ToggleStream:
    __commandname__ = 'Toggle Stream'

    @staticmethod
    async def execute():
        obs_ws.toggle_stream()

class ChangeScene:
    __commandname__ = 'Change Scene'

    @staticmethod
    async def execute(name: str):
        obs_ws.set_current_program_scene(name)

class GetScenes:
    __commandname__ = 'Get Scenes'

    @staticmethod
    async def execute():
        return obs_ws.get_scene_list().scenes
        
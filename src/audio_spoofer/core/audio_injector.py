import os
import glob

class AudioInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        noise_script = os.path.join(self.modules_dir, 'audio_noise_engine.js')
        if os.path.exists(noise_script):
            with open(noise_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        spoofer_script = os.path.join(self.modules_dir, 'audio_spoofer.js')
        if os.path.exists(spoofer_script):
            with open(spoofer_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the combined JS payload for audio manipulation.
        """
        return self.scripts

audio_injector = AudioInjector()

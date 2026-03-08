import os
import glob

class WebRTCInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        # Ensure dependencies load first
        sdp_script = os.path.join(self.modules_dir, 'sdp_sanitizer.js')
        cand_script = os.path.join(self.modules_dir, 'candidate_filter.js')
        spoofer_script = os.path.join(self.modules_dir, 'webrtc_spoofer.js')

        for script_path in [sdp_script, cand_script, spoofer_script]:
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the bundled WebRTC spoofing payload.
        """
        return self.scripts

webrtc_injector = WebRTCInjector()

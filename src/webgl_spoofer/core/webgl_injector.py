import os
import glob

class WebGLInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        # Load helpers first
        mapper = os.path.join(self.modules_dir, 'gpu_parameter_mapper.js')
        noise = os.path.join(self.modules_dir, 'render_noise_engine.js')
        main_spoofer = os.path.join(self.modules_dir, 'webgl_spoofer.js')

        for script_path in [mapper, noise, main_spoofer]:
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the bundled WebGL runtime spoofing script.
        """
        return self.scripts

webgl_injector = WebGLInjector()

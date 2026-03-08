import os
import glob

class FontInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        metrics_script = os.path.join(self.modules_dir, 'font_metrics_engine.js')
        if os.path.exists(metrics_script):
            with open(metrics_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        spoofer_script = os.path.join(self.modules_dir, 'font_spoofer.js')
        if os.path.exists(spoofer_script):
            with open(spoofer_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the combined JS payload for font manipulation.
        """
        return self.scripts

font_injector = FontInjector()

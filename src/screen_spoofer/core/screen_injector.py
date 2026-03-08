import os
import glob

class ScreenInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        screen_spoofer = os.path.join(self.modules_dir, 'screen_spoofer.js')
        if os.path.exists(screen_spoofer):
            with open(screen_spoofer, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        metrics_engine = os.path.join(self.modules_dir, 'window_metrics_engine.js')
        if os.path.exists(metrics_engine):
            with open(metrics_engine, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the bundled Screen and Window spoofing payload natively.
        """
        return self.scripts

screen_injector = ScreenInjector()

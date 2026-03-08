import os
import glob

class ChromeEnvInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'modules')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        # Ensure order: chrome_object.js must be first to create window.chrome
        main_script = os.path.join(self.modules_dir, 'chrome_object.js')
        if os.path.exists(main_script):
            with open(main_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        for file in sorted(glob.glob(os.path.join(self.modules_dir, '*.js'))):
            if not file.endswith('chrome_object.js'):
                with open(file, 'r', encoding='utf-8') as f:
                    bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the complete JavaScript bundle simulating the Chrome runtime environment.
        """
        return self.scripts

chrome_env_injector = ChromeEnvInjector()

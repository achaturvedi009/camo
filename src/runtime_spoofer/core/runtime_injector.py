import os
import glob
from src.runtime_spoofer.integration.fingerprint_adapter import generate_injection_script

class RuntimeInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'modules')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        for file in sorted(glob.glob(os.path.join(self.modules_dir, '*.js'))):
            with open(file, 'r', encoding='utf-8') as f:
                bundle.append(f.read())
        return "\n\n".join(bundle)

    def build_init_script(self, fingerprint_data: dict) -> str:
        """
        Builds the entire initial payload to inject via CDP / Playwright `add_init_script`.
        It first injects the fingerprint variables, then the spoofing functions.
        """
        init_fp = generate_injection_script(fingerprint_data)
        return init_fp + "\n\n" + self.scripts

runtime_injector = RuntimeInjector()

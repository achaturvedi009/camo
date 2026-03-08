import os
import glob

class PermissionsInjector:
    def __init__(self):
        self.modules_dir = os.path.join(os.path.dirname(__file__), '..', 'runtime')
        self.scripts = self._load_scripts()

    def _load_scripts(self) -> str:
        bundle = []
        # Ensure emulator loads before spoofer
        main_script = os.path.join(self.modules_dir, 'permission_status_emulator.js')
        if os.path.exists(main_script):
            with open(main_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        spoofer_script = os.path.join(self.modules_dir, 'permissions_spoofer.js')
        if os.path.exists(spoofer_script):
            with open(spoofer_script, 'r', encoding='utf-8') as f:
                bundle.append(f.read())

        return "\n\n".join(bundle)

    def get_injection_script(self) -> str:
        """
        Returns the complete JavaScript bundle simulating the Permissions API.
        """
        return self.scripts

permissions_injector = PermissionsInjector()

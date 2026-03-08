from src.chrome_emulation.core.chrome_env_injector import chrome_env_injector

def get_chrome_emulation_bundle() -> str:
    """
    Retrieves the Chrome environment emulation JS bundle.
    Integrates with CAMO's main injection pipeline.
    """
    return chrome_env_injector.get_injection_script()

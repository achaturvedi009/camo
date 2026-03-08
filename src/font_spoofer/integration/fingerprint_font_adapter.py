from src.font_spoofer.core.font_dataset_manager import get_fonts_for_os

def integrate_font_seed(fingerprint: dict, os_type: str) -> dict:
    """
    Ensures the exact font dataset arrays are passed down to the javascript environment natively.
    """
    fonts = get_fonts_for_os(os_type)
    fingerprint["fonts"] = fonts

    if "environment" not in fingerprint:
        fingerprint["environment"] = {}
    fingerprint["environment"]["fonts"] = fonts

    return fingerprint

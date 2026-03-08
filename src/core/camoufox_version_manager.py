import subprocess
import json
import os
import requests
from pathlib import Path
from src.core.db import SessionLocal, CamoufoxVersionModel
import datetime
import packaging.version

VERSIONS_DIR = Path(os.path.expanduser("~/.camo/camoufox_versions"))
VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

class CamoufoxVersionManager:
    def fetch_available_versions(self):
        try:
            res = requests.get("https://pypi.org/pypi/camoufox/json", timeout=10)
            releases = list(res.json().get("releases", {}).keys())

            # Filter valid versions and sort
            valid_releases = []
            for r in releases:
                try:
                    packaging.version.parse(r)
                    valid_releases.append(r)
                except:
                    pass

            sorted_versions = sorted(valid_releases, key=packaging.version.parse, reverse=True)
            return sorted_versions
        except Exception as e:
            print(f"Error fetching versions: {e}")
            return []

    def get_installed_versions(self):
        db = SessionLocal()
        versions = db.query(CamoufoxVersionModel).filter(CamoufoxVersionModel.installed == True).all()
        result = [{"version": v.version, "is_default": v.is_default, "install_path": v.install_path} for v in versions]
        db.close()
        return result

    def install_version(self, version: str):
        target_dir = VERSIONS_DIR / version
        subprocess.run([
            "python", "-m", "pip", "install", f"camoufox=={version}",
            "--target", str(target_dir), "--no-deps"
        ], check=True)

        db = SessionLocal()
        v_model = db.query(CamoufoxVersionModel).filter(CamoufoxVersionModel.version == version).first()
        if not v_model:
            v_model = CamoufoxVersionModel(
                version=version,
                installed=True,
                install_path=str(target_dir),
                installed_at=datetime.datetime.utcnow()
            )
            db.add(v_model)
        else:
            v_model.installed = True
            v_model.install_path = str(target_dir)
            v_model.installed_at = datetime.datetime.utcnow()

        # If no default is set, set this as default
        default = db.query(CamoufoxVersionModel).filter(CamoufoxVersionModel.is_default == True).first()
        if not default:
            v_model.is_default = True

        db.commit()
        db.close()
        return True

    def set_active_version(self, version: str):
        db = SessionLocal()
        db.query(CamoufoxVersionModel).update({"is_default": False})
        v_model = db.query(CamoufoxVersionModel).filter(CamoufoxVersionModel.version == version).first()
        if v_model:
            v_model.is_default = True
        db.commit()
        db.close()
        return True

    def uninstall_version(self, version: str):
        db = SessionLocal()
        v_model = db.query(CamoufoxVersionModel).filter(CamoufoxVersionModel.version == version).first()
        if v_model:
            import shutil
            if os.path.exists(v_model.install_path):
                shutil.rmtree(v_model.install_path)
            db.delete(v_model)
            db.commit()
        db.close()
        return True

version_manager = CamoufoxVersionManager()

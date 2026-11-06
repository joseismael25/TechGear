"""Launcher de Django para ejecutar comandos desde la carpeta principal de TechGear."""
from pathlib import Path
import runpy
import sys

PROJECT_DIR = Path(__file__).resolve().parent / "techgear_web"
DJANGO_MANAGE = PROJECT_DIR / "manage.py"

if not DJANGO_MANAGE.is_file():
    raise SystemExit(
        "No se encontró techgear_web/manage.py. "
        "Comprueba que el ZIP se haya extraído completo."
    )

# Permite que Python encuentre el paquete techgear_web y la app store.
sys.path.insert(0, str(PROJECT_DIR))
runpy.run_path(str(DJANGO_MANAGE), run_name="__main__")

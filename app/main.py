import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
from app.config.router import main as router_main

if __name__ == "__main__":
    ft.app(target=router_main)
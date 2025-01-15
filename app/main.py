import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
from app.presentation.login import main

if __name__ == "__main__":
    ft.app(target=main)
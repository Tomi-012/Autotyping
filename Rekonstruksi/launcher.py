"""Run the recovered AutoTyping application bytecode in a frozen package."""

import marshal
from pathlib import Path
import sys

# Explicit imports make the recovered application's dependencies visible to PyInstaller.
import keyboard
import pyautogui
import tkinter
from tkinter import scrolledtext, ttk
import threading
import time
from templates import add_templates
from themes import add_themes
from interface import create_widgets


def main():
    package_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    payload = (package_dir / "AutoTyping.recovered.pyc").read_bytes()
    code = marshal.loads(payload[16:])
    namespace = {"__name__": "recovered_autotyping", "__file__": "AutoTyping.py"}
    exec(code, namespace)
    root = tkinter.Tk()
    namespace["AutoTypingApp"].create_widgets = create_widgets
    app = namespace["AutoTypingApp"](root)
    root.title("Auto Typing By Mas Rori")
    root.geometry("560x500")
    root.minsize(480, 420)
    root.iconbitmap(str(package_dir / "Logo Mas Rori.ico"))
    add_templates(app)
    add_themes(app)
    root.mainloop()


if __name__ == "__main__":
    main()

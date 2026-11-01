"""Two selectable themes for the recovered application and template panel."""
import json
import os
from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import ttk

from templates import default_store_path

ORANGE = "#ff7624"
BLACK = "#111111"
SURFACE = "#202020"
INPUT = "#292929"
WHITE = "#f8f8f8"
MUTED = "#a5a5a5"


class ThemeManager:
    def __init__(self, app, path=None):
        self.app = app
        self.path = Path(path) if path is not None else default_store_path().with_name("theme.json")
        self.style = ttk.Style(app.root)
        self.default_theme = self.style.theme_use()
        self.style.configure("Brand.TLabel", font=("Segoe UI", 13, "bold"), foreground="#ab4a0c")
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 9), foreground="#555555")
        self.style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"))
        self.style.configure("Muted.TLabel", font=("Segoe UI", 9), foreground="#555555")
        self.original_status = {key: app.status_label.cget(key) for key in ("background", "foreground")}
        self.original = {}
        self.mode = tk.StringVar(value=self.read_mode())

        settings = app.notebook.nametowidget(app.notebook.tabs()[1])
        row = ttk.LabelFrame(settings, text="Tema", padding=4)
        self.theme_frame = row
        row.pack(fill=tk.X, pady=(4, 0))
        ttk.Radiobutton(row, text="Oranye Hitam", variable=self.mode, value="dark",
                        command=self.change).pack(side=tk.LEFT, padx=(0, 14))
        ttk.Radiobutton(row, text="Default", variable=self.mode, value="default",
                        command=self.change).pack(side=tk.LEFT)

        self.capture_widgets(app.root)
        self.create_dark_theme()
        self.apply(self.mode.get())

    def read_mode(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data.get("theme") if data.get("theme") in ("dark", "default") else "dark"
        except (OSError, ValueError, AttributeError):
            return "dark"

    def capture_widgets(self, widget):
        if isinstance(widget, (tk.Tk, tk.Text, tk.Button)):
            options = ("background", "foreground", "insertbackground", "selectbackground",
                       "selectforeground", "activebackground", "activeforeground",
                       "disabledforeground", "highlightbackground", "highlightcolor")
            self.original[widget] = {key: widget.cget(key) for key in options if key in widget.keys()}
        for child in widget.winfo_children():
            self.capture_widgets(child)

    def create_dark_theme(self):
        if "rori-dark" in self.style.theme_names():
            return
        self.style.theme_create("rori-dark", parent="clam", settings={
            ".": {"configure": {"background": BLACK, "foreground": WHITE, "font": ("Segoe UI", 10)}},
            "TFrame": {"configure": {"background": BLACK}},
            "TLabel": {"configure": {"background": BLACK, "foreground": WHITE}},
            "Header.TLabel": {"configure": {"background": BLACK, "foreground": WHITE, "font": ("Arial", 10, "bold")}},
            "Brand.TLabel": {"configure": {"background": BLACK, "foreground": ORANGE, "font": ("Segoe UI", 13, "bold")}},
            "Subtitle.TLabel": {"configure": {"background": BLACK, "foreground": MUTED, "font": ("Segoe UI", 9)}},
            "Section.TLabel": {"configure": {"background": BLACK, "foreground": WHITE, "font": ("Segoe UI", 11, "bold")}},
            "Muted.TLabel": {"configure": {"background": BLACK, "foreground": "#c4c4c4", "font": ("Segoe UI", 9)}},
            "TLabelframe": {"configure": {"background": BLACK, "foreground": ORANGE, "bordercolor": "#525252"}},
            "TLabelframe.Label": {"configure": {"background": BLACK, "foreground": ORANGE}},
            "TButton": {"configure": {"background": SURFACE, "foreground": WHITE, "bordercolor": "#555555", "padding": (5, 4)},
                        "map": {"background": [("active", ORANGE), ("disabled", BLACK)], "foreground": [("active", BLACK), ("disabled", MUTED)]}},
            "TRadiobutton": {"configure": {"background": BLACK, "foreground": WHITE},
                             "map": {"background": [("active", BLACK)], "foreground": [("disabled", MUTED)]}},
            "TCheckbutton": {"configure": {"background": BLACK, "foreground": WHITE},
                             "map": {"background": [("active", BLACK)], "foreground": [("disabled", MUTED)]}},
            "TEntry": {"configure": {"fieldbackground": INPUT, "foreground": WHITE, "insertcolor": WHITE}},
            "TCombobox": {"configure": {"fieldbackground": INPUT, "background": SURFACE, "foreground": WHITE, "arrowcolor": ORANGE},
                          "map": {"fieldbackground": [("readonly", INPUT)], "foreground": [("readonly", WHITE)], "selectbackground": [("readonly", INPUT)], "selectforeground": [("readonly", WHITE)]}},
            "TSpinbox": {"configure": {"fieldbackground": INPUT, "background": SURFACE, "foreground": WHITE, "arrowcolor": ORANGE}},
            "TNotebook": {"configure": {"background": BLACK, "bordercolor": BLACK}},
            "TNotebook.Tab": {"configure": {"background": SURFACE, "foreground": WHITE, "padding": (8, 5)},
                              "map": {"background": [("selected", ORANGE), ("active", "#3b3b3b")], "foreground": [("selected", BLACK)]}},
            "Vertical.TScrollbar": {"configure": {"background": SURFACE, "troughcolor": BLACK, "arrowcolor": WHITE}},
        })

    def apply(self, mode):
        dark = mode == "dark"
        self.style.theme_use("rori-dark" if dark else self.default_theme)
        self.app.status_label.configure(**({"background": BLACK, "foreground": WHITE} if dark else self.original_status))
        for widget, original in self.original.items():
            if not widget.winfo_exists():
                continue
            if not dark:
                widget.configure(**original)
            elif isinstance(widget, tk.Text):
                widget.configure(background=INPUT, foreground=WHITE, insertbackground=ORANGE,
                                 selectbackground=ORANGE, selectforeground=BLACK,
                                 highlightbackground=SURFACE, highlightcolor=ORANGE)
            elif isinstance(widget, tk.Button):
                primary = widget is self.app.start_button
                widget.configure(background=ORANGE if primary else SURFACE,
                                 foreground=BLACK if primary else WHITE,
                                 activebackground="#ff9a57" if primary else "#424242",
                                 activeforeground=BLACK if primary else WHITE, disabledforeground="#898989",
                                 highlightbackground=BLACK)
            else:
                widget.configure(background=BLACK)

    def change(self):
        self.apply(self.mode.get())
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                                 prefix=".theme-", suffix=".tmp", delete=False) as stream:
                    temp_path = Path(stream.name)
                    json.dump({"theme": self.mode.get()}, stream)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temp_path, self.path)
            finally:
                if temp_path is not None and temp_path.exists():
                    temp_path.unlink()
        except OSError:
            self.app.status_label.config(text="Tema aktif, tetapi pilihan tidak dapat disimpan")


def add_themes(app, path=None):
    app.theme_manager = ThemeManager(app, path)
    return app.theme_manager

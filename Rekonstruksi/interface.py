"""Interface for the recovered typing engine."""
import tkinter as tk
from tkinter import scrolledtext, ttk


def create_widgets(self):
    shell = ttk.Frame(self.root, padding=(10, 8, 10, 6))
    shell.pack(fill=tk.BOTH, expand=True)

    self.notebook = ttk.Notebook(shell)
    self.notebook.pack(fill=tk.BOTH, expand=True)

    editor_tab = ttk.Frame(self.notebook, padding=8)
    self.notebook.add(editor_tab, text="  Bot Typing  ")
    editor = ttk.Frame(editor_tab)
    editor.pack(fill=tk.BOTH, expand=True)
    ttk.Label(editor, text="Masukkan Teks Untuk Diketik:", style="Section.TLabel").pack(
        anchor="w", pady=(0, 5))
    self.text_input = scrolledtext.ScrolledText(editor, wrap=tk.WORD, height=3,
                                                font=("Segoe UI", 10), relief=tk.FLAT,
                                                borderwidth=0, padx=10, pady=9)
    self.text_input.pack(fill=tk.BOTH, expand=True)

    controls = ttk.Frame(editor_tab)
    controls.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0), before=editor)
    actions = ttk.Frame(controls)
    actions.pack(fill=tk.X)
    self.start_button = tk.Button(actions, text="Mulai Mengetik", command=self.start_typing,
                                  font=("Segoe UI", 9, "bold"), relief=tk.RAISED,
                                  borderwidth=2, overrelief=tk.GROOVE,
                                  background="#4CAF50", foreground="white", padx=9, pady=4)
    self.start_button.pack(side=tk.LEFT)
    self.stop_button = tk.Button(actions, text="Berhenti", command=self.stop_typing,
                                 font=("Segoe UI", 9), relief=tk.RAISED, borderwidth=2,
                                 overrelief=tk.GROOVE, state=tk.DISABLED, disabledforeground="#eeeeee",
                                 background="#F44336", foreground="white", padx=9, pady=4)
    self.stop_button.pack(side=tk.LEFT, padx=(7, 0))
    tk.Button(actions, text="Bersihkan", command=self.clear_text, font=("Segoe UI", 9),
              relief=tk.RAISED, borderwidth=2, overrelief=tk.GROOVE,
              background="#2196F3", foreground="white", padx=9, pady=4).pack(
                  side=tk.LEFT, padx=(7, 0))
    ttk.Checkbutton(actions, text="Selalu di atas", variable=self.always_on_top,
                    command=self.toggle_always_on_top).pack(side=tk.RIGHT)
    countdown = ttk.Frame(controls)
    countdown.pack(fill=tk.X, pady=(5, 0))
    ttk.Label(countdown, text="Mulai setelah").pack(side=tk.LEFT)
    ttk.Spinbox(countdown, from_=1, to=10, textvariable=self.delay_before_typing,
                width=4).pack(side=tk.LEFT, padx=8)
    ttk.Label(countdown, text="detik").pack(side=tk.LEFT)

    settings = ttk.Frame(self.notebook, padding=8)
    self.notebook.add(settings, text="  Pengaturan  ")
    methods = ttk.LabelFrame(settings, text="Metode pengetikan", padding=(8, 3))
    methods.pack(fill=tk.X, pady=(0, 5))
    method_values = {"Karakter (lambat tapi stabil)": "char",
                     "Batch (cepat, sedikit buffer)": "batch",
                     "Keyboard API (sangat cepat)": "keyboard"}
    self.method_choice = tk.StringVar(value=next(label for label, value in method_values.items()
                                                  if value == self.typing_method.get()))
    self.method_select = ttk.Combobox(methods, state="readonly", textvariable=self.method_choice,
                                     values=list(method_values))
    self.method_select.pack(fill=tk.X)
    self.method_select.bind("<<ComboboxSelected>>",
                            lambda event: self.typing_method.set(method_values[self.method_choice.get()]))
    settings_grid = ttk.Frame(settings)
    settings_grid.pack(fill=tk.X)
    settings_grid.columnconfigure(0, weight=1, uniform="settings")
    settings_grid.columnconfigure(1, weight=1, uniform="settings")
    char_frame = ttk.LabelFrame(settings_grid, text="Karakter", padding=6)
    char_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    ttk.Label(char_frame, text="Delay per karakter (detik)").pack(anchor="w", pady=(0, 5))
    ttk.Spinbox(char_frame, from_=0.0001, to=0.1, increment=0.001,
                textvariable=self.typing_speed, width=12).pack(anchor="w")
    batch = ttk.LabelFrame(settings_grid, text="Batch", padding=6)
    batch.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
    ttk.Label(batch, text="Ukuran batch (karakter)").pack(anchor="w", pady=(0, 5))
    ttk.Spinbox(batch, from_=5, to=50, textvariable=self.batch_size, width=12).pack(anchor="w")
    ttk.Label(batch, text="Delay antar batch (detik)").pack(anchor="w", pady=(4, 3))
    ttk.Spinbox(batch, from_=0.001, to=0.1, increment=0.001,
                textvariable=self.batch_delay, width=12).pack(anchor="w")

    self.status_label = ttk.Label(shell, text="Siap Untuk Mengetik", anchor="w", padding=(1, 4, 0, 0))
    self.status_label.pack(side=tk.BOTTOM, fill=tk.X, before=self.notebook)

"""Local template management for the recovered AutoTyping interface."""
import json
import os
from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk


def default_store_path():
    base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    return Path(base) / "AutoTyping Mas Rori" / "templates.json"


class TemplatePanel:
    def __init__(self, app, path=None):
        self.app = app
        self.path = Path(path) if path is not None else default_store_path()
        self.items = {}
        self.load_error = None
        self.load()

        editor_tab = app.notebook.nametowidget(app.notebook.tabs()[0])
        editor_frame = app.text_input.master.master
        self.quick_frame = ttk.Frame(editor_tab)
        self.quick_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0), before=editor_frame)
        ttk.Label(self.quick_frame, text="Template:").pack(side=tk.LEFT, padx=(0, 5))
        self.quick_name = tk.StringVar()
        self.quick_select = ttk.Combobox(
            self.quick_frame, textvariable=self.quick_name, state="readonly", width=20
        )
        self.quick_select.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(self.quick_frame, text="Tampilkan", command=self.apply_template).pack(
            side=tk.LEFT, padx=(5, 0)
        )

        self.tab = ttk.Frame(app.notebook, padding=8)
        app.notebook.add(self.tab, text="  Template  ")
        self.tab.columnconfigure(0, weight=1)
        self.tab.rowconfigure(3, weight=1)
        ttk.Label(self.tab, text="Pilih template tersimpan:").grid(row=0, column=0, sticky="w")
        self.selected_name = tk.StringVar()
        self.template_select = ttk.Combobox(
            self.tab, textvariable=self.selected_name, state="readonly"
        )
        self.template_select.grid(row=1, column=0, sticky="ew", pady=(2, 6))
        self.template_select.bind("<<ComboboxSelected>>", self.select_template)
        name_row = ttk.Frame(self.tab)
        name_row.grid(row=2, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(name_row, text="Nama:").pack(side=tk.LEFT, padx=(0, 5))
        self.name = tk.StringVar()
        ttk.Entry(name_row, textvariable=self.name).pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.text = scrolledtext.ScrolledText(self.tab, wrap=tk.WORD, height=3)
        self.text.grid(row=3, column=0, sticky="nsew")
        actions = ttk.Frame(self.tab)
        actions.grid(row=4, column=0, sticky="ew", pady=(6, 0))
        ttk.Button(actions, text="Baru", command=self.new_template).pack(side=tk.LEFT)
        ttk.Button(actions, text="Simpan", command=self.save_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="Hapus", command=self.delete_template).pack(side=tk.LEFT)
        ttk.Button(self.tab, text="Tampilkan di Bot Typing", command=self.apply_editor_template).grid(
            row=5, column=0, sticky="ew", pady=(5, 0)
        )
        self.refresh()
        if self.load_error:
            self.app.root.after(0, lambda: messagebox.showerror(
                "Template tidak dapat dibaca",
                f"Data template tidak diubah. Periksa file berikut:\n{self.path}\n\n{self.load_error}",
                parent=self.app.root,
            ))

    def load(self):
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("templates"), dict):
                raise ValueError("Format file template tidak dikenali")
            if any(not isinstance(k, str) or not isinstance(v, str) for k, v in data["templates"].items()):
                raise ValueError("Nama dan isi template harus berupa teks")
            self.items = data["templates"]
        except (OSError, ValueError) as exc:
            self.load_error = str(exc)

    def persist(self, items):
        if self.load_error:
            raise ValueError("File template gagal dibaca; perbaiki file terlebih dahulu")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=self.path.parent,
                                             prefix=".templates-", suffix=".tmp", delete=False) as stream:
                tmp = Path(stream.name)
                json.dump({"version": 1, "templates": items}, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, self.path)
        finally:
            if tmp is not None and tmp.exists():
                tmp.unlink()
        self.items = items

    def refresh(self, selected=None):
        names = list(self.items)
        self.quick_select["values"] = names
        self.template_select["values"] = names
        if selected in self.items:
            self.quick_name.set(selected)
            self.selected_name.set(selected)
        else:
            self.quick_name.set(names[0] if names else "")
            self.selected_name.set("")

    def select_template(self, event=None):
        name = self.selected_name.get()
        if name in self.items:
            self.name.set(name)
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", self.items[name])
            self.quick_name.set(name)

    def new_template(self):
        self.selected_name.set("")
        self.name.set("")
        self.text.delete("1.0", tk.END)

    def save_template(self):
        name = self.name.get().strip()
        content = self.text.get("1.0", "end-1c")
        if not name or not content.strip():
            messagebox.showwarning("Template", "Isi nama dan teks template terlebih dahulu.", parent=self.app.root)
            return
        updated = dict(self.items)
        updated[name] = content
        try:
            self.persist(updated)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Gagal menyimpan template", str(exc), parent=self.app.root)
            return
        self.refresh(name)
        self.app.status_label.config(text="Template disimpan")

    def delete_template(self):
        name = self.selected_name.get()
        if name not in self.items:
            messagebox.showwarning("Template", "Pilih template yang ingin dihapus.", parent=self.app.root)
            return
        if not messagebox.askyesno("Hapus template", f'Hapus template "{name}"?', parent=self.app.root):
            return
        updated = dict(self.items)
        del updated[name]
        try:
            self.persist(updated)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Gagal menghapus template", str(exc), parent=self.app.root)
            return
        self.new_template()
        self.refresh()
        self.app.status_label.config(text="Template dihapus")

    def show_text(self, text):
        self.app.text_input.delete("1.0", tk.END)
        self.app.text_input.insert("1.0", text)
        self.app.notebook.select(0)
        self.app.status_label.config(text="Template ditampilkan di Bot Typing")

    def apply_template(self):
        name = self.quick_name.get()
        if name not in self.items:
            messagebox.showwarning("Template", "Pilih atau buat template terlebih dahulu.", parent=self.app.root)
            return
        self.show_text(self.items[name])

    def apply_editor_template(self):
        text = self.text.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Template", "Isi teks template terlebih dahulu.", parent=self.app.root)
            return
        self.show_text(text)


def add_templates(app, path=None):
    app.template_panel = TemplatePanel(app, path)
    return app.template_panel

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import threading
import time
import queue
import os
import webbrowser
import subprocess
import sys
import importlib.util
import random

TRANSLATIONS = {
    'en': {
        'title': 'Universal Bootstrap Creator',
        'banner': '🛠️ Universal Bootstrap Creator',
        'subtitle': 'Create your Python installers easily!',
        'add_module': 'Add Python Module:',
        'add': '➕ Add',
        'remove': '❌ Remove',
        'clear': '🧹 Clear',
        'copy': '📋 Copy',
        'req': '💾 Req.txt',
        'selected_modules': '📦 Selected Modules:',
        'generate': '🚀 Generate Bootstrap Installer',
        'open_folder': '📂 Open Folder',
        'dark_mode': 'Dark mode',
        'empty': 'No modules added yet...',
        'warning_empty': 'Module name is empty!',
        'warning_exists': 'Module already added!',
        'warning_no_modules': 'No modules to remove!',
        'warning_no_save': 'No modules to save!',
        'copied': 'Module list copied to clipboard!',
        'saved': 'requirements.txt saved!',
        'signature': 'Enter your signature:',
        'signature_required': 'Signature is required!',
        'success': '✅ bootstrap_output.py created successfully!',
        'error': 'Failed to create file:',
        'tooltip_add': 'Add module',
        'tooltip_remove': 'Remove last module',
        'tooltip_clear': 'Clear list',
        'tooltip_copy': 'Copy list',
        'tooltip_req': 'Save requirements.txt',
        'tooltip_search': 'Search module on PyPI',
        'tooltip_help': 'Show help / FAQ',
        'tooltip_info': 'Show info/FAQ',
        'pypi_empty': 'Enter a module name to search on PyPI.org!',
        'info': 'Описание всех кнопок...',
        'info_title': 'Info / FAQ',
        'help': 'Help',
        'help_text': '1. Enter module name and click "Add".\n2. Remove — removes last module.\n3. Clear — clears the list.\n4. Copy — copies the list.\n5. Req.txt — saves requirements.txt.\n6. Help — shows this window.\n7. PyPI Search — opens module page on pypi.org.\n8. Generate — creates installer.\n9. Open Folder — opens output folder.\n10. Console below shows all actions.',
    },
    'ru': {
        'title': 'Universal Bootstrap Creator',
        'banner': '🛠️ Universal Bootstrap Creator',
        'subtitle': 'Создавай свои Python-установщики легко!',
        'add_module': 'Добавить Python-модуль:',
        'add': '➕ Добавить',
        'remove': '❌ Удалить',
        'clear': '🧹 Очистить',
        'copy': '📋 Копировать',
        'req': '💾 Req.txt',
        'selected_modules': '📦 Выбранные модули:',
        'generate': '🚀 Создать Bootstrap-установщик',
        'open_folder': '📂 Открыть папку',
        'dark_mode': 'Тёмная тема',
        'empty': 'Модули не добавлены...',
        'warning_empty': 'Имя модуля пустое!',
        'warning_exists': 'Модуль уже добавлен!',
        'warning_no_modules': 'Нет модулей для удаления!',
        'warning_no_save': 'Нет модулей для сохранения!',
        'copied': 'Список модулей скопирован!',
        'saved': 'requirements.txt сохранён!',
        'signature': 'Введите вашу подпись:',
        'signature_required': 'Требуется подпись!',
        'success': '✅ bootstrap_output.py успешно создан!',
        'error': 'Ошибка создания файла:',
        'tooltip_add': 'Добавить модуль',
        'tooltip_remove': 'Удалить последний модуль',
        'tooltip_clear': 'Очистить список',
        'tooltip_copy': 'Скопировать список',
        'tooltip_req': 'Сохранить requirements.txt',
        'tooltip_search': 'Поиск модуля на PyPI',
        'tooltip_help': 'Показать справку / FAQ',
        'tooltip_info': 'Показать информацию/FAQ',
        'pypi_empty': 'Введите название модуля для поиска на PyPI.org!',
        'info': 'Описание всех кнопок...',
        'info_title': 'Информация/FAQ',
        'help': 'Справка',
        'help_text': '1. Введите название модуля и нажмите "Добавить".\n2. Удалить — удаляет последний модуль.\n3. Очистить — очищает список.\n4. Копировать — копирует список.\n5. Req.txt — сохраняет requirements.txt.\n6. Справка — показывает это окно.\n7. Поиск PyPI — открывает страницу модуля на pypi.org.\n8. Создать — генерирует установщик.\n9. Открыть папку — открывает папку с файлом.\n10. Внизу — консоль логов.',
    }
}

class NeonButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(corner_radius=12, fg_color="#23272f", hover_color="#2d323c", text_color="#fff", font=ctk.CTkFont(size=14))
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    def _on_enter(self, event=None):
        self.configure(fg_color="#2d323c")
    def _on_leave(self, event=None):
        self.configure(fg_color="#23272f")

class GlassFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="#181c22", corner_radius=16)

class BootstrapCreator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = 'en'
        self.trans = TRANSLATIONS[self.lang]
        self.title(self.trans['title'])
        self.resizable(False, False)
        self.selected_modules = []
        self.queue = queue.Queue()
        self.geometry("420x220")  # маленький размер для splash
        self.show_splash()

    def show_splash(self):
        self.splash_frame = ctk.CTkFrame(self, fg_color="#181c22", corner_radius=16)
        self.splash_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        ctk.CTkLabel(self.splash_frame, text="🛠️ Universal Bootstrap Creator", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00fff7").pack(pady=(38, 2))
        ctk.CTkLabel(self.splash_frame, text="by Fal1sev4n", font=ctk.CTkFont(size=14), text_color="#aaa").pack()
        ctk.CTkLabel(self.splash_frame, text="Loading resources...", font=ctk.CTkFont(size=15), text_color="#fff").pack(pady=(16, 8))
        self.splash_progress = ctk.CTkProgressBar(self.splash_frame, orientation="horizontal", height=10, corner_radius=5, fg_color="#222", progress_color="#00fff7")
        self.splash_progress.pack(padx=60, pady=(0, 18), fill="x")
        self.splash_progress.set(0)
        self.splash_progress.after(50, self.animate_splash)
        self.after(5000, self.hide_splash)

    def animate_splash(self, step=0):
        if hasattr(self, 'splash_progress'):
            self.splash_progress.set((step % 100) / 100)
            self.splash_progress.after(40, self.animate_splash, step+2)

    def hide_splash(self):
        self.splash_frame.destroy()
        self.geometry("700x800")  # основной размер окна
        self.setup_ui()
        self.check_queue()

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task[0] == "show_dialog":
                    self.show_author_dialog()
                elif task[0] == "show_message":
                    color = "#2aa44f" if task[1] == "Success" else "#d33"
                    icon = "✅" if task[1] == "Success" else "⚠️"
                    self.show_status(task[2], color=color, icon=icon)
                    messagebox.showinfo(task[1], task[2])
                elif task[0] == "update_progress":
                    self.progressbar.set(task[1] / 100)
                elif task[0] == "show_open_folder":
                    self.open_folder_btn.pack(pady=5)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.check_queue)

    def setup_ui(self):
        self.geometry("700x800")
        ctk.set_appearance_mode("dark")
        # Верхний блок: язык и тема
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=(12, 0), padx=30, fill="x")
        ctk.CTkLabel(top_frame, text="Language:", font=ctk.CTkFont(size=13)).pack(side="left", padx=2)
        self.lang_var = ctk.StringVar(value=self.lang)
        lang_switch = ctk.CTkSegmentedButton(top_frame, values=["en", "ru"], variable=self.lang_var, command=self.change_language)
        lang_switch.pack(side="left", padx=2)
        self.theme_var = ctk.StringVar(value="dark")
        theme_switch = ctk.CTkSwitch(top_frame, text=self.trans['dark_mode'], variable=self.theme_var, onvalue="dark", offvalue="light", command=self.toggle_theme)
        theme_switch.pack(side="left", padx=12)
        # Баннер
        self.banner = ctk.CTkLabel(self, text=self.trans['banner'], font=ctk.CTkFont(size=30, weight="bold"), text_color="#fff")
        self.banner.pack(pady=(18, 0))
        self.header = ctk.CTkLabel(self, text=self.trans['subtitle'], font=ctk.CTkFont(size=16), text_color="#aaa")
        self.header.pack(pady=(0, 18))
        # Новый layout на grid: всё в одной колонке, кнопки всегда внизу
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(padx=12, pady=(6, 0), fill="both", expand=True)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # Поле ввода
        input_frame = GlassFrame(main_frame)
        input_frame.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))
        self.add_module_label = ctk.CTkLabel(input_frame, text=self.trans['add_module'], font=ctk.CTkFont(size=14, weight="bold"), text_color="#fff")
        self.add_module_label.pack(pady=(12, 2))
        self.entry = ctk.CTkEntry(input_frame, placeholder_text="e.g. numpy pandas", height=32, font=ctk.CTkFont(size=14))
        self.entry.pack(pady=5, padx=10, fill="x")
        # Список модулей с прокруткой
        modules_frame = GlassFrame(main_frame)
        modules_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=(2, 2))
        self.selected_modules_label = ctk.CTkLabel(modules_frame, text=self.trans['selected_modules'], font=ctk.CTkFont(size=14, weight="bold"), text_color="#fff")
        self.selected_modules_label.pack(pady=(10, 0))
        self.listbox = ctk.CTkTextbox(modules_frame, height=120, font=ctk.CTkFont(family="Consolas", size=13), corner_radius=12)
        self.listbox.pack(pady=10, padx=10, fill="both", expand=True)
        self.listbox.insert("1.0", self.trans['empty'])
        self.listbox.configure(state="disabled")
        # Кнопки управления — вертикально справа
        right_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, rowspan=3, sticky="ns", padx=(8, 0), pady=0)
        self.search_btn = NeonButton(right_frame, text="🔍 PyPI", width=120, height=36, font=ctk.CTkFont(size=13), command=self.search_pypi)
        self.add_btn = NeonButton(right_frame, text=self.trans['add'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.add_module)
        self.remove_btn = NeonButton(right_frame, text=self.trans['remove'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.remove_selected)
        self.clear_btn = NeonButton(right_frame, text=self.trans['clear'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.clear_modules)
        self.copy_btn = NeonButton(right_frame, text=self.trans['copy'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.copy_modules)
        self.req_btn = NeonButton(right_frame, text=self.trans['req'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.save_requirements)
        self.help_btn = NeonButton(right_frame, text=self.trans['help'], width=120, height=36, font=ctk.CTkFont(size=13), command=self.show_help)
        for btn, tip in zip(
            [self.search_btn, self.add_btn, self.remove_btn, self.clear_btn, self.copy_btn, self.req_btn, self.help_btn],
            [self.trans['tooltip_search'], self.trans['tooltip_add'], self.trans['tooltip_remove'], self.trans['tooltip_clear'], self.trans['tooltip_copy'], self.trans['tooltip_req'], self.trans['tooltip_help']]
        ):
            btn.tooltip = ctk.CTkLabel(self, text=tip, font=ctk.CTkFont(size=12), text_color="#fff", fg_color="#222", corner_radius=6)
            btn.pack(pady=3, padx=2, fill="x")
        # Консоль-лог с прокруткой
        self.console = ctk.CTkTextbox(main_frame, height=70, font=ctk.CTkFont(family="Consolas", size=13), corner_radius=10, fg_color="#181c22", text_color="#00fff7", border_width=2, border_color="#00fff7")
        self.console.grid(row=2, column=0, sticky="ew", padx=6, pady=(2, 2))
        self.console.insert("1.0", "[LOG] Bootstrap Creator started.\n")
        self.console.configure(state="disabled")
        # Кнопки "Создать" и "Открыть папку" всегда внизу
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=6, pady=(2, 8))
        self.generate_btn = NeonButton(action_frame, text=self.trans['generate'], font=ctk.CTkFont(weight="bold"), width=180, height=40, command=self.start_generation)
        self.open_folder_btn = NeonButton(action_frame, text=self.trans['open_folder'], width=140, height=40, font=ctk.CTkFont(size=15, weight="bold"), fg_color="#23272f", text_color="#fff", command=self.open_output_folder)
        self.generate_btn.pack(side="left", padx=8, pady=8, expand=True, fill="x")
        self.open_folder_btn.pack(side="left", padx=8, pady=8, expand=True, fill="x")
        self.open_folder_btn.pack_forget()
        # Лог сборки exe
        self.build_log_frame = GlassFrame(self)
        self.build_log = ctk.CTkTextbox(self.build_log_frame, height=140, font=ctk.CTkFont(family="Consolas", size=14), corner_radius=12)
        self.build_log.pack(padx=10, pady=(8, 10), fill="x")
        self.build_log.insert("1.0", "")
        self.build_log_frame.pack_forget()
        # Прогрессбар
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", height=5, corner_radius=3, fg_color="#222", progress_color="#00fff7")
        self.progressbar.pack(fill="x", padx=60)
        self.progressbar.set(0)
        self.progressbar.pack_forget()
        # Статусная строка с иконкой
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16), text_color="#fff")
        self.status_icon = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20))
        self.status_icon.pack(pady=(0,0))
        self.status_label.pack(pady=(0, 0))

    def show_tooltip(self, btn):
        btn.tooltip.place(x=btn.winfo_rootx() - self.winfo_rootx(), y=btn.winfo_rooty() - self.winfo_rooty() - 30)
    def hide_tooltip(self, btn):
        btn.tooltip.place_forget()

    def update_list(self):
        self.listbox.configure(state="normal")
        self.listbox.delete("1.0", "end")
        if not self.selected_modules:
            self.listbox.insert("1.0", self.trans['empty'])
        else:
            for i, m in enumerate(self.selected_modules, 1):
                self.listbox.insert("end", f"{i}. {m}\n")
        self.listbox.configure(state="disabled")

    def toggle_theme(self):
        mode = self.theme_var.get()
        ctk.set_appearance_mode(mode)
        if mode == "light":
            text_color = "#222"
            btn_fg = "#f5f5f5"
            btn_hover = "#e0e0e0"
        else:
            text_color = "#fff"
            btn_fg = "#23272f"
            btn_hover = "#2d323c"
        for btn in [self.search_btn, self.add_btn, self.remove_btn, self.clear_btn, self.copy_btn, self.req_btn, self.help_btn, self.generate_btn, self.open_folder_btn]:
            btn.configure(text_color=text_color, fg_color=btn_fg, hover_color=btn_hover)
        self.banner.configure(text_color=text_color)
        self.header.configure(text_color=text_color)
        self.selected_modules_label.configure(text_color=text_color)
        self.status_label.configure(text_color=text_color)
        self.log(f"[ACTION] Changed theme to {mode}.")

    def change_language(self, lang):
        self.lang = self.lang_var.get()
        self.trans = TRANSLATIONS[self.lang]
        self.title(self.trans['title'])
        self.banner.configure(text=self.trans['banner'])
        self.header.configure(text=self.trans['subtitle'])
        self.add_module_label.configure(text=self.trans['add_module'])
        self.add_btn.configure(text=self.trans['add'])
        self.remove_btn.configure(text=self.trans['remove'])
        self.clear_btn.configure(text=self.trans['clear'])
        self.copy_btn.configure(text=self.trans['copy'])
        self.req_btn.configure(text=self.trans['req'])
        self.help_btn.configure(text=self.trans['help'])
        self.selected_modules_label.configure(text=self.trans['selected_modules'])
        self.generate_btn.configure(text=self.trans['generate'])
        self.open_folder_btn.configure(text=self.trans['open_folder'])
        tooltips = [self.trans['tooltip_search'], self.trans['tooltip_add'], self.trans['tooltip_remove'], self.trans['tooltip_clear'], self.trans['tooltip_copy'], self.trans['tooltip_req'], self.trans['tooltip_help']]
        for btn, tip in zip([self.search_btn, self.add_btn, self.remove_btn, self.clear_btn, self.copy_btn, self.req_btn, self.help_btn], tooltips):
            if hasattr(btn, 'tooltip'):
                btn.tooltip.configure(text=tip)
        self.update_list()
        self.log(f"[ACTION] Changed language to {self.lang}.")

    def add_module(self):
        module = self.entry.get().strip()
        if not module:
            messagebox.showwarning("Warning", self.trans['warning_empty'])
            self.log("[WARN] Empty module name attempted to add.")
            return
        if module in self.selected_modules:
            messagebox.showwarning("Warning", self.trans['warning_exists'])
            self.log(f"[WARN] Module already in list: {module}")
            return
        self.selected_modules.append(module)
        self.update_list()
        self.entry.delete(0, ctk.END)
        self.log(f"[ACTION] Added module: {module}")

    def remove_selected(self):
        if not self.selected_modules:
            messagebox.showwarning("Warning", self.trans['warning_no_modules'])
            self.log("[WARN] Tried to remove from empty list.")
            return
        removed = self.selected_modules.pop()
        self.update_list()
        self.log(f"[ACTION] Removed module: {removed}")

    def clear_modules(self):
        self.selected_modules.clear()
        self.update_list()
        self.log("[ACTION] Cleared module list.")

    def copy_modules(self):
        self.clipboard_clear()
        self.clipboard_append(' '.join(self.selected_modules))
        messagebox.showinfo(self.trans['copied'], self.trans['copied'])
        self.log("[ACTION] Copied module list to clipboard.")

    def save_requirements(self):
        if not self.selected_modules:
            messagebox.showwarning("Warning", self.trans['warning_no_save'])
            self.log("[WARN] Tried to save empty module list.")
            return
        with open("requirements.txt", "w", encoding="utf-8") as f:
            for m in self.selected_modules:
                f.write(m + "\n")
        messagebox.showinfo(self.trans['saved'], self.trans['saved'])
        self.log("[ACTION] Saved requirements.txt.")

    def show_status(self, text, color="#2aa44f", icon="✅"):
        self.status_label.configure(text=text, text_color=color)
        self.status_icon.configure(text=icon)
        self.after(4000, lambda: (self.status_label.configure(text=""), self.status_icon.configure(text="")))
        self.log(f"[STATUS] {text}")

    def start_generation(self):
        if not self.selected_modules:
            self.show_status("No modules selected!", color="#d33")
            messagebox.showerror("Error", "No modules selected!")
            self.log("[ERROR] Tried to generate with empty module list.")
            return
        self.progressbar.pack(fill="x", padx=20)
        self.generate_btn.configure(state="disabled")
        threading.Thread(target=self.generate_with_animation, daemon=True).start()
        self.log("[ACTION] Started generation.")

    def generate_with_animation(self):
        for i in range(101):
            time.sleep(0.02)
            self.queue.put(("update_progress", i))
        self.queue.put(("show_dialog",))

    def show_author_dialog(self):
        author = simpledialog.askstring(self.trans['signature'], self.trans['signature'], parent=self)
        if not author:
            self.show_status(self.trans['signature_required'], color="#d33", icon="⚠️")
            messagebox.showwarning("Warning", self.trans['signature_required'])
            self.reset_generation_ui()
            self.log("[WARN] Generation cancelled: no signature.")
            return
        try:
            modules_repr = repr(self.selected_modules)
            author_safe = author.replace('"', '\"').replace("'", "\\'")
            with open("bootstrap_output.py", "w", encoding="utf-8") as f:
                f.write(f"# Created by: {author_safe}\n")
                f.write("import sys\n")
                f.write("import os\n")
                f.write("import importlib.util\n")
                f.write("import random\n")
                f.write("def is_frozen():\n")
                f.write("    return getattr(sys, 'frozen', False)\n\n")
                f.write("def supports_ansi():\n")
                f.write("    if sys.platform != 'win32':\n")
                f.write("        return True\n")
                f.write("    return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ or os.environ.get('TERM_PROGRAM') == 'vscode'\n\n")
                f.write("USE_COLOR = supports_ansi()\n")
                f.write("def c(text, code):\n")
                f.write("    return f'\\033[{code}m{text}\\033[0m' if USE_COLOR else text\n\n")
                f.write("def ensure_pyfiglet():\n")
                f.write("    try:\n")
                f.write("        import pyfiglet\n")
                f.write("    except ImportError:\n")
                f.write("        import subprocess\n")
                f.write("        print('Installing pyfiglet for beautiful banners...')\n")
                f.write("        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyfiglet'])\n")
                f.write("        import pyfiglet\n\n")
                f.write("if is_frozen():\n")
                f.write("    print('[!] This installer .exe cannot install modules because it is not running under Python.')\n")
                f.write("    print('Please use the .py version or run this .exe from a Python environment.')\n")
                f.write("    input('Press Enter to exit...')\n")
                f.write("    sys.exit(0)\n\n")
                f.write("ensure_pyfiglet()\n")
                f.write("from pyfiglet import figlet_format\n")
                f.write("def print_banner():\n")
                f.write("    banner = figlet_format('BOOTSTRAP', font='slant')\n")
                f.write("    print(c(banner, '96'))\n")
                f.write("print_banner()\n")
                f.write(f"print(c('Created by: {author_safe}', '94'))\n")
                f.write("# Thanks and contacts (EN only)\n")
                f.write("print(c('Author: Fal1sev4n | Discord: https://discord.gg/CZtqqx5phE', '94'))\n")
                f.write("# Easter egg: random quote (EN only)\n")
                f.write("quotes = [\n")
                f.write("    'Code with soul and everything will work out!',\n")
                f.write("    'Python is easy And you are awesome!',\n")
                f.write("    'May bugs stay away from your code!',\n")
                f.write("    'Fal1sev4n wishes you luck in coding!',\n")
                f.write("    'The best bootstrap is the one that works on the first try!',\n")
                f.write("    'Keep calm and pip install!',\n")
                f.write("    'Every bug is a lesson',\n")
                f.write("    'Automate the boring stuff',\n")
                f.write("    'Good code is its own best documentation',\n")
                f.write("    'Do not repeat yourself unless it is fun',\n")
                f.write("    'If it works do not touch it If it does not debug it',\n")
                f.write("    'Real coders use virtual environments',\n")
                f.write("    'One more module one more superpower',\n")
                f.write("    'Your script your rules!',\n")
                f.write("]\n")
                f.write("print(c(random.choice(quotes), '93'))\n")
                f.write("# ASCII-art with nickname\n")
                f.write("print(c(figlet_format('Fal1sev4n', font='mini'), '95'))\n")
                f.write("import platform\n")
                f.write("print(c(f'Python: {platform.python_version()} | OS: {platform.system()} {platform.release()}', '93'))\n")
                f.write("print(c('Starting... ⏳', '96'))\n")
                f.write("import time\n")
                f.write("time.sleep(1)\n\n")
                f.write("def is_module_installed(module_name):\n")
                f.write("    return importlib.util.find_spec(module_name) is not None\n\n")
                f.write(f"modules = {modules_repr}\n\n")
                f.write("print(c('\\n🚀 Installing modules:\\n', '96'))\n")
                f.write("for m in modules:\n")
                f.write("    if is_module_installed(m):\n")
                f.write("        print(c(f'✅ Module {m} already installed.', '92'))\n")
                f.write("    else:\n")
                f.write("        try:\n")
                f.write("            import subprocess\n")
                f.write("            subprocess.check_call([sys.executable, '-m', 'pip', 'install', m])\n")
                f.write('            print(c(f"✅ Module \'{m}\' installed successfully.", \'96\'))\n')
                f.write("        except Exception as e:\n")
                f.write('            print(c(f"❌ Error installing \'{m}\': {e}", \'91\'))\n')
                f.write("\n")
                f.write("print(c('\\n🎉 All done! Thank you for using Bootstrap Universal!', '95'))\n")
                f.write("input('\\nPress Enter to exit...')\n")
            self.queue.put(("show_message", "Success", self.trans['success']))
            self.queue.put(("show_open_folder",))
            self.log("[SUCCESS] bootstrap_output.py created.")
        except Exception as e:
            self.queue.put(("show_message", "Error", f"{self.trans['error']} {str(e)}"))
            self.log(f"[ERROR] Failed to create bootstrap_output.py: {e}")
        self.reset_generation_ui()

    def reset_generation_ui(self):
        self.progressbar.set(0)
        self.progressbar.pack_forget()
        self.generate_btn.configure(state="normal")

    def open_output_folder(self):
        folder = os.path.abspath(os.path.dirname("bootstrap_output.py"))
        if os.name == 'nt':
            os.startfile(folder)
        else:
            webbrowser.open(f'file://{folder}')
        self.log("[ACTION] Opened output folder.")

    def search_pypi(self):
        module = self.entry.get().strip()
        if not module:
            msg = self.trans['pypi_empty']
            messagebox.showinfo("PyPI Search", msg)
            self.log(f"[PyPI] {msg}")
            return
        url = f"https://pypi.org/project/{module}/"
        webbrowser.open(url)
        self.log(f"[PyPI] Opened: {url}")

    def show_help(self):
        msg = self.trans['help_text']
        messagebox.showinfo(self.trans['help'], msg)
        self.log("[ACTION] Opened help window.")

    def show_info(self):
        msg = self.trans['info']
        messagebox.showinfo(self.trans['info_title'], msg)

    def log(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = BootstrapCreator()
    app.mainloop() 

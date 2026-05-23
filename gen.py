#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import itertools

class WordlistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Wordlist Matrix Suite")
        self.root.geometry("1100x680")  # Expanded horizontally, compressed vertically
        self.root.resizable(True, True)
        
        self.is_running = False
        self.queued_files = []
        
        self.root.report_callback_exception = self.handle_tkinter_runtime_anomaly
        self.apply_modern_theme()
        
        # Main Layout Container
        main_container = ttk.Frame(self.root, style="Main.TFrame")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header Brand Block
        header_frame = ttk.Frame(main_container, style="Main.TFrame")
        header_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(header_frame, text="WORDLIST MATRIX SUITE", style="Header.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Professional-grade lexicon mutation and combinatorial stitch core engine.", style="Subheader.TLabel").pack(anchor="w", pady=(1, 0))
        
        # Notebook for Tabbed Navigation
        self.notebook = ttk.Notebook(main_container, style="Modern.TNotebook")
        self.notebook.pack(fill="both", expand=True, pady=(0, 10))
        
        self.setup_mutation_tab()
        self.setup_combiner_tab()
        self.setup_progress_frame(main_container)

    def apply_modern_theme(self):
        """Injects a premium dark/slate interface style overrides into Tkinter."""
        self.root.configure(bg="#111827") 
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        BG_MAIN = "#111827"
        BG_SURFACE = "#1f2937"
        BG_INPUT = "#374151"
        BORDER_COLOR = "#4b5563"
        ACCENT_CYAN = "#06b6d4"
        TEXT_MUTED = "#9ca3af"
        
        self.style.configure("Main.TFrame", background=BG_MAIN)
        self.style.configure("Surface.TFrame", background=BG_SURFACE)
        
        self.style.configure("Header.TLabel", background=BG_MAIN, foreground="#f3f4f6", font=("Segoe UI", 14, "bold"))
        self.style.configure("Subheader.TLabel", background=BG_MAIN, foreground=TEXT_MUTED, font=("Segoe UI", 9))
        self.style.configure("TLabel", background=BG_SURFACE, foreground="#f3f4f6", font=("Segoe UI", 9))
        self.style.configure("Muted.TLabel", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 9, "italic"))
        self.style.configure("Bold.TLabel", background=BG_SURFACE, foreground="#f3f4f6", font=("Segoe UI", 9, "bold"))
        self.style.configure("StatusHead.TLabel", background=BG_MAIN, foreground="#f3f4f6", font=("Segoe UI", 10, "bold"))
        self.style.configure("StatusBody.TLabel", background=BG_MAIN, foreground=TEXT_MUTED, font=("Segoe UI", 9))
        
        self.style.configure("Card.TLabelframe", background=BG_SURFACE, bordercolor=BORDER_COLOR, darkcolor=BG_SURFACE, lightcolor=BG_SURFACE, relief="solid", borderwidth=1)
        self.style.configure("Card.TLabelframe.Label", background=BG_SURFACE, foreground=ACCENT_CYAN, font=("Segoe UI", 10, "bold"))
        
        self.style.configure("TEntry", fieldbackground=BG_INPUT, foreground="#ffffff", bordercolor=BORDER_COLOR, lightcolor=BG_INPUT, darkcolor=BG_INPUT, insertcolor="#ffffff", padding=4)
        self.style.map("TEntry", bordercolor=[("focus", ACCENT_CYAN)])
        
        self.style.configure("TButton", background=BG_INPUT, foreground="#ffffff", bordercolor=BORDER_COLOR, font=("Segoe UI", 9, "bold"), padding=(8, 4), relief="flat")
        self.style.map("TButton", background=[("active", "#4b5563"), ("disabled", "#1f2937")], foreground=[("disabled", "#6b7280")])
        
        self.style.configure("Action.TButton", background=ACCENT_CYAN, foreground="#111827", font=("Segoe UI", 10, "bold"), padding=(12, 6), relief="flat")
        self.style.map("Action.TButton", background=[("active", "#22d3ee"), ("disabled", "#1f2937")], foreground=[("disabled", "#6b7280")])
        
        self.style.configure("Danger.TButton", background="#ef4444", foreground="#ffffff", font=("Segoe UI", 9, "bold"), padding=(8, 4), relief="flat")
        self.style.map("Danger.TButton", background=[("active", "#f87171"), ("disabled", "#1f2937")])

        self.style.configure("Modern.TNotebook", background=BG_MAIN, bordercolor=BORDER_COLOR, borderwidth=1)
        self.style.configure("Modern.TNotebook.Tab", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 9, "bold"), padding=(12, 5), borderwidth=0)
        self.style.map("Modern.TNotebook.Tab", background=[("selected", ACCENT_CYAN)], foreground=[("selected", "#111827")])
        
        self.style.configure("TCheckbutton", background=BG_SURFACE, foreground="#f3f4f6")
        self.style.map("TCheckbutton", background=[("active", BG_SURFACE)], foreground=[("active", "#ffffff")])
        self.style.configure("TRadiobutton", background=BG_SURFACE, foreground="#f3f4f6")
        self.style.map("TRadiobutton", background=[("active", BG_SURFACE)], foreground=[("active", "#ffffff")])
        
        self.style.configure("Modern.Horizontal.TProgressbar", thickness=8, bordercolor=BG_MAIN, troughcolor=BG_SURFACE, background=ACCENT_CYAN)

    def handle_tkinter_runtime_anomaly(self, exc, val, tb):
        error_msg = f"Critical Engine Exception:\nType: {exc.__name__}\nDetails: {val}"
        self.show_error_popup(error_msg)
        self.unlock_ui()

    # -------------------------------------------------------------------------
    # TAB 1: MUTATION ENGINE (SIDE-BY-SIDE SPLIT LAYOUT)
    # -------------------------------------------------------------------------
    def setup_mutation_tab(self):
        tab1 = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab1, text="  Mutation Engine  ")
        
        # Left Panel (Settings Matrix) & Right Panel (Sources & Actions)
        left_panel = ttk.Frame(tab1, style="Main.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        right_panel = ttk.Frame(tab1, style="Main.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        # --- LEFT PANEL CONTENTS ---
        limit_frame = ttk.LabelFrame(left_panel, text=" Processing Range & Volume Control ", style="Card.TLabelframe", padding=10)
        limit_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(limit_frame, text="Base Word Constraint Strategy:", style="Bold.TLabel").pack(anchor="w", pady=(0, 2))
        self.limit_type = tk.StringVar(value="capped")
        row1 = ttk.Frame(limit_frame, style="Surface.TFrame")
        row1.pack(fill="x", pady=2)
        self.limit_rd1 = ttk.Radiobutton(row1, text="Limit to top entries:", variable=self.limit_type, value="capped", command=self.toggle_limit_entry)
        self.limit_rd1.pack(side="left")
        self.limit_val_var = tk.StringVar(value="1000")
        self.limit_entry = ttk.Entry(row1, textvariable=self.limit_val_var, width=6)
        self.limit_entry.pack(side="left", padx=5)
        ttk.Radiobutton(row1, text="Scan entire file", variable=self.limit_type, value="all", command=self.toggle_limit_entry).pack(side="left", padx=10)

        ttk.Label(limit_frame, text="Generation Break Limit:", style="Bold.TLabel").pack(anchor="w", pady=(8, 2))
        self.mutate_out_type = tk.StringVar(value="all")
        row2 = ttk.Frame(limit_frame, style="Surface.TFrame")
        row2.pack(fill="x", pady=2)
        ttk.Radiobutton(row2, text="Exhaustive", variable=self.mutate_out_type, value="all", command=self.toggle_out_limit_entry).pack(side="left")
        ttk.Radiobutton(row2, text="Stop at lines:", variable=self.mutate_out_type, value="capped", command=self.toggle_out_limit_entry).pack(side="left", padx=(15, 5))
        self.mutate_out_max_var = tk.StringVar(value="100000")
        self.mutate_out_entry = ttk.Entry(row2, textvariable=self.mutate_out_max_var, width=10, state="disabled")
        self.mutate_out_entry.pack(side="left")

        human_frame = ttk.LabelFrame(left_panel, text=" Intelligence Heuristics ", style="Card.TLabelframe", padding=10)
        human_frame.pack(fill="x", pady=10)
        
        self.use_human_logic = tk.BooleanVar(value=True)
        ttk.Checkbutton(human_frame, text="Enforce Advanced Human Behavior Modeling", variable=self.use_human_logic, command=self.toggle_human_mode).pack(anchor="w")
        self.human_hint_lbl = ttk.Label(human_frame, text="Active: Selective leetspeak transforms and logical anchors.", style="Muted.TLabel")
        self.human_hint_lbl.pack(anchor="w", padx=20, pady=(1, 6))
        
        self.deep_permutations = tk.BooleanVar(value=False)
        ttk.Checkbutton(human_frame, text="Enable Multi-Pass Permutations Array Matrix", variable=self.deep_permutations).pack(anchor="w")
        ttk.Label(human_frame, text="Warning: Brute-forces orders. Yields exponential sizes.", style="Muted.TLabel").pack(anchor="w", padx=20, pady=(1, 0))

        # --- RIGHT PANEL CONTENTS ---
        file_frame = ttk.LabelFrame(right_panel, text=" Data Source ", style="Card.TLabelframe", padding=10)
        file_frame.pack(fill="x", pady=(0, 10))
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var).pack(side="left", padx=(0, 10), expand=True, fill="x")
        ttk.Button(file_frame, text="Browse File", command=lambda: self.browse_file(self.file_path_var)).pack(side="right")

        rules_frame = ttk.LabelFrame(right_panel, text=" Rule Matrices Injection Configuration ", style="Card.TLabelframe", padding=10)
        rules_frame.pack(fill="both", expand=True, pady=10)
        
        ttk.Label(rules_frame, text="Numeric Tail Generation:", style="Bold.TLabel").pack(anchor="w", pady=(0, 2))
        self.num_strategy = tk.StringVar(value="range")
        strat_row = ttk.Frame(rules_frame, style="Surface.TFrame")
        strat_row.pack(fill="x", pady=2)
        ttk.Radiobutton(strat_row, text="Integer Range Sequence", variable=self.num_strategy, value="range", command=self.toggle_number_strategy).pack(side="left")
        ttk.Radiobutton(strat_row, text="Explicit Custom Array", variable=self.num_strategy, value="list", command=self.toggle_number_strategy).pack(side="left", padx=15)
        
        self.num_config_frame = ttk.Frame(rules_frame, style="Surface.TFrame")
        self.num_config_frame.pack(fill="x", pady=6)
        self.render_number_range_inputs()
        
        ttk.Label(rules_frame, text="Special Symbols Matrix Array (Comma Parsed):", style="Bold.TLabel").pack(anchor="w", pady=(4, 2))
        self.symbols_var = tk.StringVar(value="!, @, #, $")
        ttk.Entry(rules_frame, textvariable=self.symbols_var).pack(fill="x", pady=2)

        # Lower Action Row across the tab base
        ctrl_action_row = ttk.Frame(right_panel, style="Main.TFrame")
        ctrl_action_row.pack(fill="x", side="bottom", pady=(10, 0))
        self.mutate_sort_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctrl_action_row, text="Alphabetize target output (A-Z Fast Timsort)", variable=self.mutate_sort_var).pack(side="left")
        self.mutate_start_btn = ttk.Button(ctrl_action_row, text="Execute Mutation Engine", style="Action.TButton", command=self.start_mutation)
        self.mutate_start_btn.pack(side="right")

    def render_number_range_inputs(self):
        for widget in self.num_config_frame.winfo_children(): widget.destroy()
        ttk.Label(self.num_config_frame, text="Start:").pack(side="left", padx=(0, 4))
        self.num_start_var = tk.StringVar(value="0")
        ttk.Entry(self.num_config_frame, textvariable=self.num_start_var, width=6).pack(side="left")
        ttk.Label(self.num_config_frame, text="End Bound:").pack(side="left", padx=(10, 4))
        self.num_end_var = tk.StringVar(value="100")
        ttk.Entry(self.num_config_frame, textvariable=self.num_end_var, width=6).pack(side="left")

    def render_number_list_inputs(self):
        for widget in self.num_config_frame.winfo_children(): widget.destroy()
        self.numbers_var = tk.StringVar(value="123, 1234, 2025, 2026")
        ttk.Entry(self.num_config_frame, textvariable=self.numbers_var).pack(fill="x", expand=True)

    def toggle_number_strategy(self):
        if self.num_strategy.get() == "range": self.render_number_range_inputs()
        else: self.render_number_list_inputs()

    # -------------------------------------------------------------------------
    # TAB 2: MULTI-MATRIX COMBINER (COMPACT DOUBLE-COLUMN VIEW)
    # -------------------------------------------------------------------------
    def setup_combiner_tab(self):
        tab2 = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab2, text="  Multi-Matrix Combiner  ")
        
        left_panel = ttk.Frame(tab2, style="Main.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        right_panel = ttk.Frame(tab2, style="Main.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        # --- LEFT PANEL: SOURCE FILES & TUNING ---
        base_file_frame = ttk.LabelFrame(left_panel, text=" Primary Base Matrix Target (Part 1) ", style="Card.TLabelframe", padding=10)
        base_file_frame.pack(fill="x", pady=(0, 10))
        self.comb_f1_var = tk.StringVar()
        f1_row = ttk.Frame(base_file_frame, style="Surface.TFrame")
        f1_row.pack(fill="x")
        ttk.Entry(f1_row, textvariable=self.comb_f1_var).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ttk.Button(f1_row, text="Browse Base", command=lambda: self.browse_file(self.comb_f1_var)).pack(side="right")

        tune_frame = ttk.LabelFrame(left_panel, text=" Pipeline Formatting Metrics ", style="Card.TLabelframe", padding=10)
        tune_frame.pack(fill="x", pady=10)
        
        row_glue = ttk.Frame(tune_frame, style="Surface.TFrame")
        row_glue.pack(fill="x", pady=(0, 8))
        ttk.Label(row_glue, text="Delimiting Join Glue Character:").pack(side="left", padx=(0, 5))
        self.glue_var = tk.StringVar(value="")
        ttk.Entry(row_glue, textvariable=self.glue_var, width=5).pack(side="left")

        self.comb_out_type = tk.StringVar(value="all")
        ttk.Radiobutton(tune_frame, text="Process all cross-joins completely", variable=self.comb_out_type, value="all", command=self.toggle_comb_out_entry).pack(anchor="w", pady=2)
        
        row_cap = ttk.Frame(tune_frame, style="Surface.TFrame")
        row_cap.pack(fill="x", pady=2)
        ttk.Radiobutton(row_cap, text="Enforce cut-off at lines:", variable=self.comb_out_type, value="capped", command=self.toggle_comb_out_entry).pack(side="left")
        self.comb_out_max_var = tk.StringVar(value="100000")
        self.comb_out_entry = ttk.Entry(row_cap, textvariable=self.comb_out_max_var, width=10, state="disabled")
        self.comb_out_entry.pack(side="left", padx=5)

        # --- RIGHT PANEL: QUEUE TRACK ---
        secondary_frame = ttk.LabelFrame(right_panel, text=" Secondary Append Targets Queue (Part 2) ", style="Card.TLabelframe", padding=10)
        secondary_frame.pack(fill="both", expand=True, pady=(0, 10))

        ctrl_row = ttk.Frame(secondary_frame, style="Surface.TFrame")
        ctrl_row.pack(fill="x", pady=(0, 6))
        ttk.Button(ctrl_row, text="+ Add File", command=self.add_file_to_queue).pack(side="left", padx=(0, 2))
        ttk.Button(ctrl_row, text="- Drop", command=self.remove_file_from_queue).pack(side="left", padx=2)
        ttk.Button(ctrl_row, text="Clear All", command=self.clear_file_queue).pack(side="left", padx=2)

        list_frame = ttk.Frame(secondary_frame, style="Surface.TFrame")
        list_frame.pack(fill="both", expand=True, pady=2)
        
        self.queue_listbox = tk.Listbox(list_frame, height=4, selectmode="browse", background="#374151", foreground="#ffffff", borderwidth=1, highlightthickness=0, font=("Segoe UI", 9))
        self.queue_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.queue_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.queue_listbox.config(yscrollcommand=scrollbar.set)

        custom_row = ttk.Frame(secondary_frame, style="Surface.TFrame")
        custom_row.pack(fill="x", pady=(8, 0))
        ttk.Label(custom_row, text="Custom Manual String Injectors (Comma Split):", style="Bold.TLabel").pack(anchor="w", pady=(0, 2))
        self.custom_words_var = tk.StringVar(value="admin, root, 2026")
        ttk.Entry(custom_row, textvariable=self.custom_words_var).pack(fill="x")

        ctrl_action_row2 = ttk.Frame(right_panel, style="Main.TFrame")
        ctrl_action_row2.pack(fill="x", side="bottom", pady=(10, 0))
        self.comb_sort_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctrl_action_row2, text="Alphabetize target output (A-Z)", variable=self.comb_sort_var).pack(side="left")
        self.comb_start_btn = ttk.Button(ctrl_action_row2, text="Run Combinatorial Stitch", style="Action.TButton", command=self.start_combining)
        self.comb_start_btn.pack(side="right")

    # -------------------------------------------------------------------------
    # MANAGEMENT ENGINE BACKEND LOGIC HOOKS
    # -------------------------------------------------------------------------
    def add_file_to_queue(self):
        filenames = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not filenames: return
        for file in filenames:
            if file and os.path.exists(file) and file not in self.queued_files:
                self.queued_files.append(file)
                self.queue_listbox.insert(tk.END, f" 📄 {os.path.basename(file)}")

    def remove_file_from_queue(self):
        selected_indices = self.queue_listbox.curselection()
        if not selected_indices: return
        idx = selected_indices[0]
        self.queue_listbox.delete(idx)
        self.queued_files.pop(idx)

    def clear_file_queue(self):
        self.queue_listbox.delete(0, tk.END)
        self.queued_files.clear()

    def toggle_limit_entry(self):
        self.limit_entry.config(state="disabled" if self.limit_type.get() == "all" else "normal")

    def toggle_out_limit_entry(self):
        self.mutate_out_entry.config(state="disabled" if self.mutate_out_type.get() == "all" else "normal")

    def toggle_comb_out_entry(self):
        self.comb_out_entry.config(state="disabled" if self.comb_out_type.get() == "all" else "normal")

    def toggle_human_mode(self):
        if self.use_human_logic.get():
            self.human_hint_lbl.config(text="Active: Selective leetspeak transforms and logical anchors.")
        else:
            self.human_hint_lbl.config(text="Inactive: Basic matrix expansion logic enforced without custom filters.")

    def browse_file(self, target_var):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename: target_var.set(filename)

    def setup_progress_frame(self, parent):
        progress_frame = ttk.Frame(parent, style="Main.TFrame")
        progress_frame.pack(fill="x", side="bottom", pady=(5, 0))
        
        self.status_var = tk.StringVar(value="Status Target Architecture: Standby Engine Initialization Ready.")
        ttk.Label(progress_frame, textvariable=self.status_var, style="StatusHead.TLabel").pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode="determinate", style="Modern.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=4)
        
        control_subrow = ttk.Frame(progress_frame, style="Main.TFrame")
        control_subrow.pack(fill="x")
        self.details_var = tk.StringVar(value="Metrics Processing System: Idle Vitals Track.")
        ttk.Label(control_subrow, textvariable=self.details_var, style="StatusBody.TLabel").pack(side="left", fill="x", expand=True)
        
        self.cancel_btn = ttk.Button(control_subrow, text="Terminate", style="Danger.TButton", command=self.cancel_processing, state="disabled")
        self.cancel_btn.pack(side="right")

    def cancel_processing(self):
        if self.is_running:
            self.is_running = False
            self.status_var.set("Status Target Architecture: Sending interruption matrix vector catch break signal...")

    def show_error_popup(self, error_msg):
        messagebox.showerror("Execution Matrix Failure", f"An anomaly occurred:\n{error_msg}")

    def lock_ui(self):
        self.is_running = True
        self.mutate_start_btn.config(state="disabled")
        self.comb_start_btn.config(state="disabled")
        self.cancel_btn.config(state="enabled")
        self.progress_bar["value"] = 0

    def unlock_ui(self):
        self.is_running = False
        self.mutate_start_btn.config(state="normal")
        self.comb_start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def update_ui_progress(self, percent, lines, processed):
        if self.is_running:
            self.progress_bar["value"] = percent
            self.details_var.set(f"Base Steps Done: {processed:,}  |  Temporary Buffer lines written: {lines:,}")

    def finalize_execution(self, base, final_lines, thread_exception=None):
        self.unlock_ui()
        if thread_exception:
            self.status_var.set("Status Target Architecture: Interrupted by Pipeline Crash Anomaly Vector.")
            self.show_error_popup(thread_exception)
            return

        if not self.is_running:
            self.status_var.set("Status Target Architecture: Process execution intentionally fractured.")
            messagebox.showwarning("Execution Aborted", f"Process caught force-stop signal.\nLines dumped to track: {final_lines:,}")
        else:
            self.progress_bar["value"] = 100
            self.status_var.set("Status Target Architecture: Tasks Finished.")
            self.details_var.set(f"Metrics: Completed. System Target Output contains {final_lines:,} structured entities.")
            messagebox.showinfo("Suite Execution Core Complete", f"Success details profile matrix output validation complete!\nTotal Row Payload Volume: {final_lines:,} rows.")

    def sort_file_inplace(self, target_filepath):
        self.status_var.set("Status Target Architecture: Sorting final lexicon payload matrix (A-Z Timsort)...")
        if not os.path.exists(target_filepath): return
        try:
            with open(target_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            lines.sort()
            with open(target_filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            raise RuntimeError(f"Sort verification IO lock error allocation context fault: {str(e)}")

    def generate_human_variations(self, base_word, custom_numbers, symbols, deep_mode=False):
        variations = set()
        casings = [base_word, base_word.capitalize(), base_word.lower(), base_word.upper()]
        
        leet_map = {'a': '4', 'A': '4', 'e': '3', 'E': '3', 'i': '1', 'I': '1', 'o': '0', 'O': '0', 's': '5', 'S': '5', 't': '7', 'T': '7'}
        casings.append("".join(leet_map.get(c, c) for c in base_word.capitalize()))
        casings.append("".join(leet_map.get(c, c) for c in base_word.lower()))
        casings = list(set(casings))

        target_numbers = list(custom_numbers)
        for anchor in ["123", "1234", "1111", "2026"]:
            if anchor not in target_numbers: target_numbers.append(anchor)

        for base in casings:
            if not base: continue
            variations.add(base)
            
            if deep_mode:
                for num in target_numbers:
                    for sym in symbols:
                        for p in itertools.permutations([base, num, sym]):
                            variations.add("".join(p))
                        variations.add(f"{num}{base}")
                        variations.add(f"{sym}{base}")
                        variations.add(f"{base}{num}")
                        variations.add(f"{base}{sym}")
            else:
                for sym in symbols:
                    variations.add(f"{base}{sym}")
                    variations.add(f"{sym}{base}")
                for num in target_numbers:
                    variations.add(f"{base}{num}")
                    for sym in symbols:
                        variations.add(f"{base}{num}{sym}")
                        variations.add(f"{base}{sym}{num}")
                        
        return variations

    # -------------------------------------------------------------------------
    # WORKER 1: MUTATION GENERATOR (THREAD PROTECTED)
    # -------------------------------------------------------------------------
    def start_mutation(self):
        if self.is_running: return
        filepath = self.file_path_var.get().strip()
        if not filepath or not os.path.exists(filepath):
            messagebox.showerror("Validation Error", "Target profile base dictionary data source tracking missing."); return
            
        syms = [s.strip() for s in self.symbols_var.get().split(",") if s.strip()] or [""]
        human_optimized = self.use_human_logic.get()
        deep_mode_active = self.deep_permutations.get()
        should_sort = self.mutate_sort_var.get()
        
        numbers = []
        if self.num_strategy.get() == "range":
            try:
                start_raw = self.num_start_var.get().strip()
                end_raw = self.num_end_var.get().strip()
                start_val, end_val = int(start_raw), int(end_raw)
                if start_val > end_val: raise ValueError
                pad_len = len(start_raw) if start_raw.startswith('0') and len(start_raw) > 1 else 0
                for i in range(start_val, end_val + 1):
                    numbers.append(str(i).zfill(pad_len) if pad_len > 0 else str(i))
            except ValueError:
                messagebox.showerror("Validation Range Error", "Bounds tracking variables out of integer sync scope alignment."); return
        else:
            numbers = [n.strip() for n in self.numbers_var.get().strip().split(",") if n.strip()] or [""]

        limit = int(self.limit_val_var.get()) if self.limit_type.get() == "capped" else None
        max_output = int(self.mutate_out_max_var.get()) if self.mutate_out_type.get() == "capped" else None

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not save_path: return

        self.lock_ui()
        threading.Thread(target=self.mutation_worker, args=(filepath, save_path, limit, max_output, numbers, syms, human_optimized, deep_mode_active, should_sort), daemon=True).start()

    def mutation_worker(self, infile_path, outfile_path, limit, max_output, numbers, symbols, human_optimized, deep_mode_active, should_sort):
        base_count, lines_written = 0, 0
        total_lines_est = limit if limit else 5000
        error_context = None
        self.status_var.set("Status Target Architecture: Permutating structured matrix into disk buffer stream...")
        
        try:
            with open(infile_path, 'r', encoding='utf-8', errors='ignore') as infile, open(outfile_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    if not self.is_running or (max_output and lines_written >= max_output): break
                    cleaned = line.strip()
                    if cleaned:
                        if human_optimized:
                            local_set = self.generate_human_variations(cleaned, numbers, symbols, deep_mode_active)
                        else:
                            local_set = set()
                            variants = {cleaned, cleaned.lower(), cleaned.upper(), cleaned.capitalize()}
                            for v in variants:
                                local_set.add(v)
                                if deep_mode_active:
                                    for num in numbers:
                                        for sym in symbols:
                                            for p in itertools.permutations([v, num, sym]): local_set.add("".join(p))
                                else:
                                    for num in numbers: local_set.add(f"{v}{num}")
                                    for sym in symbols: local_set.add(f"{v}{sym}")
                                    for num in numbers:
                                        for sym in symbols: local_set.add(f"{v}{num}{sym}")
                        
                        for item in local_set:
                            if max_output and lines_written >= max_output: break
                            if item:
                                outfile.write(f"{item}\n")
                                lines_written += 1
                            
                        base_count += 1
                        if base_count % 100 == 0 or base_count == total_lines_est:
                            pct = min(99, int((base_count / total_lines_est) * 99))
                            self.root.after(0, self.update_ui_progress, pct, lines_written, base_count)
                    if limit and base_count >= limit: break
            
            if should_sort and self.is_running and lines_written > 0: self.sort_file_inplace(outfile_path)
        except Exception as err: error_context = str(err)
            
        self.root.after(0, self.finalize_execution, base_count, lines_written, error_context)

    # -------------------------------------------------------------------------
    # WORKER 2: RUN MULTI-COMBINATORIAL STITCH (THREAD PROTECTED)
    # -------------------------------------------------------------------------
    def start_combining(self):
        if self.is_running: return
        f1 = self.comb_f1_var.get().strip()
        glue = self.glue_var.get()
        should_sort = self.comb_sort_var.get()

        if not f1 or not os.path.exists(f1):
            messagebox.showerror("Validation Error", "Primary Part 1 matrix source tracking verify failed."); return

        custom_words = [w.strip() for w in self.custom_words_var.get().split(",") if w.strip()]
        if not self.queued_files and not custom_words:
            messagebox.showerror("Validation Error", "Secondary targets elements arrays empty."); return

        max_output = int(self.comb_out_max_var.get()) if self.comb_out_type.get() == "capped" else None
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not save_path: return

        self.lock_ui()
        threading.Thread(target=self.multi_combiner_worker, args=(f1, list(self.queued_files), custom_words, glue, save_path, max_output, should_sort), daemon=True).start()

    def multi_combiner_worker(self, f1_path, file_queue, custom_words, glue, outfile_path, max_output, should_sort):
        lines_written, primary_processed = 0, 0
        error_context = None
        self.status_var.set("Status Target Architecture: Stitching compound array sequence combinations onto target profile space...")
        
        try:
            with open(f1_path, 'r', encoding='utf-8', errors='ignore') as f1: total_f1 = sum(1 for _ in f1) or 1
            with open(outfile_path, 'w', encoding='utf-8') as outfile, open(f1_path, 'r', encoding='utf-8', errors='ignore') as file1:
                for line1 in file1:
                    if not self.is_running or (max_output and lines_written >= max_output): break
                    word1 = line1.strip()
                    if not word1: continue
                    
                    for word2 in custom_words:
                        if max_output and lines_written >= max_output: break
                        outfile.write(f"{word1}{glue}{word2}\n"); lines_written += 1
                    
                    for secondary_file in file_queue:
                        if max_output and lines_written >= max_output: break
                        if not os.path.exists(secondary_file): continue
                        with open(secondary_file, 'r', encoding='utf-8', errors='ignore') as file2:
                            for line2 in file2:
                                if max_output and lines_written >= max_output: break
                                word2 = line2.strip()
                                if word2: outfile.write(f"{word1}{glue}{word2}\n"); lines_written += 1
                    
                    primary_processed += 1
                    if primary_processed % 500 == 0 or primary_processed == total_f1:
                        pct = min(99, int((primary_processed / total_f1) * 99))
                        self.root.after(0, self.update_ui_progress, pct, lines_written, primary_processed)
            
            if should_sort and self.is_running and lines_written > 0: self.sort_file_inplace(outfile_path)
        except Exception as err: error_context = str(err)

        self.root.after(0, self.finalize_execution, primary_processed, lines_written, error_context)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = WordlistApp(root)
        root.mainloop()
    except Exception as launch_fault:
        print(f"[!] System Init Crash Fault Vector Anomaly: {str(launch_fault)}")

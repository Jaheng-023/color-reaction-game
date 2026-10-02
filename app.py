import random
import tkinter as tk
from tkinter import ttk, messagebox

from constants import (
    WINDOW_TITLE, GAME_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_PRIMARY, COLOR_ACCENT, COLOR_PINK, COLOR_BORDER,
    GAME_COLORS, FONT_BRAND, FONT_TITLE, FONT_HEADING, FONT_BODY, FONT_WORD, FONT_TIP, FUNNY_TIP,
    TOTAL_TRIALS, SIMPLE_TRIALS, MIN_DELAY_MS, MAX_DELAY_MS, TIMEOUT_MS,
    FEEDBACK_DURATION_MS, AGE_GROUPS
)
from widgets import Card, RoundedButton, ColorSwatchButton, TrialHistoryStack, LiveScoringWidget
from game_logic import GameLogic
from sound import play_sound
from data_manager import save_data

class ColorReactionGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=COLOR_BG)
        self.resizable(False, False)

        self.game_logic = None
        self.swatch_buttons = []
        self.position_to_color = {}
        self.history_stack = None
        self.scoring_widget = None
        self.timeout_timer = None
        self.delay_timer = None
        self.buttons_enabled = False
        self.waiting_for_stimulus = False
        self.transition_shown = False
        self.age_group = ""
        self.experience = ""

        self.container = tk.Frame(self, bg=COLOR_BG)
        self.container.pack(fill="both", expand=True)

        self.bind("<Key>", self.handle_keypress)
        self.show_registration_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_registration_screen(self):
        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=30, padx=60)

        # Prominent ColorRec Brand Header
        brand_logo = tk.Label(card, text=f"🎮 {GAME_NAME}", font=FONT_BRAND, fg=COLOR_PRIMARY, bg=COLOR_CARD)
        brand_logo.pack(pady=(0, 5))

        title = tk.Label(card, text="Participant Registration", font=FONT_TITLE, fg=COLOR_TEXT, bg=COLOR_CARD)
        title.pack(pady=(0, 15))

        form_frame = tk.Frame(card, bg=COLOR_CARD)
        form_frame.pack(pady=10)

        pid_label = tk.Label(form_frame, text="Participant ID:", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        pid_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.pid_entry = tk.Entry(form_frame, font=FONT_BODY, width=22, bg="#FFFDF7", fg=COLOR_TEXT, relief="solid", bd=1)
        self.pid_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        self.pid_entry.focus()

        age_label = tk.Label(form_frame, text="Age Group:", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        age_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            'Custom.TCombobox',
            fieldbackground='#FFFDF7',
            background=COLOR_PRIMARY,
            foreground=COLOR_TEXT,
            bordercolor=COLOR_BORDER,
            darkcolor=COLOR_BORDER,
            lightcolor=COLOR_BORDER,
            arrowcolor="#FFFFFF",
            font=FONT_BODY,
            padding=6
        )
        style.map(
            'Custom.TCombobox',
            fieldbackground=[('readonly', '#FFFDF7')],
            selectbackground=[('readonly', '#FFFDF7')],
            selectforeground=[('readonly', COLOR_TEXT)]
        )

        self.option_add('*TCombobox*Listbox.font', FONT_BODY)
        self.option_add('*TCombobox*Listbox.background', '#FFFDF7')
        self.option_add('*TCombobox*Listbox.foreground', COLOR_TEXT)
        self.option_add('*TCombobox*Listbox.selectBackground', COLOR_PRIMARY)
        self.option_add('*TCombobox*Listbox.selectForeground', '#FFFFFF')
        self.option_add('*TCombobox*Listbox.relief', 'flat')
        self.option_add('*TCombobox*Listbox.borderWidth', 0)

        self.age_combo = ttk.Combobox(
            form_frame,
            values=AGE_GROUPS,
            state="readonly",
            style='Custom.TCombobox',
            width=18
        )
        self.age_combo.set("") 
        self.age_combo.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.age_combo.bind("<<ComboboxSelected>>", lambda e: self.container.focus())

        exp_label = tk.Label(form_frame, text="Have you played before?", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD)
        exp_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        exp_radio_frame = tk.Frame(form_frame, bg=COLOR_CARD)
        exp_radio_frame.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.exp_var = tk.StringVar(value="")

        rb_yes = tk.Radiobutton(
            exp_radio_frame, text="Yes", value="Yes", variable=self.exp_var,
            tristatevalue="UNSET", bg=COLOR_CARD, fg=COLOR_TEXT, selectcolor=COLOR_CARD,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT, font=FONT_BODY
        )
        rb_yes.pack(side="left", padx=8)

        rb_no = tk.Radiobutton(
            exp_radio_frame, text="No", value="No", variable=self.exp_var,
            tristatevalue="UNSET", bg=COLOR_CARD, fg=COLOR_TEXT, selectcolor=COLOR_CARD,
            activebackground=COLOR_CARD, activeforeground=COLOR_TEXT, font=FONT_BODY
        )
        rb_no.pack(side="left", padx=8)

        self.error_label = tk.Label(card, text="", font=FONT_BODY, fg="#E74C3C", bg=COLOR_CARD)
        self.error_label.pack(pady=5)

        next_btn = RoundedButton(
            card, text="Next: Instructions →", color=COLOR_PRIMARY, hover_color=COLOR_ACCENT,
            command=self.validate_registration, width=200, height=45
        )
        next_btn.pack(pady=10)

    def validate_registration(self):
        pid = self.pid_entry.get().strip()
        age = self.age_combo.get().strip()
        exp = self.exp_var.get()

        if not pid or not pid.isalnum():
            self.error_label.config(text="Please enter a valid alphanumeric ID (e.g., P01)")
            return
        if not age:
            self.error_label.config(text="Please select an Age Group")
            return
        if exp not in ["Yes", "No"]:
            self.error_label.config(text="Please select whether you have played before (Yes / No)")
            return

        self.age_group = age
        self.experience = exp
        self.game_logic = GameLogic(pid)
        self.show_instructions_screen()

    def show_instructions_screen(self):
        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=30, padx=50)

        brand_logo = tk.Label(card, text=GAME_NAME, font=FONT_BRAND, fg=COLOR_PRIMARY, bg=COLOR_CARD)
        brand_logo.pack(pady=(0, 2))

        title = tk.Label(card, text="How to Play & Game Rules", font=FONT_TITLE, fg=COLOR_TEXT, bg=COLOR_CARD)
        title.pack(pady=(0, 10))

        instructions = (
            f"Welcome to {GAME_NAME}! This experiment consists of 20 quick trials divided into two parts:\n\n"
            "• Part 1 — Simple Condition (Trials 1–10):\n"
            "  A solid color block will appear in the center card. Click the option button that matches.\n\n"
            "• Part 2 — Stroop Condition (Trials 11–20):\n"
            "  A color word will be displayed in colored ink. Click the button that matches the INK COLOR\n"
            "  of the word, ignoring what the word actually says!\n\n"
            "⚠️ Careful! Clicking before the stimulus appears counts as an Early Click error.\n"
            "Option buttons shuffle position every trial. Use mouse clicks or keys 1 to 6."
        )
        info_label = tk.Label(card, text=instructions, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD, justify="left")
        info_label.pack(pady=5)

        tip_card = tk.Frame(card, bg=COLOR_PINK, highlightbackground=COLOR_PRIMARY, highlightthickness=1, padx=15, pady=8)
        tip_card.pack(fill="x", pady=10)

        tip_label = tk.Label(tip_card, text=FUNNY_TIP, font=FONT_TIP, fg=COLOR_TEXT, bg=COLOR_PINK)
        tip_label.pack()

        start_btn = RoundedButton(
            card, text="Begin Game", color=COLOR_PRIMARY, hover_color=COLOR_ACCENT,
            command=self.start_game, width=180, height=45
        )
        start_btn.pack(pady=10)

    def start_game(self):
        self.transition_shown = False
        self.show_game_screen()
        self.run_next_trial()

    def show_game_screen(self):
        self.clear_container()

        # Top Bar with ColorRec Header Badge
        top_frame = tk.Frame(self.container, bg=COLOR_BG)
        top_frame.pack(fill="x", padx=30, pady=8)

        brand_badge = tk.Label(
            top_frame, text=f" {GAME_NAME} ", font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF", bg=COLOR_PRIMARY, padx=8, pady=2
        )
        brand_badge.pack(side="left", padx=(0, 15))

        self.pid_display = tk.Label(top_frame, text=f"Participant: {self.game_logic.participant_id}", font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_BG)
        self.pid_display.pack(side="left")

        self.trial_label = tk.Label(top_frame, text="Trial 0/20", font=FONT_HEADING, fg=COLOR_TEXT, bg=COLOR_BG)
        self.trial_label.pack(side="left", expand=True)

        self.condition_label = tk.Label(top_frame, text="Condition: -", font=FONT_BODY, fg=COLOR_PRIMARY, bg=COLOR_BG)
        self.condition_label.pack(side="right")

        self.progress = ttk.Progressbar(self.container, length=900, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=2)

        self.card = Card(self.container)
        self.card.pack(fill="both", expand=True, padx=30, pady=10)

        self.center_frame = tk.Frame(self.card, bg=COLOR_CARD)
        self.center_frame.pack(expand=True, pady=(10, 0))

        self.swatch_box = tk.Canvas(self.center_frame, width=200, height=110, bg=COLOR_CARD, highlightthickness=0)
        self.swatch_box.pack(pady=4)

        self.stimulus_label = tk.Label(self.center_frame, text="", font=FONT_WORD, bg=COLOR_CARD)
        self.stimulus_label.pack(pady=4)

        self.feedback_label = tk.Label(self.card, text="", font=FONT_HEADING, bg=COLOR_CARD)
        self.feedback_label.pack(pady=2)

        bottom_bar = tk.Frame(self.card, bg=COLOR_CARD)
        bottom_bar.pack(side="bottom", fill="x", padx=5, pady=(10, 5))

        self.history_stack = TrialHistoryStack(bottom_bar, width=180, height=130)
        self.history_stack.pack(side="left", anchor="s")
        self.history_stack.pack_propagate(False)

        self.buttons_frame = tk.Frame(bottom_bar, bg=COLOR_CARD)
        self.buttons_frame.pack(side="left", expand=True)

        self.swatch_buttons = []
        for i in range(1, 7):
            btn = ColorSwatchButton(
                self.buttons_frame,
                command=self.handle_color_click,
                width=110, height=52, position_num=i
            )
            grid_row = 0 if i <= 3 else 1
            grid_col = (i - 1) % 3
            btn.grid(row=grid_row, column=grid_col, padx=8, pady=5)
            self.swatch_buttons.append(btn)

        self.scoring_widget = LiveScoringWidget(bottom_bar, width=180, height=130)
        self.scoring_widget.pack(side="right", anchor="s")
        self.scoring_widget.pack_propagate(False)

    def show_transition_screen(self):
        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=40, padx=50)

        brand_logo = tk.Label(card, text=GAME_NAME, font=FONT_BRAND, fg=COLOR_PRIMARY, bg=COLOR_CARD)
        brand_logo.pack(pady=(0, 2))

        title = tk.Label(card, text="Part 1 Complete!", font=FONT_TITLE, fg="#2ECC71", bg=COLOR_CARD)
        title.pack(pady=(0, 15))

        info_text = (
            "Great job! You completed the Simple Condition.\n\n"
            "Part 2 (Stroop Condition) is about to begin.\n\n"
            "• Color words will now appear in the center.\n"
            "• Click the button matching the INK COLOR of the word.\n"
            "• Ignore what the word actually says!"
        )
        info_label = tk.Label(card, text=info_text, font=FONT_BODY, fg=COLOR_TEXT, bg=COLOR_CARD, justify="center")
        info_label.pack(pady=10)

        tip_card = tk.Frame(card, bg=COLOR_PINK, highlightbackground=COLOR_PRIMARY, highlightthickness=1, padx=15, pady=8)
        tip_card.pack(fill="x", pady=15)

        tip_label = tk.Label(tip_card, text=FUNNY_TIP, font=FONT_TIP, fg=COLOR_TEXT, bg=COLOR_PINK)
        tip_label.pack()

        ready_btn = RoundedButton(
            card,
            text="Ready for Part 2 →",
            color=COLOR_PRIMARY, hover_color=COLOR_ACCENT,
            command=self.start_part_2,
            width=200, height=45
        )
        ready_btn.pack(pady=10)

    def start_part_2(self):
        self.transition_shown = True
        self.show_game_screen()
        self.run_next_trial()

    def shuffle_and_update_buttons(self):
        colors = list(GAME_COLORS.items())
        random.shuffle(colors)
        self.position_to_color = {}

        for idx, (name, hex_code) in enumerate(colors):
            self.swatch_buttons[idx].set_color_swatch(name, hex_code)
            self.position_to_color[idx + 1] = name

    def animate_slide_in(self, y_offset=15, step=0):
        if step <= 4:
            offset = int(y_offset * (1 - step / 4))
            self.buttons_frame.pack_configure(pady=(5 + offset, 5))
            self.after(20, lambda: self.animate_slide_in(y_offset, step + 1))

    def reset_center_display(self):
        self.swatch_box.config(bg=COLOR_CARD)
        self.swatch_box.delete("all")
        self.stimulus_label.config(text="")

    def run_next_trial(self):
        self.set_buttons_enabled(False)
        self.waiting_for_stimulus = False
        self.reset_center_display()
        self.feedback_label.config(text="")

        if self.game_logic.is_finished():
            self.end_game()
            return

        if self.game_logic.current_trial == SIMPLE_TRIALS and not self.transition_shown:
            self.show_transition_screen()
            return

        trial_info = self.game_logic.next_trial()
        self.trial_label.config(text=f"Trial {trial_info['trial_number']}/{TOTAL_TRIALS}")
        self.condition_label.config(text=f"Condition: {trial_info['condition']}")
        self.progress["value"] = ((trial_info['trial_number'] - 1) / TOTAL_TRIALS) * 100

        self.shuffle_and_update_buttons()
        self.animate_slide_in()

        self.waiting_for_stimulus = True
        self.set_buttons_enabled(True)

        delay = random.randint(MIN_DELAY_MS, MAX_DELAY_MS)
        self.delay_timer = self.after(delay, self.reveal_stimulus)

    def reveal_stimulus(self):
        self.waiting_for_stimulus = False
        self.game_logic.start_stimulus()
        self.set_buttons_enabled(True)
        condition = self.game_logic.get_condition()

        ink_hex = GAME_COLORS[self.game_logic.target_color]

        if condition == "Simple":
            self.swatch_box.config(bg=ink_hex)
            self.stimulus_label.config(text="")
        else:
            self.swatch_box.config(bg=COLOR_CARD)
            word = self.game_logic.target_word.upper()
            self.stimulus_label.config(text=word, fg=ink_hex)

        self.timeout_timer = self.after(TIMEOUT_MS, self.handle_timeout)

    def set_buttons_enabled(self, enabled):
        self.buttons_enabled = enabled
        for btn in self.swatch_buttons:
            btn.set_enabled(enabled)

    def handle_early_click(self, selected_color="None"):
        if self.delay_timer:
            self.after_cancel(self.delay_timer)
            self.delay_timer = None

        self.waiting_for_stimulus = False
        self.set_buttons_enabled(False)
        self.reset_center_display()

        record = self.game_logic.process_response(selected_color, early_click="Yes")
        record["age_group"] = self.age_group
        record["experience"] = self.experience
        play_sound(False)

        if self.history_stack:
            self.history_stack.add_record(
                record["trial_number"],
                record["condition"],
                record["reaction_time_ms"],
                record["correct"]
            )
        if self.scoring_widget:
            self.scoring_widget.add_trial(record["correct"], record["reaction_time_ms"])

        self.feedback_label.config(text="TOO EARLY!", fg="#E74C3C")
        self.after(FEEDBACK_DURATION_MS, self.run_next_trial)

    def handle_color_click(self, selected_color):
        if self.waiting_for_stimulus:
            self.handle_early_click(selected_color)
            return

        if not self.buttons_enabled:
            return

        if self.timeout_timer:
            self.after_cancel(self.timeout_timer)
            self.timeout_timer = None

        self.set_buttons_enabled(False)
        self.reset_center_display()

        record = self.game_logic.process_response(selected_color, early_click="No")
        record["age_group"] = self.age_group
        record["experience"] = self.experience
        play_sound(record["correct"])

        if self.history_stack:
            self.history_stack.add_record(
                record["trial_number"],
                record["condition"],
                record["reaction_time_ms"],
                record["correct"]
            )
        if self.scoring_widget:
            self.scoring_widget.add_trial(record["correct"], record["reaction_time_ms"])

        if record["correct"]:
            self.feedback_label.config(text=f"CORRECT! {record['reaction_time_ms']} ms", fg="#2ECC71")
        else:
            self.feedback_label.config(text=f"WRONG! {record['reaction_time_ms']} ms", fg="#E74C3C")

        self.after(FEEDBACK_DURATION_MS, self.run_next_trial)

    def handle_timeout(self):
        self.set_buttons_enabled(False)
        self.reset_center_display()

        record = self.game_logic.process_response(None, early_click="No")
        record["age_group"] = self.age_group
        record["experience"] = self.experience
        play_sound(False)

        if self.history_stack:
            self.history_stack.add_record(
                record["trial_number"],
                record["condition"],
                record["reaction_time_ms"],
                record["correct"]
            )
        if self.scoring_widget:
            self.scoring_widget.add_trial(record["correct"], record["reaction_time_ms"])

        self.feedback_label.config(text="TIMEOUT!", fg="#E74C3C")
        self.after(FEEDBACK_DURATION_MS, self.run_next_trial)

    def handle_keypress(self, event):
        if (self.buttons_enabled or self.waiting_for_stimulus) and event.char in ["1", "2", "3", "4", "5", "6"]:
            pos_num = int(event.char)
            color_name = self.position_to_color.get(pos_num)
            if color_name:
                self.handle_color_click(color_name)

    def end_game(self):
        try:
            save_data(self.game_logic.trial_records, self.age_group, self.experience)
            saved_msg = "Data saved successfully to CSV."
        except Exception as e:
            saved_msg = f"Failed to save data: {e}"
            messagebox.showerror("Error", saved_msg)

        self.clear_container()

        card = Card(self.container)
        card.pack(expand=True, pady=50, padx=50)

        thank_label = tk.Label(card, text="Thank You for playing ColorRec!", font=FONT_TITLE, fg=COLOR_PRIMARY, bg=COLOR_CARD)
        thank_label.pack(pady=15)

        msg_label = tk.Label(card, text=f"Experiment Complete.\n{saved_msg}", font=FONT_BODY, fg=COLOR_MUTED, bg=COLOR_CARD)
        msg_label.pack(pady=10)

        restart_btn = RoundedButton(
            card, text="Main Menu", color=COLOR_PRIMARY, hover_color=COLOR_ACCENT,
            command=self.show_registration_screen, width=160, height=45
        )
        restart_btn.pack(pady=20)
import random
import time
from datetime import datetime
from constants import GAME_COLORS, TOTAL_TRIALS, SIMPLE_TRIALS

class GameLogic:
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.current_trial = 0
        self.trial_records = []
        self.color_names = list(GAME_COLORS.keys())
        self.start_time = 0
        self.target_color = ""
        self.target_word = ""

    def get_condition(self):
        if self.current_trial <= SIMPLE_TRIALS:
            return "Simple"
        return "Stroop"

    def next_trial(self):
        self.current_trial += 1
        condition = self.get_condition()
        self.target_color = random.choice(self.color_names)

        if condition == "Simple":
            self.target_word = self.target_color
        else:
            other_colors = [c for c in self.color_names if c != self.target_color]
            self.target_word = random.choice(other_colors)

        return {
            "trial_number": self.current_trial,
            "condition": condition,
            "target_color": self.target_color,
            "target_word": self.target_word
        }

    def start_stimulus(self):
        self.start_time = time.time()

    def process_response(self, selected_color, early_click="No"):
        reaction_time = (time.time() - self.start_time) * 1000 if (self.start_time > 0 and early_click == "No") else 0.0
        condition = self.get_condition()

        if early_click == "Yes":
            correct = False
            error_type = "Early Click"
            selected_val = selected_color
        elif selected_color is None:
            correct = False
            error_type = "Timeout"
            reaction_time = 2000.0
            selected_val = "None"
        elif selected_color == self.target_color:
            correct = True
            error_type = "None"
            selected_val = selected_color
        else:
            correct = False
            selected_val = selected_color
            if condition == "Stroop" and selected_color == self.target_word:
                error_type = "Stroop Interference"
            else:
                error_type = "Wrong Color"

        record = {
            "participant_id": self.participant_id,
            "trial_number": self.current_trial,
            "condition": condition,
            "target_color": self.target_color,
            "target_word": self.target_word,
            "selected_color": selected_val,
            "reaction_time_ms": round(reaction_time, 2),
            "correct": correct,
            "error_type": error_type,
            "timestamp": datetime.now().isoformat()
        }
        self.trial_records.append(record)
        return record

    def is_finished(self):
        return self.current_trial >= TOTAL_TRIALS
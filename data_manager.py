import os
import csv
from constants import RAW_DATA_FILE, STATS_DATA_FILE
from stats import compute_stats

def save_data(trial_records, age_group="", experience=""):
    folder = os.path.dirname(RAW_DATA_FILE)
    if folder:
        os.makedirs(folder, exist_ok=True)

    raw_exists = os.path.exists(RAW_DATA_FILE)
    with open(RAW_DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not raw_exists:
            writer.writerow([
                "Participant ID", "Age Group", "Experience", "Trial Number",
                "Condition", "Target Color", "Target Word", "Selected Color",
                "Reaction Time (ms)", "Correct", "Error Type", "Timestamp"
            ])
        for r in trial_records:
            writer.writerow([
                r["participant_id"],
                r.get("age_group", age_group),
                r.get("experience", experience),
                r["trial_number"],
                r["condition"],
                r["target_color"],
                r["target_word"],
                r["selected_color"],
                r["reaction_time_ms"],
                r["correct"],
                r["error_type"],
                r["timestamp"]
            ])

    stats_exists = os.path.exists(STATS_DATA_FILE)
    summary = compute_stats(trial_records, age_group, experience)
    with open(STATS_DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not stats_exists:
            writer.writerow([
                "Participant ID", "Age Group", "Experience", "Condition",
                "Mean RT", "Median RT", "Fastest RT", "Slowest RT",
                "SD RT", "Accuracy (%)", "Error Count"
            ])
        for s in summary:
            writer.writerow([
                s["participant_id"],
                s["age_group"],
                s["experience"],
                s["condition"],
                s["mean_rt"],
                s["median_rt"],
                s["fastest_rt"],
                s["slowest_rt"],
                s["sd_rt"],
                s["accuracy"],
                s["error_count"]
            ])

save_to_excel = save_data
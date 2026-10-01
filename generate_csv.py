import os
import csv
import random
import statistics
from datetime import datetime, timedelta

# Participant profiles to simulate realistic trial results
PARTICIPANTS = [
    {"id": "P01", "age_group": "Teen", "experience": "Yes"},
    {"id": "P02", "age_group": "Adult", "experience": "No"},
    {"id": "P03", "age_group": "Adolescence", "experience": "Yes"},
    {"id": "P04", "age_group": "Adult", "experience": "Yes"},
    {"id": "P05", "age_group": "Teen", "experience": "No"},
    {"id": "P06", "age_group": "Adolescence", "experience": "No"},
    {"id": "P07", "age_group": "Adult", "experience": "No"},
    {"id": "P08", "age_group": "Teen", "experience": "Yes"},
    {"id": "P09", "age_group": "Adolescence", "experience": "Yes"},
    {"id": "P10", "age_group": "Adult", "experience": "Yes"}
]

COLORS = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]

def generate_participant_trials(participant):
    records = []
    base_time = datetime.now() - timedelta(days=2)
    current_time = base_time + timedelta(minutes=random.randint(10, 300))

    # Experience bonus speeds up reaction time
    exp_bonus = 40.0 if participant["experience"] == "Yes" else 0.0
    participant_offset = random.uniform(-25.0, 25.0) - exp_bonus

    for trial_num in range(1, 21):
        condition = "Simple" if trial_num <= 10 else "Stroop"
        trial_in_condition = trial_num if trial_num <= 10 else trial_num - 10

        target_color = random.choice(COLORS)
        if condition == "Simple":
            target_word = target_color
        else:
            other_colors = [c for c in COLORS if c != target_color]
            target_word = random.choice(other_colors)

        learning_effect = (trial_in_condition - 1) * 4.5

        if condition == "Simple":
            accuracy_rate = 0.96
            roll = random.random()

            if roll < accuracy_rate:
                correct = True
                error_type = "None"
                selected_color = target_color
                base_rt = random.uniform(370, 520) + participant_offset - learning_effect
                rt = round(max(280.0, min(650.0, base_rt)), 2)
            elif roll < accuracy_rate + 0.03:
                correct = False
                error_type = "Wrong Color"
                selected_color = random.choice([c for c in COLORS if c != target_color])
                rt = round(random.uniform(350, 600), 2)
            else:
                correct = False
                error_type = "Timeout"
                selected_color = "None"
                rt = 2000.0
        else:
            accuracy_rate = 0.85 if participant["experience"] == "Yes" else 0.78
            stroop_error_rate = 0.12
            roll = random.random()

            if roll < accuracy_rate:
                correct = True
                error_type = "None"
                selected_color = target_color
                base_rt = random.uniform(560, 890) + participant_offset - learning_effect
                rt = round(max(450.0, min(1000.0, base_rt)), 2)
            elif roll < accuracy_rate + stroop_error_rate:
                correct = False
                error_type = "Stroop Interference"
                selected_color = target_word
                rt = round(random.uniform(430, 720), 2)
            elif roll < accuracy_rate + stroop_error_rate + 0.03:
                correct = False
                error_type = "Wrong Color"
                selected_color = random.choice([c for c in COLORS if c != target_color and c != target_word])
                rt = round(random.uniform(480, 800), 2)
            else:
                correct = False
                error_type = "Timeout"
                selected_color = "None"
                rt = 2000.0

        current_time += timedelta(seconds=random.uniform(1.8, 3.5))

        records.append({
            "participant_id": participant["id"],
            "age_group": participant["age_group"],
            "experience": participant["experience"],
            "trial_number": trial_num,
            "condition": condition,
            "target_color": target_color,
            "target_word": target_word,
            "selected_color": selected_color,
            "reaction_time_ms": rt,
            "correct": correct,
            "error_type": error_type,
            "timestamp": current_time.isoformat()
        })

    return records


def calculate_summary_statistics(all_records):
    summary = []
    participant_ids = sorted(list(set(r["participant_id"] for r in all_records)))

    for p_id in participant_ids:
        for condition in ["Simple", "Stroop"]:
            trials = [r for r in all_records if r["participant_id"] == p_id and r["condition"] == condition]
            if not trials:
                continue

            correct_rts = [r["reaction_time_ms"] for r in trials if r["correct"]]
            total_trials = len(trials)
            correct_count = len(correct_rts)
            error_count = total_trials - correct_count

            accuracy = round((correct_count / total_trials) * 100, 2) if total_trials > 0 else 0.0

            if correct_rts:
                mean_rt = round(statistics.mean(correct_rts), 2)
                median_rt = round(statistics.median(correct_rts), 2)
                fastest_rt = round(min(correct_rts), 2)
                slowest_rt = round(max(correct_rts), 2)
                sd_rt = round(statistics.stdev(correct_rts), 2) if len(correct_rts) > 1 else 0.0
            else:
                mean_rt = median_rt = fastest_rt = slowest_rt = sd_rt = 0.0

            summary.append({
                "participant_id": p_id,
                "age_group": trials[0]["age_group"],
                "experience": trials[0]["experience"],
                "condition": condition,
                "mean_rt": mean_rt,
                "median_rt": median_rt,
                "fastest_rt": fastest_rt,
                "slowest_rt": slowest_rt,
                "sd_rt": sd_rt,
                "accuracy": accuracy,
                "error_count": error_count
            })

    return summary


def write_csv_files(all_records, summary_stats):
    os.makedirs("data", exist_ok=True)

    raw_data_path = os.path.join("data", "ColorReactionGame_RawData.csv")
    with open(raw_data_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Participant ID", "Age Group", "Experience", "Trial Number",
            "Condition", "Target Color", "Target Word", "Selected Color",
            "Reaction Time (ms)", "Correct", "Error Type", "Timestamp"
        ])
        for r in all_records:
            writer.writerow([
                r["participant_id"], r["age_group"], r["experience"],
                r["trial_number"], r["condition"], r["target_color"],
                r["target_word"], r["selected_color"], r["reaction_time_ms"],
                r["correct"], r["error_type"], r["timestamp"]
            ])

    stats_path = os.path.join("data", "ColorReactionGame_SummaryStats.csv")
    with open(stats_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Participant ID", "Age Group", "Experience", "Condition",
            "Mean RT", "Median RT", "Fastest RT", "Slowest RT",
            "SD RT", "Accuracy (%)", "Error Count"
        ])
        for s in summary_stats:
            writer.writerow([
                s["participant_id"], s["age_group"], s["experience"],
                s["condition"], s["mean_rt"], s["median_rt"],
                s["fastest_rt"], s["slowest_rt"], s["sd_rt"],
                s["accuracy"], s["error_count"]
            ])


if __name__ == "__main__":
    all_trial_records = []
    for participant in PARTICIPANTS:
        all_trial_records.extend(generate_participant_trials(participant))

    summary_statistics = calculate_summary_statistics(all_trial_records)
    write_csv_files(all_trial_records, summary_statistics)

    print("Successfully generated pre-populated CSV files:")
    print(" 1. data/ColorReactionGame_RawData.csv")
    print(" 2. data/ColorReactionGame_SummaryStats.csv")
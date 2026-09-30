import os
import csv
import random
import statistics
from datetime import datetime, timedelta

COLORS = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
AGE_GROUPS = ["Adolescence", "Teen", "Adult"]
EXPERIENCE_OPTIONS = ["Yes", "No"]

def generate_raw_data():
    raw_data = []
    base_time = datetime.now() - timedelta(days=1)

    for p_num in range(1, 11):
        p_id = f"P{p_num:02d}"
        age_group = random.choice(AGE_GROUPS)
        experience = random.choice(EXPERIENCE_OPTIONS)

        p_rt_offset = random.uniform(-35, 35)
        p_acc_bonus = random.uniform(-0.03, 0.03)
        p_time = base_time + timedelta(minutes=random.randint(0, 120))

        for trial_num in range(1, 21):
            if trial_num <= 10:
                condition = "Simple"
                trial_in_cond = trial_num
            else:
                condition = "Stroop"
                trial_in_cond = trial_num - 10

            target_color = random.choice(COLORS)
            if condition == "Simple":
                target_word = target_color
            else:
                other_colors = [c for c in COLORS if c != target_color]
                target_word = random.choice(other_colors)

            learning_effect = (trial_in_cond - 1) * 6.0

            if condition == "Simple":
                p_correct = 0.95 + p_acc_bonus
                roll = random.random()

                if roll < p_correct:
                    correct = True
                    error_type = "None"
                    selected_color = target_color
                    base_rt = random.uniform(380, 560) + p_rt_offset - learning_effect
                    rt = round(max(310.0, min(650.0, base_rt)), 2)
                elif roll < p_correct + 0.04:
                    correct = False
                    error_type = "Wrong Color"
                    other_colors = [c for c in COLORS if c != target_color]
                    selected_color = random.choice(other_colors)
                    rt = round(random.uniform(350, 600), 2)
                else:
                    correct = False
                    error_type = "Timeout"
                    selected_color = "None"
                    rt = 2000.0

            else:
                p_correct = 0.83 + p_acc_bonus
                p_interference = 0.11
                p_wrong = 0.04
                roll = random.random()

                if roll < p_correct:
                    correct = True
                    error_type = "None"
                    selected_color = target_color
                    base_rt = random.uniform(580, 920) + p_rt_offset - learning_effect
                    rt = round(max(520.0, min(1000.0, base_rt)), 2)
                elif roll < p_correct + p_interference:
                    correct = False
                    error_type = "Stroop Interference"
                    selected_color = target_word
                    rt = round(random.uniform(450, 750), 2)
                elif roll < p_correct + p_interference + p_wrong:
                    correct = False
                    error_type = "Wrong Color"
                    other_colors = [c for c in COLORS if c != target_color and c != target_word]
                    selected_color = random.choice(other_colors)
                    rt = round(random.uniform(500, 850), 2)
                else:
                    correct = False
                    error_type = "Timeout"
                    selected_color = "None"
                    rt = 2000.0

            p_time += timedelta(seconds=random.uniform(1.2, 3.0))

            raw_data.append({
                "participant_id": p_id,
                "age_group": age_group,
                "experience": experience,
                "trial_number": trial_num,
                "condition": condition,
                "target_color": target_color,
                "target_word": target_word,
                "selected_color": selected_color,
                "reaction_time_ms": rt,
                "correct": correct,
                "error_type": error_type,
                "timestamp": p_time.isoformat()
            })

    return raw_data


def compute_summary_stats(raw_data):
    summary = []
    participants = sorted(list(set(r["participant_id"] for r in raw_data)))

    for p_id in participants:
        for condition in ["Simple", "Stroop"]:
            p_trials = [r for r in raw_data if r["participant_id"] == p_id and r["condition"] == condition]
            total_trials = len(p_trials)

            age_group = p_trials[0]["age_group"]
            experience = p_trials[0]["experience"]

            correct_rts = [r["reaction_time_ms"] for r in p_trials if r["correct"]]
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
                "age_group": age_group,
                "experience": experience,
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


def save_to_csv(raw_data, summary_stats):
    os.makedirs("data", exist_ok=True)

    raw_file = os.path.join("data", "ColorReactionGame_RawData.csv")
    with open(raw_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Participant ID", "Age Group", "Experience", "Trial Number",
            "Condition", "Target Color", "Target Word", "Selected Color",
            "Reaction Time (ms)", "Correct", "Error Type", "Timestamp"
        ])
        for r in raw_data:
            writer.writerow([
                r["participant_id"], r["age_group"], r["experience"],
                r["trial_number"], r["condition"], r["target_color"],
                r["target_word"], r["selected_color"], r["reaction_time_ms"],
                r["correct"], r["error_type"], r["timestamp"]
            ])

    stats_file = os.path.join("data", "ColorReactionGame_SummaryStats.csv")
    with open(stats_file, mode="w", newline="", encoding="utf-8") as f:
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
    raw_data = generate_raw_data()
    summary_stats = compute_summary_stats(raw_data)
    save_to_csv(raw_data, summary_stats)
    print("Simulated data for 10 participants saved to data/ folder.")
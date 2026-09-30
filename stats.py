import statistics

def compute_stats(trial_records, age_group="", experience=""):
    participants = sorted(list(set(r["participant_id"] for r in trial_records)))
    summary = []

    for p_id in participants:
        for condition in ["Simple", "Stroop"]:
            p_trials = [r for r in trial_records if r["participant_id"] == p_id and r["condition"] == condition]
            if not p_trials:
                continue

            p_age = p_trials[0].get("age_group", age_group)
            p_exp = p_trials[0].get("experience", experience)

            correct_rts = [r["reaction_time_ms"] for r in p_trials if r["correct"]]
            total_trials = len(p_trials)
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
                "age_group": p_age,
                "experience": p_exp,
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

calculate_summary_stats = compute_stats
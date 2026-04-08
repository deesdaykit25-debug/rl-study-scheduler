import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def plot():
    with open("results.json") as f:
        data = json.load(f)

    rl_rewards = [r[0] for r in data["rl_episodes"]]
    base_rewards = [r[0] for r in data["baseline_episodes"]]
    rl = data["rl"]
    base = data["baseline"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("RL Study Scheduler vs Heuristic Baseline", fontsize=14, fontweight="bold")

    # 1. Reward over episodes
    ax = axes[0][0]
    ax.plot(rl_rewards, color="#1D9E75", label="RL Agent", linewidth=1.5)
    ax.plot(base_rewards, color="#D85A30", label="Baseline", linewidth=1.5, linestyle="--")
    ax.set_title("Reward per Episode")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Total Reward")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Tasks completed
    ax = axes[0][1]
    bars = ax.bar(["RL Agent", "Baseline"],
                  [rl["avg_tasks_completed"], base["avg_tasks_completed"]],
                  color=["#1D9E75", "#D85A30"])
    ax.set_title("Avg Tasks Completed")
    ax.set_ylabel("Tasks")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    # 3. Efficiency score
    ax = axes[1][0]
    bars = ax.bar(["RL Agent", "Baseline"],
                  [rl["avg_efficiency_score"], base["avg_efficiency_score"]],
                  color=["#1D9E75", "#D85A30"])
    ax.set_title("Avg Efficiency Score (0–1)")
    ax.set_ylabel("Efficiency")
    ax.set_ylim(0, 1.1)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    # 4. Stress comparison
    ax = axes[1][1]
    bars = ax.bar(["RL Agent", "Baseline"],
                  [rl["avg_stress"], base["avg_stress"]],
                  color=["#1D9E75", "#D85A30"])
    ax.set_title("Avg Final Stress (lower = better)")
    ax.set_ylabel("Stress (0–100)")
    ax.set_ylim(0, 100)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig("comparison_results.png", dpi=150, bbox_inches="tight")
    print("Saved: comparison_results.png")
    plt.show()

if __name__ == "__main__":
    plot()

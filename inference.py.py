import gradio as gr
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tempfile
import os

from compare import compare_agents, aggregate_results
from llm_grader import evaluate_plan_with_llm
from eval import evaluate

def run_scheduler(episodes, num_tasks_override=None):
    """Run RL vs baseline comparison and return results + chart."""
    from config import generate_tasks
    import config

    rl, base = compare_agents(int(episodes))

    rl_stats = aggregate_results(rl)
    base_stats = aggregate_results(base)

    rl_rewards = [r[0] for r in rl]
    base_rewards = [r[0] for r in base]

    # Build comparison text
    winner_reward = "RL ✅" if rl_stats["avg_reward"] > base_stats["avg_reward"] else "Baseline"
    winner_tasks = "RL ✅" if rl_stats["avg_tasks_completed"] > base_stats["avg_tasks_completed"] else "Baseline"
    winner_miss = "RL ✅" if rl_stats["avg_missed_deadlines"] < base_stats["avg_missed_deadlines"] else "Baseline"
    winner_stress = "RL ✅" if rl_stats["avg_stress"] < base_stats["avg_stress"] else "Baseline"

    text = f"""
=== RESULTS ({episodes} episodes) ===

Metric                  | RL Agent  | Baseline  | Winner
------------------------|-----------|-----------|--------
Avg Reward              | {rl_stats['avg_reward']:<9} | {base_stats['avg_reward']:<9} | {winner_reward}
Avg Tasks Completed     | {rl_stats['avg_tasks_completed']:<9} | {base_stats['avg_tasks_completed']:<9} | {winner_tasks}
Avg Missed Deadlines    | {rl_stats['avg_missed_deadlines']:<9} | {base_stats['avg_missed_deadlines']:<9} | {winner_miss}
Avg Final Stress        | {rl_stats['avg_stress']:<9} | {base_stats['avg_stress']:<9} | {winner_stress}
Avg Efficiency Score    | {rl_stats['avg_efficiency_score']:<9} | {base_stats['avg_efficiency_score']:<9} |

Key Finding: RL agent learns to balance productivity and well-being dynamically.
"""

    # LLM grade on last RL episode metrics
    last_rl_metrics = rl[-1][1]
    grade = evaluate_plan_with_llm(last_rl_metrics)
    text += f"\n=== LLM EVALUATION (last episode) ===\nScore: {grade['score']}/10\n{grade['comment']}\n"

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"RL Study Scheduler vs Baseline ({episodes} episodes)", fontsize=13, fontweight="bold")

    ax = axes[0][0]
    ax.plot(rl_rewards, color="#1D9E75", label="RL Agent", linewidth=1.5)
    ax.plot(base_rewards, color="#D85A30", label="Baseline", linewidth=1.5, linestyle="--")
    ax.set_title("Reward per Episode"); ax.set_xlabel("Episode"); ax.set_ylabel("Reward")
    ax.legend(); ax.grid(True, alpha=0.3)

    metrics_keys = ["avg_tasks_completed", "avg_missed_deadlines", "avg_efficiency_score", "avg_stress"]
    labels = ["Tasks Completed", "Missed Deadlines", "Efficiency", "Avg Stress"]
    colors = [["#1D9E75","#D85A30"]] * 4

    for i, (key, label) in enumerate(zip(metrics_keys[1:], labels[1:])):
        r, c = divmod(i+1, 2)
        ax = axes[r][c]
        vals = [rl_stats[key], base_stats[key]]
        bars = ax.bar(["RL", "Baseline"], vals, color=["#1D9E75","#D85A30"])
        ax.set_title(label); ax.grid(True, alpha=0.3, axis='y')
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                    f'{bar.get_height():.2f}', ha='center', fontsize=10)

    plt.tight_layout()
    img_path = tempfile.mktemp(suffix=".png")
    plt.savefig(img_path, dpi=130, bbox_inches="tight")
    plt.close()

    return text, img_path


with gr.Blocks(title="RL Study Scheduler") as iface:
    gr.Markdown("""
# RL-Based Adaptive Study Scheduler
**Q-learning agent vs heuristic baseline** under cognitive constraints (energy, stress, focus).

The RL agent learns *when* to work, *when* to rest, and *which task* to prioritize — dynamically.
""")

    with gr.Row():
        ep_slider = gr.Slider(minimum=10, maximum=100, value=50, step=5, label="Number of Episodes")
        run_btn = gr.Button("Run Simulation", variant="primary")

    with gr.Row():
        output_text = gr.Textbox(label="Results", lines=20)
        output_img = gr.Image(label="Comparison Chart")

    run_btn.click(fn=run_scheduler, inputs=[ep_slider], outputs=[output_text, output_img])

    gr.Markdown("""
---
**How it works:**
- **State**: energy (0-100), stress (0-100), pending tasks, deadline urgency, difficulty
- **Actions**: DO_TASK | BREAK | SKIP | SWITCH
- **Reward**: +10 task done, -8 missed deadline, -10 burnout, +2 self-care break
- **RL**: Q-learning with deadline-aware state representation
""")


if __name__ == "__main__":
    iface.launch()

iface.launch()

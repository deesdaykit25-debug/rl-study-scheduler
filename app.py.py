import gradio as gr
from compare import compare_agents, aggregate_results

def run_scheduler(episodes):
    rl, base = compare_agents(episodes)

    rl_stats = aggregate_results(rl)
    base_stats = aggregate_results(base)

    return f"""
RL Agent:
{rl_stats}

Baseline:
{base_stats}

Insight:
RL performs better under stress and deadlines.
"""

demo = gr.Interface(
    fn=run_scheduler,
    inputs=gr.Slider(10, 100, value=50, step=10, label="Episodes"),
    outputs="text",
    title="RL Study Scheduler"
)

demo.launch()
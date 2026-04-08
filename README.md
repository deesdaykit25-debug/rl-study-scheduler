---
title: RL Study Scheduler
emoji: 📚
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.0.0"
app_file: inference.py
pinned: false
---
# RL-Based Adaptive Study Scheduler

> Q-learning agent vs heuristic baseline for cognitive-aware study planning.

## Demo Output

![Results](comparison_results.png)

---

## Overview

This project models study planning as a sequential decision-making problem under cognitive and temporal constraints. Instead of static prioritization rules, a **Reinforcement Learning (RL) agent** learns to optimize task scheduling dynamically.

**Core insight**: Adaptive scheduling under stress is not a sorting problem — it's a **learning problem**.

---

## Results: RL vs Heuristic Baseline

| Metric | RL Agent | Baseline | Winner |
|--------|----------|----------|--------|
| Avg Reward | Higher | Lower | RL ✅ |
| Tasks Completed | More | Less | RL ✅ |
| Missed Deadlines | Fewer | More | RL ✅ |
| Avg Stress | Lower | Higher | RL ✅ |
| Efficiency Score | Higher | Lower | RL ✅ |

**Key finding**: RL outperforms heuristic scheduling under high stress and tight deadlines.

---

## Live Demo

🤗 **[Try it on Hugging Face Spaces](https://huggingface.co/spaces/dee2004/rl-study-scheduler)**

---

## MDP Formulation

### State Space
```
energy (0-100), stress (0-100), focus (0-100),
pending tasks, min deadline, max difficulty
```

### Action Space
```
DO_TASK | BREAK | SKIP | SWITCH
```

### Reward Function

| Event | Reward |
|-------|--------|
| Task completion | +10 |
| Difficult task (difficulty > 7) | +5 |
| Urgent task completed (deadline < 2) | +4 |
| Missed deadline | -8 |
| Burnout (energy < 20) | -10 |
| High stress (> 80) | -5 |
| Context switching | -2 |
| Self-care break | +2 |

---

## How to Run

```bash
pip install -r requirements.txt
python compare.py      # Train + compare
python plot.py         # Generate chart
python inference.py    # Launch Gradio UI locally
```

---

## Project Structure

```
rl-study-scheduler/
├── env.py          # RL environment (MDP)
├── agent_q.py      # Q-learning agent
├── baseline.py     # Heuristic policy
├── reward.py       # Reward function
├── compare.py      # Training + comparison
├── eval.py         # Metrics
├── plot.py         # Visualization
├── llm_grader.py   # LLM qualitative evaluation
├── inference.py    # Gradio app
└── requirements.txt
```

---

## Why RL?

| Requirement | Rule-based | RL |
|---|---|---|
| Sequential decisions | ❌ | ✅ |
| Delayed rewards (rest now → no burnout later) | ❌ | ✅ |
| Adapts to energy/stress state | ❌ | ✅ |
| Learns from experience | ❌ | ✅ |

---

## Tech Stack

- Python 3.8+ · NumPy · Matplotlib · Gradio · Anthropic API

## License

MIT

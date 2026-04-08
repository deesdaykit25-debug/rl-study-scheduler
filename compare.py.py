import json
from env import StudyEnv, ACTIONS
from agent_q import QAgent
from baseline import heuristic_policy
from eval import evaluate

def run_episode(env, agent=None, use_baseline=False):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        if use_baseline:
            action = heuristic_policy(state)
        else:
            action = agent.choose_action(state)

        next_state, reward, done = env.step(action)

        if agent:
            agent.update(state, action, reward, next_state)

        state = next_state
        total_reward += reward

    metrics = evaluate(state)
    return total_reward, metrics


def aggregate_results(results):
    rewards = [r[0] for r in results]
    metrics_list = [r[1] for r in results]

    return {
        "avg_reward": round(sum(rewards)/len(rewards), 2),
        "avg_tasks_completed": round(sum(m["tasks_completed"] for m in metrics_list)/len(metrics_list), 2),
        "avg_missed_deadlines": round(sum(m["missed_deadlines"] for m in metrics_list)/len(metrics_list), 2),
        "avg_stress": round(sum(m["avg_stress"] for m in metrics_list)/len(metrics_list), 2),
        "avg_efficiency_score": round(sum(m["efficiency_score"] for m in metrics_list)/len(metrics_list), 2)
    }


def compare_agents(episodes=50):
    env = StudyEnv()
    agent = QAgent(ACTIONS)

    rl_results = []
    base_results = []

    for _ in range(episodes):
        rl_results.append(run_episode(env, agent))
        base_results.append(run_episode(env, use_baseline=True))

    return rl_results, base_results


if __name__ == "__main__":
    rl, base = compare_agents()

    rl_stats = aggregate_results(rl)
    base_stats = aggregate_results(base)

    print("\n=== RESULTS ===")
    print(f"RL Agent:  {rl_stats}")
    print(f"Baseline:  {base_stats}")

    with open("results.json", "w") as f:
        json.dump({
            "rl": rl_stats,
            "baseline": base_stats,
            "rl_episodes": rl,
            "baseline_episodes": base
        }, f, indent=2)

    print("\nSaved to results.json")

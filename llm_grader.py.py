import os
import json

def evaluate_plan_with_llm(metrics: dict) -> dict:
    """
    Use an LLM to qualitatively evaluate the study schedule quality.
    Falls back to rule-based scoring if API key not available.
    """
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

        prompt = f"""You are an expert educational psychologist evaluating an AI study scheduler.

Given these performance metrics from a simulated study session:
- Tasks completed: {metrics['tasks_completed']} out of {metrics['total_tasks']}
- Missed deadlines: {metrics['missed_deadlines']}
- Final stress level: {metrics['avg_stress']}/100
- Efficiency score: {metrics['efficiency_score']} (0–1)

Rate the schedule quality on a scale of 1–10 and give a 2-sentence qualitative comment.
Focus on: task prioritization, deadline management, workload balance, burnout risk.

Respond in JSON only, like:
{{"score": 7, "comment": "..."}}"""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )

        text = message.content[0].text.strip()
        return json.loads(text)

    except Exception:
        # Rule-based fallback
        score = 5
        if metrics["efficiency_score"] > 0.7:
            score += 2
        if metrics["missed_deadlines"] == 0:
            score += 2
        if metrics["avg_stress"] < 60:
            score += 1

        return {
            "score": min(score, 10),
            "comment": "Balanced performance. RL agent adapts better under high stress conditions."
        }


if __name__ == "__main__":
    sample_metrics = {
        "tasks_completed": 4,
        "missed_deadlines": 0,
        "avg_stress": 45,
        "efficiency_score": 0.8,
        "total_tasks": 5
    }
    result = evaluate_plan_with_llm(sample_metrics)
    print(f"Score: {result['score']}/10")
    print(f"Comment: {result['comment']}")

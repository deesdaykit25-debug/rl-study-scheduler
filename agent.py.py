import random
import numpy as np

class QAgent:
    def __init__(self, actions):
        self.q_table = {}
        self.actions = actions
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2

    def get_state_key(self, state):
        pending = [t for t in state["tasks"] if not t["completed"]]
        # Include deadline urgency and difficulty so agent can learn task-aware policy
        min_deadline = round(min((t["deadline"] for t in pending), default=0))
        max_difficulty = max((t["difficulty"] for t in pending), default=0)
        urgency_bucket = min(max(min_deadline, 0), 5)  # clamp 0-5
        diff_bucket = 1 if max_difficulty > 7 else 0

        return (
            round(state["student"]["energy"], -1),
            round(state["student"]["stress"], -1),
            len(pending),
            urgency_bucket,
            diff_bucket,
        )

    def choose_action(self, state):
        key = self.get_state_key(state)

        if key not in self.q_table:
            self.q_table[key] = np.zeros(len(self.actions))

        if random.random() < self.epsilon:
            return random.choice(self.actions)

        return self.actions[np.argmax(self.q_table[key])]

    def update(self, state, action, reward, next_state):
        key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)

        if next_key not in self.q_table:
            self.q_table[next_key] = np.zeros(len(self.actions))

        action_idx = self.actions.index(action)
        best_next = np.max(self.q_table[next_key])

        self.q_table[key][action_idx] += self.alpha * (
            reward + self.gamma * best_next - self.q_table[key][action_idx]
        )

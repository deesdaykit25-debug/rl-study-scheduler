import random

NUM_TASKS = 5
MAX_STEPS = 24

def generate_tasks():
    tasks = []
    for i in range(NUM_TASKS):
        tasks.append({
            "id": i,
            "difficulty": random.randint(1, 10),
            "deadline": random.randint(1, 5),
            "importance": random.randint(1, 10),
            "time_required": random.randint(1, 3),
            "completed": False
        })
    return tasks

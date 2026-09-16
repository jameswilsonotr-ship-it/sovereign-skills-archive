#!/usr/bin/env python3
"""
Lake Erie Gutter World - Task Handler (MCP Message Bus)
Handles structured tasks dropped by Vesper or other agents.
"""

import json
from pathlib import Path
from datetime import datetime

BUS_DIR = Path("mcp_message_bus")
BUS_DIR.mkdir(exist_ok=True)

def drop_task(task: dict, sender: str = "Vesper"):
    """Drop a new task into the message bus."""
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    task_file = BUS_DIR / f"{task_id}.json"
    
    task["id"] = task_id
    task["sender"] = sender
    task["timestamp"] = datetime.now().isoformat()
    task["status"] = "pending"
    
    with open(task_file, 'w') as f:
        json.dump(task, f, indent=2)
    
    return task_id

def get_pending_tasks():
    """Return all pending tasks."""
    tasks = []
    for f in BUS_DIR.glob("task_*.json"):
        with open(f) as file:
            task = json.load(file)
            if task.get("status") == "pending":
                tasks.append(task)
    return tasks

def mark_task_done(task_id: str):
    """Mark a task as completed."""
    task_file = BUS_DIR / f"{task_id}.json"
    if task_file.exists():
        with open(task_file) as f:
            task = json.load(f)
        task["status"] = "done"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        return True
    return False

if __name__ == "__main__":
    print("Task Handler ready. Use drop_task() or get_pending_tasks().")
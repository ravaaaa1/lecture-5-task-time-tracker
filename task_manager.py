"""Минимальная модель задач для самостоятельного запуска примера."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class Task:
    task_id: int
    title: str
    description: str
    priority: Priority
    due_date: datetime


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_task_id = 1

    def create_task(self, title, description, priority, due_date):
        task = Task(self.next_task_id, title, description, priority, due_date)
        self.tasks[task.task_id] = task
        self.next_task_id += 1
        return task

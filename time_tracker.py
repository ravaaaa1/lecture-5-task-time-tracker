"""Учёт времени для TaskManager из лекции 5."""

from dataclasses import dataclass
from time import monotonic
from typing import Callable


@dataclass
class Timer:
    accumulated: float = 0.0
    started: float | None = None

    def elapsed(self, now: float) -> float:
        active = 0.0 if self.started is None else now - self.started
        return self.accumulated + active


class TimeTracker:
    def __init__(self, manager, clock: Callable[[], float] = monotonic):
        self.tasks = manager.tasks
        self.clock = clock
        self.timers: dict[int, Timer] = {}

    def _timer(self, task_id: int) -> Timer:
        if task_id not in self.tasks:
            raise ValueError(f"Задача {task_id} не найдена")
        return self.timers.setdefault(task_id, Timer())

    def start(self, task_id: int) -> None:
        timer = self._timer(task_id)
        if timer.started is not None:
            raise ValueError("Таймер уже запущен")
        timer.started = self.clock()

    def stop(self, task_id: int) -> float:
        timer = self._timer(task_id)
        if timer.started is None:
            raise ValueError("Таймер не запущен")
        timer.accumulated = timer.elapsed(self.clock())
        timer.started = None
        return timer.accumulated

    def total(self, task_id: int) -> float:
        return self._timer(task_id).elapsed(self.clock())

    def report(self) -> dict:
        now = self.clock()
        rows = []
        for task_id, task in self.tasks.items():
            timer = self._timer(task_id)
            rows.append(dict(task_id=task_id, title=task.title,
                             seconds=timer.elapsed(now), running=timer.started is not None))
        return {"tasks": rows, "total_seconds": sum(row["seconds"] for row in rows)}

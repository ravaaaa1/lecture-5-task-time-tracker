import unittest
from datetime import datetime
from unittest.mock import Mock

from task_manager import Priority, TaskManager
from time_tracker import TimeTracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
        self.clock = Mock(return_value=0)
        self.tracker = TimeTracker(self.manager, self.clock)
        self.task = self.add("Разработка")

    def add(self, title):
        return self.manager.create_task(title, "", Priority.MEDIUM, datetime.now()).task_id

    def test_two_sessions_exclude_pause(self):
        self.tracker.start(self.task)
        self.clock.return_value = 3.5
        self.assertEqual(self.tracker.stop(self.task), 3.5)
        self.clock.return_value = 100
        self.assertEqual(self.tracker.total(self.task), 3.5)
        self.tracker.start(self.task)
        self.clock.return_value = 102
        self.assertEqual(self.tracker.stop(self.task), 5.5)

    def test_duplicate_start_preserves_timer(self):
        self.tracker.start(self.task)
        self.clock.return_value = 5
        with self.assertRaises(ValueError):
            self.tracker.start(self.task)
        self.assertEqual(self.tracker.total(self.task), 5)

    def test_stop_without_start(self):
        with self.assertRaises(ValueError):
            self.tracker.stop(self.task)

    def test_unknown_task(self):
        for method in (self.tracker.start, self.tracker.stop, self.tracker.total):
            with self.subTest(method=method), self.assertRaises(ValueError):
                method(404)

    def test_report_for_independent_tasks(self):
        second = self.add("Проверка")
        self.tracker.start(self.task)
        self.clock.return_value = 2
        self.tracker.start(second)
        self.clock.return_value = 4
        self.tracker.stop(second)
        self.clock.return_value = 7
        self.assertEqual(self.tracker.report(), {
            "tasks": [
                dict(task_id=self.task, title="Разработка", seconds=7, running=True),
                dict(task_id=second, title="Проверка", seconds=2, running=False),
            ],
            "total_seconds": 9,
        })

    def test_task_without_sessions(self):
        self.assertEqual(self.tracker.report()["tasks"][0]["seconds"], 0)

    def test_empty_report(self):
        self.assertEqual(TimeTracker(TaskManager()).report(), {"tasks": [], "total_seconds": 0})


if __name__ == "__main__":
    unittest.main()

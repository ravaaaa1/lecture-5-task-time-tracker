"""Интерактивная демонстрация учёта времени."""

from datetime import datetime, timedelta

from task_manager import Priority, TaskManager
from time_tracker import TimeTracker


def main():
    manager = TaskManager()
    tracker = TimeTracker(manager)
    print("Команды: add название | start ID | stop ID | report | exit")
    while True:
        try:
            command, _, arg = input("> ").strip().partition(" ")
        except EOFError:
            return
        try:
            if command == "exit":
                return
            if command == "add" and arg.strip():
                task = manager.create_task(arg.strip(), "", Priority.MEDIUM,
                                           datetime.now() + timedelta(days=7))
                print(f"Создана задача №{task.task_id}")
            elif command == "start":
                tracker.start(int(arg))
                print("Таймер запущен")
            elif command == "stop":
                print(f"Всего по задаче: {tracker.stop(int(arg)):.2f} с")
            elif command == "report":
                report = tracker.report()
                for row in report["tasks"]:
                    state = "идёт отсчёт" if row["running"] else "остановлен"
                    print(f"#{row['task_id']} {row['title']} — {row['seconds']:.2f} с ({state})")
                print(f"Итого: {report['total_seconds']:.2f} с")
            else:
                print("Проверьте команду и её аргументы.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()

"""Test script demonstrating automatic recurring task generation."""
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta


def test_recurring_task_auto_generation():
    """Test that daily/weekly tasks auto-generate the next instance when completed."""
    print("=" * 70)
    print("TESTING RECURRING TASK AUTO-GENERATION")
    print("=" * 70)

    # Setup
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@email.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(petId="1", name="Max", type="dog", breed="Labrador",
              age=4, healthInfo="Healthy", activityLevel="high", scheduler=scheduler)
    owner.addPet(pet)

    # Create a daily task for today at 8:00 AM
    today_8am = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    daily_task = Task(
        taskId="morning_walk",
        petId="1",
        description="Morning walk",
        time=today_8am,
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )
    owner.addTask(daily_task)

    print(f"\n[OK] Created daily task: '{daily_task.description}' at {daily_task.time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Total tasks before completion: {len(scheduler.tasks)}")
    print(f"  Task status: {daily_task.completionStatus}\n")

    # Mark the task as complete
    print("[*] Marking task as completed...")
    scheduler.taskCompleted("morning_walk")

    # Check results
    completed_task = next((t for t in scheduler.tasks if t.taskId == "morning_walk"), None)
    next_task = next((t for t in scheduler.tasks if t.taskId != "morning_walk"), None)

    print(f"\n[OK] Task marked complete: {completed_task.completionStatus}")
    print(f"  Total tasks after completion: {len(scheduler.tasks)}")

    if next_task:
        print(f"\n[OK] Next instance automatically created!")
        print(f"  Next task description: '{next_task.description}'")
        print(f"  Next task scheduled for: {next_task.time.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Next task status: {next_task.completionStatus}")

        # Verify the date difference
        time_diff = (next_task.time - completed_task.time).days
        print(f"  Time difference: {time_diff} day(s)")
        assert time_diff == 1, "Daily task should be scheduled 1 day later"
        print(f"  [OK] Correctly calculated as tomorrow using timedelta(days=1)")
    else:
        print("[ERROR] Next instance was not created!")
        return False

    # Test weekly task
    print("\n" + "=" * 70)
    print("TESTING WEEKLY TASK AUTO-GENERATION")
    print("=" * 70)

    today_10am = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    weekly_task = Task(
        taskId="vet_checkup",
        petId="1",
        description="Vet checkup",
        time=today_10am,
        frequency="weekly",
        priority="medium",
        duration=60,
        completionStatus="pending"
    )
    owner.addTask(weekly_task)

    print(f"\n[OK] Created weekly task: '{weekly_task.description}' at {weekly_task.time.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Total tasks: {len(scheduler.tasks)}")

    scheduler.taskCompleted("vet_checkup")

    next_weekly = next((t for t in scheduler.tasks if "vet_checkup" in t.taskId and t.taskId != "vet_checkup"), None)

    if next_weekly:
        print(f"\n[OK] Weekly task - next instance created!")
        print(f"  Next task scheduled for: {next_weekly.time.strftime('%Y-%m-%d %H:%M')}")

        # Verify the week difference
        week_diff = (next_weekly.time - weekly_task.time).days / 7
        print(f"  Time difference: {week_diff} week(s)")
        assert week_diff == 1, "Weekly task should be scheduled 1 week later"
        print(f"  [OK] Correctly calculated as next week using timedelta(weeks=1)")
    else:
        print("[ERROR] Weekly task next instance was not created!")
        return False

    # Test one-time task (should NOT auto-generate)
    print("\n" + "=" * 70)
    print("TESTING ONE-TIME TASK (NO AUTO-GENERATION)")
    print("=" * 70)

    today_2pm = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    one_time_task = Task(
        taskId="bath_time",
        petId="1",
        description="Bath",
        time=today_2pm,
        frequency="one-time",
        priority="medium",
        duration=45,
        completionStatus="pending"
    )
    owner.addTask(one_time_task)
    initial_count = len(scheduler.tasks)

    print(f"\n[OK] Created one-time task: '{one_time_task.description}'")
    print(f"  Total tasks before completion: {initial_count}")

    scheduler.taskCompleted("bath_time")
    final_count = len(scheduler.tasks)

    print(f"\n[OK] One-time task marked complete")
    print(f"  Total tasks after completion: {final_count}")

    if final_count == initial_count:
        print(f"  [OK] Correctly did NOT auto-generate next instance (one-time task)")
    else:
        print(f"  [ERROR] One-time task should not auto-generate!")
        return False

    print("\n" + "=" * 70)
    print("[OK] ALL TESTS PASSED!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    test_recurring_task_auto_generation()

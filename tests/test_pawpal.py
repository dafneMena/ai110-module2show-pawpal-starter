import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Verify that calling markComplete() changes the task's status to completed."""
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    # Initial status should be pending
    assert task.completionStatus == "pending"

    # Mark task as complete
    task.markComplete()

    # Status should now be completed
    assert task.completionStatus == "completed"
    print("[PASS] test_task_completion passed")


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create owner and scheduler
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    # Create pet and add to owner
    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    # Pet should have no tasks initially
    assert len(pet.getTasks()) == 0

    # Create and add a task
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )
    owner.addTask(task)

    # Pet should now have 1 task
    assert len(pet.getTasks()) == 1

    # Add another task
    task2 = Task(
        taskId="2",
        petId="1",
        description="Feeding time",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=15,
        completionStatus="pending"
    )
    owner.addTask(task2)

    # Pet should now have 2 tasks
    assert len(pet.getTasks()) == 2
    print("[PASS] test_task_addition passed")


def test_sorting_correctness():
    """Verify that tasks are returned in chronological order (by time)."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    # Create tasks in non-chronological order
    task_afternoon = Task(
        taskId="1",
        petId="1",
        description="Afternoon fetch",
        time=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="medium",
        duration=30,
        completionStatus="pending"
    )

    task_morning = Task(
        taskId="2",
        petId="1",
        description="Morning run",
        time=datetime.now().replace(hour=6, minute=30, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=45,
        completionStatus="pending"
    )

    task_evening = Task(
        taskId="3",
        petId="1",
        description="Evening walk",
        time=datetime.now().replace(hour=19, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="medium",
        duration=20,
        completionStatus="pending"
    )

    # Add tasks out of order
    owner.addTask(task_afternoon)
    owner.addTask(task_evening)
    owner.addTask(task_morning)

    # Get sorted tasks from scheduler
    sorted_tasks = sorted(scheduler.getAllTasks(), key=lambda task: task.time)

    # Verify chronological order
    assert sorted_tasks[0].taskId == "2"  # Morning run (6:30)
    assert sorted_tasks[1].taskId == "1"  # Afternoon fetch (15:00)
    assert sorted_tasks[2].taskId == "3"  # Evening walk (19:00)

    # Verify times are in ascending order
    for i in range(len(sorted_tasks) - 1):
        assert sorted_tasks[i].time <= sorted_tasks[i + 1].time, "Tasks not in chronological order"

    print("[PASS] test_sorting_correctness passed")


def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    # Create a daily recurring task
    task = Task(
        taskId="daily_walk",
        petId="1",
        description="Morning walk",
        time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )
    owner.addTask(task)

    # Verify initial state: 1 pending task
    assert len(scheduler.getAllTasks()) == 1
    assert scheduler.getAllTasks()[0].completionStatus == "pending"

    original_task = scheduler.getAllTasks()[0]
    original_time = original_task.time

    # Mark task as completed (should auto-generate next instance)
    scheduler.taskCompleted("daily_walk")

    # Verify original task is marked completed
    assert original_task.completionStatus == "completed"

    # Verify a new task was created
    assert len(scheduler.getAllTasks()) == 2

    # Find the new task
    new_task = next((t for t in scheduler.getAllTasks() if t.completionStatus == "pending"), None)
    assert new_task is not None, "No new pending task created"

    # Verify new task is scheduled for next day
    expected_next_time = original_time + timedelta(days=1)
    assert new_task.time == expected_next_time, f"Expected {expected_next_time}, got {new_task.time}"

    # Verify new task has same properties
    assert new_task.petId == original_task.petId
    assert new_task.description == original_task.description
    assert new_task.frequency == original_task.frequency
    assert new_task.priority == original_task.priority
    assert new_task.duration == original_task.duration

    print("[PASS] test_recurrence_logic passed")


def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times (same-pet conflicts)."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    shared_time = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)

    # Create two tasks at the same time for the same pet
    task1 = Task(
        taskId="1",
        petId="1",
        description="Breakfast",
        time=shared_time,
        frequency="daily",
        priority="high",
        duration=10,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="1",
        description="Playtime",
        time=shared_time,
        frequency="daily",
        priority="high",
        duration=20,
        completionStatus="pending"
    )

    owner.addTask(task1)
    owner.addTask(task2)

    # Detect conflicts
    conflicts = scheduler.detectConflicts()

    # Verify conflict was detected
    assert len(conflicts) > 0, "Expected conflicts to be detected, but none were found"

    # Verify the conflict message mentions the pet and both tasks
    conflict_msg = conflicts[0]
    assert "Max" in conflict_msg or "Pet 1" in conflict_msg, f"Pet name not in conflict message: {conflict_msg}"
    assert "Breakfast" in conflict_msg, f"First task not in conflict message: {conflict_msg}"
    assert "Playtime" in conflict_msg, f"Second task not in conflict message: {conflict_msg}"

    print("[PASS] test_conflict_detection passed")


def test_no_conflicts_when_clean():
    """Verify that detectConflicts returns empty list when schedule has no overlaps."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    # Create tasks at different times
    task1 = Task(
        taskId="1",
        petId="1",
        description="Morning run",
        time=datetime.now().replace(hour=6, minute=30, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=45,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="1",
        description="Afternoon fetch",
        time=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="medium",
        duration=30,
        completionStatus="pending"
    )

    owner.addTask(task1)
    owner.addTask(task2)

    # Detect conflicts
    conflicts = scheduler.detectConflicts()

    # Verify no conflicts
    assert len(conflicts) == 0, f"Expected no conflicts, but got: {conflicts}"

    print("[PASS] test_no_conflicts_when_clean passed")


def test_task_mark_missed():
    """Verify that markMissed() changes task status to missed."""
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    assert task.completionStatus == "pending"
    task.markMissed()
    assert task.completionStatus == "missed"

    print("[PASS] test_task_mark_missed passed")


def test_task_reschedule():
    """Verify that reschedule() updates task time."""
    original_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=original_time,
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    assert task.time == original_time

    new_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    task.reschedule(new_time)

    assert task.time == new_time

    print("[PASS] test_task_reschedule passed")


def test_task_update_priority():
    """Verify that updatePriority() changes task priority level."""
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now(),
        frequency="daily",
        priority="low",
        duration=30,
        completionStatus="pending"
    )

    assert task.priority == "low"
    task.updatePriority("high")
    assert task.priority == "high"

    print("[PASS] test_task_update_priority passed")


def test_task_get_details():
    """Verify that getDetails() returns formatted task information."""
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime(2026, 7, 5, 8, 0, 0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    details = task.getDetails()

    assert "Morning walk" in details
    assert "Pet: 1" in details
    assert "high" in details
    assert "pending" in details

    print("[PASS] test_task_get_details passed")


def test_pet_get_details():
    """Verify that Pet.getDetails() returns formatted pet information."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )

    details = pet.getDetails()

    assert "Max" in details
    assert "dog" in details
    assert "Labrador Retriever" in details
    assert "4" in details
    assert "high" in details

    print("[PASS] test_pet_get_details passed")


def test_remove_task():
    """Verify that removeTask() removes a task from the schedule."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    task1 = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="1",
        description="Evening walk",
        time=datetime.now(),
        frequency="daily",
        priority="medium",
        duration=20,
        completionStatus="pending"
    )

    owner.addTask(task1)
    owner.addTask(task2)

    assert len(scheduler.getAllTasks()) == 2

    scheduler.removeTask("1")

    assert len(scheduler.getAllTasks()) == 1
    assert scheduler.getAllTasks()[0].taskId == "2"

    print("[PASS] test_remove_task passed")


def test_remove_pet():
    """Verify that removePet() removes a pet and all its tasks."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet1 = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )

    pet2 = Pet(
        petId="2",
        name="Luna",
        type="dog",
        breed="Husky",
        age=2,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )

    owner.addPet(pet1)
    owner.addPet(pet2)

    # Add tasks for both pets
    task1 = Task(
        taskId="1",
        petId="1",
        description="Walk Max",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="2",
        description="Walk Luna",
        time=datetime.now(),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    owner.addTask(task1)
    owner.addTask(task2)

    assert len(owner.getPets()) == 2
    assert len(scheduler.getAllTasks()) == 2

    # Remove pet1
    scheduler.removePet("1")

    assert len(owner.getPets()) == 1
    assert owner.getPets()[0].petId == "2"
    assert len(scheduler.getAllTasks()) == 1
    assert scheduler.getAllTasks()[0].petId == "2"

    print("[PASS] test_remove_pet passed")


def test_get_tasks_by_status():
    """Verify that getTasksByStatus() filters tasks by completion status."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    task1 = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="1",
        description="Feeding",
        time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=10,
        completionStatus="completed"
    )

    task3 = Task(
        taskId="3",
        petId="1",
        description="Play",
        time=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="medium",
        duration=20,
        completionStatus="missed"
    )

    owner.addTask(task1)
    owner.addTask(task2)
    owner.addTask(task3)

    # Filter by pending
    pending_tasks = scheduler.getTasksByStatus("pending")
    assert len(pending_tasks) == 1
    assert pending_tasks[0].taskId == "1"

    # Filter by completed
    completed_tasks = scheduler.getTasksByStatus("completed")
    assert len(completed_tasks) == 1
    assert completed_tasks[0].taskId == "2"

    # Filter by missed
    missed_tasks = scheduler.getTasksByStatus("missed")
    assert len(missed_tasks) == 1
    assert missed_tasks[0].taskId == "3"

    print("[PASS] test_get_tasks_by_status passed")


def test_get_tasks_by_pet_name():
    """Verify that getTasksByPetName() filters tasks by pet name (case-insensitive)."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet1 = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )

    pet2 = Pet(
        petId="2",
        name="Luna",
        type="dog",
        breed="Husky",
        age=2,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )

    owner.addPet(pet1)
    owner.addPet(pet2)

    task1 = Task(
        taskId="1",
        petId="1",
        description="Walk Max",
        time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    task2 = Task(
        taskId="2",
        petId="2",
        description="Walk Luna",
        time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    task3 = Task(
        taskId="3",
        petId="1",
        description="Feed Max",
        time=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=10,
        completionStatus="pending"
    )

    owner.addTask(task1)
    owner.addTask(task2)
    owner.addTask(task3)

    # Get tasks for Max (case-insensitive)
    max_tasks = scheduler.getTasksByPetName("max")
    assert len(max_tasks) == 2
    assert all(t.petId == "1" for t in max_tasks)

    # Get tasks for Luna
    luna_tasks = scheduler.getTasksByPetName("Luna")
    assert len(luna_tasks) == 1
    assert luna_tasks[0].petId == "2"

    # Get tasks for non-existent pet
    nonexistent_tasks = scheduler.getTasksByPetName("Buddy")
    assert len(nonexistent_tasks) == 0

    print("[PASS] test_get_tasks_by_pet_name passed")


def test_reschedule_task():
    """Verify that rescheduleTask() updates a task's scheduled time."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    original_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    task = Task(
        taskId="1",
        petId="1",
        description="Morning walk",
        time=original_time,
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )
    owner.addTask(task)

    new_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    scheduler.rescheduleTask("1", new_time)

    updated_task = scheduler.getAllTasks()[0]
    assert updated_task.time == new_time

    print("[PASS] test_reschedule_task passed")


def test_generate_next_instance_daily():
    """Verify that generateNextInstance() creates daily tasks correctly."""
    task = Task(
        taskId="daily_walk",
        petId="1",
        description="Morning walk",
        time=datetime(2026, 7, 5, 8, 0, 0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )

    next_task = task.generateNextInstance()

    assert next_task is not None
    assert next_task.time == datetime(2026, 7, 6, 8, 0, 0)
    assert next_task.petId == task.petId
    assert next_task.description == task.description
    assert next_task.frequency == task.frequency

    print("[PASS] test_generate_next_instance_daily passed")


def test_generate_next_instance_weekly():
    """Verify that generateNextInstance() creates weekly tasks correctly."""
    task = Task(
        taskId="weekly_grooming",
        petId="1",
        description="Grooming session",
        time=datetime(2026, 7, 5, 10, 0, 0),
        frequency="weekly",
        priority="medium",
        duration=60,
        completionStatus="pending"
    )

    next_task = task.generateNextInstance()

    assert next_task is not None
    assert next_task.time == datetime(2026, 7, 12, 10, 0, 0)
    assert next_task.frequency == "weekly"

    print("[PASS] test_generate_next_instance_weekly passed")


def test_generate_next_instance_one_time():
    """Verify that generateNextInstance() returns None for one-time tasks."""
    task = Task(
        taskId="vet_visit",
        petId="1",
        description="Vet appointment",
        time=datetime(2026, 7, 5, 14, 0, 0),
        frequency="one-time",
        priority="high",
        duration=60,
        completionStatus="pending"
    )

    next_task = task.generateNextInstance()

    assert next_task is None

    print("[PASS] test_generate_next_instance_one_time passed")


def test_generate_daily_tasks():
    """Verify that generateDailyTasks() creates future instances of recurring tasks."""
    owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@example.com")
    scheduler = Scheduler(owner=owner)
    owner.scheduler = scheduler

    pet = Pet(
        petId="1",
        name="Max",
        type="dog",
        breed="Labrador Retriever",
        age=4,
        healthInfo="Healthy",
        activityLevel="high",
        scheduler=scheduler
    )
    owner.addPet(pet)

    task = Task(
        taskId="daily_walk",
        petId="1",
        description="Morning walk",
        time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
        frequency="daily",
        priority="high",
        duration=30,
        completionStatus="pending"
    )
    owner.addTask(task)

    initial_count = len(scheduler.getAllTasks())
    assert initial_count == 1

    scheduler.generateDailyTasks()

    updated_count = len(scheduler.getAllTasks())
    assert updated_count > initial_count

    # For a daily task, it should generate 365 instances (including the original)
    daily_tasks = [t for t in scheduler.getAllTasks() if t.petId == "1"]
    assert len(daily_tasks) >= 365

    print("[PASS] test_generate_daily_tasks passed")


if __name__ == "__main__":
    test_task_completion()
    test_task_addition()
    test_sorting_correctness()
    test_recurrence_logic()
    test_conflict_detection()
    test_no_conflicts_when_clean()
    test_task_mark_missed()
    test_task_reschedule()
    test_task_update_priority()
    test_task_get_details()
    test_pet_get_details()
    test_remove_task()
    test_remove_pet()
    test_get_tasks_by_status()
    test_get_tasks_by_pet_name()
    test_reschedule_task()
    test_generate_next_instance_daily()
    test_generate_next_instance_weekly()
    test_generate_next_instance_one_time()
    test_generate_daily_tasks()
    print("\nAll tests passed!")

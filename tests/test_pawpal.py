import sys
from datetime import datetime
sys.path.insert(0, '..')

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
    print("✓ test_task_completion passed")


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
    print("✓ test_task_addition passed")


if __name__ == "__main__":
    test_task_completion()
    test_task_addition()
    print("\nAll tests passed!")

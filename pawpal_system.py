from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
    taskId: str
    petId: str
    description: str
    time: datetime
    frequency: str  # "one-time", "daily", "weekly", etc.
    priority: str  # "high", "medium", "low"
    duration: int  # in minutes
    completionStatus: str  # "pending", "completed", "missed"

    def markComplete(self):
        """Mark task as completed."""
        self.completionStatus = "completed"

    def markMissed(self):
        """Mark task as missed."""
        self.completionStatus = "missed"

    def reschedule(self, newTime: datetime):
        """Update task's scheduled time."""
        self.time = newTime

    def updatePriority(self, newPriority: str):
        """Update task's priority level."""
        self.priority = newPriority

    def getDetails(self) -> str:
        """Return formatted string with task details."""
        return f"Task: {self.description} | Pet: {self.petId} | Time: {self.time} | Priority: {self.priority} | Status: {self.completionStatus}"


@dataclass
class Pet:
    petId: str
    name: str
    type: str  # "dog", "cat", etc.
    breed: str
    age: int
    healthInfo: str
    activityLevel: str  # "low", "medium", "high"
    scheduler: 'Scheduler' = None

    def getTasks(self) -> List[Task]:
        """Retrieve all tasks assigned to this pet."""
        return [task for task in self.scheduler.tasks if task.petId == self.petId]

    def getDetails(self) -> str:
        """Return formatted string with pet information."""
        return f"Pet: {self.name} | Type: {self.type} | Breed: {self.breed} | Age: {self.age} | Activity Level: {self.activityLevel}"


@dataclass
class Owner:
    ownerId: str
    name: str
    contactInfo: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: 'Scheduler' = None

    def addPet(self, pet: Pet):
        """Add a pet to the owner's pet list."""
        pet.scheduler = self.scheduler
        self.pets.append(pet)

    def removePet(self, petId: str):
        """Remove a pet from the owner's pet list."""
        self.pets = [pet for pet in self.pets if pet.petId != petId]

    def getPets(self) -> List[Pet]:
        """Return list of all pets owned by this owner."""
        return self.pets

    def addTask(self, task: Task):
        """Create a new task for one of the owner's pets."""
        self.scheduler.addTask(task)

    def removeTask(self, taskId: str):
        """Remove a task from the schedule."""
        self.scheduler.removeTask(taskId)

    def viewSchedule(self):
        """Display today's schedule for all pets."""
        self.scheduler.viewSchedule()

    def getTasksForAllPets(self) -> List[Task]:
        """Retrieve all tasks across all pets."""
        return self.scheduler.getAllTasks()


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner and empty task list."""
        self.owner = owner
        self.tasks: List[Task] = []

    def addTask(self, task: Task):
        """Add a task to the schedule after validating the pet exists."""
        if not any(pet.petId == task.petId for pet in self.owner.pets):
            raise ValueError(f"Pet with ID {task.petId} not found")
        self.tasks.append(task)

    def removeTask(self, taskId: str):
        """Remove a task from the schedule by task ID."""
        self.tasks = [task for task in self.tasks if task.taskId != taskId]

    def rescheduleTask(self, taskId: str, newTime: datetime):
        """Update the scheduled time for a specific task."""
        for task in self.tasks:
            if task.taskId == taskId:
                task.reschedule(newTime)
                return

    def viewSchedule(self, display_func=print, show_header=True):
        """Display formatted schedule of all tasks sorted by time."""
        # Build border
        border = "=" * 70

        # Build pet list
        pet_list = " & ".join([f"{pet.name} ({pet.breed})" for pet in self.owner.pets])

        # Display header only if requested
        if show_header:
            display_func(border)
            display_func(f"TODAY'S SCHEDULE FOR {self.owner.name.upper()}")
            display_func(f"Pets: {pet_list}")
            display_func(border)

        # Sort tasks by time and print each
        sorted_tasks = sorted(self.tasks, key=lambda task: task.time)
        for task in sorted_tasks:
            # Find pet name
            pet = next((p for p in self.owner.pets if p.petId == task.petId), None)
            pet_name = pet.name if pet else "Unknown"

            # Format time as HH:MM
            time_str = task.time.strftime("%H:%M")

            # Print formatted task
            display_func(f"{time_str} — {pet_name} {task.description} | {task.duration} min | Priority: {task.priority} | Status: {task.completionStatus}")

        # Print footer only if header was shown
        if show_header:
            display_func(border)

    def taskCompleted(self, taskId: str):
        """Mark a task as completed by task ID."""
        for task in self.tasks:
            if task.taskId == taskId:
                task.markComplete()
                return

    def getAllTasks(self) -> List[Task]:
        """Return list of all tasks in the schedule."""
        return self.tasks

    def generateDailyTasks(self):
        """Generate future task instances based on frequency (daily, weekly, monthly)."""
        new_tasks = []
        for task in self.tasks:
            if task.frequency == "daily":
                for i in range(1, 365):
                    new_task = Task(
                        taskId=f"{task.taskId}_day_{i}",
                        petId=task.petId,
                        description=task.description,
                        time=task.time + timedelta(days=i),
                        frequency=task.frequency,
                        priority=task.priority,
                        duration=task.duration,
                        completionStatus="pending"
                    )
                    new_tasks.append(new_task)
            elif task.frequency == "weekly":
                for i in range(1, 52):
                    new_task = Task(
                        taskId=f"{task.taskId}_week_{i}",
                        petId=task.petId,
                        description=task.description,
                        time=task.time + timedelta(weeks=i),
                        frequency=task.frequency,
                        priority=task.priority,
                        duration=task.duration,
                        completionStatus="pending"
                    )
                    new_tasks.append(new_task)
            elif task.frequency == "monthly":
                for i in range(1, 12):
                    new_task = Task(
                        taskId=f"{task.taskId}_month_{i}",
                        petId=task.petId,
                        description=task.description,
                        time=task.time + timedelta(days=30 * i),
                        frequency=task.frequency,
                        priority=task.priority,
                        duration=task.duration,
                        completionStatus="pending"
                    )
                    new_tasks.append(new_task)
        self.tasks.extend(new_tasks)

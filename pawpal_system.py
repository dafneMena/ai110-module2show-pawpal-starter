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

    def generateNextInstance(self) -> 'Task':
        """Create the next instance of a recurring task.

        Calculates the next occurrence based on task frequency and returns
        a new Task instance with the same attributes but an incremented time.
        Returns None for one-time tasks.

        Returns:
            A new Task instance for the next occurrence, or None if non-recurring.
        """
        if self.frequency == "one-time":
            return None

        # Calculate next occurrence based on frequency
        next_time = self.time
        if self.frequency == "daily":
            next_time = self.time + timedelta(days=1)
        elif self.frequency == "weekly":
            next_time = self.time + timedelta(weeks=1)
        elif self.frequency == "monthly":
            next_time = self.time + timedelta(days=30)
        elif self.frequency == "yearly":
            next_time = self.time + timedelta(days=365)

        # Create new task instance with incremented ID
        next_task = Task(
            taskId=f"{self.taskId}_repeat_{datetime.now().timestamp()}",
            petId=self.petId,
            description=self.description,
            time=next_time,
            frequency=self.frequency,
            priority=self.priority,
            duration=self.duration,
            completionStatus="pending"
        )
        return next_task


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
        """Remove a pet and all its tasks from the owner's pet list."""
        self.scheduler.removePet(petId)

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
        """Initialize scheduler with an owner and empty task list.

        Args:
            owner: The Owner instance managing pets and tasks.
        """
        self.owner = owner
        self.tasks: List[Task] = []
        self.deleted_pets: List[Pet] = []
        self.deleted_tasks: List[Task] = []

    def addTask(self, task: Task):
        """Add a task to the schedule after validating the pet exists."""
        if not any(pet.petId == task.petId for pet in self.owner.pets):
            raise ValueError(f"Pet with ID {task.petId} not found")
        self.tasks.append(task)

    def removeTask(self, taskId: str):
        """Remove a task from the schedule by task ID."""
        task_to_remove = next((task for task in self.tasks if task.taskId == taskId), None)
        if task_to_remove:
            self.tasks.remove(task_to_remove)
            self.deleted_tasks.append(task_to_remove)

    def removePet(self, petId: str):
        """Remove a pet and all its associated tasks, moving them to deleted lists."""
        pet_to_remove = next((pet for pet in self.owner.pets if pet.petId == petId), None)
        if pet_to_remove:
            self.owner.pets.remove(pet_to_remove)
            self.deleted_pets.append(pet_to_remove)

            # Move all tasks for this pet to deleted_tasks
            tasks_to_delete = [task for task in self.tasks if task.petId == petId]
            for task in tasks_to_delete:
                self.tasks.remove(task)
                self.deleted_tasks.append(task)

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


    def taskCompleted(self, taskId: str):
        """Mark a task as completed by task ID. Auto-generates next instance for recurring tasks."""
        for task in self.tasks:
            if task.taskId == taskId:
                task.markComplete()

                # Auto-generate next instance for recurring tasks
                if task.frequency != "one-time":
                    next_task = task.generateNextInstance()
                    if next_task:
                        self.tasks.append(next_task)
                return

    def getAllTasks(self) -> List[Task]:
        """Return list of all tasks in the schedule."""
        return self.tasks

    def getTasksByStatus(self, status: str) -> List[Task]:
        """Filter tasks by completion status (pending, completed, missed)."""
        return [task for task in self.tasks if task.completionStatus == status]

    def getTasksByPetName(self, pet_name: str) -> List[Task]:
        """Filter tasks by pet name (case-insensitive)."""
        matching_pet_id = None
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                matching_pet_id = pet.petId
                break
        if matching_pet_id:
            return [task for task in self.tasks if task.petId == matching_pet_id]
        return []

    def detectConflicts(self) -> List[str]:
        """Detect task conflicts and return warning messages for overlapping scheduled times.

        Identifies two types of conflicts:
        - Same-pet conflicts: multiple tasks for one pet at the same time
        - Multi-pet conflicts: tasks for different pets scheduled simultaneously

        Only considers pending tasks. Returns empty list if no conflicts found.

        Returns:
            A list of warning strings describing each conflict detected.
        """
        warnings = []

        # Group tasks by their scheduled time
        time_groups = {}
        for task in self.tasks:
            if task.completionStatus == "pending":
                time_key = task.time
                if time_key not in time_groups:
                    time_groups[time_key] = []
                time_groups[time_key].append(task)

        # Check each time slot for conflicts
        for scheduled_time, tasks_at_time in time_groups.items():
            if len(tasks_at_time) > 1:
                # Group tasks by pet ID
                by_pet = {}
                for task in tasks_at_time:
                    if task.petId not in by_pet:
                        by_pet[task.petId] = []
                    by_pet[task.petId].append(task)

                time_str = scheduled_time.strftime("%Y-%m-%d %H:%M")

                # Check for same-pet conflicts
                for pet_id, pet_tasks in by_pet.items():
                    if len(pet_tasks) > 1:
                        pet = next((p for p in self.owner.pets if p.petId == pet_id), None)
                        pet_name = pet.name if pet else f"Pet {pet_id}"
                        task_descs = " & ".join([f'"{t.description}"' for t in pet_tasks])
                        warnings.append(
                            f"[CONFLICT] {pet_name} has multiple tasks at {time_str}: {task_descs}"
                        )

                # Check for multi-pet conflicts
                if len(by_pet) > 1:
                    pet_names = []
                    for pet_id in by_pet.keys():
                        pet = next((p for p in self.owner.pets if p.petId == pet_id), None)
                        pet_names.append(pet.name if pet else f"Pet {pet_id}")

                    task_list = " & ".join(
                        [f'{next((p for p in self.owner.pets if p.petId == t.petId), None).name}: "{t.description}"'
                         for t in tasks_at_time]
                    )
                    warnings.append(
                        f"[MULTI-PET] {', '.join(pet_names)} scheduled simultaneously at {time_str}: {task_list}"
                    )

        return warnings

    def displayConflicts(self, display_func=print):
        """Display any detected task conflicts with warning messages."""
        warnings = self.detectConflicts()

        if not warnings:
            display_func("[OK] No scheduling conflicts detected!")
            return

        border = "=" * 70
        display_func(border)
        display_func("SCHEDULING CONFLICT WARNINGS")
        display_func(border)

        for warning in warnings:
            display_func(warning)

        display_func(border)

    def generateDailyTasks(self):
        """Generate future task instances based on frequency (daily, weekly, monthly).

        Creates multiple instances of recurring tasks to populate the schedule ahead.
        For daily tasks, generates 365 instances. For weekly, 52 instances. For monthly, 12 instances.
        One-time tasks are skipped. Generated tasks are automatically appended to the task list.
        """
        frequency_config = {
            "daily": (365, timedelta(days=1), "day"),
            "weekly": (52, timedelta(weeks=1), "week"),
            "monthly": (12, timedelta(days=30), "month"),
        }

        new_tasks = []
        for task in self.tasks:
            if task.frequency not in frequency_config:
                continue

            count, time_delta, suffix = frequency_config[task.frequency]
            for i in range(1, count):
                new_task = Task(
                    taskId=f"{task.taskId}_{suffix}_{i}",
                    petId=task.petId,
                    description=task.description,
                    time=task.time + (time_delta * i),
                    frequency=task.frequency,
                    priority=task.priority,
                    duration=task.duration,
                    completionStatus="pending"
                )
                new_tasks.append(new_task)

        self.tasks.extend(new_tasks)

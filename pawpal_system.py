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
        self.completionStatus = "completed"

    def markMissed(self):
        self.completionStatus = "missed"

    def reschedule(self, newTime: datetime):
        self.time = newTime

    def updatePriority(self, newPriority: str):
        self.priority = newPriority

    def getDetails(self) -> str:
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
        return [task for task in self.scheduler.tasks if task.petId == self.petId]

    def getDetails(self) -> str:
        return f"Pet: {self.name} | Type: {self.type} | Breed: {self.breed} | Age: {self.age} | Activity Level: {self.activityLevel}"


@dataclass
class Owner:
    ownerId: str
    name: str
    contactInfo: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: 'Scheduler' = None

    def addPet(self, pet: Pet):
        pet.scheduler = self.scheduler
        self.pets.append(pet)

    def removePet(self, petId: str):
        self.pets = [pet for pet in self.pets if pet.petId != petId]

    def getPets(self) -> List[Pet]:
        return self.pets

    def addTask(self, task: Task, petId: str):
        self.scheduler.addTask(task, petId)

    def removeTask(self, taskId: str):
        self.scheduler.removeTask(taskId)

    def viewSchedule(self):
        self.scheduler.viewSchedule()

    def getTasksForAllPets(self) -> List[Task]:
        return self.scheduler.getAllTasks()


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []

    def addTask(self, task: Task, petId: str):
        if not any(pet.petId == petId for pet in self.owner.pets):
            raise ValueError(f"Pet with ID {petId} not found")
        self.tasks.append(task)

    def removeTask(self, taskId: str):
        self.tasks = [task for task in self.tasks if task.taskId != taskId]

    def rescheduleTask(self, taskId: str, newTime: datetime):
        for task in self.tasks:
            if task.taskId == taskId:
                task.reschedule(newTime)
                return

    def viewSchedule(self):
        sorted_tasks = sorted(self.tasks, key=lambda task: task.time)
        for task in sorted_tasks:
            print(task.getDetails())

    def taskCompleted(self, taskId: str):
        for task in self.tasks:
            if task.taskId == taskId:
                task.markComplete()
                return

    def getAllTasks(self) -> List[Task]:
        return self.tasks

    def generateDailyTasks(self):
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

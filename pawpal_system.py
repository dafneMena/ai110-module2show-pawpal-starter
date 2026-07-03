from dataclasses import dataclass, field
from datetime import datetime
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
        pass

    def markMissed(self):
        pass

    def reschedule(self, newTime: datetime):
        pass

    def updatePriority(self, newPriority: str):
        pass

    def getDetails(self) -> str:
        pass


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
        pass

    def getDetails(self) -> str:
        pass


@dataclass
class Owner:
    ownerId: str
    name: str
    contactInfo: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: 'Scheduler' = None

    def addPet(self, pet: Pet):
        pass

    def removePet(self, petId: str):
        pass

    def getPets(self) -> List[Pet]:
        pass

    def addTask(self, task: Task, petId: str):
        pass

    def removeTask(self, taskId: str):
        pass

    def viewSchedule(self):
        pass

    def getTasksForAllPets(self) -> List[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []

    def addTask(self, task: Task, petId: str):
        pass

    def removeTask(self, taskId: str):
        pass

    def rescheduleTask(self, taskId: str, newTime: datetime):
        pass

    def viewSchedule(self):
        pass

    def taskCompleted(self, taskId: str):
        pass

    def getAllTasks(self) -> List[Task]:
        pass

    def generateDailyTasks(self):
        pass

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

# Create Owner
owner = Owner(ownerId="1", name="Sarah", contactInfo="sarah@email.com")

# Create Scheduler and link it to Owner
scheduler = Scheduler(owner=owner)
owner.scheduler = scheduler

# Create three unique Pets with different breeds and activity levels
pet1 = Pet(petId="1", name="Max", type="dog", breed="Labrador Retriever",
           age=4, healthInfo="Healthy, regular checkups", activityLevel="high", scheduler=scheduler)
pet2 = Pet(petId="2", name="Luna", type="dog", breed="Siberian Husky",
           age=2, healthInfo="Healthy, needs lots of exercise", activityLevel="high", scheduler=scheduler)
pet3 = Pet(petId="3", name="Cooper", type="dog", breed="Beagle",
           age=6, healthInfo="Healthy, watch diet for weight", activityLevel="medium", scheduler=scheduler)

# Add pets to owner
owner.addPet(pet1)
owner.addPet(pet2)
owner.addPet(pet3)

# Create Tasks for Max (Labrador Retriever)
task1 = Task(taskId="1", petId="1", description="Morning run",
             time=datetime.now().replace(hour=6, minute=30, second=0, microsecond=0),
             frequency="daily", priority="high", duration=45, completionStatus="pending")

task2 = Task(taskId="2", petId="1", description="Breakfast",
             time=datetime.now().replace(hour=7, minute=0, second=0, microsecond=0),
             frequency="daily", priority="high", duration=10, completionStatus="pending")

task3 = Task(taskId="3", petId="1", description="Afternoon fetch",
             time=datetime.now().replace(hour=15, minute=0, second=0, microsecond=0),
             frequency="daily", priority="medium", duration=30, completionStatus="pending")

# Create Tasks for Luna (Siberian Husky)
task4 = Task(taskId="4", petId="2", description="Early morning jog",
             time=datetime.now().replace(hour=5, minute=45, second=0, microsecond=0),
             frequency="daily", priority="high", duration=60, completionStatus="pending")

task5 = Task(taskId="5", petId="2", description="Dinner",
             time=datetime.now().replace(hour=18, minute=30, second=0, microsecond=0),
             frequency="daily", priority="high", duration=10, completionStatus="pending")

task6 = Task(taskId="6", petId="2", description="Evening play session",
             time=datetime.now().replace(hour=19, minute=0, second=0, microsecond=0),
             frequency="daily", priority="high", duration=45, completionStatus="pending")

# Create Tasks for Cooper (Beagle)
task7 = Task(taskId="7", petId="3", description="Breakfast",
             time=datetime.now().replace(hour=7, minute=30, second=0, microsecond=0),
             frequency="daily", priority="high", duration=10, completionStatus="pending")

task8 = Task(taskId="8", petId="3", description="Midday walk",
             time=datetime.now().replace(hour=12, minute=0, second=0, microsecond=0),
             frequency="daily", priority="medium", duration=20, completionStatus="pending")

task9 = Task(taskId="9", petId="3", description="Training session",
             time=datetime.now().replace(hour=16, minute=0, second=0, microsecond=0),
             frequency="daily", priority="medium", duration=25, completionStatus="pending")

# Add all tasks through owner
owner.addTask(task1)
owner.addTask(task2)
owner.addTask(task3)
owner.addTask(task4)
owner.addTask(task5)
owner.addTask(task6)
owner.addTask(task7)
owner.addTask(task8)
owner.addTask(task9)

# Print today's schedule
owner.viewSchedule()

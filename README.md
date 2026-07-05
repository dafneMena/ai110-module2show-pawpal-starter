# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
======================================================================
TODAY'S SCHEDULE FOR SARAH
Pets: Max (Labrador Retriever) & Luna (Siberian Husky) & Cooper (Beagle)
======================================================================
05:45 — Luna Early morning jog | 60 min | Priority: high | Status: pending
06:30 — Max Morning run | 45 min | Priority: high | Status: pending
07:00 — Max Breakfast | 10 min | Priority: high | Status: pending
07:00 — Cooper Breakfast | 10 min | Priority: high | Status: pending
07:00 — Max Playtime | 20 min | Priority: high | Status: pending
12:00 — Cooper Midday walk | 20 min | Priority: medium | Status: pending
12:30 — Luna Lunch | 15 min | Priority: high | Status: pending
15:00 — Max Afternoon fetch | 30 min | Priority: medium | Status: pending
16:00 — Cooper Training session | 25 min | Priority: medium | Status: pending
18:30 — Luna Dinner | 10 min | Priority: high | Status: pending
18:30 — Luna Evening play session | 45 min | Priority: high | Status: pending

======================================================================
SCHEDULING CONFLICT WARNINGS
======================================================================
[CONFLICT] Max has multiple tasks at 2026-07-05 07:00: "Breakfast" & "Playtime"
[MULTI-PET] Max, Cooper scheduled simultaneously at 2026-07-05 07:00: Max: "Breakfast" & Cooper: "Breakfast" & Max: "Playtime"
[CONFLICT] Luna has multiple tasks at 2026-07-05 18:30: "Dinner" & "Evening play session"
======================================================================
```


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.viewSchedule()` | Sorts all tasks by time using `sorted(self.tasks, key=lambda task: task.time)` |
| Filtering by status | `Scheduler.getTasksByStatus(status)` | Filters tasks by completion status: "pending", "completed", or "missed" |
| Filtering by pet | `Scheduler.getTasksByPetName(pet_name)` or `Pet.getTasks()` | Returns only tasks assigned to a specific pet (case-insensitive) |
| Conflict detection | `Scheduler.detectConflicts()` | Identifies overlapping tasks: same pet at same time OR multiple pets at same time |
| Conflict display | `Scheduler.displayConflicts()` | Formats and displays conflict warnings; shows "[OK] No conflicts" if clear |
| Recurring task generation | `Task.generateNextInstance()` | Creates next instance by calculating time based on frequency (daily +1 day, weekly +1 week, etc.) |
| Recurring task auto-generation | `Scheduler.taskCompleted(taskId)` | Marks task complete AND automatically generates next instance for recurring tasks |
| Recurring task bulk generation | `Scheduler.generateDailyTasks()` | Pre-generates future instances: 365 daily, 52 weekly, 12 monthly instances |

## 📸 Demo Walkthrough

1. **Set up your owner profile** — In the sidebar, enter your name and contact info, then click "Initialize PawPal" to create your account.

2. **Add your pets** — Go to the "🐕 Manage Pets" tab and fill in pet details (name, type, breed, age, health info, activity level). Your pets appear in a collapsible list on the right with a delete option.

3. **Create tasks for your pets** — In the "📝 Add Task" tab, select a pet from the dropdown and enter task details: description, time, frequency (one-time/daily/weekly/monthly/yearly), priority level, and duration in minutes. Click "Add Task" to save.

4. **View today's schedule** — Go to the "📅 Today's Schedule" tab to see all tasks sorted by time. The app displays each task with pet name, description, duration, priority, and completion status. If conflicts exist, they appear at the top in an expandable warning section.

5. **Manage tasks** — In the "⚙️ Manage Tasks" tab, filter tasks by status (pending/completed/missed) and/or by pet name. For each task, you can mark it complete (which auto-generates the next recurring instance) or delete it. The count shows how many tasks match your filters.

6. 

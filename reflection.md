# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  
The PawPal system uses a four-class architecture where the Owner is the primary user who manages their Pets through a Scheduler that serves as the central brain for task organization. Tasks are stored in the Scheduler and track pet care activities with properties like priority, frequency, and completion status.  

- What classes did you include, and what responsibilities did 
you assign to each?

Owner — Represents the pet owner. Manages multiple pets and delegates all task management (add, remove, view, reschedule) to the Scheduler.

Pet — Stores pet information (name, type, age, health info, activity level). Can only view its own tasks; cannot modify them.

Task — Represents a single care activity with attributes like description, time, priority, duration, and frequency. Supports marking complete, rescheduling, and priority updates. References a pet via petId.

Scheduler — The "brain" that manages all tasks across all pets. Stores all tasks in one place and handles task operations. Also generates new instances of recurring tasks daily.

**b. Design changes**

- Did your design change during implementation?

Yes. During the brainstorming process, we identified and fixed two key missing relationships:

Added Scheduler reference to Owner — We realized Owner needed a direct reference to Scheduler so it could properly delegate task operations (addTask, removeTask, etc.).

Added Scheduler reference to Pet — Pet's getTasks() method needed access to the Scheduler to filter and retrieve tasks belonging to that pet. Without this reference, Pet couldn't implement the method. 

- If yes, describe at least one change and why you made it.
  
These changes ensured proper communication between classes and made the delegation pattern functional. Without these relationships, Owner and Pet couldn't interact with Scheduler to manage tasks, which would have created dead code.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**
- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers time (preventing overlap), priority levels (high/medium/low for importance), and pet owner relationships (tasks tied to specific pets). 
- How did you decide which constraints mattered most?

I prioritized time constraints most, since scheduling conflicts directly break the schedule—whereas priority and activity level are informational but don't block task assignment. This reflects the reality that when to do something matters more than categorizing how important it is.

**b. Tradeoffs**
- Describe one tradeoff your scheduler makes.

The scheduler detects conflicts but doesn't auto resolve them—it warns users rather than automatically rescheduling. This trades automation for control. Users stay informed and decide how to handle overlaps, but must manually fix conflicts.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because pet care is personal—only the owner knows if two tasks can shift, or if one must stay at that exact time.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

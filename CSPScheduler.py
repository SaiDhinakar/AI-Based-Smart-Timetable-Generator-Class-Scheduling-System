from typing import List, Tuple, Dict

class Scheduler:
    def __init__(self,
                 subjects: List[str], 
                 teachers: Dict[str, List[str]],
                 time_slots: List[Tuple[str, str]]):
        """
        Initializes the scheduler with the necessary data.
        """
        self.subjects = subjects  
        self.teachers = teachers  
        self.time_slots = time_slots  

        self.schedule = {}  

    def initialize_schedule(self) -> None:
        """
        Assigns **one** available time slot per subject to avoid conflicts.
        """
        available_slots = self.time_slots[:]  # Copy of time slots
        for subject in self.subjects:
            if available_slots:
                chosen_slot = available_slots.pop(0)  # Assign one slot per subject
                self.schedule[subject] = [chosen_slot]
            else:
                self.schedule[subject] = []  # No slots available

    def find_teacher_conflicts(self) -> Dict[str, List[Tuple[str, str]]]:
        """Finds teacher conflicts where the same teacher is assigned overlapping subjects."""
        teacher_conflicts = {}

        for teacher, subjects in self.teachers.items():
            occupied_slots = {}  

            for subject in subjects:
                for time_slot in self.schedule.get(subject, []): 
                    if time_slot in occupied_slots:
                        teacher_conflicts.setdefault(teacher, []).append((subject, time_slot))
                        teacher_conflicts[teacher].append((occupied_slots[time_slot], time_slot))  
                    else:
                        occupied_slots[time_slot] = subject  

        return teacher_conflicts
    
    def resolve_teacher_conflicts(self):
        """Resolves teacher conflicts by finding an alternative slot or swapping subjects."""
        conflicts = self.find_teacher_conflicts()

        for teacher, sub_time_pairs in conflicts.items():
            for subject, time_slot in sub_time_pairs:
                alternative_slot = self.find_alternative_slot(time_slot)

                if alternative_slot:
                    self.schedule[subject].remove(time_slot)
                    self.schedule[subject].append(alternative_slot)
                else:
                    # If no alternative, swap with another subject
                    for swap_subject, swap_slots in self.schedule.items():
                        if swap_subject != subject and time_slot in swap_slots:
                            swap_slots.remove(time_slot)
                            swap_slots.append(self.find_alternative_slot(time_slot) or time_slot)
                            break

    def find_alternative_slot(self, conflicting_slot: Tuple[str, str]) -> Tuple[str, str] | None:
        """Finds an available time slot that is not occupied."""
        occupied_slots = {slot for slots in self.schedule.values() for slot in slots}

        for slot in self.time_slots:
            if slot not in occupied_slots:
                return slot

        return None  # No alternative slot found

    def finalize_schedule(self):
        """Finalizes the schedule by assigning subjects that couldn't be scheduled initially."""
        unassigned_subjects = [subject for subject in self.subjects if not self.schedule.get(subject)]
        available_slots = set(self.time_slots) - {slot for slots in self.schedule.values() for slot in slots}

        for subject in unassigned_subjects:
            for time_slot in available_slots:
                self.schedule[subject] = [time_slot]
                available_slots.remove(time_slot)  
                break

if __name__ == '__main__':
    # Sample Subjects and Teachers
    subjects = ["Math", "Physics", "Chemistry", "Biology"]
    teachers = {
        "Alice": ["Math", "Physics"],
        "Bob": ["Chemistry"],
        "Charlie": ["Biology"]
    }
    time_slots = [("Monday", "9AM"), ("Monday", "10AM"), ("Monday", "11AM")]

    # Initialize the Scheduler
    scheduler = Scheduler(subjects, teachers, time_slots)

    # Run the Scheduling Methods
    scheduler.initialize_schedule()
    scheduler.resolve_teacher_conflicts()  
    scheduler.finalize_schedule()

    # Print Final Schedule
    print("\nFinal Schedule:")
    for subject, slots in scheduler.schedule.items():
        if slots:
            print(f"{subject}: {slots[0]}")

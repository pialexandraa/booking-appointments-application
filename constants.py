from typing import List, Dict

# Working days of the week defined
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# The standardweekday slots
WEEKDAY_SLOTS: Dict[str, List[str]] = {
    "Monday": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
    "Tuesday": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
    "Wednesday": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
    "Thursday": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
    "Friday": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
    "Saturday": ["10:00", "11:00", "12:00"],
    "Sunday": ["No working hours. For emergencies, please reach the on-call vet the main line listed on the website."]
}

# The veterinarians working in the clinic
VETERINARIANS: Dict[str, str] = {
    "a" : "Dr. Arron",
    "b" : "Dr. Beth",
    "c" : "Dr. Kalyen",
    "d" : "Dr. Neelini",
    "e" : "Dr. Mihael"
    }

# Ths standard shifts of vets; all vets work full-time shifts
VET_SCHEDULES: Dict[str, List[str]] = {
    "Dr. Arron": ["Monday", "Wednesday", "Friday"],
    "Dr. Beth": ["Tuesday", "Thursday", "Saturday"],
    "Dr. Kalyen": ["Monday", "Tuesday", "Wednesday", "Thursday"],
    "Dr. Neelini": ["Friday", "Saturday"],
    "Dr. Mihael": ["Wednesday", "Saturday"]
}
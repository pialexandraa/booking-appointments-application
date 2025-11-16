import logging
import datetime as dt
from constants import *
from dataclasses import dataclass
from appointments_logic.service import get_current_day, find_vet_schedule
from typing import Dict, List, Tuple, Set

# Logger initialization
logger = logging.getLogger(__name__)

# Defining the Slot class
@dataclass(order=True)
class Slot:
    datetime: dt.datetime
    vet: str

# Customer exception with context
class InvalidSlotError(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field
    def __str__(self):
        if self.field:
            return f"[{self.field}]: {super().__str__()}"
        return super().__str__()

# Erorr handling for slot format
def check_slot_format(slot):
    if not isinstance(slot, Slot):
        raise InvalidSlotError("The slot must be an instance of the Slot class.", field="slot")
    elif not isinstance(slot.datetime, dt.datetime):
        raise InvalidSlotError("Slot.datetime must be a datetime object.", field="datetime")
    elif not isinstance(slot.vet, str):
        raise InvalidSlotError("Slot.vet must be a string.", field="vet")
    else:
        return True
    
# Check slot
def check_slot_error(slot):
    try:
        check_slot_format(slot)
        return True, None
    except InvalidSlotError as err:
        logger.error(f"Slot format error: {err}")
        return False, str(err)        

# Basic layer of slot-time logic
def make_slot(datetime, vet):
    return Slot(datetime=datetime, vet=vet)

def slot_vet(slot):
    return slot.vet

def slot_date_time(slot):
    return slot.datetime

# Adding a slot
def add_slot(slots: Set[Slot], slot: Slot) -> Set[Slot]:
    valid, not_valid = check_slot_error(slot)
    if not valid:
        logger.warning(f"Can't add slot: slot not valid: {not_valid}")
        return slots
    elif not(slot in slots and valid):
        logger.info(f"UNKNOWN ERROR. Either the slot already exists or there is another issue. Please, try again.")
    else:
        slots.add(slot)
        logger.info(f"Slot added successfully.")
        return slots
    
# Removing a slot
def remove_slot(slots: Set[Slot], slot: Slot) -> Set[Slot]:
    valid, not_valid =check_slot_error(slot)
    if not valid:
        logger.warning(f"Can't remove slot: slot not valid: {not_valid}")
        return slots
    else:
        try:
            slots.remove(slot)
            logger.info(f"Slot removed successfully.")
            return slots
        except KeyError:
            logger.error(f"Can't remove slot: slot not found in slots.")
            return slots

# Defining the slot duration, appointment=1 hour
SLOT_DURATION = dt.timedelta(hours=1)

# The possible slots for a given day
def subdivise_day(schedule: List[str], day: dt.date) -> List[dt.datetime]:
    possible_slots = []
    working_day = get_current_day(day)
    shifts = find_vet_schedule(schedule, working_day)

    for shift in shifts:
        if "No working hours" in shift: 
            print(shift)
            return None
        else:
            start_string, end_string = shift.split("-")
            start_hour = dt.datetime.strptime(start_string, "%H:%M").time()
            end_hour = dt.datetime.strptime(end_string, "%H:%M").time()
            start_dt = dt.datetime.combine(day, start_hour)
            end_dt = dt.datetime.combine(day, end_hour)
            current = start_dt
            while current < end_dt:
                possible_slots.append(current)
                current += SLOT_DURATION
    return possible_slots
  
# Make the daily schedule slots
def make_daily_slots(WEEKDAYS_SLOTS: dict, date: dt.date) -> Set[Slot]:
    slots = set()
    for vet, schedule in WEEKDAY_SLOTS.items():
        possible_slots = subdivise_day(schedule, date)
        for datetime_point in possible_slots:
            slot = Slot(datetime_point, vet)
            add_slot(slots, slot)
    return slots

# Filtering functions
def filter_slots_by_vet(slots: Set, vet: str) -> Set[Slot]:
    filtered_slots = set()
    if vet not in VETERINARIANS:
        logger.warning(f"The specified vet does not exist. Please, try again.")
        return None
    else:
        for slot in slots:
            if slot.vet == vet:
                filtered_slots.add(slot)
        return filtered_slots
    
# Filtering the available slots for a given date
def filter_slots_by_date(slots, date):
    filtered_slots = set()
    if not isinstance(date, dt.date):
        logger.warning("Please, re-initiate the process and insert a valid date for your appointment.")
        return None
    else:
        filtered_slots = set()
        for slot in slots:
            if slot.datetime.date() == date:
                filtered_slots.add(slot)
        return filtered_slots
        

# Defining slot operations
# union of slots
def union_slots(*slot_sets: Set[Slot]) -> Set[Slot]:
    result = set()
    for slot in slot_sets:
        result = result.union(slot)
    return result

# slots intersection
def common_slots(*slot_sets: Set[Slot]) -> Set[Slot]:
    if not slot_sets:
        return set()
    result = slot_sets[0]
    for slot in slot_sets[:1]:
        result = result.intersection(slot)
    return result

# slots differences - only the slots that are in slot1 and not in other_slots
def slots_difference(slot1: Set[Slot], *other_slots: Set[Slot]) -> Set[Slot]:
    result = slot1.copy()
    for slot in other_slots:
        result = result.difference(slot)
    return result

# slots symetric difference - the slots that are in either of the sets, but not in both
def slots_symmetric_difference(slot1: Set[Slot], slot2: Set[Slot]) -> Set[Slot]:
    return slot1.symmetric_difference(slot2)

# slots subset
def is_subset(slot1: Set[Slot], slot2: Set[Slot]) -> bool:
    return slot1.issubset(slot2)

# slots superset
def is_superset(slot1: Set[Slot], slot2: Set[Slot]) -> bool:
    return slot1.issuperset(slot2)
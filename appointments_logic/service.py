import datetime as dt
import logging
from constants import *
from slot_times import (add_slot, check_slot, filter_slots_by_date, filter_slots_by_vet, make_slot, make_daily_slots)
from appointments_logic.core import appointment_slot, add_appointment, make_appointment
from vet_schedules import (find_vet_schedule)

# Initializing the logger
logger = logging.getLogger(__name__)

# High-level logic for the appointment system
def create_appointment(appointments, appointment, available_slots, reserved_slots):
    slot = appointment_slot(appointment)
    if check_slot(available_slots, slot) is True:
        add_appointment(appointments, appointment)
        add_slot(reserved_slots, slot)
        available_slots.remove(slot)
        logger.info("Successfully created the appointment.")
        return appointments, available_slots, reserved_slots
    else:
        logger.warning("The appointment could not be created! The slot is either reserved or unavailable. Please, refresh the page/system and try again.")
        return None, available_slots, reserved_slots
    
def get_available_slots_for_vet(vet, date_time, VET_SCHEDULES, reserved_slots):
    current_day_slots = make_daily_slots(VET_SCHEDULES, date_time.date())
    check_slots_vet = filter_slots_by_vet(current_day_slots, vet)
    check_slots_date = filter_slots_by_date(current_day_slots, date_time)
    intersect_slots = set(check_slots_vet).intersection(set(check_slots_date))
    available_slots = list(intersect_slots - set(reserved_slots))
    logger.debug(f"The available slots for the vet '{vet}' on the date '{date_time.date()}' are:\n{available_slots}.")
    return available_slots

# Certain slots are already reserved for emergencies
def reserved_slot_appointments(customer, date_time, vet, VET_SCHEDULES, reserved_slots, appointments, available_slots):
    current_schedules = find_vet_schedule(VET_SCHEDULES, VETERINARIANS)
    current_day_slots = make_daily_slots(VET_SCHEDULES, date_time.date())
    if (current_schedules is False) or (current_schedules is None):
        logger.warning("Our veterinarian is not available at the chosen moment.")
        return None
    elif date_time not in current_day_slots:
        logger.warning("The chose date and time combination is not available.")
        return None
    elif (date_time, vet) in reserved_slots:
        logger.warning("The chosen slot is already reserved for emergency appointments. Please, retry to make the appointment or contact our team.")
        return None
    else:
        check_slots_vet = filter_slots_by_vet(current_day_slots, vet)
        check_slots_date = filter_slots_by_date(current_day_slots, date_time)
        intersect_slots = set(check_slots_vet).intersection(set(check_slots_date))
        if len(intersect_slots) == 0:
            logger.warning("The chosen slot is not available. Please, retry to make the appointment or contact our team.")
            return None
        else:
            slot = make_slot(date_time, vet)
            appointment = make_appointment(customer, slot)
            logger.debug(f"Creating emergency reservation for the slot: {slot}.")   
            return create_appointment(appointments, appointment, available_slots, reserved_slots)
# Low-level logic for the appointment system
from dataclasses import dataclass
from slot_times import Slot
from typing import List
import logging
from slot_times import *

# Logger initialization
logger = logging.getLogger(__name__)

# Base class (with init, repr and eq included)
@dataclass(frozen=True)
class Appointment:
    customer: str
    slot: Slot

# Basic appointment constructors and accessors
def appointment_customer(appointment: Appointment) -> str:
    return appointment.customer
    
def appointment_slot(appointment: Appointment) -> object:
    return appointment.slot
    
def appointment_vet(appointment: Appointment):
    return slot_vet(appointment.slot)

def appointment_date_time(appointment: Appointment):
    return slot_date_time(appointment.slot)
    
# Appointment logic functions

# this function creates an appointment object, the instantiation:
def make_appointment(customer: str, slot: object) -> Appointment:
    return Appointment(customer, slot)

# this function adds the appointment to the list:
def add_appointment(appointments: List[Appointment], appointment: Appointment):
    if not isinstance(appointments, list):
        logger.error("The apointments entry is not a valid list.")
        raise TypeError("The appointments entry is not valid. Please, try again.")
    elif check_slot_error(appointment_slot(appointment)) is None:
        logger.warning("The appointment has not been added due to an invalid slot format.")
        return None
    else:
        appointments.append(appointment)
        logger.info("Successfully added the appointment.")
        return appointments

def remove_appointment(appointments, appointment):
    if not isinstance(appointments, list):
        logger.error("The apointments entry is not a valid list.")
        raise TypeError("The appointments entry is not valid. Please, try again.")
    elif check_slot_error(appointment_slot(appointment)) is None:
        logger.warning("Can't remove appointment due to an invalid slot.")
        return None
    elif appointment in appointments:
        appointments.remove(appointment)
        logger.info(f"Successfully removed the apointment: {appointment}.")
        return appointments
    else:
        logger.warning("The given appointment entry is not currently in the list of appointments.")
        return None

def check_appointment_status(appointments, appointment):
    if not isinstance(appointments, list):
        logger.error("The apointments entry is not a valid list.")
        raise TypeError("The appointments entry is not valid. Please, try again.")
    elif check_slot_error(appointment_slot(appointment)) is None:
        logger.warning("Can't check the appointment status due to an invalid slot.")
        return False
    elif appointment in appointments:
        logger.info(f"The records show that the given appointmet is present in the system: '{appointment}'")
        return True
    else:
        logger.info(f"The records show that the given appointment ({appointment}) is NOT scheduled in the system.")
        return False
    
def update_current_appointment(appointments: List[Appointment], old_appointment: Appointment, new_appointment: Appointment):
    if not isinstance(appointments, list):
        logger.error("The apointments entry is not a valid list.")
        raise TypeError("The appointments entry is not valid. Please, try again.")
    elif check_slot_error(appointment_slot(old_appointment)) is None or False:
        logger.warning("Can't update the old appointment data due to an invalid slot format. Please, try again.")
        return None
    elif check_slot_error(appointment_slot(new_appointment)) is None or False:
        logger.warning("Can't update the new appointment data due to an invalid slot format. Please, try again.")
        return None
    elif old_appointment not in appointments:
        logger.warning("The old appointment is not in the list. Can't update. Please, try again.")
        return None                 
    else:
        remove_appointment(appointments, old_appointment)
        add_appointment(appointments, new_appointment)
        logger.info(f"The appointment has been successfully updated. Old appointment: {old_appointment};\nNew appointment: {new_appointment}.")
        return appointments
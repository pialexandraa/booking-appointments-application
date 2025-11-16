from pathlib import Path
from threading import Lock
from typing import Set, List, Dict
from slot_times import Slot
from datetime import datetime
from appointments_logic.core import Appointment
import json
import logging
import tempfile
import os

# Initializing the logger
logger = logging.getLogger(__name__)

# Data pointing to the JSON file
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"
AVAILABLE_SLOTS_FILE = DATA_DIR / "available_slots.json"
RESERVED_SLOTS_FILE = DATA_DIR / "reserved_slots.json"

# Initialized the lock for thread-safe operations
lock = Lock()

# Atomic write helper (for adding and removing appointments); atomicity ensured at write-data level
def atomic_write_json(file_path, data, indent=4):
    dir_path = file_path.parent
    temp_file_handle, temp_file_path = tempfile.mkstemp(dir=str(dir_path))
    try:
        with os.fdopen(temp_file_handle, 'w', encoding="utf-8") as temp_file:
            json.dump(data, temp_file, indent=indent)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_file_path, file_path)
    except OSError as os_err:
        logger.error(f"Atomic write of the file {file_path} failed due to error: {os_err}.")
        raise os_err
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Atomic read helper
def atomic_read_json(file_path):
    if not file_path.exists():
        logger.warning(f"The file {file_path} does not exist. Returning empty list.")
        return []
    with lock:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as json_err:
            logger.error(f"Error decoding JSON from file {file_path}. Error: {json_err}. Returning empty list.")
            return []

# Serialization and deserialization helpers for the objects Appointment and Slot

# convert Slot object into dictionary into JSON serializable format
def serialize_slot(slot: Slot) -> dict:
    return {
        "datetime": slot.datetime.isoformat(),
        "vet": slot.vet
    }

# convert JSON dictionary data into Slot object
def deserialize_slot(slot_dict: Dict) -> Slot:
    return Slot(
        datetime=datetime.fromisoformat(slot_dict["datetime"]),
        vet=slot_dict["vet"]
    )
# convert appointment object into JSON serializable format
def serialize_appointment(appointment: Appointment) -> Dict:
    return {
        "customer": appointment.customer,
        "slot": serialize_slot(appointment.slot)
    }

# convert JSON dictionary data into appointment object
def deserialize_appointment(appointment_dictionary: Dict) -> Appointment:
    return Appointment(
        customer=appointment_dictionary["customer"],
        slot=deserialize_slot(appointment_dictionary["slot"])
    )

# Load the state of data using the atomic read helper
def load_state():
    try:
        appointments = atomic_read_json(APPOINTMENTS_FILE)
        available_slots = atomic_read_json(AVAILABLE_SLOTS_FILE)
        reserved_slots = atomic_read_json(RESERVED_SLOTS_FILE)

        appointments = [deserialize_appointment(data) for data in appointments]
        available_slots = [deserialize_slot(data) for data in available_slots]
        reserved_slots = [deserialize_slot(data) for data in reserved_slots]

        logger.info("Successfully loaded the state/data from the JSON files.")
        return appointments, available_slots, reserved_slots        
    except Exception as err:
        logger.error(f"An error has occured while loading the state. Error: {err}. Returning empty lists.")
        return [], [], []
    
# Save the state of data using the atomic read helper
def save_state(appointments, available_slots, reserved_slots):
    try:
        appointments_serialized = [serialize_appointment(data) for data in appointments]
        available_slots_serialized = [serialize_slot(data) for data in available_slots]
        reserved_slots_serialized = [serialize_slot(data) for data in reserved_slots]

        atomic_write_json(APPOINTMENTS_FILE, appointments_serialized)
        atomic_write_json(AVAILABLE_SLOTS_FILE, available_slots_serialized)
        atomic_write_json(RESERVED_SLOTS_FILE, reserved_slots_serialized)
        
        logger.info("Successfully saved the state/data to JSON files.")
    except Exception as err:
        logger.error(f"An error has occured while saving the state: {err}")
        raise err

class AppointmentStorage:
    def __init__(self):
        self._lock = Lock()
        self.appointments, self.available_slots, self.reserved_slots = load_state()

    def save(self):
        with self._lock:
            save_state(self.appointments, self.available_slots, self.reserved_slots)
            return None

    def find_appointment(self, customer: str, slot: Slot) -> Appointment:
        with self._lock:
            for appointment in self.appointments:
                if (appointment.customer == customer) and (appointment.slot == slot):
                    logger.info(f"Successfully identified the appointment. The appointment is for {customer} at {slot}.")
                    return appointment
                else:
                    logger.warning(f"This appointment was not found. If you believe this is an error, please, try again and make sure you insert the correct details.")
                    return None
        
    def add_appointment(self, appointment: Appointment):
        with self._lock:
            self.appointments.append(appointment)
            self.save_state()
            logger.info(f"Appointment {appointment} was added successfully.")
            return None

    def remove_appointment(self, appointment: Appointment):
        with self._lock:
            if appointment in self.appointments:
                self.appointments.remove(appointment)
                self.save_state()
                logger.info(f"Appointment {appointment} was removed successfully.")
                return None
            else:
                logger.warning(f"Appointment {appointment} not found. Can't complete the removal action. Try again.")
                return None

    def reserve_slot(self, slot: Slot):
        with self._lock:
            self.reserved_slots.append(slot)
            self.save()
            logger.info(f"Slot {slot} was reserved successfully.")
            return None
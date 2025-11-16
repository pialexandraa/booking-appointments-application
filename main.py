from asyncio.log import logger
from appointments_logic.core import (appointment_slot, appointment_customer, add_appointment, check_appointment_status, remove_appointment)
from appointments_logic.service import create_appointment, make_appointment, get_available_slots_for_vet
from constants import *
import datetime as dt
import logging
from slot_times import * # has to be refined, can't go slot_times logic and storage_logic functions simulaneously
from storage_logic import *

# Defining the global logger
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  )

# Initializing the storage system
storage = AppointmentStorage()

# Loading the existing state from storage:
appointments, reserved_slots, available_slots = load_state()

# Helper function to print veterinarian options: 
def print_veterinarians(VETERINARIANS):
    print("Veterinarians in our clinic:")
    for key, value in VETERINARIANS.items():
        print("{}. {}".format(key, value))
    return None

# Getting the available schedules for a given day
def get_day_schedule(WEEKDAY_SLOTS, day):
    if type(day) is not str:
        new_day = get_current_day(day)
        return WEEKDAY_SLOTS[new_day]
    elif day not in WEEKDAY_SLOTS.keys() or day == "Sunday":
        print("The clinic is closed on Sundays. For emergencies, please reach the on-call vet the main line listed on the website.")
        return None
    else:
        return WEEKDAY_SLOTS[day]

def request_date():
  raw_input = input('Please, enter a date in the format YYYY-MM-DD (use the separator "-" ): ')
  year, month, day = tuple(raw_input.split("-"))
  year, month, day = int(year), int(month), int(day)   
  return dt.date(year, month, day)

def request_time():
  raw_input = input("Please, enter a time with minutes in the 24H format. Remember: 1 appointment lasts 1 hour, so appointments start at fixed hours. Example: HH:MM (e.g. 10:00):\n")
  hour, minute = tuple(raw_input.split(":"))
  hour, minute = int(hour), int(minute)
  return dt.time(hour, minute)

def make_date_time():
  date = request_date()
  time = request_time()
  return dt.datetime.combine(date, time)

# Interactive helper to check an existing appointment (Option [8])
def check_existing_appointment_interactive():
  pass

# Application logic starts here:
def main():
  while True:
    message = input("""Hello and welcome to out vet clinic appointment system! Here are your options:
                    [1]. Check available slots for a given day.\nPlease, follow the instructions:
                    [2]. Check our overall schedule for availability.
                    [3]. Check the overall schedule of a specific veterinarian.
                    [4]. See the available slots for a specific vet.
                    [5]. Make an appointment.
                    [6]. Reserve a time slot.
                    [7]. Cancel an appointment.
                    [8]. Check the status of a current appointment.
                    [9]. Request help for medical vet emergencies.
                    [10]. Exit the appointment system.
                    Please, enter the number of the desired option:
                    """)
    if message == "1":
      day_inserted = input("Please, enter the day you want to check the available slots for (example input: 'YYYY-MM-DD' or 'Friday')")
      available_slots = get_day_schedule(WEEKDAY_SLOTS, day_inserted)
      print(available_slots)

      individual_slots = input("Do you want to see the individual slots available for that day? Type 'yes' or 'no': ")
      if individual_slots.lower() == "yes":
        specific_date = request_date().strftime("%y-%m-%d")
        requested_day = get_current_day(specific_date)
        print(f"The available slots for {requested_day} are: ", subdivise_day())
        
    elif message == "2":
      schedule_check = get_day_schedule(WEEKDAY_SLOTS, request_date())
      print(schedule_check)
    elif message == "3":
      print("Next, we will show you the list of veterinarians available at our clinic.")
      print_veterinarians(VETERINARIANS)
      vet_choice = input("Please, enter the letter corresponding to the vet of your choice:\n")
      if isinstance(vet_choice, str) is False:
        logging.error(f"The given input is not valid: {vet_choice}.")
        print("Please, restart the process.")
        return False
      else:
         if vet_choice not in VETERINARIANS.keys():
            logger.warning("The input is not a valid option/choice.")
            print("The given input is not valid choice/option. Please, restart the process")
            return None
         else:
            info = "Normal working times are: 9:00-12:00 & 14:00-17:00 on weekdays, and 10:00-13:00 on Saturday. Sundays are normally off/closed.\n"
            vet_name = VETERINARIANS[vet_choice]
            vet_schedule = VET_SCHEDULES[vet_name]
            print(f"{vet_name}'s shifts include normal working hours in the following days {vet_schedule}. Remember: if it is a Saturday, the working hours end at 13:00. Hence, the last appointment should start at 12:00.")
            return None
    elif message == "4":
      print("Here are our lovely veterinarians: ", list(VETERINARIANS.values()))
      availability = get_available_slots_for_vet()
      print(availability)
    elif message == "5":
      pass
    elif message == "6":
      pass
    elif message == "7":
      pass
    elif message == "8":
      pass

    elif message == "9":
      print("For medical emergencies, please contact our 24/7 emergency line at (555) 123-4567. Our on-call veterinarian will assist you promptly.")
    elif message == "10":
      print(f"Thank you for using our vet clinic appointment system. Wish you a very good day ahead! Exiting programme...")
      exit()     

if __name__ == "__main__":
    main()
**[Work in progress]**
- At the moment, I just wrote a lot of code (many functions and helpers). There must be a refactoring done to "slim down" the process and finalize a comprehensive data flow.
Initially, the application was supposed to be small, but later, I decided to introduce the JSON files, stored in "data."

- This led me to create an extensive set of functions and atomic helpers - see "storage_logic.py" :) obviously, this introduced 2 paths/routes of data writting and fetching - via the slot_times.py (with more traditional functions I wrote) and the option with derived availability via the JSON files.

- Also, main.py has to be refined.


---
Title: **Booking appointments application (for a Veterinary clinic)**

Description: The application is designed to be a booking system for the Vet clinic. That means that structurally, it can write, retain, remove, and manipulate information about bookings and the respective time slots.

About the technical implementation:

1. In this application, I tried to refine my code and make it a bit more modern and "pythonic." For example, I used dataclasses hoping to make the code implementations simplistic and modular. I believe this also adds immutability, better readability, and offers more control over the specific types I am dealing with.
2. I tried to reduce my rather excessive tendency for error handling and blend it into the code more nicely. Hence, I wrote the specific functions for conducting regular checks. Alternatively, I used the "logging" liberary and set up the logger in the main.py file. This helped greatly handle the error messages, warnings, or debug-logging activity, especially for the code written in the core.py and service.py files, code that actually handles the appointments logic.
3. For data storing, I chose to go with JSON files (lightweight, simple, user-readable format). Alternativelly, there could be a lightweight database connected to the application; given the demonstrative nature of this application, the JSON files would do just good for now.
4. Speaking of error handling (as previously mentioned), I have taken a chance at integrating into the project and using the "typing" library. Its main purpose for me was to help me handled the inputs and outputs, for catching errors beforehand - pre-runtime errors, as well as for improving readability and refactoring. So the type hinting is used pretty extensively (which offers more clarity and control over the operations).
   
Disclaimer: Everything listed here is free and has the purpose of serving as a training/educational resource for the current GitHub user (the author).

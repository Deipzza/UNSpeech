import schedule as sc
from threading import Thread
from time import sleep

from .tasks import *

def create_schedule_thread(send_alert):
    """Creates and initializes the schedule thread.
    
    Inputs:
    send_alert -> function to run scheduled alerts.
    """

    send_time = "01:00"
    sc.every().day.at(send_time).do(send_alert)

    # Start the scheduler thread
    scheduler_thread = Thread(target = run_scheduler)
    scheduler_thread.start()

def run_scheduler():
    """Constantly runs the scheduler thread"""

    while True:
        sc.run_pending()
        sleep(30)

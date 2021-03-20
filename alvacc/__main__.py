#!/usr/bin/python3

import os
import sys
from datetime import datetime
import time
import argparse
import webbrowser

from .locations import Availability, sort_avail, next_avail, get_locations
from .config import config


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--sleep",
        action="store",
        dest="sleep_time",
        help="Time to sleep between queries (seconds)",
        default=300,
    )
    parser.add_argument(
        "--current_appointment_date",
        action="store",
        dest="current_appointment_date",
        help='current appointment in "Month day" format',
        nargs="+",
        default="",
    )
    parser.add_argument(
        "--confirmation_number",
        action="store",
        dest="confirmation_number",
        help="Confirmation number from previously booked appointment",
        default=None,
    )
    parser.add_argument(
        "--locations",
        action="store",
        dest="locations",
        nargs="+",
        help="space-seperated list of counties to use. available counties:\n"
        + " ".join(sorted(get_locations())),
        default=None,
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        dest="reset_config",
        help="reset and recreate config file",
    )
    parser.add_argument(
        "-c",
        "--cfg",
        action="store",
        dest="config_file",
        help="path to yaml config file",
    )
    return parser.parse_args()


def bold(text, should_bold=True):
    """add term codes to make bold and escape

    Args:
        text: text to be printed as bold
        should_bold: bool to return bold or original
    """
    return f"\033[1m{text}\033[0m" if should_bold else text


def main():
    args = parse_args()
    args.current_appointment_date = " ".join(args.current_appointment_date)
    cfg = config(**vars(args))
    max_name_len = max([len(loc.name) for loc in cfg.locations])
    while True:
        new_availability = False
        # check each location for new availability
        for loc in cfg.locations:
            # getting previous availability clears bold by reprinting
            new_availability |= loc.availability.is_new
            try:
                loc.availability.current = loc.check_next_available()
                new_availability |= loc.availability.is_new
            except OSError:
                continue
            appt_avail = bool(
                loc.availability.current.date < cfg.current_appointment_date
                if loc.availability.is_new and loc.availability.current.date
                else False
            )
            if appt_avail:
                print(f"--- New Appointment Available! ---")
                # open browser to vaccine edit page
                webbrowser.open(cfg.confirmation_url)
        # print results
        current_time = datetime.now().strftime("%H:%M:%S")
        if new_availability:
            os.system("cls" if os.name == "nt" else "clear")
            print(current_time)
            # print all, bolding changes
            print_strings = [
                f"  {name:{max_name_len}} - {bold(str(avail), avail.is_new)}"
                for name, avail in sort_avail(cfg.locations).items()
            ]
            print("\n".join(print_strings))
        print("Last checked at " + str(current_time), end="\r")
        time.sleep(int(args.sleep_time))
    return 0


if __name__ == "__main__":
    sys.exit(main())

import os
import sys
import pkg_resources
from datetime import datetime
import yaml
import importlib
import re
import readline

from .locations import get_locations


def dist_is_editable(package_name):
    """Is distribution an editable install?"""
    for path_item in sys.path:
        egg_link = os.path.join(path_item, package_name + ".egg-link")
        if os.path.isfile(egg_link):
            return True
    return False


def _import_locations(location_names=None):
    if not location_names:
        return None
    return [importlib.import_module(loc, "locations") for loc in location_names]


class config:
    def __init__(self, **kwargs):
        self._current_appointment_date = kwargs.get("current_appointment_date")
        self.confirmation_number = kwargs.get("confirmation_number")
        self.locations = _import_locations(kwargs.get("locations"))
        self._config_file = kwargs.get("config_file")
        self._reset_config = kwargs.get("reset_config")

        parent_package = importlib.find_loader(__name__.split(".")[0])
        parent_package = parent_package.name if parent_package else None
        root_dir = (
            os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            if parent_package and dist_is_editable(parent_package)
            else os.path.expanduser("~")
        )
        self._config_file = kwargs.get("config_file") or os.path.join(
            root_dir, ".config", "alvacc.yaml"
        )
        if self._reset_config or not self.get_config():
            self.set_config()

    @property
    def confirmation_url(self):
        return (
            "https://al-telegov.egov.com/alabamavaccine/"
            "CustomerCreateAppointments/Confirmation?"
            f"confirmationNumber={self.confirmation_number}"
        )

    @property
    def current_appointment_date(self):
        return self._current_appointment_date

    @current_appointment_date.setter
    def current_appointment_date(self, date):
        # ToDo: subclass datetime for simpler date handling
        if isinstance(date, str):
            date = datetime.strptime(
                date,
                "%B %d",
            )
        # add 1 to the year if month is in the past (assumes year wrap)
        self._current_appointment_date = date.replace(
            year=datetime.today().year + int(date.month < datetime.today().month)
        )

    def get_config(self):
        # no need to load if set explicitly
        if (
            self.current_appointment_date
            and self.confirmation_number
            and self.locations
        ):
            return True
        # try to open config file and load parameters
        try:
            with open(self._config_file) as f:
                cfg = yaml.safe_load(f)
            self.current_appointment_date = self.current_appointment_date or cfg.get(
                "current_appointment_date"
            )
            self.confirmation_number = self.confirmation_number or cfg.get(
                "confirmation_number"
            )
            self.locations = self.locations or get_locations(cfg.get("locations"))
            return all(
                [
                    self.current_appointment_date,
                    self.confirmation_number,
                    self.locations,
                ]
            )
        # config file doesn't exist
        except FileNotFoundError as e:
            print(type(e)(f"Cannot find config file at {self._config_file}"))
            return False
        # config file is missing an attribute
        except AttributeError as e:
            print(repr(e))
            print("Config file has missing values. Prompting to recreate")
            return False
        # Date not correct
        except (TypeError, ValueError) as e:
            print(repr(e))
            print("Config file is misconfigured. Prompting to recreate")
            return False

    def set_config(self):
        """Create config file, prompting for user preferences"""
        # get date from user and ensure proper format
        while True:
            try:
                self.current_appointment_date = input(
                    "Enter current appointment date as `Month dd`: "
                )
                break
            except ValueError:
                print("  Unable to parse date, please enter as `mm/dd` (e.g. June 11)")

        # get confirmation number, not certain about error handling so only warn
        # if wrong, submit an issue on github with confirmation number format,
        # just noting position of letters and numbers (e.g. ABC000D00)
        self.confirmation_number = input("Enter confirmation number: ").strip().upper()
        if not re.match("^[A-Z]{3}[0-9]{6}", self.confirmation_number):
            print(
                "  This confirmation might not be correct. The ones I have seen are three letters and six numbers (e.g. ABC000000)\n"
                "  Confirm this is correct by visiting the following link which will prompt for your email or give and error\n"
                f"    {self.confirmation_url}"
            )

        # get list of locations from user, and ensure they exist
        should_list = False
        while True:
            list_prompt = (
                ". To print a complete list of available locations, enter `l`"
                if not should_list
                else ""
            )
            locations = input(
                f"Enter all counties of interest seperated by spaces{list_prompt}: "
            )
            if locations.lower().strip() in ["l", "list"]:
                should_list = True
                print_cols(get_locations())
                continue
            try:
                # split on "," and " " and ", " etc.
                self.locations = get_locations(
                    [loc.strip().title() for loc in re.split("[\W,;]+", locations)]
                )
                break
            except AttributeError as e:
                print(f"  {e}. Available locations:")
                print_cols(get_locations())
        with open(self._config_file, "w") as file:
            cfg = {
                "current_appointment_date": self.current_appointment_date.strftime("%B %d"),
                "confirmation_number": self.confirmation_number,
                "locations": [loc.name for loc in self.locations],
            }
            yaml.dump(cfg, file)


def print_cols(arr, num_columns=None):
    max_len = max(len(s) for s in arr)
    num_columns = num_columns or os.get_terminal_size().columns // (max_len + 2)
    # pad with None
    arr.extend([""] * (num_columns - len(arr) % num_columns))
    for sub_arr in zip(*[iter(arr)] * num_columns):
        print("".join([f"  {val:<{max_len}}" for val in sub_arr]))

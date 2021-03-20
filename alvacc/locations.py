import sys
from dataclasses import dataclass
from datetime import datetime
import urllib.request
import json


class Availability:
    def __init__(self, next_avail=None):
        self.is_new = False
        self._current = next_avail

    def __repr__(self):
        return (
            self._current.date.strftime("%B %d")
            if self._current and self._current.date
            else "No availability"
        )

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, next_avail):
        if self._current and next_avail and self._current.date == next_avail.date:
            self.is_new = False
        else:
            self.is_new = True
            self._current = next_avail


def sort_avail(avail) -> dict:
    try:
        return(
            {
                name: date
                for name, date in sorted(
                    avail.items(), key=lambda c: c[1] or datetime.max
                )
            }
            if isinstance(avail, dict)
            else {
                loc.name: loc.availability
                for loc in sorted(
                    avail, key=lambda c: c.availability.current.date or datetime.max
                )
            }
        )
    except AttributeError:
        return {}


class next_avail:
    def __init__(self, response):
        # response text of following form (including ")
        # "Month day, # available."
        # ex. "June 14, 125 available."
        self.text = response.read().decode("utf-8").strip('"')
        try:
            # ToDo: subclass datetime for simpler date handling
            date = datetime.strptime(
                self.text.split(", ")[0],
                "%B %d",
            )
            # add 1 to the year if month is in the past (assumes year wrap)
            self.date = date.replace(
                year=datetime.today().year + int(date.month < datetime.today().month)
            )
            self.num_available = int(self.text.split()[2])
        except ValueError:
            self.date = self.num_available = None

    def __repr__(self):
        return self.text


class Location:
    def __init__(
        self,
        name: str,
        full_name: str,
        city: str,
        zip_code: str,
        location_id: int,
        availability: Availability = None,
    ):
        self.name = name
        self.full_name = full_name
        self.city = city
        self.zip_code = zip_code
        self.location_id = location_id
        self.availability = Availability()

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([k + '=' + repr(v) for k, v in self.__dict__.items()])})"

    def check_next_available(self):
        url = f"https://al-telegov.egov.com/alabamavaccine/CustomerCreateAppointments/GetEarliestAvailability?appointmentTypeId=1&locationId={self.location_id}"
        with urllib.request.urlopen(url) as f:
            na = next_avail(f)
        return na

    def get_available_dates_for_month(self, month):
        if isinstance(month, str):
            month = datetime.strptime(month.strip(), ["%b", "%B", "%m"])
        url = f"https://al-telegov.egov.com/alabamavaccine/CustomerCreateAppointments/GetAvailableDatesForMonth?duration=15&locationId={self.location_id}&date=2021-{month:02d}-01T06:00:00.000Z"
        with urllib.request.urlopen(url) as f:
            days = [
                datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
                for x in json.loads(f.read().decode("utf-8"))
            ]
        # Parse the response, which is a JSON array of days in which appointments are available
        return days


def get_locations(locations=None):
    if not locations:
        return sorted(all_locations)
    return [getattr(sys.modules[__name__], loc.title()) for loc in locations]


all_locations = [
    "Autauga",
    "Baldwin",
    "Barbour",
    "Bibb",
    "Blount",
    "Bullock",
    "Butler",
    "Chambers",
    "Cherokee",
    "Chilton",
    "Choctaw",
    "Clarke",
    "Clay",
    "Coffee",
    "Colbert",
    "Covington",
    "Crenshaw",
    "Cullman",
    "Dale",
    "Dallas",
    "Dekalb",
    "Elmore",
    "Etowah",
    "Fayette",
    "Franklin",
    "Geneva",
    "Greene",
    "Hale",
    "Heflin",
    "Henry",
    "Houston",
    "Jackson",
    "Lamar",
    "Lauderdale",
    "Lawrence",
    "County",
    "Limestone",
    "Lowndes",
    "Macon",
    "Huntsville",
    "Madison",
    "Marengo",
    "Marion",
    "Marshall",
    "Monroe",
    "Montgomery",
    "Decatur",
    "Morgan",
    "Rainsville",
    "Perry",
    "Pickens",
    "Pike",
    "Randolph",
    "Russell",
    "Sumter",
    "Sylacauga",
    "Talladega",
    "Tallapoosa",
    "Tuscaloosa",
    "Walker",
    "Washington",
    "Wilcox",
    "Winston",
]
Autauga = Location(
    name="Autauga",
    full_name="Autauga County Health Department",
    city="Prattville",
    zip_code="36067",
    location_id=61,
)
Baldwin = Location(
    name="Baldwin",
    full_name="Baldwin County Health Department",
    city="Robertsdale",
    zip_code="36567",
    location_id=51,
)
Barbour = Location(
    name="Barbour",
    full_name="Barbour County Health Department",
    city="Eufaula",
    zip_code="36027",
    location_id=34,
)
Bibb = Location(
    name="Bibb",
    full_name="Bibb County Health Department",
    city="Centerville",
    zip_code="35041",
    location_id=72,
)
Blount = Location(
    name="Blount",
    full_name="Blount County Health Department",
    city="Oneonta",
    zip_code="35121",
    location_id=18,
)
Bullock = Location(
    name="Bullock",
    full_name="Bullock County Health Department",
    city="Union Springs",
    zip_code="36089",
    location_id=60,
)
Butler = Location(
    name="Butler",
    full_name="Butler County Health Department",
    city="Greenville",
    zip_code="36037",
    location_id=33,
)
Chambers = Location(
    name="Chambers",
    full_name="Chambers County Health Department",
    city="Valley",
    zip_code="36854",
    location_id=59,
)
Cherokee = Location(
    name="Cherokee",
    full_name="Cherokee County Rescue Business",
    city="Centre",
    zip_code="35960",
    location_id=89,
)
Chilton = Location(
    name="Chilton",
    full_name="Chilton County Health Department",
    city="Clanton",
    zip_code="35045",
    location_id=71,
)
Choctaw = Location(
    name="Choctaw",
    full_name="Choctaw County Health Department",
    city="Butler",
    zip_code="36904",
    location_id=49,
)
Clarke = Location(
    name="Clarke",
    full_name="Clarke County Health Department",
    city="Grove Hill",
    zip_code="36451",
    location_id=48,
)
Clay = Location(
    name="Clay",
    full_name="Clay County Health Department",
    city="Lineville",
    zip_code="36266",
    location_id=78,
)
Coffee = Location(
    name="Coffee",
    full_name="Coffee County Health Department",
    city="Enterprise",
    zip_code="36330",
    location_id=32,
)
Colbert = Location(
    name="Colbert",
    full_name="Colbert County Health Department",
    city="Sheffield",
    zip_code="35660",
    location_id=7,
)
Covington = Location(
    name="Covington",
    full_name="Covington County Health Department",
    city="Andalusia",
    zip_code="36420",
    location_id=31,
)
Crenshaw = Location(
    name="Crenshaw",
    full_name="Crenshaw County Health Department",
    city="Luverne",
    zip_code="36049",
    location_id=30,
)
Cullman = Location(
    name="Cullman",
    full_name="Cullman County Health Department",
    city="Cullman",
    zip_code="35055",
    location_id=8,
)
Dale = Location(
    name="Dale",
    full_name="Dale County Health Department",
    city="Ozark",
    zip_code="36360",
    location_id=29,
)
Dallas = Location(
    name="Dallas",
    full_name="Dallas County Health Department",
    city="Selma",
    zip_code="36701",
    location_id=45,
)
Dekalb = Location(
    name="Dekalb",
    full_name="Dekalb County VFW Fairgrounds",
    city="Fort Payne",
    zip_code="35968",
    location_id=92,
)
Elmore = Location(
    name="Elmore",
    full_name="Elmore County Health Department",
    city="Wetumpka",
    zip_code="36092",
    location_id=58,
)
Etowah = Location(
    name="Etowah",
    full_name="Etowah County Health Department",
    city="Gadsden",
    zip_code="35903",
    location_id=21,
)
Fayette = Location(
    name="Fayette",
    full_name="Fayette County Health Department",
    city="Fayette",
    zip_code="35555",
    location_id=70,
)
Franklin = Location(
    name="Franklin",
    full_name="Franklin County Health Dept",
    city="Russellville",
    zip_code="35654",
    location_id=9,
)
Geneva = Location(
    name="Geneva",
    full_name="Geneva County Health Department",
    city="Hartford",
    zip_code="36344",
    location_id=28,
)
Greene = Location(
    name="Greene",
    full_name="Greene County Health Department",
    city="Eutaw",
    zip_code="35462",
    location_id=69,
)
Hale = Location(
    name="Hale",
    full_name="Hale County Health Department",
    city="Greensboro",
    zip_code="36744",
    location_id=68,
)
Heflin = Location(
    name="Heflin",
    full_name="Heflin Armory",
    city="Heflin",
    zip_code="36264",
    location_id=90,
)
Henry = Location(
    name="Henry",
    full_name="Henry County Health Department",
    city="Abbeville",
    zip_code="36310",
    location_id=27,
)
Houston = Location(
    name="Houston",
    full_name="Houston County Health Department",
    city="Dothan",
    zip_code="36301",
    location_id=26,
)
Jackson = Location(
    name="Jackson",
    full_name="Jackson County Health Department",
    city="Scottsboro",
    zip_code="35769",
    location_id=10,
)
Lamar = Location(
    name="Lamar",
    full_name="Lamar County Health Department",
    city="Vernon",
    zip_code="35592",
    location_id=67,
)
Lauderdale = Location(
    name="Lauderdale",
    full_name="Lauderdale County Health Department",
    city="Florence",
    zip_code="35630",
    location_id=86,
)
Lawrence = Location(
    name="Lawrence",
    full_name="Lawrence County Health Dept",
    city="Moulton",
    zip_code="35650",
    location_id=11,
)
County = Location(
    name="County",
    full_name="Lee County Health Department",
    city="Opelika",
    zip_code="36801",
    location_id=57,
)
Limestone = Location(
    name="Limestone",
    full_name="Limestone County Health Department",
    city="Athens",
    zip_code="35611",
    location_id=12,
)
Lowndes = Location(
    name="Lowndes",
    full_name="Lowndes County Health Department",
    city="Hayneville",
    zip_code="36040",
    location_id=56,
)
Macon = Location(
    name="Macon",
    full_name="Macon County Health Department",
    city="Tuskegee",
    zip_code="36083",
    location_id=55,
)
Huntsville = Madison = Location(
    name="Madison",
    full_name="Madison County Health Department",
    city="Huntsville",
    zip_code="35811",
    location_id=13,
)
Marengo = Location(
    name="Marengo",
    full_name="Marengo County Health Department",
    city="Linden",
    zip_code="36748",
    location_id=88,
)
Marion = Location(
    name="Marion",
    full_name="Marion County Health Department",
    city="Hamilton",
    zip_code="35570",
    location_id=14,
)
Marshall = Location(
    name="Marshall",
    full_name="Marshall County Health Department",
    city="Guntersville",
    zip_code="35976",
    location_id=15,
)
Monroe = Location(
    name="Monroe",
    full_name="Monroe County Health Department",
    city="Monroeville",
    zip_code="36460",
    location_id=39,
)
Montgomery = Location(
    name="Montgomery",
    full_name="Montgomery County Health Department",
    city="Montgomery",
    zip_code="36108",
    location_id=54,
)
Decatur = Morgan = Location(
    name="Morgan",
    full_name="Morgan County Health Department",
    city="Decatur",
    zip_code="35603",
    location_id=16,
)
Rainsville = Location(
    name="Rainsville",
    full_name="Northeast Alabama Agricultural Business Center",
    city="Rainsville",
    zip_code="35986",
    location_id=91,
)
Perry = Location(
    name="Perry",
    full_name="Perry County Health Department",
    city="Marion",
    zip_code="36756",
    location_id=66,
)
Pickens = Location(
    name="Pickens",
    full_name="Pickens County Health Department",
    city="Carrollton",
    zip_code="35447",
    location_id=65,
)
Pike = Location(
    name="Pike",
    full_name="Pike County Health Department",
    city="Troy",
    zip_code="36081",
    location_id=25,
)
Randolph = Location(
    name="Randolph",
    full_name="Randolph County Health Department",
    city="Roanoke",
    zip_code="36274",
    location_id=22,
)
Russell = Location(
    name="Russell",
    full_name="Russell County Health Department",
    city="Phenix City",
    zip_code="36867",
    location_id=53,
)
Sumter = Location(
    name="Sumter",
    full_name="Sumter County Health Department",
    city="Livingston",
    zip_code="35470",
    location_id=64,
)
Sylacauga = Location(
    name="Sylacauga",
    full_name="Talladega County Health Department (Sylacauga)",
    city="Sylacauga",
    zip_code="35150",
    location_id=85,
)
Talladega = Location(
    name="Talladega",
    full_name="Talladega County Health Department (Talladega)",
    city="Talladega",
    zip_code="35160",
    location_id=84,
)
Tallapoosa = Location(
    name="Tallapoosa",
    full_name="Tallapoosa County Health Dept. (Alexandar City)",
    city="Alexander City",
    zip_code="35010",
    location_id=52,
)
Tuscaloosa = Location(
    name="Tuscaloosa",
    full_name="Tuscaloosa County Health Department",
    city="Tuscaloosa",
    zip_code="35405",
    location_id=63,
)
Walker = Location(
    name="Walker",
    full_name="Walker County Health Department",
    city="Jasper",
    zip_code="35501",
    location_id=62,
)
Washington = Location(
    name="Washington",
    full_name="Washington County Health Department",
    city="Chatom",
    zip_code="36518",
    location_id=37,
)
Wilcox = Location(
    name="Wilcox",
    full_name="Wilcox County Health Department",
    city="Camden",
    zip_code="36726",
    location_id=35,
)
Winston = Location(
    name="Winston",
    full_name="Winston County Health Department",
    city="Double Springs",
    zip_code="35553",
    location_id=17,
)

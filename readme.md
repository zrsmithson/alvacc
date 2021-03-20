# Purpose
This script polls the vaccine appointment database, looking for open time slots.

## Procedure:

1. Create an appointment on any available date at https://alcovidvaccine.gov/
2. Note your email address and confirmation code
3. Run this script and follow the prompts to configure.
4. When it finds an open slot, it will open the confirmation page.
5. Click either the first or second edit, depending on whether you need to change location and time, or just time.

If you're not quick enough, the appointment slot may be grabbed before you can get to it. Good luck!

Feel free to submit an issue and I'll do what I can to help. And try to avoid going to low on the sleep timer. I have never had any issues querying their website, but still best not to overload the servers.

## Usage
The simplest usage is to run `alvacc` and follow the prompts to create a configuration file.

These values can also be provided directly through the command line arguments, or the `.config/alvacc.yaml` file (either in repo directory or /home/user) can be manually edited.

```
usage: alvacc.py [-h] [-s SLEEP_TIME] [--current_appointment_date CURRENT_APPOINTMENT_DATE]
                 [--confirmation_number CONFIRMATION_NUMBER]
                 [--locations LOCATIONS [LOCATIONS ...]] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -s, --sleep SLEEP_TIME
                        Time to sleep between queries (seconds)
  --current_appointment_date CURRENT_APPOINTMENT_DATE
                        curret appointment in `Month day` format
  --confirmation_number CONFIRMATION_NUMBER
                        Confirmation number from previously booked appointment
  --locations LOCATIONS [LOCATIONS ...]
                        space-seperated list of counties to use. available counties: Autauga
                        Baldwin Barbour Bibb Blount Bullock Butler Chambers Cherokee Chilton
                        Choctaw Clarke Clay Coffee Colbert County Covington Crenshaw Cullman Dale
                        Dallas Decatur Dekalb Elmore Etowah Fayette Franklin Geneva Greene Hale
                        Heflin Henry Houston Huntsville Jackson Lamar Lauderdale Lawrence Limestone
                        Lowndes Macon Madison Marengo Marion Marshall Monroe Montgomery Morgan
                        Perry Pickens Pike Rainsville Randolph Russell Sumter Sylacauga Talladega
                        Tallapoosa Tuscaloosa Walker Washington Wilcox Winston
```

## Installation
This package can be installed or just run directly from the repo folder. Beyond Python 3+, the only package requirement is `PyYAML`

Clone
```
git@github.com:zrsmithson/alvacc.git
```

Install from repo folder
```
pip install .
```

## Future work
I've only dealt with my own configuration, so if there are any issues running the program, submit an issue or a PR. I'm sure something will change on the website side, so let me know if you come across any issues.

There was some work on watching the entire month instead of just the next avilable time, but I found it was easiest just to watch next available appointment slots. With all the walk-in clinics, I'm pretty sure people are setting up their appointments then getting it somewhere else.

Simplification can definitely be done between configuration, locations, etc. This would be useful depending on interest in using this package for other purposes than the script.

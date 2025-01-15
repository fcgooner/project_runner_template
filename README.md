# General
This template is mostly focused on interacting with crypto project websites using playwright library.
It's written with AdsPower in mind, but can be easily changed for other anti-detect browsers.
To do so, update utils/browser_handler.py accordingly.

This template can also be used to run API request tasks or tasks that directly interact with blockchain using web3 library.

## Task run logic
* Task results reset to `False` every separate run, unless `FRESH_RUN` set to `False` in **config.py**
* If you run only browserless tasks, a browser won't launch.
* If `MAX_CYCLES` parameter in **config.py** is bigger than 1, the script will rerun profiles with failed tasks after all profiles processed.
* If **profile_database.csv** contains 50 profiles, but **tasks_data.csv** contains only 10 profiles of these 50, only 10 profiles from **tasks_data.csv** will be processed.

# config.py
This file contains configurable variables, like projects list, tasks list, anti-detect browser port etc.

# CSV Data tables
## core/profile_database.csv
Stores profiles data. Need to be filled manually.

You can add as many new columns as you like, just don't forget to update `create_profiles_from_csv()` function in **utils/profiles_handler.py** and `__init__` method in Profile class (**core/profile.py**)

## projects/[project_name]/project_data/tasks_data.csv
Stores task results data for each profile. Need to be filled manually.

# Variable files
## projects/[project_name]/project_data/variables.py
Contain variables for specific project (project urls etc.)

# Utils
## utils/email_parser.py
Contains function to retrieve 6-digits verification code.
Pass subject of expected email and current time to`get_code()`.
Use`datetime.now(timezone.utc).replace(microsecond=0)` for current time.

## utils/wallet_extension.py
Contains static methods for interaction with various wallet extensions (unlock, sign, approve, add).
Currently, three wallets implemented: OKX, Rabby and Phantom. 

# IMPORTANT: Task names
1. Task names in config.py must consist of a project name and activity name divided by one blank space. For example:
`LIFECHANGER CHECKIN` - OK
`LIFECHANGER CHECK IN` - NOT OK

2. Task names in **tasks_data.csv** must consist only of an activity name (no project name and blank spaces). For example:
`CHECKIN` - OK
`LIFECHANGER CHECKIN` - NOT OK

To summarize, if a task in **config.py** called `LIFECHANGER CHECKIN`, in task_data.csv it must be called `CHECKIN`

# Logger
The template has 2 loggers:
 * for console output
 * for file output

Each run, the script creates a log file with unique name, based on current time.
File output can be disabled with `LOG_TO_FILE` parameter in **config.py**

# Profile class (core/profile.py)
Class for easy access to profile data (private keys, wallet addresses, passwords, task results etc.)
Class instances created at the start of the script with data from **data/profile_database.csv** and then updated with data from **tasks_data.csv** files.

# Useful tips
## Run script for specific project(s)
To run the script only for specific project(s), comment out projects you don't need in `PROJECTS` parameter in **config.py**

In this example, the script will only run tasks for LIFECHANGER project:
```
PROJECTS = [
    "LIFECHANGER",
    #"REKT"
]
```
## Run script for specific task(s)
To run the script only for specific task(s), comment out tasks you don't need in `PROJECT_TASKS` parameter in **config.py**

In this example, the script will only run `LIFECHANGER CHECKIN` and `REKT LOGIN`:
```
PROJECT_TASKS = {
    "LIFECHANGER": {
        'CORE': [               
            # "LIFECHANGER SWAP",
        ],
        'OPTIONAL': [
            "LIFECHANGER CHECKIN",
            # "LIFECHANGER STAKE",
        ],
        'GROUP': [
            # "LIFECHANGER VOTE",
            # "LIFECHANGER DELEGATE"
        ]
    },
    "REKT": {
        'CORE': [
                "REKT LOGIN",
                # "REKT CHECKIN"
        ],
        'OPTIONAL': [
                # "REKT SWAP"
        ],
        'GROUP': []
    }
}
```

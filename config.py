# SETTINGS
ADS_PORT = 50325                        # ADSPOWER -> API -> API Settings -> Connection (http://local.adspower.net:PORT)
FRESH_RUN = True                        # If True, task results will be reset. If False, tasks with result True will be skipped.
LOG_TO_FILE = False
LOG_LEVEL_CONSOLE = 'INFO'
LOG_LEVEL_FILE = 'DEBUG'

CONCURRENT_PROFILES = 10                # HOW MANY PROFILES RUN AT ONCE
                                        # OPTIMAL NUMBER FOR BROWSER TASKS: 10-20 (WITH 32GB OF RAM)
                                        # OPTIMAL NUMBER FOR BROWSERLESS TASKS: ANY REASONABLE NUMBER SHOULD BE FINE

MAX_CYCLES = 1                          # 1 - RUN ONCE AND EXIT | >2 - RUN ONCE, RETRY ANY FAILED TASKS

WALLETS_TO_UNLOCK = [                   # LIST OF WALLETS TO UNLOCK BEFORE EXECUTING BROWSER TASKS
    'RABBY',                            # CURRENTLY IMPLEMENTED UNLOCK, CONNECT, SIGN/CONFIRM, APPROVE/ADD FOR
    'PHANTOM',                          # OKX, PHANTOM AND RABBY WALLETS
    # 'OKX'
]

# ----------------------------------------
# ------    COMMON CONFIGURATION    ------
# ----------------------------------------

PROJECTS = [            # LIST OF PROJECTS TO EXECUTE. COMMENT OUT ANY PROJECT YOU DON'T WANT TO EXECUTE
    "LIFECHANGER",
    "REKT",
    # "THIRD"
]

# TASKS BY PROJECTS. COMMENT OUT ANY TASKS YOU DON'T WANT TO EXECUTE
# CORE TASKS - EXECUTED FIRST, ORDER NOT SHUFFLED
# OPTIONAL TASKS - EXECUTED AFTER CORE TASKS, ORDER IS SHUFFLED
# GROUP TASKS - OPTIONAL TASKS WITH ORDER NOT SHUFFLED. INSERTED INSIDE OPTIONAL TASKS AT A RANDOM INDEX
PROJECT_TASKS = {
    "LIFECHANGER": {
        'CORE': [
            # "LIFECHANGER LOGIN",
        ],
        'OPTIONAL': [
            # "LIFECHANGER VOTE",
        ],
        'GROUP': [
            # "LIFECHANGER FAUCET",
            "LIFECHANGER SWAP",
        ]
    },
    "REKT": {
        'CORE': [
                "REKT LOGIN",
        ],
        'OPTIONAL': [
            "REKT CHECKIN",
            # "REKT STAKE"
        ],
        'GROUP': []
    }
}
# BLOCKER TASKS. IF A PROJECT'S BLOCKER TASK FAILS, OTHER PROJECT TASKS WON'T BE EXECUTED
CRITICAL_TASKS = ["LIFECHANGER LOGIN", "REKT LOGIN"]

# TASKS THAT DON'T REQUIRE BROWSER (API TASKS ETC.)
BROWSERLESS_TASKS = ["LIFECHANGER SWAP", "REKT CHECKIN", "REKT LOGIN"]

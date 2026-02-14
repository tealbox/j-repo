Python Logging Notes:


"Cows
Eat
Wheat
In
Ditches"
→ Critical, Error, Warning, Info, Debug
(From highest to lowest severity)

root (level=WARNING)
│
└── myapp (level=INFO)
    │
    ├── myapp.core (level=NOTSET → inherits INFO)
    │   └── Logs: DEBUG ❌, INFO ✅, WARNING ✅, ERROR ✅
    │
    └── myapp.network (level=DEBUG)
        └── Logs: DEBUG ✅, INFO ✅, WARNING ✅, ERROR ✅

Incoming Log Records:
┌──────────────┐
│ DEBUG (10)   │ ────❌───→ DROPPED (below INFO if setLevel(logging.INFO) )
├──────────────┤
│ INFO (20)    │ ────✅───→ PROCESSED
├──────────────┤
│ WARNING (30) │ ────✅───→ PROCESSED
├──────────────┤
│ ERROR (40)   │ ────✅───→ PROCESSED
├──────────────┤
│ CRITICAL (50)│ ────✅───→ PROCESSED
└──────────────┘


Python Logging Levels (Built-in)

Level       | Numeric Value | When to Use
------------|---------------|--------------------------------------------
CRITICAL    | 50            | Serious errors that may cause program abort   | All will be recorded
ERROR       | 40            | Errors that prevent a feature from working    |
WARNING     | 30            | Unexpected behavior, but not an error         |
INFO        | 20            | General progress or status information -------| if logging level is set to Info
DEBUG       | 10            | Detailed diagnostic info for developers
NOTSET      | 0             | Inherits level from parent logger

**Note**:
so higher levels are always recorded not lower.
e.g. if setLevel(logging.INFO) then INFO, WARNING, ERROR & CRITICAL will be recorded **but not DEBUG**

If a logger’s level is set to DEBUG (10), it will record all log messages with level ≥ 10, which includes:
DEBUG (10)
INFO (20)
WARNING (30)
ERROR (40)
CRITICAL (50)

Python’s logging system uses numeric severity levels, and a logger processes all records at or above its configured level.
DEBUG (10) < INFO (20) < WARNING (30) < ERROR (40) < CRITICAL (50)

Setting level=DEBUG means:
“Log everything — I want the most verbose output.”

**📌 Rule of Thumb:
Lower level setting = more logs
Higher level setting = fewer logs**

**Logger Level  | Logs Recorded (inclusive)**
--------------|----------------------------------------
CRITICAL (50) | CRITICAL
ERROR (40)    | ERROR, CRITICAL
WARNING (30)  | WARNING, ERROR, CRITICAL
INFO (20)     | INFO, WARNING, ERROR, CRITICAL
DEBUG (10)    | DEBUG, INFO, WARNING, ERROR, CRITICAL



----------------------------------------------------------------------------------------
mypackage/
├── __init__.py
├── module1.py
└── module2.py


**mypackage/__init__.py**
##################################################################
# mypackage/__init__.py
import logging
import logging.config

def setup_logging():
    # Avoid reconfiguring
    if hasattr(setup_logging, '_configured'):
        return
    setup_logging._configured = True

    # Configure the 'mypackage' logger (parent of all sub-loggers)
    package_logger = logging.getLogger("mypackage")
    package_logger.setLevel(logging.DEBUG)

    # Clear any existing handlers (prevent duplicates on reload)
    package_logger.handlers.clear()

    # --- Handler 1: INFO+ to app.log ---
    app_handler = logging.FileHandler("app.log")
    app_handler.setLevel(logging.INFO)
    app_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    app_handler.setFormatter(app_formatter)

    # --- Handler 2: WARNING+ to errors.log ---
    error_handler = logging.FileHandler("errors.log")
    error_handler.setLevel(logging.WARNING)
    error_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    error_handler.setFormatter(error_formatter)

    package_logger.addHandler(app_handler)
    package_logger.addHandler(error_handler)
    package_logger.propagate = False  # Don't pass logs to root logger

# Run setup when package is imported
setup_logging()
##################################################################

**mypackage/module1.py**
##################################################################
# mypackage/module1.py
import logging

# Automatically gets name "mypackage.module1"
logger = logging.getLogger(__name__)

def do_something():
    logger.info("Processing in module1")
    logger.warning("Warning from module1")
##################################################################    

**mypackage/module2.py**
##################################################################
# mypackage/module2.py
import logging

# Automatically gets name "mypackage.module2"
logger = logging.getLogger(__name__)

def do_another_thing():
    logger.debug("Debug from module2")
    logger.error("Error in module2!")
##################################################################

app.log
2026-02-15 12:00:00,123 - mypackage.module1 - INFO - Processing in module1
2026-02-15 12:00:00,124 - mypackage.module1 - WARNING - Warning from module1
2026-02-15 12:00:00,125 - mypackage.module2 - ERROR - Error in module2!

##################################################################
errors.log
2026-02-15 12:00:00,124 - mypackage.module1 - WARNING - do_something:7 - Warning from module1
2026-02-15 12:00:00,125 - mypackage.module2 - ERROR - do_another_thing:7 - Error in module2!

Why This Works
__name__ in mypackage/module1.py → "mypackage.module1"
The logger "mypackage.module1" is a child of "mypackage"
By default, child loggers propagate messages to parent loggers
But we set propagate = False on the parent ("mypackage") and attached handlers there
So all child loggers reuse the same handlers without duplication
💡 This is the standard Python logging best practice for packages.


The Magic: __name__
In Python, every module has a built-in variable called __name__.
When you import a module as part of a package, __name__ is set to the full dotted path from the top-level package.

logger = logging.getLogger(__name__)
**is exactly equivalent to in mypackage/module1.py:**
logger = logging.getLogger("mypackage.module1")


"mypackage" is the parent logger
"mypackage.module1" and "mypackage.module2" are child loggers
**By default, child loggers propagate messages up to their parents.**


You don’t need to configure each child logger. Instead:
Configure the parent logger ("mypackage") once.
**All children ("mypackage.*") inherit behavior via propagation.**
This gives you centralized control with per-module identification (via %(name)s).

##################################################################
import logging
logger = logging.getLogger(__name__)

print("Logger name:", logger.name)          # → mypackage.module1
print("Parent:", logger.parent.name)        # → mypackage
print("Propagate:", logger.propagate)       # → True
##################################################################
Is a new instance of logger created in module1.py when we do logging.getLogger(__name__)?
The logging.getLogger(name) function does not create a new instance every time. Instead:
It returns the same logger object for the same name.
This is managed internally by the logging module’s logger registry (logging.Logger.manager.loggerDict).


# In module1.py
logger1 = logging.getLogger("mypackage.module1")

# Elsewhere (even in another file)
logger2 = logging.getLogger("mypackage.module1")

print(logger1 is logger2)  # → True

logger = logging.getLogger(__name__)  # __name__ == "mypackage.module1"

**You get the one and only logger instance for "mypackage.module1".**
🔹** So: Not a new instance each time, but a shared singleton per name.**
This is safe, efficient, and allows consistent configuration across modules.

mypackage.module1  →  mypackage  →  root
In your setup:
mypackage.module1 has no handlers → propagates to mypackage
mypackage has handlers (from __init__.py) → logs appear in files
**If mypackage didn’t handle it, it would go to the root logger**

The Propagation Chain (by default)
When you log from mypackage.module1:

logger = logging.getLogger("mypackage.module1")
logger.info("Hello")

The logging system follows this path:
mypackage.module1
→ Checks its own handlers → none?
→ Since propagate=True (default), passes the record up to its parent.
mypackage
→ Checks its handlers → none?
→ Still propagate=True (by default for all loggers), so passes it up to its parent.
Root logger ("")
→ This is the top of the hierarchy.
→ **By default, the root logger has no handlers… unless:**
You’ve called logging.basicConfig(), or
You’ve manually added a handler to it.
🧪 Default Behavior: Silent Drop

If no logger in the chain has a handler, and you never configured logging, then:
❌ **The log message is silently discarded.**

This is a common source of confusion! Example:
# test.py
import logging
logger = logging.getLogger("mypackage.module1")
logger.warning("This might disappear!")

Output: Nothing appears — because:
mypackage.module1 → no handler
mypackage → no handler
root logger → no handler (since basicConfig was never called)


If anywhere in your code you do:
logging.basicConfig(level=logging.INFO)
Then the root logger gets a StreamHandler (prints to console).
So now:
Log record propagates up to root
Root has a handler → message prints to console

Key Takeaway
Loggers don’t output anything by themselves — they need handlers.
If no handler exists in the entire propagation chain (including root), the message vanishes.
That’s why it’s crucial to:
Either configure a parent logger (like mypackage) with handlers, or
Call logging.basicConfig() at the top level (common in scripts), or
Attach a handler directly to the child logger (not recommended for packages)

print(logging.getLogger("mypackage.module1").handlers)      # []
print(logging.getLogger("mypackage").handlers)             # [] or [handler...]
print(logging.root.handlers)                               # Often []



[ mypackage.module1 ] 
        │
        │ (propagate=True → send up)
        ▼
[   mypackage     ] 
        │
        │ (propagate=True → send up)
        ▼
[     root        ] ← (name = "")
        │
        └──► Handlers? → If yes: output; if no: **silently drop**
        

[ mypackage.module1 ] 
        │
        │ (propagate=True)
        ▼
[   mypackage     ] ← has handlers + propagate=False
        │
        └──► [app.log] and [errors.log]
        │
        ✘ NO further propagation to root!
        
        



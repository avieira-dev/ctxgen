"""
FILE: utils/messages.py
DESCRIPTION: Centralized terminal messaging, branding, and graceful shutdown utilities.
RESPONSIBILITIES:
  - Store and render the official ctxgen ASCII banner
  - Display version and product identity information
  - Provide standardized terminal feedback messages
  - Handle graceful interruption and cancellation flows
  - Ensure consistent visual communication across the CLI
"""

import sys
import signal
from .colors import Colors

BANNER = r"""
       _                        
   ___| |___  ____ _  ___ _ __  
  / __| __\ \/ / _` |/ _ \ '_ \ 
 | (__| |_ >  < (_| |  __/ | | |
  \___|\__/_/\_\__, |\___|_| |_|
               |___/            
"""

def banner():
    print(Colors.text_banner(BANNER))

def version():
    print(Colors.text_version("v1.0.0", "Turn entire projects into a single context for LLMs."))
    print()

def abort(message=None):
    print()

    if message is not None:
        print(Colors.error_abort(message))
    
    print(Colors.yellow("⚠ Operation cancelled."))
    print(Colors.cyan("Bye!"))
    print()
    sys.exit(128 + signal.SIGINT)
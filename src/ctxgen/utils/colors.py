"""
FILE: utils/colors.py
DESCRIPTION: Centralized ANSI escape sequences for terminal styling.
RESPONSIBILITIES:
  - Provide a consistent color palette for the CLI (Blue, Cyan, etc.)
  - Define text formatting styles (Bold, Dim, Underline)
  - Support background colors for UI elements like badges and banners
  - Enable the 'END' reset token to prevent color bleeding into user input
"""

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m' 
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m' 
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    END = '\033[0m' 
    BG_BLUE = '\033[44m'
    BG_CYAN = '\033[46m'
    WHITE = '\033[97m'

    @classmethod
    def cyan(cls, text):
        return f"{cls.CYAN}{text}{cls.END}"
    
    @classmethod
    def green(cls, text):
        return f"{cls.GREEN}{text}{cls.END}"
    
    @classmethod
    def yellow(cls, text):
        return f"{cls.YELLOW}{text}{cls.END}"
    
    @classmethod
    def white(cls, text):
        return f"{cls.WHITE}{text}{cls.END}"
    
    @classmethod
    def dim(cls, text):
        return f"{cls.DIM}{text}{cls.END}"
    
    @classmethod
    def text_version(cls, version, text):
        return f"{cls.BG_BLUE}{cls.WHITE}{cls.BOLD} {version} {cls.END} {cls.DIM}{text}{cls.END}"
    
    @classmethod
    def text_banner(cls, text):
        return f"{cls.BLUE}{text}{cls.END}"
        
    @classmethod
    def success(cls, number_files, path):
        return f"{cls.GREEN}[✓ Success]{cls.END} {cls.DIM}{number_files}{cls.END} files written to: {cls.DIM}{path}{cls.END}"
    
    @classmethod
    def error_saving(cls, path):
        return f"{cls.RED}[✗ Error]{cls.END} Unable to generate and save the file at: {cls.DIM}{path}{cls.END}"
    
    @classmethod
    def error_abort(cls, message):
        return f"{cls.RED}[✗ Error]{cls.END} {message}"
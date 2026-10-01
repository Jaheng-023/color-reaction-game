import tkinter.font as tkfont

WINDOW_TITLE = "Color Reaction Time & Stroop Task"
WINDOW_WIDTH = 920
WINDOW_HEIGHT = 700

# Color Palette
COLOR_BG = "#EFECE3"          # Warm Off-White / Ivory
COLOR_CARD = "#FFFFFF"        # Pure White Card Surface
COLOR_TEXT = "#000000"        # Deep Black Text
COLOR_MUTED = "#555555"       # Muted Dark Gray Text
COLOR_ACCENT = "#4A70A9"      # Slate Blue Accent
COLOR_HIGHLIGHT = "#8FABD4"   # Soft Blue Accent
COLOR_BORDER = "#D0CCC0"      # Subtle Border Tint
COLOR_DISABLED = "#CCCCCC"    # Disabled State Neutral

GAME_COLORS = {
    "Red": "#E74C3C",
    "Blue": "#3498DB",
    "Green": "#2ECC71",
    "Yellow": "#F1C40F",
    "Purple": "#9B59B6",
    "Orange": "#E67E22"
}

KEY_MAPPINGS = {
    "1": "Red",
    "2": "Blue",
    "3": "Green",
    "4": "Yellow",
    "5": "Purple",
    "6": "Orange"
}

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_HEADING = (FONT_FAMILY, 16, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_BUTTON = (FONT_FAMILY, 13, "bold")
FONT_WORD = (FONT_FAMILY, 36, "bold")
FONT_TIP = (FONT_FAMILY, 12, "italic")

TOTAL_TRIALS = 20
SIMPLE_TRIALS = 10
STROOP_TRIALS = 10

MIN_DELAY_MS = 1000
MAX_DELAY_MS = 3000
TIMEOUT_MS = 2000
FEEDBACK_DURATION_MS = 1000

AGE_GROUPS = ["Adolescence", "Teen", "Adult"]

RAW_DATA_FILE = "data/ColorReactionGame_RawData.csv"
STATS_DATA_FILE = "data/ColorReactionGame_SummaryStats.csv"

FUNNY_TIP = "💡 Pro-Tip: Words can lie! Trust the ink color, not what the text says."
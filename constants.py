import tkinter.font as tkfont

WINDOW_TITLE = "ColorRec - Reaction Time & Stroop Task"
GAME_NAME = "ColorRec"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720

# Color Hunt Palette
COLOR_BG = "#FFF6DC"          # Warm Cream Background
COLOR_CARD = "#FFFFFF"        # Crisp White Surface
COLOR_PRIMARY = "#425B9A"     # Deep Blue Primary
COLOR_ACCENT = "#76C0EC"      # Sky Blue Accent
COLOR_PINK = "#FF95A5"        # Soft Pink / Coral Accent
COLOR_TEXT = "#1C2541"        # Dark Navy Text
COLOR_MUTED = "#6C7A89"       # Muted Gray Text
COLOR_BORDER = "#E5DCBE"      # Border Tint
COLOR_DISABLED = "#D1D5DB"    # Neutral Disabled State

GAME_COLORS = {
    "Red": "#E74C3C",
    "Blue": "#3498DB",
    "Green": "#2ECC71",
    "Yellow": "#F1C40F",
    "Purple": "#9B59B6",
    "Orange": "#E67E22"
}

FONT_FAMILY = "Segoe UI"
FONT_BRAND = (FONT_FAMILY, 18, "bold")
FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_HEADING = (FONT_FAMILY, 15, "bold")
FONT_BODY = (FONT_FAMILY, 13)
FONT_BUTTON = (FONT_FAMILY, 13, "bold")
FONT_WORD = (FONT_FAMILY, 38, "bold")
FONT_TIP = (FONT_FAMILY, 12, "italic")

TOTAL_TRIALS = 20
SIMPLE_TRIALS = 10
STROOP_TRIALS = 10

MIN_DELAY_MS = 1000
MAX_DELAY_MS = 3000
TIMEOUT_MS = 2000
FEEDBACK_DURATION_MS = 1000

AGE_GROUPS = ["17 - 19", "20 - 22", "23 - 25"]

RAW_DATA_FILE = "data/ColorReactionGame_RawData.csv"
STATS_DATA_FILE = "data/ColorReactionGame_SummaryStats.csv"

FUNNY_TIP = "💡 Pro-Tip: Words can lie! Trust the ink color, not what the text says."
import tkinter.font as tkfont

WINDOW_TITLE = "Color Reaction Time & Stroop Task"
WINDOW_WIDTH = 850
WINDOW_HEIGHT = 650

COLOR_BG = "#1e1e1e"
COLOR_CARD = "#2d2d2d"
COLOR_TEXT = "#ffffff"
COLOR_MUTED = "#aaaaaa"
COLOR_ACCENT = "#4a9eff"
COLOR_BORDER = "#3d3d3d"
COLOR_DISABLED = "#444444"

GAME_COLORS = {
    "Red": "#e74c3c",
    "Blue": "#3498db",
    "Green": "#2ecc71",
    "Yellow": "#f1c40f",
    "Purple": "#9b59b6",
    "Orange": "#e67e22"
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
FONT_TITLE = (FONT_FAMILY, 24, "bold")
FONT_HEADING = (FONT_FAMILY, 18, "bold")
FONT_BODY = (FONT_FAMILY, 14)
FONT_BUTTON = (FONT_FAMILY, 14, "bold")
FONT_WORD = (FONT_FAMILY, 38, "bold")
FONT_TIP = (FONT_FAMILY, 13, "italic")

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
import enum
import os

SCHEMA = "schema"
SELENIUM = "selenium"
GOOGLE_RECORDING = "google_recording"
SELENIUM_RECORDING = "selenium_recording"


class JsonType(enum.Enum):
    SCHEMA = "schema"
    GOOGLE_RECORDING = "google_recording"
    SELENIUM_RECORDING = "selenium_recording"


globals = {
    "log_folder": os.path.join(os.getcwd(), "logs"),
    "ext_folder": os.path.join(os.getcwd(), "extensions"),
    "templates_folder": os.path.join(os.getcwd(), "templates"),
}

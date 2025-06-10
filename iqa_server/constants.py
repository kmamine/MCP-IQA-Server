"""
IQA Server Constants Module

Contains configuration and constant values used throughout the server.
"""

# Server Configuration
SERVER_NAME = "iqa-pytorch"
SERVER_VERSION = "0.1.0"

# Resource URIs
RESOURCE_URI_PREFIX = "iqa://models"
RESOURCE_URIS = {
    "all": f"{RESOURCE_URI_PREFIX}/all",
    "fr": f"{RESOURCE_URI_PREFIX}/fr",
    "nr": f"{RESOURCE_URI_PREFIX}/nr",
    "specific": f"{RESOURCE_URI_PREFIX}/specific"
}

# Model Types
MODEL_TYPE_FR = "FR"
MODEL_TYPE_NR = "NR"
MODEL_TYPE_SPECIFIC = "Specific"
MODEL_TYPE_ALL = "all"

MODEL_TYPES = [MODEL_TYPE_FR, MODEL_TYPE_NR, MODEL_TYPE_SPECIFIC, MODEL_TYPE_ALL]

# Model Categories
CATEGORY_GENERAL_FR = "General FR"
CATEGORY_GENERAL_NR = "General NR"
CATEGORY_COLOR_IQA = "Color IQA"
CATEGORY_FACE_IQA = "Face IQA"
CATEGORY_UNDERWATER_IQA = "Underwater IQA"

# Database Keys
KEY_FR_METHODS = "fr_methods"
KEY_NR_METHODS = "nr_methods"
KEY_SPECIFIC_METHODS = "specific_methods"

# Model Info Keys
KEY_TYPE = "type"
KEY_NAMES = "names"
KEY_DESCRIPTION = "description"
KEY_CATEGORY = "category"
KEY_NOTE = "note"
KEY_PAPER_INFO = "paper_info"
KEY_BACKWARD_SUPPORT = "backward_support"

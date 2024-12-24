from logging import basicConfig, getLogger, DEBUG

# put in entry point file
CHAR_GREEN = "\033[32m"
CHAR_RESET = "\033[0m"
FORMAT = f"{CHAR_GREEN}%(asctime)s %(levelname)s %(name)s {CHAR_RESET}: %(message)s"
basicConfig(level=DEBUG, format=FORMAT)

# put in all files
logger = getLogger(__name__)

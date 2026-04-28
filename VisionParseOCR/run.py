from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
from app.main import App

if __name__ == "__main__":
    app = App()
    app.MainLoop()
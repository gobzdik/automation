import os
from datetime import datetime


def create_screenshot_folder(base_name="screenshots"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = os.path.join("reports", f"{base_name}_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    return folder

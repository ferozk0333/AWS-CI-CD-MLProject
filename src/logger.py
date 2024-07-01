# logger is for the purpose that any execution that happens, we should be able to track everything in a file.
import logging   
import os 
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"   # f string - text file with this naming convention
log_path = os.path.join(os.getcwd(),"logs",LOG_FILE)               # creating path in the src folder itself
os.makedirs(log_path, exist_ok = True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,

)


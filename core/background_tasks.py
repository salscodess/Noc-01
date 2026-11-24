import asyncio
import time
from core import inactive_check

#Async tasks
asyncio.create_task(inactive_check())

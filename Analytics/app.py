from analytics import Analysis
import time

analysis = Analysis()

while True:
    print(analysis.get_analytics())
    time.sleep(5)
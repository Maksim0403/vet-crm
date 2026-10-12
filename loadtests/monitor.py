import csv
import time

import psutil

DURATION = 210  # секунд, трохи довше за тест (3m = 180 c)
INTERVAL = 2


def find(names):
    result = []
    for p in psutil.process_iter(["name"]):
        try:
            if any(n in (p.info["name"] or "").lower() for n in names):
                result.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return result


def measure(names):
    cpu = 0.0
    ram = 0
    for p in find(names):
        try:
            cpu += p.cpu_percent(interval=None)
            ram += p.memory_info().rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # процес завершився між переліком і вимірюванням
    return round(cpu, 1), round(ram / 1024 / 1024)


with open("resources.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["t", "python_cpu_%", "python_ram_MB", "postgres_cpu_%", "postgres_ram_MB"])
    start = time.time()
    while time.time() - start < DURATION:
        py_cpu, py_ram = measure(["python"])
        pg_cpu, pg_ram = measure(["postgres"])
        w.writerow([round(time.time() - start), py_cpu, py_ram, pg_cpu, pg_ram])
        f.flush()  # щоб дані не пропали, якщо скрипт перервати
        time.sleep(INTERVAL)

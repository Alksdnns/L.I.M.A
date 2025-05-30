import psutil

def get_battery_status():
    battery = psutil.sensors_battery()
    warnings = []

    if battery:
        battery_percent = battery.percent
        charging = battery.power_plugged
        battery_status = "charging" if charging else "not charging"
        battery_info = f"Battery Status: {battery_percent}% ({battery_status})"

        if battery_percent == 100 and charging:
            warnings.append("⚠️ Battery is fully charged. Please unplug the charger.")
        elif battery_percent < 15 and not charging:
            warnings.append("⚠️ Battery is below 15%. Please plug in the charger soon.")
    else:
        battery_info = "Battery information not available."

    if warnings:
        battery_info += "\n" + "\n".join(warnings)

    return battery_info

def get_ram_status():
    memory = psutil.virtual_memory()
    total_ram = memory.total / (1024 ** 3)
    available_ram = memory.available / (1024 ** 3)
    used_ram = memory.used / (1024 ** 3)

    ram_info = (
        f"RAM Status:\n"
        f"  Total RAM: {total_ram:.2f} GB\n"
        f"  Available RAM: {available_ram:.2f} GB\n"
        f"  Used RAM: {used_ram:.2f} GB"
    )
    return ram_info

def get_disk_status():
    disk = psutil.disk_usage('/')
    total_space = disk.total / (1024 ** 3)
    free_space = disk.free / (1024 ** 3)
    used_space = disk.used / (1024 ** 3)

    disk_info = (
        f"Disk Status:\n"
        f"  Total Space: {total_space:.2f} GB\n"
        f"  Free Space: {free_space:.2f} GB\n"
        f"  Used Space: {used_space:.2f} GB"
    )
    return disk_info

def get_system_status():
    return (
        "System Status:\n\n"
        + get_battery_status() + "\n\n"
        + get_ram_status() + "\n\n"
        + get_disk_status()
    )

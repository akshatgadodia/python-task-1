import ping3
from DeviceDataManagement import DeviceDataManagement
from typing import List
from datetime import datetime
import schedule
import time


def ping_device(device_ip: str) -> int:
    """
    This function pings the ip and return the result
    Args:
        device_ip (str): IP of the device to ping
    Returns:
        status (int): Status of the ping, 1 for success, 0 for failure
    """
    try:
        status = ping3.ping(device_ip)
    except Exception as e:
        print(e)
        status = 0
    return status


def ping_all_devices(device_data_management: DeviceDataManagement) -> None:
    """
    Pings all the devices and store the results
    Args:
        device_data_management (str): Object of the DeviceDataManagement Class
    Return:
        None
    """
    devices_data: List[dict] = device_data_management.load_device_data_file()
    devices_status_data: List[List] = []
    for device_data in devices_data:
        status: int = 1 if ping_device(device_data["ip"]) else 0
        devices_status_data.append([device_data["id"], datetime.now(), status])
    device_data_management.save_device_availability_data_file(devices_status_data)


def main() -> None:
    """
    Main function to execute the program.
    Returns:
        None
    """
    device_data_filename: str = "device_data.json"
    device_availability_data_filename: str = "device_availability_data.csv"
    device_data_management: DeviceDataManagement = DeviceDataManagement(device_data_filename,
                                                                        device_availability_data_filename)
    ping_all_devices(device_data_management)
    # device_data_management.add_device("My Mobile", "192.168.29.1")
    # device_data_management.update_device_data_by_id(2)
    # device_data_management.update_device_data_by_id(3, device_name="H")
    # device_data_management.delete_device_by_id(2)
    # device_data_management.print_all_device_data()
    # device_data_management.print_device_data_by_id(2)
    # device_data_management.save_device_availability_data_file([["Device ID", "Timestamp", "Status"]])
    # device_data_management.load_device_availability_data_file()
    # device_data_management.print_all_device_availability_data()
    # device_data_management.print_device_availability_data_by_id(1)


if __name__ == "__main__":
    schedule.every(5).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

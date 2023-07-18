from device_data_management import DeviceDataManagement
import time
import sys


def main() -> None:
    """
    Main function to execute the program.
    Returns:
        None
    Raises:
            IndexError: If a parameter is not provided.
            ValueError: If the value is not in correct format
    """
    device_data_filename: str = "device_data.json"
    device_availability_data_filename: str = "device_availability_data.csv"
    device_data_management: DeviceDataManagement = DeviceDataManagement(device_data_filename,
                                                                        device_availability_data_filename)
    try:
        command: str = sys.argv[1]
        match command:
            case "list-devices":
                device_data_management.print_all_device_data()
            case "list-device":
                try:
                    device_data_management.print_device_data_by_id(int(sys.argv[2]))
                except IndexError:
                    print(device_data_management.device_id_not_provided)
                except ValueError:
                    print(device_data_management.device_id_should_be_number)
            case "add-device":
                try:
                    device_id: int = int(input("Enter Device ID (it must be a number): "))
                    device_name: str = input("Enter Device Name: ")
                    device_ip: str = input("Enter Device IP: ")
                    device_data_management.add_device(device_id, device_name, device_ip)
                except ValueError:
                    print(device_data_management.device_id_should_be_number)
            case "delete-device":
                try:
                    device_data_management.delete_device_by_id(int(sys.argv[2]))
                except IndexError:
                    print(device_data_management.device_id_not_provided)
            case "update-device":
                try:
                    device_name: str = input("Enter Device Name: ")
                    device_ip: str = input("Enter Device IP: ")
                    device_data_management.update_device_data_by_id(int(sys.argv[2]), device_name, device_ip)
                except IndexError:
                    print(device_data_management.device_id_not_provided)
            case _:
                print("UNKNOWN COMMAND")
    except IndexError:
        while True:
            device_data_management.ping_all_devices()
            time.sleep(300)


main()

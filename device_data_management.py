import json
import csv
import ping3
from datetime import datetime


class DeviceDataManagement:
    """
    Class for managing device data.
    Attributes:
        device_not_found_message (str): A message to display when a device with a given ID is not found.
        nothing_to_update_message (str): A message to display when no device name or IP is provided for an update.
        device_data_filename (str): Name of the file that contains the device data (JSON File)
        device_availability_data_filename (str): Name of the file that store device availability data (CSV File)
    Methods:
        __init__(self, device_data_filename: str) -> None:
            Initialize the DeviceDataManagement object.

        load_device_data_file(self) -> list[dict]:
            Load or get the device data from the device data file.

        __get_device_index(self, device_id: int) -> int:
            Find the device index in the devices data and return it, if not available return -1.

        add_device(self, device_name: str, device_ip: str) -> None:
            Add a new device to the device data file.

        print_all_device_data(self) -> None:
            Print all the devices data present in the devices data file.

        print_device_data_by_id(self, device_id: int) -> None:
            Print the device details by ID.

        update_device_data_by_id(self, device_id: int, device_name: Optional[str] = None,
                                    device_ip: Optional[str] = None) -> None:
            Update the device data.

        delete_device_by_id(self, device_id: int) -> None:
            Delete the device from device data file.

        save_device_data_file(self, data: list[dict]) -> None:
            Save the device data in the device data file.

        load_device_availability_data_file(self) -> list[dict]:
            Load or get the device availability data from the device availability data file.

        print_all_device_availability_data -> None:
            Print all the devices availability data present in the devices availability data file.

        print_device_availability_data_by_id -> None:
            Print the device availability details by ID.

        save_device_availability_data_file(self, data: list[dict]) -> None:
            Save the device availability data in the device availability data file.

        __ping_device(self, device_ip: str) -> int | float:
             This function pings the ip and return the result

        ping_all_devices(self) -> None:
            Pings all the devices and store the results

        __str__(self) -> str:
            Return a string representation of the DeviceDataManagement object.

        __repr__(self) -> str:
            Return a string representation of the DeviceDataManagement object that can be used to recreate the object.
    """

    device_not_found_message = "DEVICE WITH THIS ID NOT FOUND"
    nothing_to_update_message = "DEVICE NAME AND IP IS NOT PROVIDED SO THERE IS NOTHING TO UPDATE"
    device_id_not_provided = "DEVICE ID NOT PROVIDED"
    device_with_id_already_exists = "DEVICE WITH THIS ID ALREADY EXISTS"
    device_id_should_be_number = "DEVICE ID SHOULD BE A NUMBER"
    device_name_ip_not_provided = "DEVICE NAME OR IP IS NOT PROVIDED"
    device_added_successfully = "DEVICE ADDED SUCCESSFULLY"
    device_deleted_successfully = "DEVICE DELETED SUCCESSFULLY"
    device_updated_successfully = "DEVICE UPDATED SUCCESSFULLY"

    def __init__(self, device_data_filename: str, device_availability_data_filename: str) -> None:
        """
        Initialize the DeviceDataManager object.
        Args:
            device_data_filename (str): The filename of the device data file.
        Returns:
            None
        """
        self.device_data_filename: str = device_data_filename
        self.device_availability_data_filename = device_availability_data_filename

    def __str__(self) -> str:
        """
        Return a string representation of the DeviceDataManagement object.

        Returns:
            str: String representation of the object.
        """
        return f"DeviceDataManagement(device_data_filename={self.device_data_filename}, " \
               f"device_availability_data_filename={self.device_availability_data_filename})"

    def __repr__(self) -> str:
        """
        Return a string representation of the DeviceDataManagement object
        that can be used to recreate the object.

        Returns:
            str: String representation of the object.
        """
        return f"DeviceDataManagement(device_data_filename='{self.device_data_filename}, " \
               f"device_availability_data_filename={self.device_availability_data_filename}')"



    def load_device_data_file(self) -> list[dict]:
        """
        Load or get the device data from the device data file.
        Returns:
            list[dict]: A list containing the device data.
        Raises:
            FileNotFoundError: If the device data file is not found.
            Exception: If an error occurs while loading the device data.
        """
        try:
            with open(self.device_data_filename) as file:
                return json.load(file)
        except FileNotFoundError:
            print("File Not Found")
            exit(1)
        except json.JSONDecodeError:
            print("Empty JSON File")
            return []
        except Exception as e:
            print("Some Error Occurred")
            print(e)
            exit(1)

    def __get_device_index(self, device_id: int) -> int:
        """
        Finds the device id in the devices data and return it, if not available return -1
        Args:
            device_id (int): id of the device
        Returns:
            int: The index of the device if found, else -1
        """
        devices_data: list[dict] = self.load_device_data_file()
        for i in range(len(devices_data)):
            if devices_data[i]["id"] == device_id:
                return i
        return -1

    def add_device(self, device_id: int, device_name: str, device_ip: str) -> None:
        """
        Add a new device to the device data file
        Args:
            device_id (int): id of the device
            device_name (str): name of the device
            device_ip (str): ip of the device
        Returns:
            None
        """
        if device_name == "" or device_ip == "":
            print(self.device_name_ip_not_provided)
            return
        devices_data: list[dict] = self.load_device_data_file()
        if self.__get_device_index(device_id) != -1:
            print(self.device_with_id_already_exists)
            return
        devices_data.append({'id': device_id, 'name': device_name, 'ip': device_ip})
        print(devices_data)
        self.save_device_data_file(devices_data)
        print(self.device_added_successfully)

    def print_all_device_data(self) -> None:
        """
        Print all the device data present in devices data file
        Returns:
            None
        """
        devices_data: list[dict] = self.load_device_data_file()
        for device_data in devices_data:
            print(device_data)

    def print_device_data_by_id(self, device_id: int) -> None:
        """
        Prints the device details by id
        Args:
            device_id (int): ID of the device to print
        Returns:
            None
        """
        devices_data: list[dict] = self.load_device_data_file()
        device_index: int = self.__get_device_index(device_id)
        print(self.device_not_found_message) if device_index == -1 else print(devices_data[device_index])

    def update_device_data_by_id(self, device_id: int, device_name: str,
                                 device_ip: str) -> None:
        """
        Update the device data
        Args:
            device_id (int): ID of the device to update.
            device_name (str): The new name for the device. Defaults to None.
            device_ip (str): The new IP address for the device. Defaults to None.
        Return:
            None
        """
        devices_data: list[dict] = self.load_device_data_file()
        device_index: int = self.__get_device_index(device_id)
        if device_index == -1:
            print(self.device_not_found_message)
            return
        if device_name != "":
            devices_data[device_index]["name"] = device_name
        if device_ip != "":
            devices_data[device_index]["ip"] = device_ip
        self.save_device_data_file(devices_data)
        print(self.device_updated_successfully)

    def delete_device_by_id(self, device_id: int) -> None:
        """
        Delete the device from device data file
        Args:
            device_id (int): id of the device to delete
        Returns:
            None
        """
        devices_data: list[dict] = self.load_device_data_file()
        device_index: int = self.__get_device_index(device_id)
        if device_index == -1:
            print(self.device_not_found_message)
            return
        devices_data.pop(device_index)
        self.save_device_data_file(devices_data)
        print(self.device_deleted_successfully)

    def save_device_data_file(self, data: list[dict]) -> None:
        """
        Save the device data in device data file
        Args:
            data (list[dict]): data to save in the device data file
        Returns:
            None
        Raises:
            FileNotFoundError: If the device data file is not found.
            Exception: If an error occurs while loading the device data.
        """
        try:
            with open(self.device_data_filename, "w") as file:
                file_data = json.dumps(data, indent=4)
                file.write(file_data)
        except FileNotFoundError:
            print("File Not Found")
            exit(1)
        except Exception as e:
            print("Some Error Occurred")
            print(e)
            exit(1)

    def load_device_availability_data_file(self) -> list:
        """
        Load or get the device data from the device data file.
        Returns:
            Reader: CSV reader for device availability data file
        Raises:
            FileNotFoundError: If the device data file is not found.
            Exception: If an error occurs while loading the device data.
        """
        try:
            with open(self.device_availability_data_filename, "r") as file:
                reader = csv.reader(file)
                device_availability_data = list(reader)
                return device_availability_data
        except FileNotFoundError:
            print("File Not Found")
            exit(1)
        except Exception as e:
            print("Some Error Occurred")
            print(e)
            exit(1)

    def print_all_device_availability_data(self) -> None:
        """
        Print all the device data present in devices data file
        Returns:
            None
        """
        device_availability_data: list = self.load_device_availability_data_file()
        for availability_data in device_availability_data:
            print(availability_data)

    def print_device_availability_data_by_id(self, device_id: int) -> None:
        """
        Prints the device details by id
        Args:
            device_id (int): ID of the device to print
        Returns:
            None
        """
        device_availability_data: list = self.load_device_availability_data_file()
        print(device_availability_data[0])
        for i in range(1, len(device_availability_data)):
            availability_data = device_availability_data[i]
            if int(availability_data[0]) == device_id:
                print(availability_data)

    def save_device_availability_data_file(self, data: list[list]) -> None:
        """
        Save the device data in device data file
        Args:
            data (list[list]): data to save in the device data file
        Returns:
            None
        Raises:
            FileNotFoundError: If the device data file is not found.
            Exception: If an error occurs while loading the device data.
        """
        try:
            with open(self.device_availability_data_filename, "a") as file:
                writer_object = csv.writer(file, lineterminator='\n')
                writer_object.writerows(data)
        except FileNotFoundError:
            print("File Not Found")
            exit(1)
        except Exception as e:
            print("Some Error Occurred")
            print(e)
            exit(1)

    def __ping_device(self, device_ip: str) -> int | float:
        """
        This function pings the ip and returns the result
        Args:
            device_ip (str): IP of the device to ping
        Returns:
            status (int | float): Status of the ping, 1 for success, 0 for failure
        """
        try:
            status = ping3.ping(device_ip)
        except Exception as e:
            print(e)
            status = 0
        return status

    def ping_all_devices(self) -> None:
        """
        Pings all the devices and store the results
        Return:
            None
        """
        devices_data: list[dict] = self.load_device_data_file()
        devices_status_data: list[list] = []
        for device_data in devices_data:
            status: int = 1 if self.__ping_device(device_data["ip"]) else 0
            devices_status_data.append([device_data["id"], datetime.now(), status])
        self.save_device_availability_data_file(devices_status_data)

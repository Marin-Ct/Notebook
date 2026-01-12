"""
Task 4: Semaphore for Routing Cars to Stations
Routes cars to appropriate CarStation instances based on their properties.
"""
import json
import unittest
import sys
import os

# Import from previous tasks
sys.path.insert(0, os.path.dirname(__file__))
from task1 import ListQueue
from task2 import (
    PeopleDinner, RobotDinner, ElectricStation, GasStation,
    Dineable, Refuelable
)
from task3 import Car, CarStation


class Semaphore:
    """
    Routes cars to appropriate CarStation instances.
    Creates and manages multiple stations based on car requirements.
    """
    
    def __init__(self):
        """Initialize the semaphore with various car stations."""
        # Create stations for all possible combinations
        self.stations: dict[tuple[str, str, bool], CarStation] = {}
        
        # Electric + People + Dining
        self.stations[("ELECTRIC", "PEOPLE", True)] = CarStation(
            refueling_service=ElectricStation(),
            dining_service=PeopleDinner()
        )
        
        # Electric + People + No Dining
        self.stations[("ELECTRIC", "PEOPLE", False)] = CarStation(
            refueling_service=ElectricStation(),
            dining_service=None
        )
        
        # Electric + Robots + Dining
        self.stations[("ELECTRIC", "ROBOTS", True)] = CarStation(
            refueling_service=ElectricStation(),
            dining_service=RobotDinner()
        )
        
        # Electric + Robots + No Dining
        self.stations[("ELECTRIC", "ROBOTS", False)] = CarStation(
            refueling_service=ElectricStation(),
            dining_service=None
        )
        
        # Gas + People + Dining
        self.stations[("GAS", "PEOPLE", True)] = CarStation(
            refueling_service=GasStation(),
            dining_service=PeopleDinner()
        )
        
        # Gas + People + No Dining
        self.stations[("GAS", "PEOPLE", False)] = CarStation(
            refueling_service=GasStation(),
            dining_service=None
        )
        
        # Gas + Robots + Dining
        self.stations[("GAS", "ROBOTS", True)] = CarStation(
            refueling_service=GasStation(),
            dining_service=RobotDinner()
        )
        
        # Gas + Robots + No Dining
        self.stations[("GAS", "ROBOTS", False)] = CarStation(
            refueling_service=GasStation(),
            dining_service=None
        )
    
    def route_car(self, car: Car) -> None:
        """
        Route a car to the appropriate station based on its properties.
        
        Args:
            car: The car to route
        """
        key = (car.type, car.passengers, car.is_dining)
        station = self.stations.get(key)
        
        if station:
            station.add_car(car)
        else:
            raise ValueError(f"No station available for car configuration: {key}")
    
    def process_all_cars(self) -> None:
        """Process all cars in all stations."""
        for station in self.stations.values():
            station.serve_cars()
    
    def get_statistics(self) -> dict:
        """
        Get service statistics from all stations.
        
        Returns:
            Dictionary with statistics matching generator output format
        """
        stats = {
            "ELECTRIC": ElectricStation.get_served_count(),
            "GAS": GasStation.get_served_count(),
            "PEOPLE": PeopleDinner.get_served_count(),
            "ROBOTS": RobotDinner.get_served_count(),
            "DINING": PeopleDinner.get_served_count() + RobotDinner.get_served_count(),
            "NOT_DINING": (
                ElectricStation.get_served_count() + GasStation.get_served_count()
                - PeopleDinner.get_served_count() - RobotDinner.get_served_count()
            ),
            "CONSUMPTION": {
                "ELECTRIC": ElectricStation.get_total_consumption(),
                "GAS": GasStation.get_total_consumption()
            }
        }
        return stats
    
    def process_json_string(self, json_string: str) -> None:
        """
        Process a single car from JSON string.
        
        Args:
            json_string: JSON string representing a car
        """
        car_data = json.loads(json_string)
        car = Car(
            id=car_data["id"],
            type=car_data["type"],
            passengers=car_data["passengers"],
            is_dining=car_data["isDining"],
            consumption=car_data["consumption"]
        )
        self.route_car(car)
    
    def process_json_array(self, json_array: str) -> None:
        """
        Process multiple cars from JSON array string.
        
        Args:
            json_array: JSON array string containing multiple cars
        """
        cars_data = json.loads(json_array)
        for car_data in cars_data:
            car = Car(
                id=car_data["id"],
                type=car_data["type"],
                passengers=car_data["passengers"],
                is_dining=car_data["isDining"],
                consumption=car_data["consumption"]
            )
            self.route_car(car)


# TESTS
class TestSemaphore(unittest.TestCase):
    """Test Semaphore routing and statistics."""
    
    def setUp(self):
        """Reset all service counters and create fresh semaphore."""
        PeopleDinner.reset_count()
        RobotDinner.reset_count()
        ElectricStation.reset_count()
        GasStation.reset_count()
        self.semaphore = Semaphore()
    
    def test_route_electric_car_to_electric_station(self):
        """Test that electric cars are routed to electric stations."""
        car1 = Car(1, "ELECTRIC", "PEOPLE", False, 25)
        car2 = Car(2, "ELECTRIC", "ROBOTS", False, 30)
        
        self.semaphore.route_car(car1)
        self.semaphore.route_car(car2)
        self.semaphore.process_all_cars()
        
        self.assertEqual(ElectricStation.get_served_count(), 2)
        self.assertEqual(GasStation.get_served_count(), 0)
    
    def test_route_gas_car_to_gas_station(self):
        """Test that gas cars are routed to gas stations."""
        car1 = Car(1, "GAS", "PEOPLE", False, 40)
        car2 = Car(2, "GAS", "ROBOTS", False, 35)
        
        self.semaphore.route_car(car1)
        self.semaphore.route_car(car2)
        self.semaphore.process_all_cars()
        
        self.assertEqual(GasStation.get_served_count(), 2)
        self.assertEqual(ElectricStation.get_served_count(), 0)
    
    def test_dining_routing(self):
        """Test that dining preferences are respected."""
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 25)
        car2 = Car(2, "ELECTRIC", "PEOPLE", False, 30)
        car3 = Car(3, "GAS", "ROBOTS", True, 40)
        
        self.semaphore.route_car(car1)
        self.semaphore.route_car(car2)
        self.semaphore.route_car(car3)
        self.semaphore.process_all_cars()
        
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        self.assertEqual(RobotDinner.get_served_count(), 1)
    
    def test_process_json_string(self):
        """Test processing cars from JSON strings."""
        json1 = '{"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": true, "consumption": 42}'
        json2 = '{"id": 2, "type": "GAS", "passengers": "ROBOTS", "isDining": false, "consumption": 35}'
        
        self.semaphore.process_json_string(json1)
        self.semaphore.process_json_string(json2)
        self.semaphore.process_all_cars()
        
        self.assertEqual(ElectricStation.get_served_count(), 1)
        self.assertEqual(GasStation.get_served_count(), 1)
        self.assertEqual(PeopleDinner.get_served_count(), 1)
        self.assertEqual(RobotDinner.get_served_count(), 0)
    
    def test_statistics_match_expected(self):
        """Test that statistics match expected values."""
        # Add specific cars with known properties
        cars = [
            Car(1, "ELECTRIC", "PEOPLE", False, 42),
            Car(2, "ELECTRIC", "PEOPLE", False, 26),
            Car(3, "GAS", "ROBOTS", True, 41)
        ]
        
        for car in cars:
            self.semaphore.route_car(car)
        
        self.semaphore.process_all_cars()
        stats = self.semaphore.get_statistics()
        
        self.assertEqual(stats["ELECTRIC"], 2)
        self.assertEqual(stats["GAS"], 1)
        self.assertEqual(stats["PEOPLE"], 0)  # No dining
        self.assertEqual(stats["ROBOTS"], 1)
        self.assertEqual(stats["DINING"], 1)
        self.assertEqual(stats["NOT_DINING"], 2)
        self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 68)
        self.assertEqual(stats["CONSUMPTION"]["GAS"], 41)
    
    def test_process_json_array(self):
        """Test processing multiple cars from JSON array."""
        json_array = '''[
            {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": false, "consumption": 42},
            {"id": 2, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": false, "consumption": 26},
            {"id": 3, "type": "GAS", "passengers": "ROBOTS", "isDining": true, "consumption": 41}
        ]'''
        
        self.semaphore.process_json_array(json_array)
        self.semaphore.process_all_cars()
        stats = self.semaphore.get_statistics()
        
        self.assertEqual(stats["ELECTRIC"], 2)
        self.assertEqual(stats["GAS"], 1)
        self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 68)
        self.assertEqual(stats["CONSUMPTION"]["GAS"], 41)
    
    def test_mixed_car_types(self):
        """Test processing a mix of all car types."""
        cars = [
            Car(1, "ELECTRIC", "PEOPLE", True, 20),
            Car(2, "ELECTRIC", "PEOPLE", False, 25),
            Car(3, "ELECTRIC", "ROBOTS", True, 30),
            Car(4, "ELECTRIC", "ROBOTS", False, 15),
            Car(5, "GAS", "PEOPLE", True, 40),
            Car(6, "GAS", "PEOPLE", False, 35),
            Car(7, "GAS", "ROBOTS", True, 45),
            Car(8, "GAS", "ROBOTS", False, 50)
        ]
        
        for car in cars:
            self.semaphore.route_car(car)
        
        self.semaphore.process_all_cars()
        stats = self.semaphore.get_statistics()
        
        self.assertEqual(stats["ELECTRIC"], 4)
        self.assertEqual(stats["GAS"], 4)
        self.assertEqual(stats["PEOPLE"], 2)  # 2 people dining
        self.assertEqual(stats["ROBOTS"], 2)  # 2 robots dining
        self.assertEqual(stats["DINING"], 4)
        self.assertEqual(stats["NOT_DINING"], 4)


if __name__ == "__main__":
    unittest.main()

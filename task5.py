"""
Task 5: Main Application
Synchronous version - reads cars.json and processes all cars.
"""
import json
import os
import sys
from pathlib import Path

# Import from previous tasks
sys.path.insert(0, os.path.dirname(__file__))
from task2 import PeopleDinner, RobotDinner, ElectricStation, GasStation
from task3 import Car
from task4 import Semaphore


def load_cars_from_json(file_path: str) -> list[dict]:
    """
    Load cars from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of car dictionaries
    """
    try:
        with open(file_path, 'r') as f:
            cars_data = json.load(f)
            return cars_data if isinstance(cars_data, list) else [cars_data]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{file_path}'.")
        return []


def reset_all_statistics():
    """Reset all service statistics."""
    PeopleDinner.reset_count()
    RobotDinner.reset_count()
    ElectricStation.reset_count()
    GasStation.reset_count()


def print_statistics(stats: dict):
    """
    Print statistics in the same format as the generator script.
    
    Args:
        stats: Statistics dictionary
    """
    print("\n" + "="*50)
    print("CAR SERVICE STATISTICS")
    print("="*50)
    print(json.dumps(stats, indent=4))
    print("="*50)


def main():
    """
    Main application entry point.
    Reads cars.json and processes all cars through the semaphore.
    """
    print("Car Service Station Application")
    print("="*50)
    
    # Reset all statistics
    reset_all_statistics()
    
    # Determine the path to cars.json
    # First check current directory, then check parent directory
    possible_paths = [
        "cars.json",
        "../cars.json",
        "../../cars.json",
        os.path.join(os.path.dirname(__file__), "cars.json"),
        os.path.join(os.path.dirname(__file__), "..", "cars.json")
    ]
    
    cars_file = None
    for path in possible_paths:
        if os.path.exists(path):
            cars_file = path
            break
    
    if not cars_file:
        print("\nError: cars.json not found!")
        print("Please run the generator script first to create cars.json")
        print("\nSearched in:")
        for path in possible_paths:
            print(f"  - {os.path.abspath(path)}")
        return
    
    print(f"\nLoading cars from: {os.path.abspath(cars_file)}")
    
    # Load cars from JSON file
    cars_data = load_cars_from_json(cars_file)
    
    if not cars_data:
        print("No cars to process.")
        return
    
    print(f"Loaded {len(cars_data)} cars.")
    
    # Create semaphore to route cars
    semaphore = Semaphore()
    
    # Process each car
    print("\nRouting and serving cars...")
    for i, car_data in enumerate(cars_data, 1):
        car = Car(
            id=car_data["id"],
            type=car_data["type"],
            passengers=car_data["passengers"],
            is_dining=car_data["isDining"],
            consumption=car_data["consumption"]
        )
        semaphore.route_car(car)
        
        # Show progress every 5 cars
        if i % 5 == 0 or i == len(cars_data):
            print(f"  Routed {i}/{len(cars_data)} cars...")
    
    # Process all cars through their stations
    print("\nProcessing cars at service stations...")
    semaphore.process_all_cars()
    
    # Get and print statistics
    stats = semaphore.get_statistics()
    print_statistics(stats)
    
    # Verify the totals
    total_cars = stats["ELECTRIC"] + stats["GAS"]
    print(f"\nTotal cars served: {total_cars}")
    print(f"Cars with dining: {stats['DINING']}")
    print(f"Cars without dining: {stats['NOT_DINING']}")
    print(f"Total electric consumption: {stats['CONSUMPTION']['ELECTRIC']}")
    print(f"Total gas consumption: {stats['CONSUMPTION']['GAS']}")
    
    print("\n✓ All cars processed successfully!")


def test_with_sample_data():
    """
    Test function with sample data (useful if cars.json doesn't exist).
    """
    print("Running with sample test data...")
    print("="*50)
    
    # Reset statistics
    reset_all_statistics()
    
    # Sample cars data matching the generator format
    sample_cars = [
        {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": False, "consumption": 42},
        {"id": 2, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": False, "consumption": 26},
        {"id": 3, "type": "GAS", "passengers": "ROBOTS", "isDining": True, "consumption": 41},
        {"id": 4, "type": "GAS", "passengers": "PEOPLE", "isDining": True, "consumption": 35},
        {"id": 5, "type": "ELECTRIC", "passengers": "ROBOTS", "isDining": False, "consumption": 20}
    ]
    
    semaphore = Semaphore()
    
    for car_data in sample_cars:
        car = Car(
            id=car_data["id"],
            type=car_data["type"],
            passengers=car_data["passengers"],
            is_dining=car_data["isDining"],
            consumption=car_data["consumption"]
        )
        semaphore.route_car(car)
    
    semaphore.process_all_cars()
    stats = semaphore.get_statistics()
    
    print("\nExpected statistics for sample data:")
    expected = {
        "ELECTRIC": 3,
        "GAS": 2,
        "PEOPLE": 1,
        "ROBOTS": 1,
        "DINING": 2,
        "NOT_DINING": 3,
        "CONSUMPTION": {
            "ELECTRIC": 88,
            "GAS": 76
        }
    }
    print(json.dumps(expected, indent=4))
    
    print("\nActual statistics:")
    print_statistics(stats)
    
    # Verify
    matches = stats == expected
    print(f"\n{'✓' if matches else '✗'} Statistics {'match' if matches else 'do not match'} expected values")


if __name__ == "__main__":
    # Check if --test flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_with_sample_data()
    else:
        main()

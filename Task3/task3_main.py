from display import Display
from assistant import Assistant

if __name__ == "__main__":
    # Create some Display objects (reusing models from Task 1 for demonstration)
    d1 = Display(1920, 1080, 90.0, "Display A")
    d2 = Display(2560, 1440, 110.0, "Display B")
    d3 = Display(1280, 1024, 95.0, "Display C")

    # Create an Assistant and assign the displays
    assistant = Assistant("Alice")
    assistant.assignDisplay(d1)
    assistant.assignDisplay(d2)
    assistant.assignDisplay(d3)

    # Use the assistant to compare displays and get a recommendation
    recommended = assistant.assist()

    # Simulate buying the recommended display
    if recommended:
        bought = assistant.buyDisplay(recommended)
        if bought:
            print(f"{bought.model} has been bought and removed from the list.")
            # Show remaining displays in the assistant's list
            remaining_models = [disp.model for disp in assistant.assignedDisplays]
            print(f"Displays still available: {remaining_models}")

from display import Display

if __name__ == "__main__":
    # Instantiate three Display objects with different attributes
    d1 = Display(1920, 1080, 90.0, "Display A")
    d2 = Display(2560, 1440, 110.0, "Display B")
    d3 = Display(1280, 1024, 95.0, "Display C")

    # Compare Display A and Display B
    print("Comparing Display A and Display B:")
    d1.compareSize(d2)
    d1.compareSharpness(d2)
    d1.compareWithMonitor(d2)
    print()  # blank line for readability

    # Compare Display A and Display C
    print("Comparing Display A and Display C:")
    d1.compareSize(d3)
    d1.compareSharpness(d3)
    d1.compareWithMonitor(d3)
    print()

    # Compare Display B and Display C
    print("Comparing Display B and Display C:")
    d2.compareSize(d3)
    d2.compareSharpness(d3)
    d2.compareWithMonitor(d3)

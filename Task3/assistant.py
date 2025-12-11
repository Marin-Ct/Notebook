class Assistant:
    def __init__(self, assistant_name):
        """Initialize an Assistant with a name and an empty list of assigned Display objects."""
        self.assistantName = assistant_name
        self.assignedDisplays = []

    def assignDisplay(self, display):
        """Add a Display object to this assistant's list of displays."""
        self.assignedDisplays.append(display)

    def assist(self):
        """Compare all assigned displays sequentially and recommend one to buy."""
        if not self.assignedDisplays:
            print("No displays assigned to assistant for comparison.")
            return None
        if len(self.assignedDisplays) == 1:
            # Only one display, that's the only choice
            only_display = self.assignedDisplays[0]
            print(f"Only one display ({only_display.model}) is available.")
            return only_display

        # Start with the first display as the current best
        best = self.assignedDisplays[0]
        # Compare sequentially with the rest
        for next_display in self.assignedDisplays[1:]:
            print(f"Comparing {best.model} with {next_display.model}:")
            best.compareWithMonitor(next_display)  # print comparison details
            # Decide which one to keep as best (simple criteria: choose the one with higher resolution and PPI if possible)
            area_best = best.width * best.height
            area_next = next_display.width * next_display.height
            if (area_next > area_best and next_display.ppi >= best.ppi) or \
               (area_next >= area_best and next_display.ppi > best.ppi):
                best = next_display
            print()  # blank line between comparisons

        # After comparisons, 'best' is the recommended display
        print(f"Assistant {self.assistantName} recommends buying: {best.model}\n")
        return best

    def buyDisplay(self, display):
        """Remove the specified display from the list and return it (simulating a purchase)."""
        if display in self.assignedDisplays:
            self.assignedDisplays.remove(display)
            return display
        else:
            print(f"{display.model} is not in the assistant's list.")
            return None

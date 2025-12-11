class Display:
    def __init__(self, width, height, ppi, model):
        self.width = width
        self.height = height
        self.ppi = ppi
        self.model = model

    def compareSize(self, other):
        area_self = self.width * self.height
        area_other = other.width * other.height
        if area_self > area_other:
            print(f"{self.model} has a higher resolution than {other.model} ({area_self} vs {area_other} pixels).")
        elif area_self < area_other:
            print(f"{self.model} has a lower resolution than {other.model} ({area_self} vs {area_other} pixels).")
        else:
            print(f"{self.model} and {other.model} have the same resolution ({area_self} pixels).")

    def compareSharpness(self, other):
        if self.ppi > other.ppi:
            print(f"{self.model} has a higher pixel density ({self.ppi} PPI) than {other.model} ({other.ppi} PPI).")
        elif self.ppi < other.ppi:
            print(f"{self.model} has a lower pixel density ({self.ppi} PPI) than {other.model} ({other.ppi} PPI).")
        else:
            print(f"{self.model} and {other.model} have the same pixel density ({self.ppi} PPI).")

    def compareWithMonitor(self, other):
        area_self = self.width * self.height
        area_other = other.width * other.height
        if area_self == area_other and abs(self.ppi - other.ppi) < 1e-9:
            print(f"{self.model} and {other.model} are identical in resolution and sharpness.")
        elif area_self >= area_other and self.ppi >= other.ppi:
            if area_self > area_other and self.ppi > other.ppi:
                print(f"{self.model} outperforms {other.model} in both resolution and pixel density.")
            elif area_self > area_other:
                print(f"{self.model} has a higher resolution than {other.model} (equal sharpness).")
            elif self.ppi > other.ppi:
                print(f"{self.model} has a higher pixel density than {other.model} (equal resolution).")
            else:
                print(f"{self.model} and {other.model} are on par in resolution and sharpness.")
        elif area_self <= area_other and self.ppi <= other.ppi:
            if area_self < area_other and self.ppi < other.ppi:
                print(f"{self.model} has both lower resolution and lower sharpness than {other.model}.")
            elif area_self < area_other:
                print(f"{self.model} has a lower resolution than {other.model} (same sharpness).")
            elif self.ppi < other.ppi:
                print(f"{self.model} has a lower pixel density than {other.model} (same resolution).")
            else:
                print(f"{self.model} and {other.model} have comparable specs.")
        else:
            if area_self > area_other and self.ppi < other.ppi:
                print(f"{self.model} is higher resolution but less sharp than {other.model}.")
            elif area_self < area_other and self.ppi > other.ppi:
                print(f"{self.model} is lower resolution but sharper than {other.model}.")
            else:
                print(f"{self.model} and {other.model} each have different strengths.")

import json, os, pygame

# Create a class to make a data handler
class DataHandler:
    # Initialise the class
    def __init__(self):
        # Variable to track the amount of data loaded
        self.total_loaded = 0
    
    # Save to json file from dictionary
    def SaveJSON(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    # Make a generic subroutine to load data from files  -  JSON
    def LoadJSON(self, path):
        # Check if the file exists
        if os.path.exists(path) == False:
            return -1
        
        with open(path, "r") as f:
            self.total_loaded += 1
            return json.load(f)
        
    # Subroutine to load assets
    def LoadAssets(self, path):
        assets = {}
        # Get the files in each folder
        current_path = f"{path}/"
        files = os.listdir(current_path)
        # Loop through each file
        for file in files:
            # Check if the found "file" is actually a directory
            if os.path.isdir(f"{current_path}/{file}"):
                # Skip it
                continue
            # Load the file
            img = self.LoadSingleAsset(f"{current_path}/{file}")
            # Get the name of the file
            file_name = file.split(".")
            file_name.pop()
            file_name = "".join(file_name)
            if "_x" in file_name:
                size_mult = file_name.split("_x")[1]
                file_name = file_name.split("_x")[0]
                # Check if the size multiplier is a decimal
                if size_mult[0] == "0":
                    # Count the power to the decimal places
                    count = 0
                    size_mult_num = ""
                    for char in size_mult:
                        if char == "0": count += 1
                        else: size_mult_num += char
                    size_mult_num = int(size_mult_num)
                    size_mult = size_mult_num * (10**-(count+len(str(size_mult_num))-1))
                    # Resize the image
                    img = self.ScaleImage(img, size_mult)
                
            # Save it in the dict
            assets[file_name] = img
        
        return assets
            
    # Subroutine to load a single asset
    def LoadSingleAsset(self, path):
        img = pygame.image.load(path)
        return img.convert_alpha()
    
    # Subroutine to scale an image
    def ScaleImage(self, img, scale):
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
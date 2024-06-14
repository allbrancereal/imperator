class InputLibrary:
    identifier = 'input'
    
    def __init__(self, tab):  # Add a tab argument
        self.tab = tab  # Store the tab instance
        print("Input library created")

# The 'registered_vars' attribute is a dictionary that maps identifiers to classes
registered_vars = {
    InputLibrary.identifier: InputLibrary
}

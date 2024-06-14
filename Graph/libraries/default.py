class DefaultLibrary:
    identifier = 'default'
    
    def __init__(self, tab):  # Add a tab argument
        self.tab = tab  # Store the tab instance
        print("Default library created")

# The 'registered_vars' attribute is a dictionary that maps identifiers to classes
registered_vars = {
    DefaultLibrary.identifier: DefaultLibrary
}

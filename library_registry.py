
class LibraryRegistry:
    def __init__(self):
        self.libraries = {}

    def register_library(self, name, library):
        self.libraries[name] = library

    def get_library(self, name):
        return self.libraries.get(name)
    
    def create(self, identifier, *args, **kwargs):
        LibraryClass = self.get_library(identifier)
        print(f"Creating library with identifier {identifier}: {LibraryClass}")  # Print the identifier and the LibraryClass
        if LibraryClass is not None:
            return LibraryClass(*args, **kwargs)
        return None



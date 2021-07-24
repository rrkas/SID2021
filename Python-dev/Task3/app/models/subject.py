class Subject:
    def __init__(self, name="", id=-1):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Subject({self.id}, {self.name})"

class Score:
    def __init__(self, name=None, regd_num=None, score=0, id=-1):
        self.id = id
        self.name = name
        self.regd_num = regd_num
        self.score = score

    def __repr__(self):
        return f"Score({self.id}, {self.name}, {self.regd_num}, {self.score})"

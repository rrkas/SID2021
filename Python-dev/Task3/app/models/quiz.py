class Quiz:
    def __init__(self, id=-1, num_options=-1, subj_code=-1):
        self.id = id
        self.num_options = num_options
        self.subject_code = subj_code

    def __repr__(self):
        return f"Quiz({self.id}, {self.subject_code}, {self.num_options})"

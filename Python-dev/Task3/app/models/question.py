import json


class Question:
    def __init__(self, question="", options=[], corr_idx_0=-1, id=-1, quiz_id=-1):
        self.id = id
        self.question = question
        self.options = options
        self.correct_answer_idx = corr_idx_0
        self.quiz_id = quiz_id

    def __repr__(self):
        return f"Question(id={self.id}, quiz_id={self.quiz_id}, question={self.question}, \
options={self.options_encode()}, correct_idx={self.correct_answer_idx})"

    def options_encode(self):
        return json.dumps(self.options)

    @staticmethod
    def options_decode(options_json):
        return json.loads(options_json)

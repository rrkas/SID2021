from app.services.db_handlers import QuizDB, ScoreDB
from .models.score import Score


# binding widgets in a tag for collective button click
def bind_widgets_in_tag(tag, *widgets):
    for widget in widgets:
        widget.bindtags((tag,) + widget.bindtags())


# globally usable data wrapped in a class
class UtilData:
    def __init__(self):
        self.debug = False
        self.app_name = "Quizzit"
        self.is_teacher = False
        self.student_score = Score()
        self.quiz_db = QuizDB()
        self.score_db = ScoreDB()

        self.correct_respond = 1
        self.wrong_respond = 0
        self.not_responded = 0


util_data = UtilData()

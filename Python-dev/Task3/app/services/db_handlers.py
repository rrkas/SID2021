import os
import sqlite3 as sql

from app.models.question import Question
from app.models.quiz import Quiz
from app.models.score import Score
from app.models.subject import Subject

# db directory
_db_path = "db"
if not os.path.exists(_db_path):
    os.mkdir(_db_path)


# convert query to [Quiz]
def quiz_from_query(query):
    return Quiz(
        id=query[0],
        num_options=query[1],
        subj_code=query[2],
    )


# convert query to [Subject]
def subject_from_query(query):
    return Subject(
        id=query[0],
        name=query[1],
    )


# convert query to [Question]
def question_from_query(query):
    return Question(
        id=query[0],
        question=query[1],
        options=Question.options_decode(query[2]),
        corr_idx_0=query[3],
        quiz_id=query[4],
    )


# convert query to [Score]
def score_from_query(query):
    return Score(
        id=query[0],
        name=query[1],
        regd_num=query[2],
        score=query[3],
    )


# quiz database
# tables: subject, question, quiz
class QuizDB:
    _db_name = "quiz.db"
    _quizzes_table_name = "quizzes"
    _questions_table_name = "questions"
    _subjects_table_name = "subjects"

    # create tables
    def __init__(self):
        self.conn = sql.connect(os.path.join(_db_path, QuizDB._db_name))
        self.cursor = self.conn.cursor()
        # create question table if doesn't exist
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {QuizDB._questions_table_name} (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    options TEXT,
                    correct_answer_idx INTEGER,
                    quiz_id INTEGER
                )
                """
            )
        except BaseException as e:
            print(e)
        # create quiz table if doesn't exist
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {QuizDB._quizzes_table_name}(
                    id INTEGER PRIMARY KEY,
                    num_options INTEGER,
                    subject_code INTEGER
                )
                """
            )
        except BaseException as e:
            print(e)
        # create subject table if doesn't exist
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {QuizDB._subjects_table_name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
                """
            )
        except BaseException as e:
            print(e)
        self.conn.commit()

    # create/update question
    def update_question(self, question: Question):
        try:
            if question.id < 0:
                self.cursor.execute(
                    f"INSERT INTO {QuizDB._questions_table_name}(question, options, correct_answer_idx, quiz_id) \
                    VALUES (?,?,?,?)",
                    (
                        question.question,
                        question.options_encode(),
                        question.correct_answer_idx,
                        question.quiz_id,
                    ),
                )
                question.id = self.cursor.lastrowid
            else:
                self.cursor.execute(
                    f"""
                    UPDATE {QuizDB._questions_table_name}
                    SET question=?, options=?, correct_answer_idx=?
                    WHERE id={question.id}
                    """,
                    (
                        question.question,
                        question.options_encode(),
                        question.correct_answer_idx,
                    ),
                )
            self.conn.commit()
        except BaseException as e:
            print(e)

    # create/ update quiz
    def update_quiz(self, quiz: Quiz):
        try:
            if quiz.id < 0:
                self.cursor.execute(
                    f"INSERT INTO {QuizDB._quizzes_table_name}(num_options, subject_code) VALUES (?,?)",
                    (
                        quiz.num_options,
                        quiz.subject_code,
                    ),
                )
                quiz.id = self.cursor.lastrowid
            else:
                self.cursor.execute(
                    f"""
                    UPDATE {QuizDB._quizzes_table_name}
                    SET num_options=?, subject_code=?
                    WHERE id={quiz.id}
                    """,
                    (quiz.num_options, quiz.subject_code),
                )
            self.conn.commit()
        except BaseException as e:
            print(e)

    # get all Quiz objects (latest first)
    def quizzes(self):
        try:
            query = self.cursor.execute(
                f"SELECT * from {QuizDB._quizzes_table_name} order by id desc"
            )
            return list(map(quiz_from_query, query))
        except BaseException as e:
            print(e)
            return []

    # add subject (subjects not to be modified)
    def add_subject(self, subject: Subject):
        try:
            self.cursor.execute(
                f"INSERT INTO {QuizDB._subjects_table_name}(name) VALUES (?)",
                (subject.name,),
            )
            subject.id = self.cursor.lastrowid
        except BaseException as e:
            print(e)
        self.conn.commit()

    # get all subjects
    def subjects(self):
        try:
            query = self.cursor.execute(f"SELECT * from {QuizDB._subjects_table_name}")
            return list(map(subject_from_query, query))
        except BaseException as e:
            print(e)
            return []

    # get the subject for the quiz
    def subject_of_quiz(self, quiz):
        try:
            data = self.cursor.execute(
                f"SELECT * from {QuizDB._subjects_table_name} WHERE id={quiz.subject_code}"
            )
            return subject_from_query(data.fetchone()) if data.arraysize > 0 else None
        except BaseException as e:
            print(e)

    # get the questions of the quiz
    def questions_of_quiz(self, quiz):
        try:
            data = self.cursor.execute(
                f"""
                SELECT * from {QuizDB._questions_table_name}
                WHERE quiz_id={quiz.id}
                """
            )
            ques = [question_from_query(q) for q in data]
            return ques
        except BaseException as e:
            print(e)
            return []


# score database
# tables: score
class ScoreDB:
    _db_name = "score.db"
    _table_name = "score"

    # create tables
    def __init__(self):
        self.conn = sql.connect(os.path.join(_db_path, ScoreDB._db_name))
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {ScoreDB._table_name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    regd_num TEXT,
                    score INTEGER
                )
                """
            )
        except BaseException as e:
            print(e)
        self.conn.commit()

    def update_score(self, score: Score):
        try:
            if score.id < 0:
                self.cursor.execute(
                    f"""
                    INSERT INTO {ScoreDB._table_name}(name, regd_num, score)
                    VALUES (?,?,?)
                    """,
                    (
                        score.name,
                        score.regd_num,
                        score.score,
                    ),
                )
                score.id = self.cursor.lastrowid
            else:
                self.cursor.execute(
                    f"""
                    UPDATE {ScoreDB._table_name}
                    SET name=?, regd_num=?, score=?
                    WHERE id={score.id}
                    """,
                    (
                        score.name,
                        score.regd_num,
                        score.score,
                    ),
                )
            self.conn.commit()
        except BaseException as e:
            print(e)

    def scores(self):
        try:
            query = self.cursor.execute(f"""SELECT * from {ScoreDB._table_name}""")
            return list(map(score_from_query, query))
        except BaseException as e:
            print(e)
            return []

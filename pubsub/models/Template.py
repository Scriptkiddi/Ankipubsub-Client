__author__ = 'fritz'
class Template():
    def __init__(self,
                 name,
                 answer_format,
                 question_format,
                 deck,
                 ord,
                 back_answer_format,
                 back_question_format):
        self.answer_format = answer_format
        self.name = name
        self.question_format = question_format
        # self.deck = deck
        self.ord = int(ord)
        self.back_answer_format = back_answer_format
        self.back_question_format = back_question_format
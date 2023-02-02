class Feedback:
    f_ID = 0
    def __init__(self, feedback):
        self.__ID = Feedback.f_ID
        Feedback.f_ID += 1
        self.__feedback = feedback

    def set_feedback(self,newfeedback):
        self.__feedback = newfeedback

    def set_ID(self,ID):
        self.__ID = ID

    def get_ID(self):
        return self.__ID

    def get_feedback(self):
        return self.__feedback

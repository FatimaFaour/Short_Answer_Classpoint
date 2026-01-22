class AppState:
    def __init__(self):
        self.session_id = None
        self.current_question_id = None
        self.question_start_ts = None

        # 🔽 Activity settings
        self.allow_multiple = False
        self.max_submissions = 1
        self.hide_names = False
        self.auto_close_seconds = 15

        self.closed_questions = []  # list of dicts
        #self.current_question_id = None
        self.current_question_text = None
       # self.question_start_ts = None
        

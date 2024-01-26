from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class chat_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_history_title = models.TextField(blank=True , default="テストセッション") 
    question_list = models.TextField(blank=True)  # Assuming a || list of item strings
    answer_list = models.TextField( blank=True)  # Assuming a || list of item strings
    created = models.DateTimeField(default=timezone.now)
    

    # You can add other fields like order date, total amount, etc., as needed

    def get_chat_questions(self):
        return self.question_list.split('||')
    
    def get_chat_answers(self):
        return self.answer_list.split('||')

    def __str__(self):
        return f"Message #{self.id} - User: {self.user.username}"

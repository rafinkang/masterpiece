from django.forms import ModelForm
from masterpiece.models.Test import Test
from masterpiece.example_class.DbConn import *

class post_frm(ModelForm):
    class Meta:
        model = Test
        fields = ['post_message1', 'post_message2', 'post_message3'] # form field 정의

    # form 내용 저장
    def save(self, ins_dict):
        db = DbConn()
        sql = "insert into test(test, test2, test3) values(%s, %s, %s)"
        data = [ins_dict['post_message1'], ins_dict['post_message2'], ins_dict['post_message3']]
        db.execute(sql, data)
        
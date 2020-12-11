from django.forms import ModelForm
from masterpiece.models import test_frm
from masterpiece.example_class.DbConn import *

class post_frm(ModelForm):
    class Meta:
        model = test_frm
        fields = ['post_message1', 'post_message2', 'post_message3']

    def save(self, ins_dict):

        db = DbConn()
        sql = "insert into test(test, test2, test3) values(%s, %s, %s)"
        data = [ins_dict['post_message1'], ins_dict['post_message2'], ins_dict['post_message3']]
        # sql = "insert into test(test, test2, test3) values(%s, %s, %s);"
        # data = [['1','1','1'], ['2','2','2'], ['3','3','3']]
        db.execute(sql, data)
        
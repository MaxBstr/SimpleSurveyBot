from tortoise.models import Model
from tortoise import fields


class Survey(Model):
    id = fields.IntField(pk=True)
    question = fields.CharField(max_length=60)
    answers: fields.ReverseRelation["Answer"]
    is_answered: fields.ReverseRelation["UserAnsweredSurvey"]


class Answer(Model):
    id = fields.IntField(pk=True)
    answer = fields.CharField(max_length=60)
    position_in_survey = fields.IntField()
    chosen_quantity = fields.IntField()
    survey: fields.ForeignKeyRelation[Survey] = fields.ForeignKeyField(
        model_name="models.Survey",
        related_name="answers",
    )


class UserAnsweredSurvey(Model):
    user_id = fields.IntField()
    survey: fields.ForeignKeyRelation[Survey] = fields.ForeignKeyField(
        model_name="models.Survey",
        related_name="is_answered",
    )

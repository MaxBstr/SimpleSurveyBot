from collections import defaultdict

from .models import Survey, Answer, UserAnsweredSurvey


async def set_data(data: dict):
    new_survey = await Survey.create(question=data["question"])

    for key, value in data.items():
        if key == "question":
            continue
        await Answer.create(
            answer=value,
            survey=new_survey,
            position_in_survey=int(key[-1]),
            chosen_quantity=0
        )

    return new_survey.id


async def get_statistics(survey_id: int) -> dict:
    survey = await Survey.get(id=survey_id).prefetch_related("answers")
    data = defaultdict()

    for ans in survey.answers:
        pos_in_survey = ans.position_in_survey
        answer = ans.answer
        chosen_quantity = ans.chosen_quantity
        ans_id = ans.id

        data[f"answer{pos_in_survey}"] = [answer, chosen_quantity, ans_id]

    return dict(sorted(data.items(), key=lambda x: x[0]))


async def update_data(data: dict) -> None:
    answer_object = await Answer.get(id=data["ans_id"]).prefetch_related("survey")
    answer_object.chosen_quantity += 1
    await answer_object.save()

    await UserAnsweredSurvey.create(
        user_id=data["user_id"],
        survey=answer_object.survey
    )


async def get_surveys(offset: int = 0, limit: int = 5) -> dict:
    data = defaultdict()
    surveys = await Survey.all().offset(offset).limit(limit)

    for survey in surveys:
        data[f"{survey.id}"] = survey.question

    return data


async def get_survey_question_by_id(survey_id: int) -> str:
    survey = await Survey.get(id=survey_id)
    return survey.question


async def is_zero_surveys() -> bool:
    return not await Survey.all().exists()


async def check_survey_exists(survey_id: int) -> bool:
    return await Survey.exists(id=survey_id)


async def check_answered(user_id: int, survey_id: int) -> bool:
    survey = await Survey.get(id=survey_id)
    return await UserAnsweredSurvey.filter(user_id=user_id, survey=survey).exists()


async def get_surveys_count() -> int:
    return await Survey.all().count()

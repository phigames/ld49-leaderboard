import json
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F
from leaderboard.models import Run


@require_POST
@csrf_exempt
def post_score(request):
    data = json.loads(request.body)
    if "username" not in data or "score" not in data:
        return HttpResponseBadRequest()
    username = data["username"]
    score = data["score"]
    my_run = Run.objects.create(
        username=username,
        score=score,
    )
    runs = Run.objects.annotate(
        rank=Window(expression=RowNumber(), order_by=F("score").desc())
    ).order_by("rank")
    sql, params = runs.query.sql_with_params()
    my_run = list(Run.objects.raw("""
        SELECT "id", "created_at", "updated_at", "username", "score", "rank" FROM ({}) WHERE "id" = %s
    """.format(sql), [*params, str(my_run.id).replace("-", "")]))[0]
    return JsonResponse(
        {
            "runs": [
                {
                    "rank": run.rank,
                    "username": run.username,
                    "score": run.score,
                    "date": run.created_at,
                }
                for i, run in enumerate(runs[:10])
            ],
            "myRun": {
                "rank": my_run.rank,
                "username": my_run.username,
                "score": my_run.score,
                "date": my_run.created_at,
            },
        }
    )


@require_GET
def get_leaderboard(request):
    runs = Run.objects.annotate(
        rank=Window(expression=RowNumber(), order_by=F("score").desc())
    ).order_by("rank")[:10]
    return JsonResponse(
        {
            "runs": [
                {
                    "rank": run.rank,
                    "username": run.username,
                    "score": run.score,
                    "date": run.created_at,
                }
                for run in runs
            ]
        }
    )

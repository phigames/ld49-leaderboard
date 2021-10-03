import json
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseBadRequest, JsonResponse
from leaderboard.models import Run


@require_POST
@csrf_exempt
def post_score(request):
    data = json.loads(request.body)
    if "username" not in data or "score" not in data:
        return HttpResponseBadRequest()
    username = data["username"]
    score = data["score"]
    Run.objects.create(
        username=username,
        score=score,
    )
    return JsonResponse({})


@require_GET
def get_leaderboard(request):
    return JsonResponse(
        {
            "runs": [
                {
                    "username": run.username,
                    "score": run.score,
                    "date": run.created_at,
                }
                for run in Run.objects.order_by("-score")[:10]
            ]
        }
    )

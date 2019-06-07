import os

from django.views.generic import View
from django.http import JsonResponse

from django_project import settings


class PostReceiveGitHubWebHookView(View):
    def post(self, request, *args, **kwargs):
        event_type = request.POST['X-GitHub-Event']
        delivery_id = request.POST['X-GitHub-Delivery']
        signature = request.POST['X-Hub-Signature']
        if (event_type == 'push'
           and delivery_id
           and signature == settings.GITHUB_HOOK_SIGNATURE):
            cmd_str = "/home/italo/server-management/hooks/post-receive.sh"
            cmd_output = os.popen(cmd_str).read()
            # TODO: send cmd_output as a mail
            if not cmd_output:
                return JsonResponse({
                    "success": False,
                    "message": "Error: {} {} {}".format(
                                event_type, delivery_id, signature)
                })
        else:
            return JsonResponse({
                "success": False,
                "message": "Error: {} {} {}".format(
                            event_type, delivery_id, signature)
            })
        return JsonResponse({"success": True})

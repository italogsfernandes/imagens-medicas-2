import os

from django.views.generic import View
from django.http import JsonResponse, HttpResponse


class PostReceiveGitHubWebHookView(View):
    def post(self, request, *args, **kwargs):
        event_type = request.POST['X-GitHub-Event']
        delivery_id = request.POST['X-GitHub-Delivery']
        signature = request.POST['X-Hub-Signature']
        if ((event_type == 'push' or event_type == 'ping')
           and delivery_id
           and signature):
            cmd_str = "/home/italo/server-management/hooks/post-receive.sh"
            cmd_output = os.popen(cmd_str).read()
            # TODO: send cmd_output as a mail
            if not cmd_output:
                return JsonResponse({
                    "success": True,
                    "message": "Error: {} {} {}".format(
                                event_type, delivery_id, signature)
                })
            else:
                with open("/home/italo/xablaus.txt", 'w+') as cmd_file:
                    cmd_file.write(cmd_output)
        else:
            return JsonResponse({
                "success": True,
                "message": "Error: {} {} {}".format(
                            event_type, delivery_id, signature)
            })
        return JsonResponse({"success": True})

    def get(self, request, *args, **kwargs):
        cmd_str = "/home/italo/server-management/hooks/post-receive.sh"
        cmd_output = os.popen(cmd_str).read()
        return HttpResponse(cmd_output)

from flask import (
    Blueprint,
    jsonify,
    url_for,
    request,
    send_file,
    json,
    redirect,
    current_app,
)
from flask_login import login_required, current_user
from soundcloud import celery
from soundcloud.services import get_all_songs_by_user
import random
import time
import os

background = Blueprint("background", __name__)


@celery.task(bind=True)
def download_task(self, res):
    message = ""
    total = random.randint(10, 20)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = "Your file is preparing for download"
        self.update_state(
            state="PROGRESS", meta={"current": i, "total": total, "status": message}
        )
        print(message)
        time.sleep(1)
    print(res)
    path = f"/~/project/project-SoundCloud/soundcloud/static/user_info/user-info-{res['username']}.txt"
    with open(path, "w+") as f:
        for key, value in res.items():
            f.write("%s:%s\n" % (key, value))
    f.close()
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}


@background.route("/task", methods=["POST"])
@login_required
def longtask():
    print("Process start")
    res = request.get_json()
    #print(res)
    task = download_task.delay(res)
    # return redirect(url_for("background.download",username=res['username']))
    return (
        jsonify({}),
        202,
        {"Location": url_for("background.taskstatus", task_id=task.id)},
    )


@background.route("/status/<task_id>")
def taskstatus(task_id):
    task = download_task.AsyncResult(task_id)
    if task.state == "PENDING":
        # job did not start yet
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info), 
        }
    return jsonify(response)


@background.route("/download/<user>")
def download(user):
    path = f"/~/project/project-SoundCloud/soundcloud/static/user_info/user-info-{user}.txt"
    return send_file(path)

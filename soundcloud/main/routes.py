from flask import Blueprint
from flask import render_template, request, flash
from flask_login import login_required
from soundcloud.users.utils import post_comments
from soundcloud.services import get_song_list, get_count_list

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home", methods=["GET", "POST"])
def home():
    page = request.args.get("page", 1, type=int)
    songs = get_song_list(page)
    play = get_count_list()
    print(play)
    return render_template("home.html", songs=songs, play=play)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/home/post_comment", methods=["GET", "POST"])
@login_required
def post_comment():
    res = request.get_json()
    print(res)
    if len(res) == 3:
        post_comments(res)
        flash("Your comment has been posted.", "success")
    return render_template("songs.html", song_id=res["song_id"])


# @main.route("/search", methods=["GET", "POST"])
# def search():
#     if request.method == "POST":
#         keyword = request.form["search"]
#         body = {"query": {"multi_match": {"query": keyword}}}
#     else:
#         keyword = request.args.get("q", None)
#         body = {"query": {"multi_match": {"query": keyword}}}
#         print(keyword)

#     res = es.search(index="soundcloud", doc_type="songs", body=body)

#     if res["hits"]["hits"]:
#         res = res["hits"]["hits"]
#         print(res)
#         return render_template("search.html", title="Search Results", res=res)
#     else:
#         res = "Not Found"
#         return render_template("search.html", title="Search Results", res=res)


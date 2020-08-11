from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, Http404
from mongoengine import Q
import datetime
from .models import Miner, Status

import json
import tweetymine


def index(request):
    """ Show All potential miners on startup. """
    surl = request.build_absolute_uri(reverse("minersearch"))
    aurl = request.build_absolute_uri(reverse("mineradd"))
    murl = request.build_absolute_uri(
        reverse("minemanage", kwargs={"minerid":  "0"}))
    uurl = request.build_absolute_uri(reverse("minerupdate"))

    latest_updated = Miner.objects.aggregate([
        {"$sort": {"last_updated": -1}},
        {"$project": {"last_updated": 1}}
    ]).next()

    context = {
        "last_updated": latest_updated["last_updated"],
        "search_url": surl,
        "add_url": aurl,
        "miner_url": murl,
        "update_url": uurl
    }

    return HttpResponse(render(request, "miner/index.html", context))


def add(request):
    print("POST", request.POST)

    handle = request.POST.get("handle")
    miner = Miner.objects(handle=handle)

    if len(miner) > 0:
        return HttpResponse("Miner already exists.", status=304)

    miner = Miner(handle=handle).save()
    miner = json.loads(miner.to_json())
    tweetymine.main()

    return JsonResponse(miner)


def update_mine(request):
    tweetymine.main()
    latest_updated = Miner.objects.aggregate([
        {"$sort": {"last_updated": -1}},
        {"$project": {"last_updated": 1}}
    ]).next()

    print(latest_updated["last_updated"])

    data = {
        "last_updated": latest_updated["last_updated"]
    }

    return JsonResponse(data)


def manage(request, minerid):
    miner = Miner.objects(tid=str(minerid)).first()

    if miner is None:
        return Http404("Miner with ID does not exist.")

    latest_updated = Miner.objects.aggregate([
        {"$sort": {"last_updated": -1}},
        {"$project": {"last_updated": 1}}
    ]).next()

    tweets = Status.objects.filter(user__tid=str(minerid))

    retweet_list = []
    favourite_list = []
    creation_dates = []
    for idx, tweet in enumerate(tweets):
        retweet_list.append(tweet["retweet_count"])
        favourite_list.append(tweet["favourite_count"])
        d = datetime.datetime.strptime(
            tweet["creationDate"], "%a %b %d %H:%M:%S %z %Y")
        creation_dates.append(d)

    context = {
        "last_updated": latest_updated["last_updated"],
        "retweet_list": retweet_list,
        "favourite_list": favourite_list,
        "creation_dates": creation_dates,
        "miner": miner,
        "tweets": tweets
    }

    return HttpResponse(render(request, "miner/manage.html", context))


def search(request):
    query = request.GET.get("q")
    ajax = bool(request.GET.get("ajax"))

    if query == "":
        miners = Miner.objects.all().to_json()
    else:
        miners = Miner.objects.filter(
            Q(handle__icontains=query) | Q(name__icontains=query)
        ).to_json()

    if ajax:
        return JsonResponse(json.loads(miners), safe=False)

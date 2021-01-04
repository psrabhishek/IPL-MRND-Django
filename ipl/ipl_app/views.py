from django.shortcuts import render
from ipl_app.models import *
from django.shortcuts import render, redirect
from django.db.models import *
import datetime
from debug_toolbar.panels import logging
from django.views import View
from ipl_app.forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

team_logo = {
    'Mumbai Indians': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/1200px-Mumbai_Indians_Logo.svg.png',
    'Sunrisers Hyderabad': 'https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Sunrisers_Hyderabad.svg/1200px-Sunrisers_Hyderabad.svg.png',
    'Delhi Capitals': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Delhi_Capitals_Logo.svg/1200px-Delhi_Capitals_Logo.svg.png',
    'Delhi Daredevils': 'https://vignette.wikia.nocookie.net/logopedia/images/8/8a/Delhi_Daredevils.svg.png/revision/latest?cb=20180113221053',
    'Deccan Chargers': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a6/HyderabadDeccanChargers.png/200px-HyderabadDeccanChargers.png',
    'Royal Challengers Bangalore': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Royal_Challengers_Bangalore_Logo_2016.svg/200px-Royal_Challengers_Bangalore_Logo_2016.svg.png',
    'Kolkata Knight Riders': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/200px-Kolkata_Knight_Riders_Logo.svg.png',
    'Gujarat Lions': 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c4/Gujarat_Lions.png/200px-Gujarat_Lions.png',
    'Pune Warriors': 'https://upload.wikimedia.org/wikipedia/en/4/4a/Pune_Warriors_India_IPL_Logo.png',
    'Rajasthan Royals': 'https://i.pinimg.com/originals/ce/b7/04/ceb7040289e35b9a2358cf18bb6a9315.png',
    'Kochi Tuskers Kerala': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/96/Kochi_Tuskers_Kerala_Logo.svg/1200px-Kochi_Tuskers_Kerala_Logo.svg.png',
    'Rising Pune Supergiants': 'http://pngriver.com/wp-content/uploads/2018/04/Download-Rising-Pune-Supergiants-Logo-PNG.png',
    'Kings XI Punjab': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e7/Kings_XI_Punjab_logo.svg/1200px-Kings_XI_Punjab_logo.svg.png',
    'Rising Pune Supergiant': 'http://pngriver.com/wp-content/uploads/2018/04/Download-Rising-Pune-Supergiants-Logo-PNG.png',
    'Chennai Super Kings': 'https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/1200px-Chennai_Super_Kings_Logo.svg.png',
}


def points_view(request, **kwargs):
    matches = Match.objects.filter(**kwargs).order_by('mid')
    seasons = [i["season"] for i in Match.objects.values('season').distinct().order_by("-season")]
    pt = {}
    for match in matches:
        if match.team1 not in pt:
            pt.update({match.team1: [match.team1, 0, 0, 0, 0]})
        if match.team2 not in pt:
            pt.update({match.team2: [match.team2, 0, 0, 0, 0]})

        pt[match.team1][1] += 1
        pt[match.team2][1] += 1

        if match.result == "no result":
            pt[match.team1][-1] += 1
            pt[match.team2][-1] += 1
        else:
            pt[match.winner][-1] += 2
            pt[match.winner][2] += 1
            if match.team1 == match.winner:
                pt[match.team2][3] += 1
            else:
                pt[match.team2][3] += 1

    pt = sorted(pt.values(), key=lambda x: -x[-1])

    return render(
        request,
        template_name="ipl_app/points.html",
        context={
            "seasons": seasons,
            "season": kwargs["season"],
            "teams": pt,
        }
    )


def points_home(request):
    latest_season = Match.objects.aggregate(Max('season'))["season__max"]
    return redirect("points_html", **{"season": latest_season})


def season_view(request, **kwargs):
    if "season" not in kwargs:
        latest_season = Match.objects.aggregate(Max('season'))["season__max"]
        kwargs.update({"season": latest_season})
    matches = Match.objects.filter(**kwargs).order_by('mid')
    seasons = [i["season"] for i in Match.objects.values('season').distinct().order_by("-season")]
    return render(
        request,
        template_name="ipl_app/season.html",
        context={
            "seasons": seasons,
            "season": kwargs["season"],
            "matches": matches,
        }
    )


def home_view(request, **kwargs):
    latest_season = Match.objects.aggregate(Max('season'))["season__max"]
    matches = Match.objects.filter(season=latest_season).order_by('mid')
    pt = {}
    for match in matches:
        if match.team1 not in pt:
            pt.update({match.team1: [match.team1, 0, 0, 0, 0]})
        if match.team2 not in pt:
            pt.update({match.team2: [match.team2, 0, 0, 0, 0]})

        pt[match.team1][1] += 1
        pt[match.team2][1] += 1

        if match.result == "no result":
            pt[match.team1][-1] += 1
            pt[match.team2][-1] += 1
        else:
            pt[match.winner][-1] += 2
            pt[match.winner][2] += 1
            if match.team1 == match.winner:
                pt[match.team2][3] += 1
            else:
                pt[match.team2][3] += 1

    pt = sorted(pt.values(), key=lambda x: -x[-1])

    year_end = datetime.datetime(latest_season, 12, 31)
    year_start = datetime.datetime(latest_season - 1, 12, 31)
    end_match = Match.objects.filter(date__lte=year_end, date__gte=year_start).aggregate(Max('mid'))["mid__max"]
    end_match = Match.objects.get(mid=end_match)

    return render(
        request,
        template_name="ipl_app/home.html",
        context={
            "season": latest_season,
            "teams": pt,
            "champion": end_match.winner,
            "icon": team_logo[end_match.winner],
        }
    )


@login_required(login_url='login')
def match_view(request, **kwargs):
    match = Match.objects.get(mid=kwargs["mid"])
    year_end = datetime.datetime(kwargs["season"], 12, 31)
    year_start = datetime.datetime(kwargs["season"] - 1, 12, 31)
    start_match = Match.objects.filter(date__lte=year_end, date__gte=year_start).aggregate(Min('mid'))["mid__min"]
    deliveries1 = Delivery.objects.filter(match_id=match, inning=1)
    deliveries2 = Delivery.objects.filter(match_id=match, inning=2)
    print(start_match, match.mid - start_match + 1)

    i1b = Delivery.objects.filter(match_id=match, inning=1).exclude(player_dismissed=None).values('bowler').annotate(
        total=Count('bowler')).order_by('-total')[:3]
    i2b = Delivery.objects.filter(match_id=match, inning=2).exclude(player_dismissed=None).values('bowler').annotate(
        total=Count('bowler')).order_by('-total')[:3]

    i1b = [player["bowler"] + " - " + str(player["total"]) + " wks" for player in i1b]
    i2b = [player["bowler"] + " - " + str(player["total"]) + " wks" for player in i2b]

    i1ba = Delivery.objects.filter(match_id=match, inning=1).values('batsman').annotate(
        total=Sum('batsman_runs')).values_list('batsman', 'total').order_by('-total')[:3]
    i2ba = Delivery.objects.filter(match_id=match, inning=2).values('batsman').annotate(
        total=Sum('batsman_runs')).values_list('batsman', 'total').order_by('-total')[:3]

    i1ba = [player[0] + " - " + str(player[1]) + " runs" for player in i1ba]
    i2ba = [player[0] + " - " + str(player[1]) + " runs" for player in i2ba]

    if (match.toss_winner == match.team1 and match.toss_decision == "field") or (
                    match.toss_winner == match.team1 and match.toss_decision == "field"):
        t1i1 = i1b  # team 1 innings 1
        t2i1 = i1ba  # team 2 innings 1

        t1i2 = i2ba  # team 1 innings 2
        t2i2 = i2b  # team 2 innings 2

    else:
        t1i1 = i1b  # team 1 innings 1
        t2i1 = i1ba  # team 2 innings 1

        t1i2 = i2ba  # team 1 innings 2
        t2i2 = i2b  # team 2 innings 2

    return render(
        request,
        template_name="ipl_app/match.html",
        context={
            "season": kwargs["season"],
            "match": match,
            "matchno": match.mid - start_match + 1,
            "deliveries1": deliveries1,
            "deliveries2": deliveries2,
            "t1i1": t1i1,
            "t1i2": t1i2,
            "t2i1": t2i1,
            "t2i2": t2i2,
            "t1logo": team_logo[match.team1],
            "t2logo": team_logo[match.team2],
        }
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        title = "Login"

        if request.user.is_authenticated:
            return redirect('home_html')

        return render(request,
                      template_name="ipl_app/login_form.html",
                      context={
                          'title': title,
                          'form': form,
                      })

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next = request.GET.get('next')
            if next:
                return HttpResponseRedirect(next)

            return redirect('home_html')
        else:
            messages.error(request, "Invalid Credentials")
            form = LoginForm(request.POST)

            title = "Login"
            return render(request,
                          template_name="ipl_app/login_form.html",
                          context={
                              'title': title,
                              'form': form,
                          })


def LogoutView(request):
    logout(request)
    return redirect('login')


def details_view(request, **kwargs):
    pass


def team_view(request, **kwargs):
    team = kwargs["team"]
    seasons = [i["season"] for i in Match.objects.filter(team1=team).values('season').distinct().order_by("-season")
               | Match.objects.filter(team2=team).values('season').distinct().order_by("-season")]
    details = {}
    for season in seasons:
        season_details = {}
        year_end = datetime.datetime(season, 12, 31)
        year_start = datetime.datetime(season - 1, 12, 31)
        end_match = Match.objects.filter(date__lte=year_end, date__gte=year_start).aggregate(Max('mid'))["mid__max"]
        team_end_match = max(
            Match.objects.filter(date__lte=year_end, date__gte=year_start, team1=team).aggregate(Max('mid'))[
                "mid__max"],
            Match.objects.filter(date__lte=year_end, date__gte=year_start, team2=team).aggregate(Max('mid'))["mid__max"]
        )
        caption = "Lost in Leagues"
        if end_match - team_end_match < 2:
            caption = "Playoffs"
            if end_match - team_end_match == 0:
                match = Match.objects.get(mid=end_match)
                if match.winner == team:
                    caption = "Champion"
                else:
                    caption = "Runner Up"

        matches = Match.objects.filter(season=season, team1=team) | Match.objects.filter(season=season, team2=team)
        matches = sorted(matches, key=lambda x: x.mid)

        details.update(
            {
                season: [
                    caption,
                    matches,
                ]
            })

    latest_season = Match.objects.aggregate(Max('season'))["season__max"]

    return render(request,
                  template_name="ipl_app/team.html",
                  context={
                      'title': team,
                      'logo': team_logo[team],
                      'team': team,
                      'seasons': seasons,
                      'latest_season': latest_season,
                      'details': details,
                  })


@login_required(login_url='login')
def admin_view(request, **kwargs):
    return render(request,
                  template_name="ipl_app/admin.html",
                  )

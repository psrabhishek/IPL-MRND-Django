# id	season	city	date	team1	team2	toss_winner	toss_decision	result	dl_applied	winner	win_by_runs	win_by_wickets	player_of_match	venue	umpire1	umpire2	umpire3

# match_id	inning	batting_team	bowling_team	over	ball	batsman	non_striker	bowler	is_super_over	wide_runs	bye_runs	legbye_runs	noball_runs	penalty_runs	batsman_runs	extra_runs	total_runs	player_dismissed	dismissal_kind	fielder

import openpyxl
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipl.settings")
django.setup()
from ipl_app.models import Match, Delivery

skip = True
wb = openpyxl.load_workbook("deliveries.xlsx")
ws = wb['deliveries']
for row in ws.rows:
    if skip:
        skip = False
        continue
    temp = [cell.value for cell in row]
    print(*temp)
    d = Delivery(
        match_id=Match.objects.get(mid=temp[0]),
        inning=temp[1],
        batting_team=temp[2],
        bowling_team=temp[3],
        over=temp[4],
        ball=temp[5],
        batsman=temp[6],
        non_striker=temp[7],
        bowler=temp[8],
        is_super_over=temp[9],
        wide_runs=temp[10],
        bye_runs=temp[11],
        legbye_runs=temp[12],
        noball_runs=temp[13],
        penalty_runs=temp[14],
        batsman_runs=temp[15],
        extra_runs=temp[16],
        total_runs=temp[17],
        player_dismissed=temp[18],
        dismissal_kind=temp[19],
        fielder=temp[20],
    )
    d.save()
    print(temp[0])

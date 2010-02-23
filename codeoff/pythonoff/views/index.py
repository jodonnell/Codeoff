from django.shortcuts import render_to_response
from django import http

from codeoff.pythonoff.models import ChallangeQueue, Goals, Problems, Challenge, PlayerChallenge

import datetime

# some threading issues, like if two users hit at the same time both could be in challenge queue and never talk
# two people could get the same challenger player id from challenge queue
def index(request):
    request.session['challenge_id'] = 0
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return http.HttpResponseRedirect('/accounts/login/')

    try:
        queued = ChallangeQueue.objects.get(player=request.user)
        queued.delete()
    except ChallangeQueue.DoesNotExist:
        pass

    # see if can find challenger
    challengers = ChallangeQueue.objects.order_by('-time')
    try:
        # TODO delete challenge queue entry
        challenger = challengers[0]

        goal = Goals.objects.all()[0]
        problem = Problems.objects.all()[0]
        challenge = Challenge.objects.create(goal=goal, problem=problem)
    
        player_challenge = PlayerChallenge(challenge=challenge, player=challenger.player, start_time=datetime.datetime.now(), new_challenge=True)
        player_challenge.save()
        player_challenge = PlayerChallenge(challenge=challenge, player=request.user, start_time=datetime.datetime.now(), new_challenge=False)
        player_challenge.save()
        
        request.session['challenge_id'] = challenge.id

        need_challenger = False

    except IndexError:
        # TODO if player already in queue, delete their old record
        ChallangeQueue.objects.create(player=request.user)
        need_challenger = True

    return render_to_response('index.html', {'username':username, 'need_challenger':need_challenger})

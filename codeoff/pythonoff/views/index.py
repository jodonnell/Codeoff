from django.shortcuts import render_to_response
from django import http

from codeoff.pythonoff.models import ChallangeQueue, Goals, Problems, Challenge, PlayerChallenge

import datetime


def delete_challenge_queue_entry(user):
    try:
        queued = ChallangeQueue.objects.get(player=user)
        queued.delete()
    except ChallangeQueue.DoesNotExist:
        pass


# some threading issues, like if two users hit at the same time both could be in challenge queue and never talk
# two people could get the same challenger player id from challenge queue
def index(request):
    template_vars = {}

    request.session['challenge_id'] = 0
    if request.user.is_authenticated():
        template_vars['username'] = request.user.username
    else:
        return http.HttpResponseRedirect('/accounts/login/')

    delete_challenge_queue_entry(request.user)


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

        template_vars['problem'] = challenge.problem.problem
        template_vars['goal'] = challenge.goal.goal
        template_vars['need_challenger'] = False

    except IndexError:
        # TODO if player already in queue, delete their old record
        ChallangeQueue.objects.create(player=request.user)
        template_vars['need_challenger'] = True

    return render_to_response('index.html', template_vars)

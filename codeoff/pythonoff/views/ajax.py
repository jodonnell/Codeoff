from django import http

from codeoff.pythonoff.models import PlayerChallenge, Challenge
from codeoff.pythonoff.classes.run_python import RunPython

import json
import StringIO
import sys

def update(request):
    # need to make sure they don't break out of HTML Area
    my_buffer = request.POST['my_buffer']
    challenge_id = request.session.get('challenge_id', None)
    challenge = Challenge.objects.get(pk = challenge_id)

    player_challenge = PlayerChallenge.objects.get(challenge=challenge, player=request.user)
    player_challenge.current_buffer = my_buffer
    player_challenge.save()

    not_current_user = PlayerChallenge.objects.filter(challenge=challenge).exclude(player=request.user)

    if not_current_user[0].current_buffer:
        challenger_buffer = not_current_user[0].current_buffer
    else:
        challenger_buffer = ''
    response = {'challenger_buffer': challenger_buffer}

    return http.HttpResponse(json.dumps(response))

def find_challenger(request):
    try:
        player_challenge = PlayerChallenge.objects.get(player=request.user, new_challenge=True)
        player_challenge.new_challenge = False
        player_challenge.save()
        request.session['challenge_id'] = player_challenge.challenge.id
        response = {'found_challenger':1, 'problem':player_challenge.challenge.problem.problem, 'goal':player_challenge.challenge.goal.goal}
    except PlayerChallenge.DoesNotExist:
        response = {'found_challenger':0}

    return http.HttpResponse(json.dumps(response))

def run_program(request):
    user_answer = request.POST['my_buffer']

    challenge_id = request.session.get('challenge_id', None)
    challenge = Challenge.objects.get(pk=challenge_id)
    rp = RunPython()
    success = rp.execute(challenge.problem, user_answer)

    if success:
        # TODO: race condition possible
        challenge.winner = request.user
        challenge.save()

    response = {'success':success, 'error':rp.error, 'output':rp.get_user_output_string()}
    return http.HttpResponse(json.dumps(response))

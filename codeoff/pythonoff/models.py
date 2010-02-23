from django.db import models
from django.contrib.auth.models import User

import random

SMALL_POSITIVE_INTS = 1
SMALL_POSITIVE_INT_MAX = 64

class Goals(models.Model):
    goal = models.CharField(max_length=1024)

class Problems(models.Model):
    problem = models.CharField(max_length=2048)
    answer = models.TextField()
    function_name = models.CharField(max_length=255)
    testing_range = models.IntegerField()

    def get_test_input(self):
        if self.testing_range == SMALL_POSITIVE_INTS:
            tests = [random.randint(1, SMALL_POSITIVE_INT_MAX) for x in range(5)]
            tests.append(0)
            return tests

    def cast_answer(self, inValue):
        if self.testing_range == SMALL_POSITIVE_INTS:
            return int(inValue)

class Challenge(models.Model):
    goal = models.ForeignKey(Goals)
    problem = models.ForeignKey(Problems)
    players = models.ManyToManyField(User, through='PlayerChallenge')

class CompileHistory(models.Model):
    compiled_code = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

class PlayerChallenge(models.Model):
    challenge = models.ForeignKey(Challenge)
    player = models.ForeignKey(User)
    compiles = models.ManyToManyField(CompileHistory)
    current_buffer = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    new_challenge = models.BooleanField()
#    last_update = models.DateTimeField() # make it so this gets polled and closed if opponent has closed page

class ChallangeQueue(models.Model):
    player = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

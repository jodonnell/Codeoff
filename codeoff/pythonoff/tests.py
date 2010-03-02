"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from codeoff.pythonoff.classes.run_python import RunPython
from codeoff.pythonoff.models import Problems

class RunPythonTest(TestCase):
    fixtures = ['test.json']
    def test_run_python(self):
        rp = RunPython()
        problem = Problems.objects.all()[0]
        success = rp.execute(problem, problem.answer)
        self.failUnlessEqual(success, True)

        success = rp.execute(problem, 'def fibonnaci(): return 0')
        self.failIfEqual(success, True)

import random
import traceback
import sys
import StringIO

allowed_builtins = {"__builtins__":{'int':int, 'str':str, 'range':range,
                                    'zip':zip, 'xrange':xrange, 'unicode':unicode, 'type':type, 'tuple':tuple,
                                    'sum':sum, 'slice':slice, 'round':round, 'repr':repr, 'reduce':reduce, 'pow':pow, 
                                    'float':float, 'filter':filter, 'enumerate':enumerate, 'dict':dict, 
                                    'bool':bool, 'abs':abs, 
                                    'AttributeError':AttributeError, 'ValueError':ValueError, 
                                    'ArithmeticError':ArithmeticError, 
                                    'AssertionError':AssertionError, 'TypeError':TypeError, 'None':None, 
                                    'ZeroDivisionError':ZeroDivisionError, 
                                    'UnicodeError':UnicodeError, 'True':True, 'False':False, }}

class RunPython(object):
    def __init__(self):
        self.inputs = []
        self.our_answers = []
        self.user_answers = []
        self.error = ''

    def _exec(self, answer, function_name, input):
        exec_string = answer + '\nprint %s(%s)' % (function_name, input)
        exec exec_string in allowed_builtins, {}

    def execute(self, problem, user_answer):
        success = True
        tb = ''

        test_data = problem.get_test_input()

        for input in test_data:
            self.inputs.append(input)
            try:
                codeOut = StringIO.StringIO()
                codeErr = StringIO.StringIO()
                sys.stdout = codeOut
                sys.stderr = codeErr

                problem.cast_answer( self._exec(user_answer, problem.function_name, input) )
                our_result = problem.cast_answer( self._exec(problem.answer, problem.function_name, input) )
                if user_result != our_result:
                    success = False

                self.our_answers.append(our_result)
                self.user_answers.append(user_result)
            except:
                success = False
                traceback.print_exc()
                self.error = codeErr.getvalue()
                break

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
                        

        return success
        

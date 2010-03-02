import random
import traceback
import sys
import StringIO

allowed_builtins = {"__builtins__":{'int':int, 'str':str, 'range':range, 'dir':dir,
                                    'zip':zip, 'xrange':xrange, 'unicode':unicode, 'type':type, 'tuple':tuple,
                                    'sum':sum, 'slice':slice, 'round':round, 'repr':repr, 'reduce':reduce, 'pow':pow, 
                                    'float':float, 'filter':filter, 'enumerate':enumerate, 'dict':dict, 
                                    'bool':bool, 'abs':abs, 
                                    'AttributeError':AttributeError, 'ValueError':ValueError, 
                                    'ArithmeticError':ArithmeticError, 
                                    'AssertionError':AssertionError, 'TypeError':TypeError, 'None':None, 
                                    'ZeroDivisionError':ZeroDivisionError, 
                                    'UnicodeError':UnicodeError, 'True':True, 'False':False, },
                    "result":''}

class RunPython(object):
    def __init__(self):
        self.inputs = []
        self.our_answers = []
        self.user_answers = []
        self.error = ''

    def _exec(self, answer, function_name, input):
        global result
        exec_string = answer + '\n'
        exec_string += 'global result; result = %s(%s);' % (function_name, input)
        exec exec_string in allowed_builtins, allowed_builtins
        return allowed_builtins['result']

    def get_user_output_string(self):
        output = []

        if len(self.inputs) == len(self.our_answers) == len(self.user_answers):
            for i in range(len(self.user_answers)):
                run = 'Run %i\n' % (i + 1)
                run += 'Input:%i\n' % self.inputs[i]
                run += 'Our answer:%s\n' % self.our_answers[i]
                run += 'Your answer:%s\n' % self.user_answers[i]
                output.append(run)
            
        return '\n'.join(output)

    def execute(self, problem, user_answer):
        success = True

        test_data = problem.get_test_input()
        for input in test_data:
            self.inputs.append(input)
            try:
                answer = self._exec(user_answer, problem.function_name, input)
                self.user_answers.append(answer)

                answer = self._exec(problem.answer, problem.function_name, input)
                self.our_answers.append(answer)

                if self.our_answers[-1] != self.user_answers[-1]:
                    success = False
                
            except:
                success = False
                codeErr = StringIO.StringIO()
                sys.stderr = codeErr
                traceback.print_exc()
                sys.stderr = sys.__stderr__
                self.error = codeErr.getvalue()
                break

        return success
        

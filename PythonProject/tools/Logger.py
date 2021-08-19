import sys


#class Logger:
def logger_log(log_string):
    # this_frame = sys._getframe()
    # this_line_no = this_frame.f_lineno
    # this_fcode = this_frame.f_code
    # this_name = this_fcode.co_name

    caller_frame = sys._getframe(1)
    caller_line_no = caller_frame.f_lineno
    caller_fcode = caller_frame.f_code
    caller_name = caller_fcode.co_name

    print(caller_name + " --- " + log_string);

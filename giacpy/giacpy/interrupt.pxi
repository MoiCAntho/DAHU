###########################################################################
#       Initialisation of the ctrl_c handler for giac                     #
#                                                                         #
#  Don't forget to include this file to let giac handle ctrl_c, or all    #
#  the session might be killed by a ctrl_c                                #
###########################################################################
#cdef extern from "signal.h"  namespace "std":
#    void signal "signal"(int sig, void (*func)(int))

from libc.signal cimport *

cdef extern from "giac/giac.h"  namespace "giac" nogil:
    void GIAC_ctrl_c_signal_handler "giac::ctrl_c_signal_handler"(int)
#    int SIGINT "SIGINT"


signal(SIGINT,GIAC_ctrl_c_signal_handler)

ressetctrl_c() #NB: I failed to do this with a cython variable. How to improve?

###########################################################################


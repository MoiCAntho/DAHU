#*****************************************************************************
#    AUTHOR:  Han Frederic <frederic.han@imj-prg.fr>
#  2012
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************




from libcpp.string cimport string

cdef extern from "giac/giac.h" namespace "giac":
    cdef cppclass context:
         context()         


    cdef cppclass gen:
         pass



cdef extern from "libqcas/giacpy.h":
     int QCAS_qcas "externalqcas"(gen &, context *) except +

cdef extern from "libqcas/giacpy.h":
     int QCAS_interactiveqcas "externalinteractiveqcas"(gen &, context *, string) except +


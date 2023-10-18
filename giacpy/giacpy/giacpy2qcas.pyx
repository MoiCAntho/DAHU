cimport giacpy2qcas




from giacpy cimport Pygen
from giacpy cimport context_ptr


cdef cqcas(Pygen g,s=None):



       if (s==None):
         try:
           QCAS_qcas((<Pygen>g).gptr[0],context_ptr)
           return
         except:
           raise RuntimeError
       else:
         try:
           QCAS_interactiveqcas((<Pygen>g).gptr[0],context_ptr,<string>s.encode())
           return
         except:
           raise RuntimeError



def toqcas(Pygen g,s=None):

        cqcas(g,s)


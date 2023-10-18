#*****************************************************************************
#    AUTHOR:  Han Frederic <frederic.han@imj-prg.fr>
#  2012
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
"""
giacpy: Interface to the C++ library giac (Computer Algebra System).


Giac is a general computer algebra system created by Bernard Parisse. It is used in Xcas.

Homepage http://www-fourier.ujf-grenoble.fr/~parisse/giac.html


The natural way to use giacpy is through the giac function. This function creates a Pygen object and evaluate it with the giac C++ library.

The initialisation of a Pygen just create an object in the C++ library giac, but the mathematical computation  is not done. This class is mainly usefull for cython users.


EXAMPLES::

    >>> from giacpy import giac
    >>> x,y,z=giac('x,y,z');  # define some basic giac objects
    >>> f=(x+3*y)/(x+z+1)**2 -(x+z+1)**2/(x+3*y)  # then we can compute
    >>> f.factor()
    (3*y-x**2-2*x*z-x-z**2-2*z-1)*(3*y+x**2+2*x*z+3*x+z**2+2*z+1)/((x+z+1)**2*(3*y+x))
    >>> f.normal()
    (-x**4-4*x**3*z-4*x**3-6*x**2*z**2-12*x**2*z-5*x**2+6*x*y-4*x*z**3-12*x*z**2-12*x*z-4*x+9*y**2-z**4-4*z**3-6*z**2-4*z-1)/(x**3+3*x**2*y+2*x**2*z+2*x**2+6*x*y*z+6*x*y+x*z**2+2*x*z+x+3*y*z**2+6*y*z+3*y)

. To obtain more hints on giacpy consider the help of the giac function.

    >>> help(giac)             # doctest: +SKIP

GETTING HELP::

#. To obtain some help on a giac keyword use the help() method. To open the more detailled (local) html documentation in an external browser, use:  htmlhelp()

    >>> from giacpy import *
    >>> gcd.help()              # doctest: +SKIP
    "Returns the greatest common divisor of 2 polynomials of several variables or of 2 integers or of 2 rationals.
    (Intg or Poly),(Intg or Poly)
    gcd(45,75);gcd(15/7,50/9);gcd(x^2-2*x+1,x^3-1);gcd(t^2-2*t+1,t^2+t-2);gcd((x^2-1)*(y^2-1)*z^2,x^3*y^3*z+(-(y^3))*z+x^3*z-z)
    lcm,euler,modgcd,ezgcd,psrgcd,heugcd,Gcd"
    >>> gcd.htmlhelp('fr')          # doctest: +SKIP

#. You can find full html documentation in several languages (en, fr, el) at:

   http://www-fourier.ujf-grenoble.fr/~parisse/giac/doc/en/cascmd_en/

   or you can try to open its local copy with the command:

    >>> from giacpy import htmlhelp
    >>> htmlhelp()        # doctest: +SKIP
    >>> htmlhelp('fr')    # doctest: +SKIP

#. You can import more giac/xcas keywords to work in a symbolic ring.

EXAMPLES::

    >>> from giacpy import *
    >>> x=giac('x');f=1/(2+sin(5*x))
    >>> f.int()
    2/5/sqrt(3)*(atan((-sqrt(3)*sin(5*x)+cos(5*x)+2*sin(5*x)+1)/(sqrt(3)*cos(5*x)+sqrt(3)-2*cos(5*x)+sin(5*x)+2))+5*x/2)
    >>> f.series(x,0,3)
    1/2-5/4*x+25/8*x**2-125/48*x**3+x**4*order_size(x)
    >>> (sqrt(5)+pi).approx(100)
    5.377660631089582934871817052010779119637787758986631545245841837718337331924013898042449233720899343

#. Cas Settings. Some convenient settings are obtained from: giacsettings:

    >>> from giacpy import giacsettings


#. Graphics 2D Output. If your version of giacpy has built giacpy2qcas, you can send graphics to qcas. For experimental interactive geometry see: help(qcas)

EXAMPLES::

    >>> from giacpy import *
    >>> C=giac('plot(x*sin(x)),x=-3*pi,3*pi')
    >>> C.qcas()             # doctest: +SKIP
    >>> l=[(C*t*0.1).color(t) for t in range(10)]
    >>> giac(l).qcas)        # doctest: +SKIP
    >>> A=randvector(200)
    >>> (histogram(classes(A,0,10))).qcas()         # doctest: +SKIP
    >>> C=giac('plot(sin(x)/x),x=-3*pi,3*pi')
    >>> C.qcas()             # doctest: +SKIP
    >>> l=[(C*t*0.1).color(t) for t in range(10)]
    >>> giac(l).qcas()       # doctest: +SKIP


"""
########################################################

cimport giacpy

from webbrowser import open as wwwbrowseropen
from sys import maxsize as Pymaxint
import os
import math

from time import sleep
from cpython.exc cimport PyErr_CheckSignals

#### Python3 compatibility  #############################
from sys import version_info as Pyversioninfo
if Pyversioninfo[0]>2 :
   PythonVersion3 = True
else:
   PythonVersion3 = False

def decstring23(s):
  if PythonVersion3 :
      return s.decode()
  else:
      return s


def encstring23(s):
  if PythonVersion3 :
      return bytes(s,'UTF-8')
  else:
      return s


if PythonVersion3:
    listrange=list,range
else:
    listrange=list

####End of Python3 compatibility########################

########################################################
#   Don't forget to include the    CTRL C settings     #
#   for giac, otherwise CTRL C might kill the session  #

include 'interrupt.pxi'
########################################################


########################################################
# A global context pointer. One by giac session.
########################################################
context_ptr=new context()
#
# Some global variables for optimisation
GIACNULL=Pygen('NULL')
#



# Create a giac setting instance
giacsettings=GiacSetting()


# remove lock to enable write access from giac
unsetsecure_run()


#######################################################
# The wrapper to eval with giac
#######################################################
def giac(s):
  """
    This function evaluate a python object with the giac library.

    * It creates in python a Pygen element and evaluate it with giac. For instance\
 to compute a trigonometric expansion of cos(x+2y) where x and y are just formal\
 symbols  we can do:

     >>> from giacpy import giac,pi
     >>> x,y=giac('x,y')
     >>> (x+2*y).cos().texpand()
     cos(x)*(2*cos(y)**2-1)-sin(x)*2*cos(y)*sin(y)


   Coercion, Pygen and internal giac variables:
   --------------------------------------------

   * The most usefull objects will be the Python object of type Pygen. In the following\
 example, we start by defining symbols x,y,z and do some formal computations

    >>> from giacpy import *
    >>> x,y,z=giac('x,y,z')
    >>> ((x+2*y/z)*(y+1)**2).diff(y)  # compute the partial derivative with respect to y
    2/z*(y+1)**2+(x+2*y/z)*2*(y+1)

    In the next example x was previously defined as a symbol so x[i] is just another symbol.\
 So we can use the symbols x[i] to work with polynomial in several variables as we do with the\
other symbols x,y,z.

    For instance to compute the coefficient of x[0]^12 in (x[0]+x[1]+x[2]+x[3]+x[4])^15/(y+z)\
 we just do the following
    >>> f=sum([x[i] for i in range(5)])**15/(y+z);f.coeff(x[0],12)
    (455*(x[1])**3+1365*(x[1])**2*x[2]+1365*(x[1])**2*x[3]+1365*(x[1])**2*x[4]+1365*x[1]*(x[2])**2+2730*x[1]*x[2]*x[3]+2730*x[1]*x[2]*x[4]+1365*x[1]*(x[3])**2+2730*x[1]*x[3]*x[4]+1365*x[1]*(x[4])**2+455*(x[2])**3+1365*(x[2])**2*x[3]+1365*(x[2])**2*x[4]+1365*x[2]*(x[3])**2+2730*x[2]*x[3]*x[4]+1365*x[2]*(x[4])**2+455*(x[3])**3+1365*(x[3])**2*x[4]+1365*x[3]*(x[4])**2+455*(x[4])**3)/(y+z)

      Warning: The complex number sqrt(-1) is exported in python as I. (But it may appears as i)

    >>> ((1+I*sqrt(3))**3).normal(); 1+I
    -8
    1+i

   * Python integers and reals can be directly converted to giac.

    >>> a=giac(2**1024);a.nextprime();(giac(1.234567)).erf().approx(10)
    179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137859
    0.9191788641


   * There are some natural coercion to Pygen elements:

    >>> pi>3.14 ; pi >3.15 ; giac(3)==3
    True
    False
    True

   But sometimes you need to prevent Python from doing a computation before the conversion. For example\
 if 1/3 is done in Python2 you will obtain 0 while in Python3 0.33333 so to create: x+1/3:
   >>> x+'1/3'
   x+1/3
   >>> x+giac(1)/3
   x+1/3

   while to create x/(1+x) or x+x/3 you don't need quotes because at each step one of the two object is a Pygen.
   >>> x/(1+x)
   x/(1+x)
   >>> (x+x/3).factor()
   4*x/3


   * The Python object y defined above is of type Pygen. It is not an internal giac variable. (Most of the time you won't need to use internal giac variables).

    >>> yyyy=2;giac('yyyy:=1');yyyy
    1
    2


   Linear Algebra:
   ---------------

   * In Giac/Xcas vectors are just lists and matrices are lists of list.

    >>> x,y=giac('x,y')
    >>> A=giac([[1,2],[3,4]])  # we create a giac matrix from it lines
    >>> v=giac([x,y]); v   # a giac vector
    [x,y]
    >>> A*v # matrix product with a vector outputs a vector
    [x+2*y,3*x+4*y]
    >>> v*v  # dot product
    x*x+y*y

    Remark that w=giac([[x],[y]]) is a matrix of 1 column and 2 rows. It is not a vector\
    so w*w doesn't make sense.
    >>> w=giac([[x],[y]])
    >>> w.transpose()*w   # this matrix product makes sense and output a 1x1 matrix.
    matrix[[x*x+y*y]]

   * In Python affectation doesn't create a new matrix. (cf. pointers) see also \
 the doc of  'giacpy.Pygen.__setitem__'

    >>> B1=A;
    >>> B1[0,0]=43; B1 # in place affectation changes both B1 and A
    [[43,2],[3,4]]
    >>> A
    [[43,2],[3,4]]
    >>> A[0][0]=A[0][0]+1; A  # similar as A[0,0]=A[0,0]+1
    [[44,2],[3,4]]
    >>> A.pcar(x)  # compute the characteristic polynomial of A
    x**2-48*x+170
    >>> B2=A.copy() # use copy to create another object
    >>> B2[0,0]=55; B2  # here A is not modified
    [[55,2],[3,4]]
    >>> A
    [[44,2],[3,4]]



   * Sparse Matrices are avaible via the table function.
    >>> import giacpy
    >>> A=giacpy.table(()); A  # create an empty giac table
    table(
    )
    >>> A[2,3]=33; A[0,2]='2/7' # set non zero entries of the sparse matrix
    >>> A*A  # basic matrix operation are supported with sparse matrices
    table(
    (0,3) = 66/7
    )
    >>> D=giacpy.diag([22,3,'1/7']); D  # some diagonal matrix
    [[22,0,0],[0,3,0],[0,0,1/7]]
    >>> giacpy.table(D)    # to create a sparse matrix from an ordinary one
    table(
    (0,0) = 22,
    (1,1) = 3,
    (2,2) = 1/7
    )


     But many matrix functions apply only with ordinary matrices so need conversions

    >>> B1=A.matrix(); B1 # convert the sparse matrix to a matrix, but the size is minimal
    [[0,0,2/7,0],[0,0,0,0],[0,0,0,33]]
    >>> B2=B1.redim(4,4); B2.pmin(x)  # so we may need to resize B1
    x**3


   Lists of Pygen and Giac lists:
   ------------------------------

   * Here l1 is a giac list and l2 is a python list of Pygen type objects.

    >>> l1=giac(range(10)); l2=[1/(i**2+1) for i in l1]
    >>> sum(l2)
    33054527/16762850

    So l1+l1 is done in giac and means a vector addition. But l2+l2 is done in Python so it is the list concatenation.

    >>> l1+l1
    [0,2,4,6,8,10,12,14,16,18]

    >>> l2+l2
    [1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82, 1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82]


   * Here V is not a Pygen element. We need to push it to giac to use a giac method like dim, or we need to use an imported function.

    >>> V=[ [x[i]**j for i in range(8)] for j in range(8)]

    >>> giac(V).dim()
    [8,8]

    >>> dt=det_minor(V).factor(); dt.nops()  # 28 factors
    28

    >>> sort(list(dt.op()))
    [x[1]-(x[2]),x[1]-(x[3]),x[1]-(x[4]),x[1]-(x[5]),x[1]-(x[6]),x[1]-(x[7]),x[2]-(x[3]),x[2]-(x[4]),x[2]-(x[5]),x[2]-(x[6]),x[2]-(x[7]),x[3]-(x[4]),x[3]-(x[5]),x[3]-(x[6]),x[3]-(x[7]),x[4]-(x[5]),x[4]-(x[6]),x[4]-(x[7]),x[5]-(x[6]),x[5]-(x[7]),x[6]-(x[7]),x[0]-(x[1]),x[0]-(x[2]),x[0]-(x[3]),x[0]-(x[4]),x[0]-(x[5]),x[0]-(x[6]),x[0]-(x[7])]


   * Modular objects with %

    >>> V=ranm(5,6) % 2;

    >>> ker(V).rowdim()+V.rank()
    6

    >>> a=giac(7)%3;a;a%0;7%3
    1 % 3
    1
    1

   Do not confuse with the  python integers:

    >>> type(7%3)==type(a);type(a)==type(7%3)
    False
    False

   Syntaxes with reserved or unknown Python symbols:
   -------------------------------------------------

   * In general equations needs symbols such as = < > or that have another meaning in Python. So those objects must be quoted.

 ::

    >>> from giacpy import *

    >>> x=giac('x')

    >>> (1+2*sin(3*x)).solve(x).simplify()
    list[-pi/18,7*pi/18]

    >>> solve('sin(3*x)>2*sin(x)',x)
    "Unable to find numeric values solving equation. For trigonometric equations this may be solved using assumptions, e.g. assume(x>-pi && x<pi) Error: Bad Argument Value"


   * You can also add some hypothesis to a giac symbol:

    >>> assume('x>-pi && x<pi')
    x
    >>> solve('sin(3*x)>2*sin(x)',x)
    list[((x>(-5*pi/6)) and (x<(-pi/6))),((x>0) and (x<(pi/6))),((x>(5*pi/6)) and (x<pi))]

   * To remove those hypothesis use the giac function: purge

    >>> purge('x')
    assume[[],[line[-pi,pi]],[-pi,pi]]
    >>> solve('x>0')
    list[x>0]

 ::

   * Same problems with the ..

    >>> from giacpy import *

    >>> x=giac('x')

    >>> f=1/(5+cos(4*x));f.int(x)
    1/2/(2*sqrt(6))*(atan((-sqrt(6)*sin(4*x)+2*sin(4*x))/(sqrt(6)*cos(4*x)+sqrt(6)-2*cos(4*x)+2))+4*x/2)
    >>> fMax(f,'x=-0..pi').simplify()
    pi/4,3*pi/4
    >>> fMax.help()    # doctest: +SKIP
    "Returns the abscissa of the maximum of the expression.
    Expr,[Var]
    fMax(-x^2+2*x+1,x)
    fMin"
    >>> sum(1/(1+x**2),'x=0..infinity').simplify()
    (pi*exp(pi)**2+pi+exp(pi)**2-1)/(2*exp(pi)**2-2)


   MEMENTO of usual GIAC functions:
   ===============================

   * Expand with simplification

         - ``ratnormal``, ``normal``, ``simplify``   (from the fastest to the most sophisticated)

         -  NB: ``expand`` function doesn't regroup nor cancel terms, so it could be slow. (pedagogical purpose only?)

   * Factor/Regroup

         - ``factor``, ``factors``, ``regroup``, ``cfactor``, ``ifactor``

   * Misc

         - ``unapply``, ``op``, ``subst``

   * Polynomials/Fractions

         - ``coeff``,  ``gbasis``, ``greduce``, ``lcoeff``, ``pcoeff``, ``canonical_form``,

         - ``proot``,  ``poly2symb``,  ``symb2poly``, ``posubLMQ``, ``poslbdLMQ``, ``VAS``, ``tcoeff``,  ``valuation``

         - ``gcd``, ``egcd``, ``lcm``, ``quo``, ``rem``, ``quorem``, ``abcuv``, ``chinrem``,

         - ``peval``, ``horner``, ``lagrange``, ``ptayl``, ``spline``,  ``sturm``,  ``sturmab``

         - ``partfrac``, ``cpartfrac``

   * Memory/Variables

         * ``assume``, ``about``, ``purge``, ``ans``

   * Calculus/Exact

         - ``linsolve``,  ``solve``,  ``csolve``,  ``desolve``,  ``seqsolve``, ``reverse_rsolve``, ``matpow``

         - ``limit``, ``series``, ``sum``, ``diff``, ``fMax``, ``fMin``,

         - ``integrate``, ``subst``, ``ibpdv``, ``ibpu``, ``preval``

   * Calculus/Exp, Log, powers

         - ``exp2pow``, ``hyp2exp``, ``expexpand``, ``lin``, ``lncollect``, ``lnexpand``, ``powexpand``, ``pow2exp``

   * Trigo

         - ``trigexpand``, ``tsimplify``, ``tlin``, ``tcollect``,

         - ``halftan``, ``cos2sintan``, ``sin2costan``, ``tan2sincos``, ``tan2cossin2``, ``tan2sincos2``, ``trigcos``, ``trigsin``, ``trigtan``, ``shift_phase``

         - ``exp2trig``, ``trig2exp``

         - ``atrig2ln``, ``acos2asin``, ``acos2atan``, ``asin2acos``, ``asin2atan``, ``atan2acos``, ``atan2asin``

   * Linear Algebra

         - ``identity``, ``matrix``, ``makemat``, ``syst2mat``, ``matpow``, ``table``,  ``redim``

         - ``det``,  ``det_minor``, ``rank``, ``ker``, ``image``, ``rref``, ``simplex_reduce``,

         - ``egv``, ``egvl``,  ``eigenvalues``, ``pcar``, ``pcar_hessenberg``, ``pmin``,

         - ``jordan``, ``adjoint_matrix``, ``companion``, ``hessenberg``, ``transpose``,

         - ``cholesky``, ``lll``,  ``lu``, ``qr``, ``svd``, ``a2q``, ``gauss``, ``gramschmidt``,
           ``q2a``, ``isom``, ``mkisom``


   * Finite Fieds

         - ``%``, ``% 0``, ``mod``, ``GF``, ``powmod``


   * Integers

         - ``gcd``, ``iabcuv``, ``ichinrem``, ``idivis``, ``iegcd``,

         - ``ifactor``, ``ifactors``, ``iquo``, ``iquorem``, ``irem``,

         - ``is_prime, is_pseudoprime``, ``lcm``, ``mod``, ``nextprime``, ``pa2b2``, ``prevprime``,
           ``smod``, ``euler``, ``fracmod``

   * List

         - ``append``, ``accumulate_head_tail``, ``concat``, ``head``, ``makelist``, ``member``, ``mid``, ``revlist``, ``rotate``, ``shift``, ``size``, ``sizes``, ``sort``, ``suppress``, ``tail``

   * Set

         - ``intersect``, ``minus``, ``union``, ``is_element``, ``is_included``


  """
  return Pygen(s).threadeval()


#######################################
# A class to adjust giac configuration
#######################################
cdef class GiacSetting(Pygen):
     """
     A class to customise the Computer Algebra  System settings

     * property threads:

         Maximal number of allowed theads in giac

     * property digits:

         Default digits number used for approximations:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.digits=20;giacsettings.digits
             20
             >>> giac('1/7').approx()
             0.14285714285714285714
             >>> giacsettings.digits=12;

     * property sqrtflag:

         Flag to allow sqrt extractions during solve and factorizations:

         ::

             >>> from giacpy import giac,giacsettings
             >>> giacsettings.sqrtflag=False;giacsettings.sqrtflag
             False
             >>> giac('x**2-2').factor()
             x**2-2
             >>> giacsettings.sqrtflag=True;
             >>> giac('x**2-2').factor()
             (x-sqrt(2))*(x+sqrt(2))

     * property complexflag:

         Flag to allow complex number in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.complexflag=False;giacsettings.complexflag
            False
            >>> giac('x**2+4').factor()
            x**2+4
            >>> giacsettings.complexflag=True;
            >>> giac('x**2+4').factor()
            (x+2*i)*(x-2*i)


     * property eval_level:

         Recursive level of substitution of variables during an evaluation:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.eval_level=1
             >>> giac("purge(a):;b:=a;a:=1;b")
             "Done",a,1,a
             >>> giacsettings.eval_level=25; giacsettings.eval_level
             25
             >>> giac("purge(a):;b:=a;a:=1;b")
             "Done",a,1,1

     * property proba_epsilon:

         Maximum probability of a wrong answer with a probabilist algorithm.
         Set this number to 0 to disable probabilist algorithms (slower):

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.proba_epsilon=0;giac('proba_epsilon')
             0.0
             >>> giacsettings.proba_epsilon=10^(-13)
             >>> giac('proba_epsilon')<10^(-14)
             False

     * property epsilon:

         Value used by the epsilon2zero function:

         ::

             >>> from giacpy import giacsettings,giac
             >>> giacsettings.epsilon=1e-10
             >>> x=giac('x')
             >>> P=giac('1e-11+x+5')
             >>> P==x+5
             False
             >>> (P.epsilon2zero()).simplify()
             x+5

     """

     def __repr__(self):
       return "Giac Settings"


     property digits:
         r"""
         Default digits number used for approximations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.digits=20;giacsettings.digits
            20
            >>> giac('1/7').approx()
            0.14285714285714285714
            >>> giacsettings.digits=12;

         """
         def __get__(self):
           return (self.cas_setup()[6])._val


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[6]=value
           Pygen('cas_setup(%s)'%(pl)).eval()


     property sqrtflag:
         r"""
         Flag to allow square roots in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.sqrtflag=False;giacsettings.sqrtflag
            False
            >>> giac('x**2-2').factor()
            x**2-2
            >>> giacsettings.sqrtflag=True;
            >>> giac('x**2-2').factor()
            (x-sqrt(2))*(x+sqrt(2))

         """
         def __get__(self):
           return (self.cas_setup()[9])._val == 1


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           if value:
              pl[9]=1
           else:
              pl[9]=0
           Pygen('cas_setup(%s)'%(pl)).eval()


     property complexflag:
         r"""
         Flag to allow complex number in solving equations or factorizations:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.complexflag=False;giacsettings.complexflag
            False
            >>> giac('x**2+4').factor()
            x**2+4
            >>> giacsettings.complexflag=True;
            >>> giac('x**2+4').factor()
            (x+2*i)*(x-2*i)

         """
         def __get__(self):
           return (self.cas_setup()[2])._val == 1


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           if value:
              pl[2]=1
           else:
              pl[2]=0
           Pygen('cas_setup(%s)'%(pl)).eval()


     property eval_level:
         """
         Recursive level of substitution of variables during an evaluation:

            >>> from giacpy import giacsettings,purge
            >>> giacsettings.eval_level=1
            >>> giac("purge(a):;b:=a;a:=1;b")
            "Done",a,1,a
            >>> giacsettings.eval_level=25; giacsettings.eval_level
            25
            >>> giac("purge(a):;b:=a;a:=1;b")
            "Done",a,1,1

         """
         def __get__(self):
           return (self.cas_setup()[7][3])._val


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[7]=[l[7][0],l[7][1],l[7][2],value]
           Pygen('cas_setup(%s)'%(pl)).eval()



     property proba_epsilon:
         """
         Maximum probability of a wrong answer with a probabilist algorithm.
         Set this number to 0 to disable probabilist algorithms (slower):

            >>> from giacpy import giacsettings,giac
            >>> giacsettings.proba_epsilon=0;giac('proba_epsilon')
            0.0
            >>> giacsettings.proba_epsilon=10**(-15);giac('proba_epsilon')=='1e-15'
            True

         """
         def __get__(self):
           return (self.cas_setup()[5][1])._double


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[5]=[l[5][0],value]
           Pygen('cas_setup(%s)'%(pl)).eval()


     property epsilon:
         r"""
         Value used by the epsilon2zero function:

         ::

            >>> from giacpy import giac,giacsettings
            >>> giacsettings.epsilon=1e-10
            >>> P=giac('1e-11+x+5')
            >>> P==x+5
            False
            >>> (P.epsilon2zero()).simplify()
            x+5

         """
         def __get__(self):
           return (self.cas_setup()[5][0])._double


         def __set__(self,value):
           l=Pygen('cas_setup()').eval()
           pl=[ i for i in l ]
           pl[5]=[value,l[5][1]]
           Pygen('cas_setup(%s)'%(pl)).eval()

     property threads:
         """
         Maximal number of allowed theads in giac
         """
         def __get__(self):
           return (self.cas_setup()[7][0])._val

         def __set__(self,value):
           Pygen('threads:=%s'%(str(value))).eval()



########################################################
#                                                      #
#    The python class that points to a cpp giac gen    #
#                                                      #
########################################################
include 'auto-methods.pxi'

cdef class Pygen(GiacMethods_base):
     """
     The class Pygen is the main tool to interact from python/sage with the c++
     library giac via cython.  The initialisation of a Pygen just create an object
     in giac, but the mathematical computation  is not done. This class is mainly
     for cython users.  Here A is a Pygen element, and it is ready for any giac
     function.::

     >>> from giacpy import Pygen
     >>> A = Pygen('2+2')
     >>> A
     2+2
     >>> A.eval()
     4

     In general, you may prefer to directly create a Pygen and execute the
     evaluation in giac. This is exactly the meaning of the :func:`libgiac`
     function.::

     >>> a = giac('2+2')
     >>> a
     4
     >>> isinstance(a, Pygen)
     True

     """

     def __cinit__(self, s=None):

         #NB: the  != here gives problems with  the __richcmp__ function
         #if (s!=None):
         # so it's better to use isinstance
         if (isinstance(s,None.__class__)):
             # Do NOT replace with: self=GIACNULL  (cf the doctest in __repr__
             self.gptr = new gen ((<Pygen>GIACNULL).gptr[0])
             return

         if isinstance(s,int):       # This looks 100 faster than the str initialisation
           if PythonVersion3:
             #in python3 int and long are int
             if s.bit_length()< Pymaxint.bit_length():
                self.gptr = new gen(<long long>s)
             else:
                self.gptr = new gen(pylongtogen(s))
           else:
                self.gptr = new gen(<long long>s)

         #
         # Warning: the conversion to double is faster than strings but some Digits look lost?
         # not so much as it first look : giac(1/7.0)._double -1/7.0

         elif isinstance(s,float):
             self.gptr = new gen(<double>s)
         #

         elif isinstance(s,long):
             #s=str(s)
             #self.gptr = new gen(<string>s,context_ptr)
             self.gptr = new gen(pylongtogen(s))


         elif isinstance(s,Pygen):
             #in the test: x,y=Pygen('x,y');((x+2*y).sin()).texpand()
             # the y are lost without this case.
             self.gptr = new gen((<Pygen>s).gptr[0])


         elif isinstance(s,listrange):
             self.gptr = new gen(_wrap_pylist(<list>s),<short int>0)

         elif isinstance(s,tuple):
             self.gptr = new gen(_wrap_pylist(<tuple>s),<short int>1)

         # Other types are converted with strings.
         else:
           if not(isinstance(s,str)):  #modif python3
             s=s.__str__()
             #s=s.__repr__()   # with big gen repr is intercepted
           #self.gptr = new gen(<string>s,context_ptr)
           self.gptr = new gen(<string>encstring23(s),context_ptr)


     def __dealloc__(self):
         del self.gptr


     def __repr__(self):
        """
         >>> vide=Pygen()
         >>> "giac version dpt: either NULL or seq[]", vide    # doctest: +ELLIPSIS
         ('giac version dpt: either NULL or seq[]', ...)

        """
        #if self.gptr == NULL:
        #  return ''
        try:
          # fast evaluation of the complexity of the gen. (it's not the number of char )
          t=GIAC_taille(self.gptr[0], 6000)
        except:
          raise RuntimeError
        if (t<6000) :
           return decstring23(GIAC_print(self.gptr[0], context_ptr).c_str()) #python3
        else:
          return str(self.type)+"\nResult is too big for Display. If you really want to see it use print"

     def __str__(self):
        #if self.gptr == NULL:
        #  return ''
        return decstring23(GIAC_print(self.gptr[0], context_ptr).c_str()) #python3

     def __len__(self):
       #if (self.gptr != NULL):
         try:
           rep=GIAC_size(self.gptr[0],context_ptr).val
           #GIAC_size return a gen. we take the int: val
           return rep
         except:
           raise RuntimeError
       #else:
       #  raise MemoryError,"This Pygen is not associated to a giac gen"


     def __getitem__(self,i):  #TODO?: add gen support for indexes
        """
         Lists of 10**6 integers should be translated to giac easily

           >>> l=giac(list(range(10**6)));l[5]   #python3
           5
           >>> l[35:50:7]
           [35,42,49]
           >>> t=giac(tuple(range(10)))
           >>> t[:4:-1]
           9,8,7,6,5
           >>> x=giac('x'); sum([ x[i] for i in range(5)])**3
           (x[0]+x[1]+x[2]+x[3]+x[4])**3
           >>> import giacpy
           >>> A=giacpy.ranm(5,10); A[3,7]-A[3][7]
           0
           >>> A.transpose()[8,2]-A[2][8]
           0
           >>> A=giac('[ranm(5,5),ranm(5,5)]')
           >>> A[1,2,3]-A[1][2][3]
           0

        Crash test:

           >>> l=Pygen()
           >>> l[0]      # doctest: +SKIP
           Traceback (most recent call last):
           ...
           RuntimeError

        """
        cdef gen result

        if(self._type == 7) or (self._type == 12):   #if self is a list or a string
          if isinstance(i,int):
            n=len(self)
            if(i<n)and(-i<n):
                if(i<0):
                  i=i+n
                try:
                  result=self.gptr[0][<int>i]
                  return _wrap_gen(result)
                except:
                  raise RuntimeError
            else:
                raise IndexError,'list index %s out of range'%(i)
          else:
            if isinstance(i,slice):
              result=gen(_getgiacslice(self,i),<short int>self._subtype)
              return _wrap_gen(result)

            # add support for multi indexes
            elif isinstance(i,tuple):
               if(len(i)==2):
                  return self[i[0]][i[1]]
               elif(len(i)==1):
                  # in case of a tuple like this: (3,)
                  return self[i[0]]
               else:
                  return self[i[0],i[1]][tuple(i[2:])]

            else:
              raise TypeError,'gen indexes are not yet implemented'
        # Here we add support to formal variable indexes:
        else:
          cmd='%s[%s]'%(self,i)
          ans=Pygen(cmd).eval()
          # if the answer is a string, it must be an error message because self is not a list or a string
          if (ans._type == 12):
            raise TypeError, "Error executing code in Giac\nCODE:\n\t%s\nGiac ERROR:\n\t%s"%(cmd, ans)
          return ans


     def __setitem__(self,key,value):
        """
        Set the value of a coefficient of a giac vector or matrix or list.
           Warning: It is an in place affectation.


        >>> A=giac([ [ j+2*i for i in range(3)] for j in range(3)]); A
        [[0,2,4],[1,3,5],[2,4,6]]
        >>> A[1,2]=44;A
        [[0,2,4],[1,3,44],[2,4,6]]
        >>> A[2][2]=giac(1)/3;A
        [[0,2,4],[1,3,44],[2,4,1/3]]
        >>> x=giac('x')
        >>> A[0,0]=x+1/x; A
        [[x+1/x,2,4],[1,3,44],[2,4,1/3]]
        >>> A[0]=[-1,-2,-3]; A
        [[-1,-2,-3],[1,3,44],[2,4,1/3]]
        >>> B=A; A[2,2]
        1/3
        >>> B[2,2]=6    # in place affectation
        >>> A[2,2]      # so A is also modified
        6
        >>> A.pcar(x)
        x**3-8*x**2-159*x


        NB: For Large matrix it seems that the syntax A[i][j]= is faster that A[i,j]=

        >>> import giacpy
        >>> from time import time
        >>> A=giacpy.ranm(4000,4000)
        >>> t1=time(); A[500][500]=12345;t1=time()-t1
        >>> t2=time(); A[501,501]=54321;t2=time()-t2
        >>> t1,t2 # doctest: +SKIP
        (0.0002014636993408203, 0.05124521255493164)
        >>> A[500,500],A[501][501]
        (12345, 54321)

        """
        cdef gen v
        cdef gen g = gen(<string>encstring23('GIACPY_TMP_NAME050268070969290100291003'),context_ptr)
        GIAC_sto((<Pygen>self).gptr[0],g,1,context_ptr)
        g=gen(<string>encstring23('GIACPY_TMP_NAME050268070969290100291003[%s]'%(str(key))),context_ptr)
        v=(<Pygen>(Pygen(value).eval())).gptr[0]
        GIAC_sto(v,g,1,context_ptr)
        Pygen('purge(GIACPY_TMP_NAME050268070969290100291003):;').eval()
        return


     def __iter__(self):
       """
         Pygen lists of 10**6 elements should be yield

           >>> from time import time
           >>> l=giac(range(10**6))
           >>> t=time();l1=[ i for i in l ];t1=time()-t;'time for a list of 10**6  i ',t1        # doctest: +ELLIPSIS
           ('time for a list of 10**6  i ', ...)
           >>> t=time();l1=[ i+i for i in l ];t2=time()-t;'time for a list of 10**6  i+i ',t2    # doctest: +ELLIPSIS
           ('time for a list of 10**6  i+i ', ...)
           >>> t=time();l1=[ 1+i for i in l ];t3=time()-t;"time for a list of 10**6  1+i ",t3    # doctest: +ELLIPSIS
           ('time for a list of 10**6  1+i ', ...)
           >>> t=time();l1=[ i+1 for i in l ];t4=time()-t;"time for a list of 10**6  i+1 ",t4    # doctest: +ELLIPSIS
           ('time for a list of 10**6  i+1 ', ...)

       """
       cdef int i
       #FIXME, should be improved: is it slow? and needs sig_on()?
       ressetctrl_c()
       for i in range(len(self)):
          if(GIACctrl_c):
            raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
          yield self[i]

     def __int__(self):
        """
          Convert a giac integer (type Pygen in python) to  a Python <int>

            >>> a=giac('2*pi')
            >>> list(range((a.floor()).__int__()))
            [0, 1, 2, 3, 4, 5]

        """
        tmp=self.eval()
        if(tmp._type==0):
           # C int
           return tmp._val
        elif(tmp._type==2):
           # gmp int
           return int(str(tmp))
        else:
           raise TypeError,"self is not a giac integer"

     def __float__(self):
        """
           Convert a giac real to a Python <float>

             >>> a=giac('pi/4.0')
             >>> import math
             >>> math.sin(a)    # doctest: +ELLIPSIS
             0.70710678118654...
             >>> a=giac(2)
             >>> math.sqrt(a) == math.sqrt(2)
             True

        """
        # round with 14 digits should give type 1
        # but if it depends on the arch we add the type 3 test
        tmp=self.round(14).eval()
        if(tmp._type==1):
           return tmp._double
        elif(tmp._type==3):
           return float(str(tmp))
        else:
           raise TypeError,"self is not a giac real"

     def eval(self):
        cdef gen result
        ressetctrl_c()
        try:
           result=GIAC_protecteval(self.gptr[0],giacsettings.eval_level,context_ptr)
           return _wrap_gen(result)
        except:
           raise RuntimeError

     def threadeval(self,*args):
        cdef gen result
        cdef gen * param
        param=&result

        count=0
        maxcount=1000000

        n=len(args)
        if (n>1):
           right=Pygen(args).eval()
        elif (n==1):
           right=Pygen(args[0])
#        if isinstance(self,Pygen)==False:
#           self=Pygen(self)

        ressetctrl_c()

        try:
           if(n>0):
              condi=CASmakethread(GIAC_symbof((<Pygen>self).gptr[0],(<Pygen>right).gptr[0]),giacsettings.eval_level,param,context_ptr)
           else:
              condi=CASmakethread((<Pygen>self).gptr[0],giacsettings.eval_level,param,context_ptr)
           if( condi == 1):
              cont=True

              while(cont):
                   if(CASmonitor(context_ptr) == 1):
                      if(count <maxcount):
                         count=count+1

                      PyErr_CheckSignals()
                      if(testctrl_c()==1):
                         sleep(2) # try to wait if the thread stops alone
                         cont=False
                         if(CASmonitor(context_ptr) == 1):
                            print("killing thread")
                            CASkillthread(context_ptr)
                            raise KeyboardInterrupt

                      if(count >= maxcount):
                         sleep(0.05)
                      if(count >= maxcount//100):
                         sleep(0.001)
                   else:
                      cont=False

              result=param[0]
              return _wrap_gen(result)


           else:
              raise RuntimeError,"Failed to start a thread"
        except:
           setctrl_c()
           print("trying soft interruption (wait 2s)")
           sleep(2)
           print("cas monitor status:",CASmonitor(context_ptr))
           if(CASmonitor(context_ptr) == 1):
              print("warning: Killing thread")
              CASkillthread(context_ptr)
              sleep(2)
              print("cas monitor status after killing thread:",CASmonitor(context_ptr))
           raise RuntimeError


     def __add__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         # Curiously this case is important:
         # otherwise: f=1/(2+sin(5*x)) crash
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>self).gptr[0] + (<Pygen>right).gptr[0]
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __radd__(self, right):
         """
            Reverse operator

                >>> d=giac('d')
                >>> 1+d   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                1+d

         """
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         # Curiously this case is important:
         # otherwise: f=1/(2+sin(5*x)) crash
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>right).gptr[0] + (<Pygen>self).gptr[0] 
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __call__(self, *args):
         cdef gen result
         n=len(args)
         if (n>1):
           right=Pygen(args).eval()
         elif (n==1):
           right=Pygen(args[0])
         else:
           right=GIACNULL
         if isinstance(self,Pygen)==False:
           self=Pygen(self)
         ressetctrl_c()
         #try:
         result= ((<Pygen>self).gptr[0])((<Pygen>right).gptr[0],context_ptr)
         return _wrap_gen(result)
         #except:
         #   raise RuntimeError


     def __sub__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>self).gptr[0] - (<Pygen>right).gptr[0]
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __rsub__(self, right):
         """
            Reverse operator

                >>> d=giac('d')
                >>> 2-d   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                2-d

         """
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= (<Pygen>right).gptr[0] - (<Pygen>self).gptr[0]
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __mul__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] * (<Pygen>right).gptr[0]
             #NB: with the natural previous method, the following error generated by
             #giac causes python to quit instead of an error message.
             #l=Pygen([1,2]);l.transpose()*l;
             result= GIAC_giacmul((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __rmul__(self, right):
         """
            Reverse operator

                >>> d=giac('d')
                >>> 7*d   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                7*d

         """
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_giacmul((<Pygen>right).gptr[0] , (<Pygen>self).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

#PB / in python3 is truediv
     def __div__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] / (<Pygen>right).gptr[0]
             result= GIAC_giacdiv((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0], context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __truediv__(self, right):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= (<Pygen>self).gptr[0] / (<Pygen>right).gptr[0]
             result= GIAC_giacdiv((<Pygen>self).gptr[0] , (<Pygen>right).gptr[0], context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __rtruediv__(self, right):
         """
            Reverse operator

                >>> d=giac('d')
                >>> 7/d   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                7/d

         """
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_giacdiv((<Pygen>right).gptr[0] , (<Pygen>self).gptr[0], context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError


     def __pow__(self, right ,ignored):
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_pow((<Pygen>self).gptr[0],(<Pygen>right).gptr[0], context_ptr )
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __rpow__(self, right ,ignored):
         """
            Reverse operator

                >>> d=giac('d')
                >>> (7**d)   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                7**d

         """
         cdef gen result
         if isinstance(right,Pygen)==False:
            right=Pygen(right)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_pow((<Pygen>right).gptr[0],(<Pygen>self).gptr[0], context_ptr )
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __mod__(self, right):
         cdef gen result
         if not isinstance(right,Pygen):
            right=Pygen(right)
         if not isinstance(self,Pygen):
            self=Pygen(self)
         ressetctrl_c()
         try:
             #result= gen(GIAC_makenewvecteur((<Pygen>self).gptr[0],(<Pygen>right).gptr[0]),<short int>1)
             #integer output:
             #result= GIAC_smod(result,context_ptr)
             #modular output:
             result= GIAC_giacmod((<Pygen>self).gptr[0],(<Pygen>right).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __rmod__(self, right):
         """
            Reverse operator

                >>> 7%giac(3)   # Called by Cython>3.0.0 when the type can't handle  the non reversed one
                1 % 3

         """
         cdef gen result
         if not isinstance(right,Pygen):
            right=Pygen(right)
         if not isinstance(self,Pygen):
            self=Pygen(self)
         ressetctrl_c()
         try:
             #modular output:
             result= GIAC_giacmod((<Pygen>right).gptr[0],(<Pygen>self).gptr[0],context_ptr)
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __neg__(self):
         cdef gen result
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= GIAC_neg((<Pygen>self).gptr[0])
             return _wrap_gen(result)
         except:
             raise RuntimeError

     def __pos__(self):
         return self

     # To be able to use the eval function before the GiacMethods initialisation
     def cas_setup(self,*args):
        return Pygen('cas_setup')(self,*args)

     # ipython pretty printing
     def _repr_latex_(self):
        # remove quotes
        #return str(self.latex())[1:-1]
        # tester: a=ifactor(100) ; a._repr_latex_()
        return decstring23(GIAC_gen2tex(self.gptr[0], context_ptr).c_str()) #python3

     def _repr_html_(self):
        if self._type == 8:
           if self.sommet() == 'pnt':
              # no mathml output for graphics
              return None
        # remove quotes
        #tmp = str(self.mathml())[1:-1]
        # Fix a PB with "" and mathml error in jupyter 
        #tmp = tmp.replace('mode=""display"" xmlns=""http://www.w3.org/1998/Math/MathML""', 'display="block" xmlns="http://www.w3.org/1998/Math/MathML"')
        #return tmp
        return decstring23(GIAC_ingen2mathml(self.gptr[0],0, context_ptr).c_str()) #python3

     #
     def save(self, str filename):
        """
          Archive a Pygen element to a file in giac compressed format.

          Use the loadgiacgen command to get back the Pygen from the file.

          In C++ these files can be opened with giac::unarchive

            >>> from giacpy import *
            >>> f=giac('(x+y+z+2)**10'); g=f.normal()
            >>> g.save("fichiertest")           #  doctest: +SKIP
            >>> a=loadgiacgen("fichiertest")    #  doctest: +SKIP
            >>> from tempfile import NamedTemporaryFile
            >>> F=NamedTemporaryFile()   # chose a temporary file for a test
            >>> Fname=F.name; F.close()  # so Fname can be our filename  
            >>> g.save(Fname)
            >>> a=loadgiacgen(Fname)
            >>> a.factor()
            (x+y+z+2)**10
            >>> F.close()

        """
        ressetctrl_c()
        try:
            GIAC_archive( <string>encstring23(filename), (<Pygen>self).gptr[0], context_ptr)
        except:
             raise RuntimeError


     def htmlhelp(self, str lang='en'):
         """
         Open the giac  html  detailled help about self in an external  browser

         There are currently 3 supported languages: 'en', 'fr', 'el'

          >>> from giacpy import gcd
          >>> gcd.htmlhelp('fr')           # doctest: +SKIP

         """
         l={'fr':1 , 'en':2, 'el':4}
         if (not lang in ['en', 'fr', 'el']):
           lang='en'
         try:
           url=decstring23(browser_help(self.gptr[0],l[lang])) #python3
           giacbasedir=decstring23(GIAC_giac_aide_dir())  # python3
         except:
           raise RuntimeError,'giac docs dir not found'
         print(url)
         if os.access(giacbasedir,os.F_OK):
            url='file:'+url
            wwwbrowseropen(url)



     def help(self):
        return self.findhelp()

     def redim(self,a,b=None):
        """
        * Increase the size of a matrix when possible, otherwise return self.

        >>> C=giac([[1,2]])
        >>> C.redim(2,3)
        [[1,2,0],[0,0,0]]
        >>> C.redim(2,1)
        [[1,2]]

        """
        d=self.dim()
        if d.type()==7:
           if(a>d[0] and b>=d[1]):
               A=self.semi_augment(Pygen((a-d[0],d[1])).matrix())
               if(b>d[1]):
                   A=A.augment(Pygen((a,b-d[1])).matrix())
               return A
           elif(b>d[1] and a==d[0]):
               return self.augment(Pygen((d[0],b-d[1])).matrix())
           else:
              return self
        else:
           raise TypeError, "self is not a giac List"


     def qcas(self,s=None):
       """
       * Send a giac graphic to qcas. (3D is currently not supported in qcas)

        >>> d1=giac('plot(x*sin(x))')
        >>> d1.qcas()    # doctest: +SKIP
        >>> l=giac([(d1*t*0.1).color(t) for t in range(10)])
        >>> l.qcas()     # doctest: +SKIP

       """
       ressetctrl_c()
       try:
          from giacpy2qcas import toqcas
          toqcas(self,s)
       except:
          raise RuntimeError


     # # # # # # # # # # # # # # # # # # # # # # # # #
     #           WARNING:
     #
     # Do not use things like != in  Pygen's __cinit__
     # with this __richcmp__ enabled
     # The methods will bug: a=Pygen(2); a.sin()
     #
     # # # # # # # # # # # # # # # # # # # # # # # # #

     def __richcmp__( self, other,op):
         if isinstance(other,Pygen)==False:
            other=Pygen(other)
         if isinstance(self,Pygen)==False:
            self=Pygen(self)
         ressetctrl_c()
         try:
             result= giacgenrichcmp((<Pygen>self).gptr[0],(<Pygen>other).gptr[0], op, context_ptr )
         except:
             raise RuntimeError
         if result==1 :
             return True
         else:
             return False

     #
     # Some attributes of the gen class:
     #
     property _type:
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.type
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _subtype:
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.subtype
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _val:  # immediate int (type _INT_)
         """
         immediate int value of an _INT_ type gen.
         """
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr.val
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen"


     property _double:  # immediate double (type _DOUBLE_)
         """
         immediate conversion to float for a gen of _DOUBLE_ type.
         """
         def __get__(self):
           #if (self.gptr != NULL):
             return self.gptr._DOUBLE_val
           #else:
           #  raise MemoryError,"This Pygen is not associated to a giac gen."

     ## Remove property help because the help method is already defined givig PB with cython 3.0
     #property help:
     #    def __get__(self):
     #      return self.help()

     ###################################################
     # Add the others methods
     ###################################################
     #
     #  NB: with __getattr__ this is about 10 times slower: [a.normal() for i in range(10**4)]
     #      than [GiacMethods["normal"](a) for i in range(10**4)]
     #
     #     def __getattr__(self, name):
     #       return GiacMethods[str(name)](self)
     ##








##
################################################################
#   A wrapper from a cpp element of type giac gen to create    #
#   the Python object                                          #
################################################################
cdef inline _wrap_gen(gen  g)except +:

#   cdef Pygen pyg=Pygen('NULL')
# It is much faster with ''
#      [x-x for i in range(10**4)]
#      ('clock: ', 0.010000000000000009,
# than with 'NULL':
#      [x-x for i in range(10**4)]
#      ('clock: ', 1.1999999999999997,
#    #    #    #    #    #
# This is faster than with:
#    cdef Pygen pyg=Pygen('')
# ll=giac(range(10**6))
# ('clock: ', 0.40000000000000036, ' time: ', 0.40346789360046387)
# gg=[1 for i in ll]
# ('clock: ', 0.669999999999999, ' time: ', 0.650738000869751)
#
# But beware when changing the None case in  Pygen init.
#
    cdef Pygen pyg=Pygen() # NB: for stability reasons it creates a full Pygen
    del pyg.gptr # so we have to free its gptr here to avoid a memory leak.
    pyg.gptr=new gen(g)
    return pyg
#    if(pyg.gptr !=NULL):
#      return pyg
#    else:
#      raise MemoryError,"empty gen"






################################################################
#    A wrapper from a python list to a vector of gen           #
################################################################

cdef  vecteur _wrap_pylist(L) except +:
   cdef Pygen pyg=Pygen()
   cdef vecteur  * V
   cdef int i

   if (isinstance(L,tuple) or isinstance(L,listrange)):
      n=len(L)
      V=new vecteur()
      ressetctrl_c()
#      sig_on()
      for i in range(n):
        if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
        V.push_back((<Pygen>Pygen(L[i])).gptr[0])
#      sig_off()
      return V[0]
   else:
     raise TypeError,"argument must be a tuple or a list"


#################################
#  slice wrapper for a giac list
#################################
cdef  vecteur _getgiacslice(Pygen L,slice sl) except +:
   cdef Pygen pyg=Pygen()
   cdef vecteur  * V
   cdef int u

   if (L.type()=="DOM_LIST"):
      n=len(L)
      V=new vecteur()
      ressetctrl_c()
#      sig_on()
#      for u in range(n)[sl]:   #pb python3
      (b,e,st)=sl.indices(n)
      for u in range(b,e,st):
        if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
        V.push_back((L.gptr[0])[u])
#      sig_off()
      return V[0]
   else:
     raise TypeError,"argument must be a Pygen list and a slice"





cdef  gen pylongtogen(a) except +:
   #                                                                     #
   # basic conversion of Python long integers to gen via Horner's Method #
   #                                                                     #
   ressetctrl_c()
   aneg=False
   cdef gen g=gen(<int>0)
   cdef gen M

   if (a<0):
     aneg=True
     a=-a
   if Pyversioninfo >= (2,7):
      size=a.bit_length()  # bit_length python >= 2.7 required.
      shift=Pymaxint.bit_length()-1
   else:
      size=math.trunc(math.log(a,2))+1
      shift=math.trunc(math.log(Pymaxint))
   M=gen(<long long>(1<<shift))

   while (size>=shift):
     if(GIACctrl_c):
          raise KeyboardInterrupt,"Interrupted by a ctrl-c event"
     size=size-shift
     i=int(a>>size)
     g=(g*M+gen(<long long>i))
     a=a-(i<<size)

   g=g*gen(<long long>(1<<size))+gen(<long long> a)
   if aneg:
     # g=-g doesnt cythonize with cython 0.24, (- operator not declared?)
     g=GIAC_neg(g)
   return g;



#############################################################
# Examples of python functions directly implemented from giac
#############################################################
#def giaceval(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_protecteval(self.gptr[0],1,context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#def giacfactor(Pygen self):
#
#    cdef gen result
#    ressetctrl_c() #It's better to do this before calling giac.
#    try:
#      result=GIAC_factor(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#
#def giacfactors(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_factors(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#
#
#def giacnormal(Pygen self):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=GIAC_normal(self.gptr[0],context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise
#
#
#def giacgcd(Pygen a, Pygen b):
#    cdef gen result
#    ressetctrl_c()
#    try:
#      result=gen( GIAC_makenewvecteur(a.gptr[0],b.gptr[0]) ,<short int>1)
#      result=GIAC_gcd(result,context_ptr)
#      return _wrap_gen(result)
#    except:
#      raise



#############################################
# giac functions/keywords
#############################################

I=Pygen('i')  # The complex number sqrt(-1)


def htmlhelp(s='en'):
   """
   Open the giac html detailled help in an external  browser

   There are currently 3 supported lanquages: 'en', 'fr', 'el'
    >>> htmlhelp('fr')         # doctest: +SKIP
    >>> htmlhelp()             # doctest: +SKIP

   """
   giacbasedir=decstring23(GIAC_giac_aide_dir())  # python3
   if (not s in ['en', 'fr', 'el']):
     s='en'
   s='doc/'+s+'/cascmd_'+s+'/index.html'
   ressetctrl_c()
   try:
     #if 1==htmlbrowserhelp(s) :
     #  raise RuntimeError,'unable to launch browser'
     url=giacbasedir+s
     if not os.access(url,os.F_OK):
         url='http://www-fourier.ujf-grenoble.fr/~parisse/giac/'+s
     else:
         url='file:'+url
     wwwbrowseropen(url)
   except:
     raise


#############################################################
#  Qcas string interactive 2D geometry; string input
#############################################################
def qcas(str s):
   """
   * EXPERIMENTAL: Send a giac command to an  interactive 2D geometry display in qcas.
     Current state: Geometric objects will be displayed, but only geometric objects STORED in a giac variable can be used for interactive geometric constructions in qcas.

    >>> d1='A:=point(1+i);t:=element(10..100,1,10);C:=circle(A,t*0.05);M:=element(C);'
    >>> qcas(d1)    # doctest: +SKIP

   """
   if s=='':
      return
   else:
      oldies=Pygen('"using sendtext"')
      ressetctrl_c()
      try:
         from .giacpy2qcas import toqcas
         toqcas(oldies,s)
         return
      except:
         raise RuntimeError







#############################################################
#  Most giac keywords
#############################################################
include 'keywords.pxi'
GiacMethods={}



__all__=['giac','Pygen','giacsettings','I','htmlhelp','qcas','loadgiacgen']+mostkeywords+nonevaluable


#################################################################
#  A Wrapper class to setup the __doc__ attribute from giac's doc
#################################################################

class ThreadedPygen(Pygen):
   """
   Use this subclass of to call your objects with the threadeval method.
   It is usefull to interupt a computation with control C with many python front ends.
   This class is used by GiacFunction
   """
   def __call__(self, *args):
      return self.threadeval(*args)


class GiacFunction:
   # docstring removed to show  self.__doc__  under IEP.

   def __init__(self,str s):
      
      directevalued=['assume', 'supposons', 'randseed', 'srand']
      
      if (s in directevalued):
         self.Pygen=Pygen(s)
      else:
         self.Pygen=ThreadedPygen(s)

      try:
         self.__doc__="(from giac's help:)"+Pygen('?'+s).eval().__str__()
      except:
         self.__doc__="failed to init doc from giac's doc"


   def __call__(self,*args):
      return self.Pygen(*args)


   def __repr__(self):
      return self.Pygen.__repr__()


   def __str__(self):
      return self.Pygen.__str__()


   def __add__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self+right


   def __sub__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self-right


   def __mul__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self*right


   def __div__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self/right


   def __truediv__(self,right):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self*right


   def __pow__(self,right,ignored):
      if isinstance(right,GiacFunction):
         right=right.Pygen
      if isinstance(self,GiacFunction):
         self=self.Pygen
      return self**right


   def __neg__(self):
      return -self.Pygen


   def diff(self,*args):
      return self.Pygen.diff(args)


   def int(self,*args):
      return self.Pygen.int(args)


   def plot(self,*args):
      return self.Pygen.plot(args)


   def htmlhelp(self,str lang='en'):
      return self.Pygen.htmlhelp(lang)




#############################################################
# Some convenient settings
#############################################################
Pygen('printpow(-1)').eval() ; # default power is ** instead of ^
Pygen('add_language(1)').eval() ; # Add the french keywords in the giac library language.
# FIXME: print I for sqrt(-1) instead of i
#GIAC_try_parse_i(False,context_ptr);


for i in mostkeywords:
   #print i
   #tmp=Pygen(i)
   tmp=GiacFunction(i)
   globals()[i]=tmp
   #GiacMethods[i]=tmp
   GiacMethods[i]=tmp.Pygen

# We put the giac names that should not be exported to Python in moremethods.
for i in moremethods:
   #tmp=Pygen(i)
   tmp=GiacFunction(i)
   #GiacMethods[i]=tmp
   GiacMethods[i]=tmp.Pygen

for i in nonevaluable:
#   print i
   tmp=Pygen(i)
   globals()[i]=tmp
   GiacMethods[i]=tmp
##
def moretests():
   """
     >>> from giacpy import giac
     >>> giac(3**100)
     515377520732011331036461129765621272702107522001
     >>> giac(-3**100)
     -515377520732011331036461129765621272702107522001
     >>> giac(-11**1000)
     -2469932918005826334124088385085221477709733385238396234869182951830739390375433175367866116456946191973803561189036523363533798726571008961243792655536655282201820357872673322901148243453211756020067624545609411212063417307681204817377763465511222635167942816318177424600927358163388910854695041070577642045540560963004207926938348086979035423732739933235077042750354729095729602516751896320598857608367865475244863114521391548985943858154775884418927768284663678512441565517194156946312753546771163991252528017732162399536497445066348868438762510366191040118080751580689254476068034620047646422315123643119627205531371694188794408120267120500325775293645416335230014278578281272863450085145349124727476223298887655183167465713337723258182649072572861625150703747030550736347589416285606367521524529665763903537989935510874657420361426804068643262800901916285076966174176854351055183740078763891951775452021781225066361670593917001215032839838911476044840388663443684517735022039957481918726697789827894303408292584258328090724141496484460001
    >>> v=[1,58,1387,17715,131260,578697,1538013,2648041,3687447,4993299,5858116,5979221,5239798,4098561,3176188,1660466,705432]
    >>> giac(v)*v
    175925584603774
    >>> giac([v])*(giac([v]).transpose())
    matrix[[175925584603774]]
    >>> v=giac('pari()')
    >>> if len(v)>200:
    ...    giac('pari(18446744073709551616)')
    ... else:
    ...    giac('2^64')
    18446744073709551616

    Testing substraction of table/sparse matrix
    >>> A=giacpy.table(())
    >>> B=giacpy.table([[1]])
    >>> A-B
    table(
    (0,0) = -1
    )

    Testing randseed
    >>> from giacpy import randvector,randseed,srand
    >>> a=randvector(50)
    >>> randseed(10)
    10
    >>> a=randvector(50)
    >>> srand(10)
    10
    >>> a==randvector(50)
    True
 
   """
   return



def loadgiacgen(str filename):
        """
          Open a file in giac compressed format to create a Pygen element.

          Use the save method from Pygen elements to create such files.

          In C++ these files can be opened with giac::unarchive and created with
          giac::archive

            >>> from giacpy import *
            >>> g=texpand('tan(10*a+3*b)')
            >>> g.save("fichiertest")           #  doctest: +SKIP
            >>> a=loadgiacgen("fichiertest")    #  doctest: +SKIP

        """
        cdef gen result
        ressetctrl_c()
        try:
            result=GIAC_unarchive( <string>encstring23(filename), context_ptr)
            return _wrap_gen(result)
        except:
             raise RuntimeError

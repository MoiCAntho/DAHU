
=============
Giacpy
=============

:Name: giacpy
:Summary: A Cython frontend to the c++ library giac. (Computer Algebra System)
:Author: Frederic Han
:Author-email: frederic.han@imj-prg.fr
:Copyright: 2012 Frederic Han
:License:  GPL v2 or above
:Home-page: https://www.imj-prg.fr/~frederic.han/xcas/giacpy/



Access from python to the Computer Algebra System giac via libgiac

------------
Introduction
------------

This is an interface to be able to use from Python the Giac features.

   * Giac is a general purpose Computer algebra system by Bernard Parisse released under GPLv3.

      - http://www-fourier.ujf-grenoble.fr/~parisse/giac.html
      - It is build on C and C++ libraries:
        PARI, NTL (arithmetic), CoCoA (Groebner basis), GSL (numerics),
        GMP (big integers), MPFR (bigfloats)
      - It  provides (fast) algorithms for multivariate polynomial operations (product, GCD, factorisation) and
      - symbolic  computations: solver, simplifications, limits/series, integration, sommation...
      - Linear Algebra with numerical or symbolic coefficients.


   * giacpy is an interface to this library. It is built with cython. Graphic output is obtained with qcas by Loic Lecoq:  http://git.tuxfamily.org/qcas/qcas.git


-----------
Short Usage
-----------

Example::

    >>> import giacpy  # outputs various messages
    Help file ... aide_cas not found
    Added 0 synonyms
    >>> giacpy.ifactor(2**128+1)
    59649589127497217*5704689200685129054721
    >>> from giacpy import giac
    >>> x,y,z=giac('x,y,z')
    >>> f=(x+y+z+1)**15+1
    >>> g=(f*(f+1)).normal()
    >>> print g.nops()
    >>> print g.factor().nops()
    >>> f.diff()

Help::

    >>> help("giacpy")
    >>> from giacpy import normal
    >>> print(normal.__doc__) ; # to have help on some giac keyword
    >>> solve.htmlhelp('fr') ; # (may be not avaible on your system) to have detailled help on some giac keyword
    >>> htmlhelp()  ; # to have help the global help pages.


    * Graphics 2D Output: (cf. help('giacpy') for examples)
     If your version of giacpy has qt support, you can send graphics to qcas with the .qcas() method. For experimental interactive geometry see: help(qcas)


-------
Install
-------

   * To build the extension from sources (unix):

      - You need the giac library, gmp and python headers. Ex: giac, libgmp-dev python-dev

      - Then execute the command: python setup.py build_ext  (or try the: make or make local)

      - If you need some options see: python setup.py build_ext --help

      - To install giacpy on unix (needs libgiac): python setup.py install

   * For binaries of giacpy: http://webusers.imj-prg.fr/~frederic.han/xcas/giacpy/

   * To run tests you can try: make test
     or run: python -m doctest giacpy.pyx -v   (in the directory of giapy.so if it is not installed)


-----------------------------------
Short Tutorial on the giac function
-----------------------------------

    This function evaluate a python object with the giac library.

    * It creates in python a Pygen element and evaluate it with giac:


     >>> from giacpy import giac,pi
     >>> x,y=giac('x,y');type(x)
     <type 'giacpy.Pygen'>
     >>> (x+2*y).cos().texpand()
     cos(x)*(2*cos(y)**2-1)-sin(x)*2*cos(y)*sin(y)


Coercion, Pygen and internal giac variables:
--------------------------------------------

   * The most usefull objects will be the Python object of type Pygen.

    >>> from giacpy import *
    >>> x,y,z=giac('x,y,z')
    >>> f=sum([x[i] for i in range(5)])**15/(y+z);f.coeff(x[0],12)
    (455*(x[1])**3+1365*(x[1])**2*x[2]+1365*(x[1])**2*x[3]+1365*(x[1])**2*x[4]+1365*x[1]*(x[2])**2+2730*x[1]*x[2]*x[3]+2730*x[1]*x[2]*x[4]+1365*x[1]*(x[3])**2+2730*x[1]*x[3]*x[4]+1365*x[1]*(x[4])**2+455*(x[2])**3+1365*(x[2])**2*x[3]+1365*(x[2])**2*x[4]+1365*x[2]*(x[3])**2+2730*x[2]*x[3]*x[4]+1365*x[2]*(x[4])**2+455*(x[3])**3+1365*(x[3])**2*x[4]+1365*x[3]*(x[4])**2+455*(x[4])**3)/(y+z)


   * The Python object y of type Pygen is not an internal giac variable. (Most of the time you won't need to use internal giac variables).

    >>> type(y);giac('y:=1');y
    <type 'giacpy.Pygen'>
    1
    y

   * There are some natural coercion to Pygen elements:

    >>> pi>3.14 ; pi >3.15 ; giac(3)==3
    True
    False
    True


Lists of Pygen and Giac lists:
------------------------------

   * Here l1 is a giac list and l2 a python list of Pygen type objects.

    >>> l1=giac(range(10)); l2=[1/(i**2+1) for i in l1]
    >>> sum(l2)
    33054527/16762850

    So l1+l1 is done in giac and means a vector addition. But l2+l2 is done in Python so it is the list concatenation.

    >>> l1+l1
    [0,2,4,6,8,10,12,14,16,18]
    >>> l2+l2
    [1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82, 1, 1/2, 1/5, 1/10, 1/17, 1/26, 1/37, 1/50, 1/65, 1/82]


   * Here V is not a Pygen element. We need to push it to giac to use a giac method like dim, or we need to use an imported function.

    >>> V=[ [x[i]**j for i in range(9)] for j in range(9)]
    >>> giac(V).dim()
    [9,9]
    >>> det_minor(V).factor()
    (x[7]-(x[8]))*(x[6]-(x[8]))*(x[6]-(x[7]))*(x[5]-(x[8]))*(x[5]-(x[7]))*(x[5]-(x[6]))*(x[4]-(x[8]))*(x[4]-(x[7]))*(x[4]-(x[6]))*(x[4]-(x[5]))*(x[3]-(x[8]))*(x[3]-(x[7]))*(x[3]-(x[6]))*(x[3]-(x[5]))*(x[3]-(x[4]))*(x[2]-(x[8]))*(x[2]-(x[7]))*(x[2]-(x[6]))*(x[2]-(x[5]))*(x[2]-(x[4]))*(x[2]-(x[3]))*(x[1]-(x[8]))*(x[1]-(x[7]))*(x[1]-(x[6]))*(x[1]-(x[5]))*(x[1]-(x[4]))*(x[1]-(x[3]))*(x[1]-(x[2]))*(x[0]-(x[8]))*(x[0]-(x[7]))*(x[0]-(x[6]))*(x[0]-(x[5]))*(x[0]-(x[4]))*(x[0]-(x[3]))*(x[0]-(x[2]))*(x[0]-(x[1]))

   * Modular objects with %

    >>> V=ranm(5,5) % 2;
    >>> ker(V).rowdim()+V.rank()
    5
    >>> a=giac(7)%3;a;a%0;7%3
    1 % 3
    1
    1

   Do not confuse with the full python integers:

    >>> type(7%3);type(a)
    <type 'int'>
    <type 'giacpy.Pygen'>

Syntaxes with reserved or unknown Python symbols:
-------------------------------------------------

   * In general equations needs symbols such as = < > or that have another meaning in Python. So those objects must be quoted.

    >>> from giacpy import *
    >>> x=giac('x')
    >>> (1+2*sin(3*x)).solve(x)
    list[-pi/3/6,7*pi/18]

    >>> solve('sin(3*x)>2*sin(x)',x)
    Traceback (most recent call last):
    ...
    RuntimeError: Unable to find numeric values solving equation. For trigonometric equations this may be solved using assumptions, e.g. assume(x>-pi && x<pi) Error: Bad Argument Value


   * You can also add some hypothesis to a giac symbol:

    >>> assume('x>-pi && x<pi')
    x
    >>> solve('sin(3*x)>2*sin(x)',x)
    list[((x>((-5*pi)/6)) and (x<((-pi)/6))),((x>0) and (x<(pi/6))),((x>(5*pi/6)) and (x<pi))]

   * To remove those hypothesis use the giac function: purge

    >>> purge('x')
    assume[[],[line[-pi,pi]],[-pi,pi]]
    >>> solve('x>0')
    list[x>0]


   * Same problems with the ..

    >>> from giacpy import *
    >>> x=giac('x')
    >>> f=1/(5+cos(4*x));f.int(x)
    1/2/(2*sqrt(6))*(atan(2*tan(4*x/2)/sqrt(6))+pi*floor(4*x/2/pi+1/2))
    >>> fMax(f,'x=-0..pi').simplify()
    pi/4,3*pi/4
    >>> fMax.help()
    "Returns the abscissa of the maximum of the expression.
    Expr,[Var]
    fMax(-x^2+2*x+1,x)
    fMin"
    >>> sum(1/(1+x**2),'x=0..infinity').simplify()
    (pi*exp(pi)**2+pi+exp(pi)**2-1)/(2*exp(pi)**2-2)





---------
Changelog
---------


   * Version 0.2:
      - Add a comparison function to Pygen. (with coersion)
      - Add a basic definition for most giac functions.
      - Add some help.

   * Version 0.2.1:
      - Add __neg__ and __pos__ support for Pygen. (Ex: -pi)
      - Change __repr__ to hide too long outputs.
      - Make ** be the default printing for powers in giac.

   * Version 0.2.2:
      - Change Pygen() to Pygen('NULL'). (Ex: rand())
      - Add direct acces to the python double value of a Pygen: a._double
      - Add  conversion to giac modulars via the operator %
      - Add  ctrl-c support during list initialisation and iteration
      - Modification of __getitem__ to allow formal variables with indexes.
      - Add htmlhelp method for Pygen objects.
      - Improve the giac initialisation of Python long integers. (basic Horner method instead of strings)
      - Improve  help(giac) and doctests
      - Add support for the slice notation with giac lists

   * Version 0.2.3:
      - Fix Pygen() None initialisation. Add crash test and improve speed in _wrap_gen
      - Add a small Makefile
      - Add a GiacSettings class with some frontends to the cas settings.
      - Add French keywords

   * Version 0.2.4:
      - Update giac 1.1 keywords.

   * Version 0.3:
      - Add a qt output for 2d graphics via qcas.
      - Fixes for giac 1.1

   * Version 0.4:
      - Fixes for Python 3 compatibility
      - Qt/qcas can be disabled at compilation. (cf setup.py)
      - 0.4.1:
	  + add some giac keywords.
      	  + add proba_epsilon in GiacSetting.
	  + test if the html doc is present locally, otherwise open the web doc.
      - 0.4.2:
          + add digits and epsilon in GiacSetting.
	  + Fix for interruptions of giac operators.
	  + Put all the GiacKeywords in a new class: GiacFunction to enable docstrings from giac.
      - 0.4.3:
	  + Update qcas to current version. (svg export added)
	  + New evaluation with threads to have better interruptions.
      - 0.4.4:
          + Add sqrt and complex flags in giac settings.
	  + Add support for multi indexes. Ex A[1,2].

   * Version 0.5:
      - 0.5.0:
          + Put all the Qt/Graphics functions in an independant submodule
          + Add a save method for Pygen and a loadgiacgen function.
      - 0.5.2:
          + Update keywords and clean __init__.py docstring
      - 0.5.3:
          + improve setup.py for mingw built
      - 0.5.4:
          + update giac.dll windows binary to giac 1.2.3-57 with subsop patch
	    and rowreduction-R55929 patch
          + post1: update win64 giac.dll to fix: interface with pari; matrix mul
            for integers

   * Version 0.6:
      - 0.6.0:
          + add a __setitem__ for Pygen elements. Ex: A[1,2]=3
	  + add Linear algebra tutorial in the giac docstring.
      - 0.6.1:
          + update giac keywords.
      - 0.6.2:
          + add _repr_html_ and _repr_latex_ for jupyter output
	  + rebuild giac.dll without ntl.
      - 0.6.3:
          + fix for randseed, srand
	  + update keywords
	  + remove qcas from tree; libqcas
      - 0.6.4:
	  + try to guess qt install from qmake
	  + upgrade giac.dll to 1.4.9.43
	  + fix keywords update
      - 0.6.5:
	  + Add GPL-2 in MANIFEST.in
      - 0.6.6:
          + disable include_package_data in setup.py to not install .cpp files
	    and remove from install directory other source files that are not needed
	    by python nor by cython users.
	  + windows rebuilt with giac-1.4.9-45 with NTL enabled
      - 0.6.7:
          + udapte keywords for giac 1.5.0
	  + update windows built with giac-1.5.0-3 with NTL+glpk+nauty enabled
      - 0.6.8:
          + udapte keywords for giac 1.5.0.53
	  + update windows built with giac-1.5.0-49
      - 0.6.9:
	  + update windows built with giac-1.5.0-63
          + doctest fix NULL ouput

   * Version 0.7:
      - 0.7.0:
          + fix a build error with  giac>1.5.0-75
	  + update windows built with giac-1.5.0-85
      - 0.7.1:
          + update windows built with giac 1.9.0-28 from giacxcas binaries
      - 0.7.2:
          + updates for cython >3.0.0 and reverse operators
      - 0.7.3:
          + add .pyi file for some editors
	  + use automethods.pxi to define Pygen methods with doc
	  + update windows built with giac 1.9.0-59




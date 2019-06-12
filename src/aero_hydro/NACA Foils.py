import numpy as np
import matplotlib.pyplot as plt
from sympy.solvers import solve
from sympy import Symbol

####ERROR HANDLING CLASS####

class Error(Exception):
    pass

class InvalidInputError(Error):
    print("Invalid Input")
    pass


####FUNCTIONS####

def plotter(xu, xl, yu, yl, colour='r', linetype='-'):
    """
    Function to plot the result
    :param xu: x-coordinates for top part of the aerofoil
    :param xl: x-coordinates for bottom part of the aerofoil
    :param yu: y-coordinates for top part of the aerofoil
    :param yl: y-coordinates for bottom part of the aerofoil
    :param colour: colour of the line, expressed as a 1-character string (red as standard)
    :param linetype: type of line used to plot as a 1-character string (continuous line as standard)
    :return: -
    """
    plt.plot(xu, yu, colour+linetype) #xu and yu are for the UPPER part of the aerofoil
    plt.plot(xl, yl, colour+linetype) #xl and yl are for the LOWER part of the aerofoil
    plt.xlim([0.0, 1.0])
    plt.axis('equal') #to preserve the aspect ratio of the plot
    plt.grid()
    plt.show()

def symmetricalcalc(xi, t, c):
    """
    Function to calculate the y-position of the aerofoil for symmetrical 4-digit aerofoils
    :param xi: x-coordinate
    :param t: maximum thickness as a fraction of the chord (last 2 digits of code)/100
    :param c: chordlength, standard as 1
    :return: y-coordinate
    """

    return 5.0*t*c*(0.2969*np.sqrt(xi/ c) -0.1260*(xi/c) - 0.3515*(xi/c)**2 + 0.2843*(xi/c)**3 - 0.1015*(xi/c)**4) #Standard formula

def cambered4digit_theta(xi, p, m, c):
    """
    Function to calculate the angle the aerofoil makes w.r.t the chord
    :param xi: x-coordinate
    :param p: location of maximum camber (10*p is the 2nd digit in the code)
    :param m: maximum camber (100*m is the first digit)
    :param c: chordlength
    :return: angle in radians
    """
    if 0 <= xi <= p * c:
        dydx = 2*m/p*(p-xi/c)                   #change in thickness w.r.t a change in chord position

    elif p * c < xi <= c:
        dydx = 2*m/(1-p)**2*(p-xi/c)            #change in thickness w.r.t a change in chord position

    return np.arctan(dydx)                      #the arctan of this derivative will give us the angle w.r.t the chord


def cambered4digit(xi, p, t, m, c):
    """
    Function to calculate the y-position of the aerofoil for cambered 4-digit aerofoils
    :param xi: x-coordinate
    :param t: maximum thickness as a fraction of the chord (last 2 digits of code)/100
    :param p: location of maximum camber (10*p is the 2nd digit in the code)
    :param m: maximum camber (100*m is the first digit)
    :param c: chordlength
    :return: tuple with (xu, yu, xl, yl)
    """
    yt = symmetricalcalc(xi, t, c)              #yt is the symmetrical thickness distribution, it is always used

    if 0 <= xi <= p*c:
        yc = (m/p**2*(2*p*xi/c-(xi/c)**2))*c    #yc is the camber distribution, which is added to yt

    elif p*c < xi <= c:
        yc = (m/((1-p)**2)*((1-2*p)+2*p*(xi/c)-(xi/c)**2))*c

    theta = cambered4digit_theta(xi, p, m, c)

    xu, xl = xi - yt*np.sin(theta), xi + yt*np.sin(theta)       #Standard formula for adding the camber distribution to yt

    yu, yl = yc + yt*np.cos(theta), yc - yt*np.cos(theta)

    return (xu, yu, xl, yl)

def cambered5digit_theta(xi, k1, m, c):
    """
    Function to calculate the angle the aerofoil makes w.r.t the chord
    :param xi: x-coordinate
    :param k1: pre-determined constant depending on the NACA code
    :param m: maximum camber
    :param c: chordlength
    :return: angle in radians
    """
    if 0 <= xi <= m:
        dydx = (k1*(3*xi**2 - 6*m*xi - m**2*(m - 3)))/6.0*c

    elif m < xi <= c:
        dydx = -m**3 * k1 / 6.0 * c

    return np.arctan(dydx)


def cambered5digit(xi, t, m, k1, c):
    """
    Function to calculate the y-position of the aerofoil for 5-digit aerofoils
    :param xi: x-coordinate
    :param t: maximum thickness as a fraction of the chord (last 2 digits of code)/100
    :param k1: pre-determined constant depending on the NACA code
    :param m: maximum camber (100*m is the first digit)
    :param c: chordlength
    :return: tuple with (xu, yu, xl, yl)
    """
    yt = symmetricalcalc(xi, t, c)

    if 0 <= xi <= m:
        yc = k1/6.0*(xi**3 - 3.0*m*xi**2 + m**2*(3.0 - m)*xi)*c

    elif m < xi <= c:
        yc = k1*m**3/6.0*(1 - xi)*c

    theta = cambered5digit_theta(xi, k1, m, c)

    xu, xl = xi - yt*np.sin(theta), xi + yt*np.sin(theta)

    yu, yl = yc + yt*np.cos(theta), yc - yt*np.cos(theta)

    return (xu, yu, xl, yl)

####DATA###
# Data necessary to plot the 5 digit aerofoils
meanline = [210,220,230,240,250]
maxcamb  = [0.05,0.10,0.15,0.20,0.25]
mn       = [0.058,0.126,0.2025,0.29,0.391]
k1n      = [361.4,51.64,15.957,6.643,3.23]


####PROGRAM####

dx = 0.0001 #Numerical calculation increment
running = True
while running:

    NACA = input("NACA# = ")
    NACAlst = list(NACA)

    for i in NACAlst:
        try:
            int(i)
        except Exception:
            print("Invalid Input\n")
            break
    try:
        if len(NACAlst) != 4 and len(NACAlst) != 5:
            raise InvalidInputError
    except InvalidInputError:
        pass

    if len(NACAlst) == 4 and NACAlst[0] == '0' and NACAlst[1] == '0':
        t = float(NACAlst[2]+NACAlst[3])/100.0
        c = 1.0
        x_range = np.arange(0.0,c+dx,dx)

        y_U = []
        y_L = []
        for i in range(len(x)):
            yttop = symmetricalcalc(x[i], t, c) #For the top of the aerofoil
            ytbot = -yttop
            y_U.append(yttop)
            y_L.append(ytbot)

        x_U = x_range
        x_L = x_U
        running = False

    elif len(NACAlst) == 4 and not NACAlst[0] == '0' and not NACAlst[1] == '0':
        m = float(NACAlst[0])/100.0
        p = float(NACAlst[1])/10.0
        t = float(NACAlst[2]+NACAlst[3])/100.0
        c = 1.0
        x1 = np.arange(0.0,p*c,dx)
        x2 = np.arange(p*c,c+dx,dx)
        x_range = np.concatenate((x1,x2))

        x_U = []
        x_L = []
        y_U = []
        y_L = []

        for xi in x_range:
            xu, yu, xl, yl = cambered4digit(xi, p, t, m, c)
            x_U.append(xu)
            x_L.append(xl)
            y_U.append(yu)
            y_L.append(yl)
        running = False

    elif len(NACAlst) == 5:
        if NACAlst[2] == '0' and NACAlst[0] == '2' and int(NACAlst[1]) in range(1,6):
            cli = float(NACAlst[0])*3/2
            p = float(NACAlst[1]+NACAlst[2])/200.0
            t = float(NACAlst[3]+NACAlst[4])/100.0
            c = 1.0
            m = mn[int(NACAlst[1])-1]
            k1 = k1n[int(NACAlst[1])-1]
            x1 = np.arange(0.0,p,dx)
            x2 = np.arange(p,c+dx,dx)
            x_range = np.concatenate((x1, x2))

            x_U = []
            x_L = []
            y_U = []
            y_L = []

            for xi in x_range:
                xu, yu, xl, yl = cambered5digit(xi, t, m, k1, c)
                x_U.append(xu)
                x_L.append(xl)
                y_U.append(yu)
                y_L.append(yl)
        running = False

    else:
        print("Please insert a 4 or 5 digit aerofoil code with only numbers\n")

plotter(x_U, x_L, y_U, y_L)

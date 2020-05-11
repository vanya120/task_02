import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import re
import scipy.special as sc
import matplotlib.ticker as mt

def h(n, x):
    return sc.spherical_jn(n, x) + 1j * sc.spherical_yn(n, x)

def a(n, x):
    return sc.spherical_jn(n, x) / h(n, x)

def b(n, x):
    return ((x * sc.spherical_jn(n - 1, x) - n * sc.spherical_jn(n, x))
            / (x * h(n - 1, x) - n * h(n, x)))

def RCS(D, fmin, fmax):
    c = 3e8
    r = D/2
    f = np.arange(fmin, fmax+1e8, 1e8)
    sigma = []
    for i in f:
        lambda_ = c / i
        k = 2 * np.pi / lambda_
        summa = []
        for n in range(1,100):
            summa.append((-1) ** n * (n + 0.5) * (b(n, k * r) - a(n, k * r)))
        sigma.append((lambda_ ** 2 / np.pi) * abs(sum(summa)) ** 2)
    with open('results/task_02_40-506C_KORNEV_01.txt', 'w') as ouf:
        ouf.write('f, [ГГц]\tsigma, [м^2]\n')
        for i in range(len(f)):
            ouf.write(str('{0:.2f}\t\t{1}\n'.format(f[i] * 1e-9, sigma[i])))
    plt.plot(f, sigma)
    plt.grid()
    plt.ylabel(r'$\sigma$, [$м^2$]', fontsize = 18)
    plt.xlabel('$f$, [ГГц]')
    plt.show()
           
if __name__ == '__main__':
    try: os.mkdir('results')
    except OSError: pass
    r = requests.get('https://jenyay.net/uploads/Student/Modelling/task_02.txt')
    for i in r.text.splitlines():
        if re.match(r'1\.', i): z = i 
    match = list(map(lambda z:float(z), re.findall(r'=(\d+\.?\d*[e-]*\d+)',z)))
    D, fmin, fmax = match[0], match[1], match[2]
    RCS(D, fmin, fmax)
    
    
    

    

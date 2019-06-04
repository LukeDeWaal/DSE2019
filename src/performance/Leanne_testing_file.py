import matplotlib.pyplot as plt

def test1(y):
    a = [1,2,3,4,5]
    plt.subplot(121)
    plt.plot(a,y)
    return

def test2(y):
    b = [2,3,4,5,6]
    plt.subplot(122)
    plt.plot(b, y)

y = [1,2,3,4,5]

test1(y)
test2(y)

plt.show()







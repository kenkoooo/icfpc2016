from fractions import Fraction
import copy
import matplotlib.pyplot as plt
# 縦横比を揃えるおまじない
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([-0.5,1.5])
plt.ylim([-0.5,1.5])


# グリッド
plt.grid(which='major', color='black', linestyle='dashed')

vs=[]
for y in range(9):
    for x in range(9):
        vs.append([Fraction(x/8),Fraction(y/8)])

vs_source=copy.deepcopy(vs)

facets=[]
for i in range(72):
    if i%18==1 or i%18==5:
        facets.append([i, i+1, i+11, i+8])
        facets.append([i+8, i+11, i+19, i+18])
    if i%18==2:
        facets.append([i, i+3, i+11, i+10])
        facets.append([i+10, i+11, i+21, i+18])
    if i%18==6:
        facets.append([i,i+2,i+11,i+10])
        facets.append([i+10, i+11, i+20, i+18])
    if i%18==0:
        facets.append([i,i+1,i+9])
        facets.append([i+9, i+18, i+19])




# 1回目の
for i in range(len(vs)):
    x, y=vs[i]
    if y>Fraction(1/2):
        y=Fraction(1)-y
    vs[i]=[x,y]


# 2回目の
for i in range(len(vs)):
    x, y=vs[i]
    if y>Fraction(1/4):
        y=Fraction(1/2)-y
    vs[i]=[x,y]

# 3回目の
for i in range(len(vs)):
    x, y=vs[i]
    if y>Fraction(1/8):
        y=Fraction(1/4)-y
    vs[i]=[x,y]


#1回目の
for i in range(len(vs)):
    x, y=vs[i]
    if y==Fraction(0) and x>=Fraction(2/8):
        y=x-Fraction(2/8)
        x=Fraction(2/8)
    elif y==Fraction(1/8) and x>=Fraction(3/8):
        y=x-Fraction(2/8)
        x=Fraction(3/8)
    vs[i]=[x,y]




#2回目の
for i in range(len(vs)):
    x, y=vs[i]
    if x==Fraction(2/8) and y>=Fraction(3/8):
        x=x-(y-Fraction(3/8))
        y=Fraction(3/8)
    elif x==Fraction(3/8) and y>=Fraction(2/8):
        x=x-(y-Fraction(2/8))
        y=Fraction(2/8)
    vs[i]=[x,y]



#3回目の
for i in range(len(vs)):
    x, y=vs[i]
    if y==Fraction(3/8) and x<=Fraction(1/8):
        y=y-(Fraction(1/8)-x)
        x=Fraction(1/8)
    elif x==Fraction(-1/8) and y==Fraction(2/8):
        x=Fraction(0)
        y=Fraction(1/8)
    elif x==Fraction(0) and y==Fraction(0):
        x=Fraction(1/8)
        y=Fraction(1/8)
    vs[i]=[x,y]


facet_check=[False]*len(vs)
for facet in facets:
    for i in facet:
        facet_check[i]=True

k=0
checked_index=[-1]*len(vs)
for i in range(len(vs)):
    if facet_check[i]:
        checked_index[i]=k
        k+=1


print(k)
for i in range(len(vs_source)):
    if facet_check[i]:
        x,y=vs_source[i]
        print(str(x)+","+str(y))

print(len(facets))
for facet in facets:
    facet=[checked_index[i] for i in facet]
    print(str(len(facet))+" "+" ".join(map(str,facet)))

for i in range(len(vs)):
    if facet_check[i]:
        x,y=vs[i]
        print(str(x)+","+str(y))


x=[vs_source[i][0] for i in range(len(vs)) if facet_check[i]]
y=[vs_source[i][1] for i in range(len(vs)) if facet_check[i]]
for polygon in facets:
    polygon=[vs_source[p] for p in polygon]
    plt.gca().add_patch(plt.Polygon(polygon, alpha=0.3))


plt.scatter(x,y)
plt.show()
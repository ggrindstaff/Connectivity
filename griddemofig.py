#requires git, installs alternate ripser version from directory
git clone https://github.com/ggrindstaff/ripser.py
%cd ripser.py
pip install -e .

import numpy as np
from numpy import genfromtxt

from matplotlib import pyplot as plt
from matplotlib import collections  as mc
from matplotlib.transforms import Affine2D
import matplotlib.gridspec as gridspec
from matplotlib.patches import ConnectionPatch
from matplotlib.colors import LinearSegmentedColormap, to_rgba

import scipy
from scipy import ndimage
import random

from ripser import ripser
from scipy import stats
from scipy import sparse
import skimage
from skimage import measure


plt.rcParams.update(plt.rcParamsDefault)

data = np.array([[0.86177198, 0.86231934, 0.86242337, 0.860157, 0.86029416, 0.86158316,
  0.86128466, 0.86092225, 0.86092587, 0.86237965],
 [0.86295079, 0.86263436, 0.86081007, 0.86039829, 0.86089049, 0.86189078,
  0.86200083, 0.86149954, 0.861862,  0.86358942],
 [0.8618287,  0.86209426, 0.86077447, 0.86160931, 0.8620815,  0.86305682,
  0.86266645, 0.86266585, 0.86357294, 0.86425865],
 [0.86174632, 0.86075554, 0.86140343, 0.86237797, 0.86335305, 0.86288816,
  0.86334845, 0.86331681, 0.86454815, 0.86422201],
 [0.86252426, 0.86192215, 0.863218,   0.86438554, 0.86516824, 0.86482549,
  0.86308477, 0.8642117,  0.86476069, 0.86320487],
 [0.86227117, 0.8625662 , 0.86437098, 0.8644288,  0.86426836, 0.86336185,
  0.86375321, 0.86502151, 0.86509492, 0.86458407],
 [0.86248328, 0.86242205, 0.86315812, 0.86378427, 0.86296295, 0.86444846,
  0.86410309, 0.86408847, 0.86354987, 0.86423841],
 [0.86223582, 0.86249903, 0.86323181, 0.86293446, 0.86528842, 0.86484928,
  0.86511704, 0.86485379, 0.86444904, 0.86418466],
 [0.8625511 , 0.86181715, 0.86209187, 0.86314486, 0.86396691, 0.86452231,
  0.86323388, 0.86351332, 0.86482025, 0.86393913],
 [0.86280803, 0.86176169, 0.86285082, 0.86297043, 0.86262443, 0.86337541,
  0.86375353, 0.86374458, 0.86400033, 0.86222872]])

def tobinary(data,thr,super=False):
  dat = data.copy()
  dat[dat <= thr]=0
  dat[np.isnan(dat)]=1
  dat[dat > thr]=1
  if super==False:
    dat = 1-dat 
  return dat

def img_to_sparse(img):
  # Modified from source code
    m, n = img.shape

    idxs = np.arange(m * n).reshape((m, n))

    I = idxs.flatten()
    J = idxs.flatten()
    V = img.flatten()

    # Connect 8 spatial neighbors
    tidxs = np.ones((m + 2, n + 2), dtype=np.int64) * np.nan
    tidxs[1:-1, 1:-1] = idxs

    tD = np.ones_like(tidxs) * np.nan
    tD[1:-1, 1:-1] = img

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:

            if di == 0 and dj == 0:
                continue

            thisJ = np.roll(np.roll(tidxs, di, axis=0), dj, axis=1)
            thisD = np.roll(np.roll(tD, di, axis=0), dj, axis=1)
            thisD = np.maximum(thisD, tD)

            # Deal with boundaries
            boundary = ~np.isnan(thisD)
            thisI = tidxs[boundary]
            thisJ = thisJ[boundary]
            thisD = thisD[boundary]

            I = np.concatenate((I, thisI.flatten()))
            J = np.concatenate((J, thisJ.flatten()))
            V = np.concatenate((V, thisD.flatten()))

    return sparse.coo_matrix((V, (I, J)), shape=(idxs.size, idxs.size))


def cocycles_to_plot(cocycles,rotate=False):
  m,n = data.shape
  birthloc = [cocycles[i][0][0] for i in range(len(cocycles))]
  xloc = []
  yloc = []
  for ind in birthloc:
    if rotate==False:
      yi = int(ind/n)
      xi = ind%n
#need index_t to coordinate map
    if rotate==True:
      yi = m-int(ind/n)-1
      xi = ind%n  
    xloc.append(xi)
    yloc.append(yi)
  return xloc,yloc

def complex_from_data(data,t,rotate=False):
  xvals=[]
  yvals=[]
  edges=[]
  m,n = data.shape
  sparseDM = (img_to_sparse(data)).tocsr()
  for i in range(m*n):
    if sparseDM[i,i]<t:
      if rotate==False:
        xi = int(i/n)
        yi = i%n
      if rotate==True:
        yi = m-int(i/n)
        xi = i%n        
      xvals.append(xi)
      yvals.append(yi)
      for j in range(m*n):
        if sparseDM[j,j]<t and sparseDM[i,j]!=0 and i!=j:
          if rotate==True:
            yj = m-int(j/n)
            xj = j%n   
          if rotate==False:
            xj = int(j/n)
            yj = j % n
          edges.append([(xi,yi),(xj,yj)])
  return xvals, yvals, edges

def to_nary(binary,color_data):
  bin = 1-binary
  blobs = measure.label(bin, background=0)
  ref = (bin)*(color_data)
  m,n = bin.shape
  out = np.zeros((m,n))
  blobby = np.unique(blobs)
  for i in blobby:
    if i!=0:
      x,y =  np.where(blobs==i)
      col = min(ref[x[j],y[j]] for j in range(len(x)))
      out[x,y] = col
  return out


sparseDM = img_to_sparse(data)
rip = ripser(sparseDM, distance_matrix=True, maxdim=2, do_cocycles=True)
dgm0 = rip["dgms"][0]
dgm1 = rip["dgms"][1]
cocycles = rip["cocycles"]
xcycle,ycycle = cocycles_to_plot(cocycles[0],rotate=False)

epsilon = .0001
maxi = data.max()-epsilon
mini = data.min()+epsilon

m,n = data.shape
color_data = np.zeros((m,n))
hwidth = 0.00001

for i in range(len(dgm0)):
  im = np.where((data >= dgm0[i][0]-hwidth)&(data<dgm0[i][1]+hwidth),1,0) #find locations with filtration val between birth and death
  blobs = measure.label(im)
  labeli = blobs[ycycle[i],xcycle[i]]
  maski = np.where(blobs==labeli,i,0)
  color_data = color_data + maski

  

b_inf = (maxi-mini) * 0.45
do1=False

birth0=[]
death0=[]
persistence0=[]
bars=[]
y=0.5
for feat in dgm0:
  birth0.append(feat[0])
  death0.append(feat[1])
  if np.isinf(feat[1]):
    bars.append([(feat[0],y),(maxi+0.0005,y)])
    persistence0.append(b_inf)
  else:
    bars.append([(feat[0],y),(feat[1],y)])
    persistence0.append(feat[1]-feat[0])
  y = y+1

if do1 == True:
  birth1=[]
  death1=[]
  persistence1=[]
  bars1=[]
  for feat in dgm1:
    birth1.append(feat[0])
    death1.append(feat[1])
    if np.isinf(feat[1]):
      bars1.append([(feat[0],y),(maxi+0.0005,y)])
      persistence1.append(b_inf)
    else:
      bars1.append([(feat[0],y),(feat[1],y)])
      persistence1.append(feat[1]-feat[0])
    y = y+1

plt.rc('font', size=14) 
fig = plt.figure(constrained_layout=True, figsize = (14,7))
spec2 = gridspec.GridSpec(ncols=12, nrows=8, figure=fig)
spec2.update(top=2)

axb0 = fig.add_subplot(spec2[4, 0:2])
axb1 = fig.add_subplot(spec2[4, 2:4]) 
axb2 = fig.add_subplot(spec2[4, 4:6]) 
axb3 = fig.add_subplot(spec2[4, 6:8]) 
axb4 = fig.add_subplot(spec2[4, 8:10]) 
axb5 = fig.add_subplot(spec2[4, 10:]) 
axb = [axb0,axb1,axb2,axb3,axb4,axb5]

axc0 = fig.add_subplot(spec2[5, 0:2])
axc1 = fig.add_subplot(spec2[5, 2:4]) 
axc2 = fig.add_subplot(spec2[5, 4:6]) 
axc3 = fig.add_subplot(spec2[5, 6:8]) 
axc4 = fig.add_subplot(spec2[5, 8:10]) 
axc5 = fig.add_subplot(spec2[5, 10:]) 
axc = [axc0,axc1,axc2,axc3,axc4,axc5]

axl = fig.add_subplot(spec2[0:1,4:5])

axbar = fig.add_subplot(spec2[6:, :]) 
axim = fig.add_subplot(spec2[0:3, :5])
axpd = fig.add_subplot(spec2[0:3, 7:]) 

axim.imshow(data, cmap = 'gist_earth',interpolation='nearest')
axim.set_axis_off()
axl.set_axis_off()


ts = [round((i/(len(axb)-1)*(maxi-mini)+mini),4) for i in range(len(axb))]

textlabel = ['b1)','b2)','b3)','b4)','b5)','b6)']
col='gray'
i=0
for ax in axc:
  xvals,yvals, lines = complex_from_data(data,ts[i],rotate=True)
  y = len(data[0])
  x = len(data)
  lc = mc.LineCollection(lines, linewidths=1,color=col)
  ax.add_collection(lc)
  #  plt.autoscale()
  ax.scatter(xvals,yvals,s=2,color=col)
  ax.set_xlim([-1,y])
  ax.set_ylim([0,x+1])
  ax.set_xticks([])
  ax.set_yticks([])
  conl = ConnectionPatch(xyA=(0, 0), xyB=(ts[i], y+0.5), 
                         coordsA='axes fraction', coordsB="data", axesA=ax, axesB=axbar,linestyle=':')
  conr = ConnectionPatch(xyA=(1, 0), xyB=(ts[i], y+0.5), 
                         coordsA='axes fraction', coordsB="data", axesA=ax, axesB=axbar,linestyle=":")
  fig.add_artist(conl)
  fig.add_artist(conr)
  i = i+1

fig.text(0.085,0.65,"Adjacency \n   graph",rotation=90)
fig.text(0.085,0.85,"Thresholded \n    image",rotation=90)

colorkeys = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_data_keys = [colorkeys[9]]+colorkeys[:9]
white = ['#FFFFFF']+color_data_keys
colors = [to_rgba(c)
          for c in colorkeys]
plotcolors=[to_rgba(c)
          for c in white]
featcmap = LinearSegmentedColormap.from_list('features',colors,N=len(colors))
plotcmap = LinearSegmentedColormap.from_list('features',plotcolors,N=len(plotcolors))

vmin = 0
vmax=10

m,n = data.shape
color_data = np.zeros((m,n))
hwidth = 0.000001

for i in range(len(dgm0)-1):
  im = np.where((data >= dgm0[i][0]-hwidth)&(data<dgm0[i][1]-hwidth),1,0) #find locations with filtration val between birth and death
  blobs = measure.label(im)
  labeli = blobs[ycycle[i],xcycle[i]]
  maski = np.where(blobs==labeli,i+1,0)
  color_data = color_data + maski
color_data = color_data+1

textlabel = ['a1)','a2)','a3)','a4)','a5)','a6)']
i=0
for ax in axb:
    dat = tobinary(data,ts[i],super)
    col_dat = to_nary(dat,color_data)
    label = textlabel[i]+' t = {0}'.format(ts[i])
    ax.imshow(col_dat,cmap=plotcmap,vmin=vmin,vmax=vmax)
    ax.set_xticks([])
    ax.set_yticks([])
    i = i+1


color0='skyblue'
color1='firebrick'
lc = mc.LineCollection(bars, linewidths=4,color=colors)
if do1==True:
  lc1 = mc.LineCollection(bars1,linewidths=4,color=color1)
axbar.add_collection(lc)
if do1==True:
  axbar.add_collection(lc1)
axbar.set_xlim(mini-0.0008,maxi+0.0005)
axbar.set_xticks(ts)
axbar.set_yticks([])
axbar.set_xlabel("Threshold value")
axbar.set_ylim(0,y+0.5)
for i in range(len(axb)):
  axbar.axvline(ts[i],linestyle=":",color='k')
axbar.text(maxi+0.0003,-0.6, '$\cdots  \infty$',fontsize='x-large')
axbar.spines['left'].set_visible(False)
axbar.spines['top'].set_visible(False)


line = plt.Line2D((.5,.5),(.1,.9), color="k", linewidth=1)
#fig.add_artist(line)

#add infinity
xmin = data.min()-0.0005
xmax = data.max()+0.0005
axpd.scatter(birth0,persistence0,color=colors,edgecolor='k',s=100,alpha = 0.7,label='$H_0$')
if do1 == True:
  axpd.scatter(birth1,persistence1,color=color1,edgecolor='k',s=100,alpha = 0.7,label='$H_1$')
axpd.set_xlim(xmin,xmax)
#axpd.legend(loc="lower right")
axpd.plot([xmin, xmax], [b_inf, b_inf], "--", c="k", label=r"$\infty$")
axpd.text(xmin-0.0005,b_inf-0.00003, '$\infty$',fontsize='x-large')
#axpd.text(xmin-0.0005,b_inf-0.00005, '$\vdots$',fontsize='x-large')
#axpd.axline(xy1=(mini,mini),slope=1)
axpd.set_xlabel("Birth threshold")
axpd.set_ylabel("Persistence")
axpd.set_title("b) Persistence Diagram")


fig.text(0.5,1.1,"c) Persistence Barcode",fontsize='large',ha='center')
axim.set_title("a) Data",fontsize='large')
# #fig.text(0.075,0.54,"c) Persistence Diagram", fontsize='large')

# plt.show()
plt.savefig('TDAFig3.pdf',format='pdf',dpi=300,bbox_inches='tight')

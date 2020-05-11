import numpy as np
import matplotlib


#Import nxn matrix of elevation

#Set n
n = 0

#Initialize grid graph

# V = nxn grid of vertices v_ij
# Edge set given by (v_ij, v_kl) = f(max(e_ij - e_kl, 0)) if k = i and l = j +/- 1, or k = i +/- 1 and j = l 
# i.e. v_ij, v_kl are directly adjacent in grid
# find function f: R -> R from literature, or adust experimentally
#Store in n^2 x n^2 matrix? Probably a better way. 

E = np.zeros((n^2,n^2))

# define matrix W_t of pointwise volume of water at time t (W_0 is nxn zero matrix)
W_0 = np.zeros((n,n))

# Set or input rain level (assumed to be constant over space and time) 
rain = 0
# Set or input soil absorption
soil = 0

# Set or input threshhold water value for concentrated flow path. Should be greater than soil.
# soil < W_t[i,j]< c indicates runoff of volume W_t[i,j] - soil
c = 0


#find the vertices with concentrated flow paths at time T and rain level rain
function compute_concentrated_flow(G,E, W_0, T, rain, soil):
  for t in range(0,T):
    #create W_t from W_t-1
    #search W_t for indices with W_t[i,j] > c

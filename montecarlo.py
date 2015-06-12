from random import gauss
from regress import data
from helper import variance
import math
### Documentation
## ========================================
# MC - creates a montecarlo function

def MC(a,b,gam,delta,lam,varw,varv,varu):
	M = 500
	N = 500
	beta = []
	for sim in xrange(M):
		W = [gauss(0,varw) for i in xrange(N)]
		V = [gauss(0,varv) for i in xrange(N)]
		U = [gauss(0,varu) for i in xrange(N)]
		dataset = [['Y','X','W','V','U']]
		dataset = dataset + [[a + b*(delta + lam*W[i] + V[i]) + gam*W[i] + U[i],delta + lam*W[i] + V[i], W[i], V[i], U[i]] for i in xrange(N)]
		d = data(dataset)
		beta.append(d.regression('Y',['X','W','Constant'])[0])


	return [sum(beta)/len(beta),math.sqrt(variance(beta))]


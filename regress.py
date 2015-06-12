from parse import parse
import numpy as np
from scipy import linalg
### Documentation
## ========================================
# Data:
## ----------------------------------------
# __init__ - initialized with a dictionary of names to index and a dataset. Can take an array or a filename
# regression - runs a linear regression of the first variable on the second variable(s). The second argument is a list.
# indicator regression - runs a linear regression on argv[0] on every possible instance of argv[1] and accounting for argv[2]
# fixed effects - runs a fixed effects regression on argv[0] with i and t as argv[1] and argv[2] on the variables argv[3]
# gen - generates data of the name argv[0], by running the function argv[1] on all other arguments
# correlation - returns a correlation matrix for all variables passed in the list

class data:
	def __init__(self,filename):
		# if given file name
		if isinstance(filename,str):
			self.dictionary, self.dataset = parse(filename)
			for instance in self.dataset:
				instance.append(1)
			self.dictionary['Constant'] = len(self.dictionary)

		# if given an list
		elif isinstance(filename,list):
			temp = filename.pop(0)
			temp =  temp + [i for i in range(len(temp))]
			self.dictionary = dict(zip(temp[0:len(temp)/2],temp[len(temp)/2:]))
			self.dataset = filename
			for instance in self.dataset:
				instance.append(1)
			self.dictionary['Constant'] = len(self.dictionary)
		else:
			print "error"

	# Beta = E(XX')^-1 * E(XY)
	def regression(self,y,x):
		y = self.dictionary[y]
		for i in xrange(len(x)):
			x[i] = self.dictionary[x[i]]
		N = len(self.dataset)

		# parts of the function
		left = np.array([[0.0]*len(x) for i in xrange(len(x))])
		right = np.array([[0.0]]*len(x))

		for instance in self.dataset:
			Xi_temp = []
			for var in x:
				Xi_temp.append([float(instance[var])])
			Xi = np.array(Xi_temp)
			left += np.dot(Xi,Xi.T)
			right += Xi*float(instance[y])
		# dot the two matricies together
		beta = np.dot(linalg.inv(left/N),right/N).tolist()

		# change from list of lists to list of floats
		for i in xrange(len(beta)):
			beta[i] = beta[i][0]

		return beta

	def indicator_regression(self,y,u,x):
		y = self.dictionary[y]
		u = self.dictionary[u]
		for i in xrange(len(x)):
			x[i] = self.dictionary[x[i]]
		N = len(self.dataset)

		vals = set()
		beta = {}

		# finds all values of u
		for instance in self.dataset:
			vals.add(instance[u])

		# for each value of u, run a linear regression
		for val in vals:
			left = np.array([[0.0]*len(x) for i in xrange(len(x))])
			right = np.array([[0.0]]*len(x))

			# linear regression on all x's
			for instance in self.dataset:
				if instance[u] == val:
					Xi_temp = []
					for var in x:
						Xi_temp.append([float(instance[var])])
					Xi = np.array(Xi_temp)
					left += np.dot(Xi,Xi.T)
					right += Xi*float(instance[y])
			beta[val] = np.dot(linalg.inv(left/N),right/N).tolist()

			# convert data
			for i in xrange(len(beta[val])):
				beta[val][i] = beta[val][i][0]

		# returns a dictionary of betas
		return beta			

	def fixed_effects(self,y,ident,t,x):
		y = self.dictionary[y]
		ident = self.dictionary[ident]
		t = self.dictionary[t]
		for i in xrange(len(x)):
			x[i] = self.dictionary[x[i]]
		valst,valsi = (set() for i in xrange(2))

		# finds all possible time and individuals
		for instance in self.dataset:
			valst.add(float(instance[t]))
			valsi.add(float(instance[ident]))

		# initialize variables
		N = len(self.dataset)
		T = len(valst)
		xDotBar = [0 for i in xrange(len(x))]
		yDotBar = 0
		xMean = [dict((val,0) for val in valsi) for j in xrange(len(x))]
		yMean = dict((val,0) for val in valsi)

		# calculate mean of x and y
		for instance in self.dataset:
			for index,val in enumerate(x):
				xMean[index][float(instance[ident])] += float(instance[val])/T
			print xMean[index][float(instance[ident])]
			yMean[float(instance[ident])] += float(instance[y])/T

		# calculate x and y dot bar
		for instance in self.dataset:
			for index,val in enumerate(x):
				xDotBar[index] += float(instance[val]) - xMean[index][float(instance[ident])]
			yDotBar += float(instance[y]) - yMean[float(instance[ident])]

		# divide xDotBar and yDotBar by NT
		for index,val in enumerate(x):
			xDotBar[index] = xDotBar[index]/N/T
		yDotBar = yDotBar/N/T

		# calculate the two parts of the beta
		top, bottom, beta = ([0 for j in xrange(len(x))] for i in xrange(3))
		for instance in self.dataset:
			for index,val in enumerate(x):
				top[index] += (float(instance[y]) - yMean[float(instance[ident])] - yDotBar)*(float(instance[val]) - xMean[index][float(instance[ident])	] - xDotBar[index])
				bottom[index] += (float(instance[val]) - xMean[index][float(instance[ident])] - xDotBar[index])**2

		# combines sections to calculate beta
		for i in xrange(len(x)):
			beta[i] = top[i]/bottom[i]
		return beta

	def gen(self, name, f, *args):
		argu = []
		# change arguments given to index
		for arg in args:
			argu.append(self.dictionary[arg])

		# create a new variable in each instance
		for instance in self.dataset:
			vals = []
			for arg in argu:
				vals.append(float(instance[arg]))
			vals = tuple(vals)
			instance.append(str(f(*vals)))

		# add entry to dictionary
		self.dictionary[name] = len(self.dictionary)

	def correlation(self,x):
		for i in xrange(len(x)):
			x[i] = self.dictionary[x[i]]

		N = float(len(self.dataset))

		# calculate mean
		mean,var = ([0.0]*len(x) for i in xrange(2))
		for instance in self.dataset:
			for index,val in enumerate(x):
				mean[index] += float(instance[val])/N

		# calculate covariance matrix
		cov, corr_matrix = ([]for i in xrange(2))
		for i in xrange(len(x)):
			cov.append([0.0]*len(x))
			corr_matrix.append([0.0]*len(x))

		# calculate variances
		for instance in self.dataset:
			for i in xrange(len(x)):
				var[i] += ((float(instance[i]) - mean[i])**2)/N
				for j in xrange(i+1,len(x)):
					cov[i][j] += ((float(instance[j]) - mean[j])*(float(instance[i]) - mean[i]))/N

		# calculate correlation matrix from the covariances and variances
		for i in xrange(len(x)):
			for j in xrange(i + 1,len(x)):
				corr_matrix[i][j] = cov[i][j]/(var[i]*var[j])
			corr_matrix[i][i] = 1
		return corr_matrix



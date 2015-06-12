# squares the given number
def square(x):
	return x**2

# finds the variance of a list
def variance(x):
	mean = sum(x)/len(x)
	mean_sq = mean **2
	var = 0
	for val in x:
		var += val**2 - mean_sq
	return var/len(x)
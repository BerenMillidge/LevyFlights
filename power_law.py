#functions for the power law distribution


from __future__ import division
import numpy as np
from stats import *


#returns the probabiliy of a point given the power law
def power_law(x, alpha,xmin):
	norm = (alpha-1)/xmin
	power = (x/xmin)**(-1*alpha)
	if (np.isnan(norm*power)):
		print "Potential nan encountered in power law"
		print "x: ", x
		print "alpha: ", alpha
		print "xmin: " , xmin
		print "norm: " , norm
		print "power: " , power
		return 0
	return norm*power


#hill estimator
def alpha_MLE(data, xmin):
	assert xmin>0, 'Minimum value must be greater than zero'
	data = data_above_xmin(data, xmin)
	N = len(data)
	#do the main sum
	MLE_sum = 0
	for i in xrange(N):
		MLE_sum += np.log(data[i]/xmin)
	return 1 + (N * (1/MLE_sum))


def MLE_error(data,xmin):
	N = len(data)
	a = alpha_MLE(data, xmin)
	error = (a - 1)/np.sqrt(N)
	return a, error

def MLE_error(alpha, N):
	return (alpha-1)/np.sqrt(N)


def power_law_cdf(data, alpha, xmin):
	N = len(data)
	ps = []
	ps_index = -1
	for i in range(N):
		x = data[i]
		if x >=xmin:
			p = power_law(x, alpha, xmin)
			if ps_index>=0:
				p+=ps[ps_index]
				ps.append(p)
				ps_index+=1

	ps = np.array(ps)
	return ps

def power_law_pdf(data, alpha, xmin):
	ps = []
	for i in xrange(len(data)):
		if(data[i])>=xmin:
			ps.append(power_law(data[i], alpha, xmin))
	ps = np.array(ps)
	ps = normalise_distribution(ps)
	return ps

def data_cdf(data,xmin):
	
	pos_data = data_above_xmin(data, xmin)
	N = len(pos_data)
	total = sum(pos_data)
	pos_data = pos_data/total
	for i in range(N-1):
		pos_data[i+1] = pos_data[i] + pos_data[i+1]
	return pos_data

def data_above_xmin(data, xmin):
	pos_data= []
	for i in xrange(len(data)):
		if(data[i]>=xmin):
			pos_data.append(data[i])
	pos_data = np.array(pos_data)
	return pos_data



def find_xmin(data, min_xmin=0, max_xmin=None):
# also need a principled way to calculate the xmin so let's figure this out - it uses the minimising
# the distance between power law model and empirical data, so hopefully not too horendous

	if max_xmin is None:
		max_xmin = np.max(data)

		# go through all possible xmins
	best_xmin = 0
	Kss = []
	for xmin in range(min_xmin, max_xmin):
		alpha = alpha_MLE(data, xmin)
		KS = KS_test(data, alpha, xmin)
		Kss.append(KS)
		if KS <=np.min(Kss):
			best_xmin=xmin

	return xmin



def sample_power_law(N, alpha):
	return np.random.power(alpha, size=N)

def sample_power_law_test(N, alpha):
	samps = np.random.uniform(low=0, high=1, size=N)
	return np.power((1-samps), (-1/alpha-1))
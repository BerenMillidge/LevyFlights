#functions for the exponential distribution

from __future__ import division
import numpy as np
from stats import *


def sample_exponential_mine(N,l):
	samps = np.random.uniform(low=0, high=1, size=N)
	return -1* (1/l) * np.log(1-samps)


def MLE_lambda(data):
	# it's just the reciprocal of the mean!
	return 1/np.mean(data)


def exponential_pdf(data, l):
	ps = []
	for i in xrange(len(data)):
		res = l * np.exp(-1*l*data[i])
		ps.append(res)
	ps = np.array(ps)
	ps = normalise_distribution(ps)
	return ps
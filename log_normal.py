#functions for the log normal distibution tests

from __future__ import division
import numpy as np
from stats import *


def sample_lognormal(N, mu, variance):
	return np.random.lognormal(mu, variance, N)


def sample_lognormal_mine(N, mu, variance):
	samps = []
	length = N//2
	for i in xrange(length):
		u1 = np.random.uniform(low=0, high=1)
		u2 = np.random.uniform(low=0, high=1)
		p = np.sqrt(-2*variance * np.log(1-u1))
		theta = 2 * np.pi * u2
		x1 = np.exp(p*np.sin(theta))
		x2 = np.exp(p*np.cos(theta))
		samps.append(x1)
		samps.append(x2)

	samps = np.array(samps)
	if len(samps)<N:
		diff = N-samps
		for i in xrange(diff):
			u1 = np.random.uniform(low=0, high=1)
			u2 = np.random.uniform(low=0, high=1)
			p = np.sqrt(-2*variance * np.log(1-u1))
			theta = 2 * np.pi * u2
			x1 = np.exp(p*np.sin(theta))
			x2 = np.exp(p*np.cos(theta))
			samps.append(x1)
		samps = np.array(samps)
	return samps
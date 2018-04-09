
from __future__ import division
import numpy as np
#get gaussian error function erf
from scipy.special import erf
from gaussian import *
from test import *
from log_normal import *
from plotting import *
from power_law import *
from exponential import *

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




def KS_test(data, alpha, xmin):
	cdf = power_law_cdf(data, alpha,xmin)
	dist = data_cdf(data, xmin)
	return np.max(np.abs(dist - cdf))


def weighted_KS(data, alpha, xmin):
	cdf = power_law_cdf(data, alpha, xmin)
	dist = data_cdf(data, xmin)
	#create diffs array by loop!
	diffs = []
	assert len(cdf)==len(dist), 'Distibutions must be of same length'
	for i in range(len(cdf)):
		num = np.abs(cdf[i] - dist[i])
		denom = np.sqrt(dist[i] * (1-dist[i]))
		diff = num/denom
		diffs.append(diff)

	diffs = np.array(diffs)
	return np.max(diffs)


def log_likelihood_ratio(dist1, dist2):
	# here the distributions are assumed to simply be 
	#approximated by vectors of probabilities
	assert len(dist1)==len(dist2), 'Distributions must have the same length'
	ratio = 0
	for i in range(len(dist1)):
		ratio += (np.log(dist1[i]) - np.log(dist2[i]))
	return ratio
	# in log space it's a simple sun of subtraction isntead of a product of divisions

def log_likelihood_variance(dist1, dist2):
	N = len(dist1)
	assert N ==len(dist2), 'distributions must have same length'
	#take logs
	dist1 = np.log(dist1)
	dist2 = np.log(dist2)

	#procede as normal!
	mu1 = np.mean(dist1)
	mu2 = np.mean(dist2)
	total = 0
	for i in range(N):
		total += ((dist1[i]-dist2[i])-(mu1-mu2))**2
	return total/N

# I need to begin being able to calculate log likelyhood ratios

def normalised_log_likelihood_ratio(ratio,N,std):
	assert ratio>=0,'Ratio must be positive'
	if ratio==0:
		ratio=-10*100
	ratio = np.log(ratio)
	return np.sqrt(N) * ratio * std

def likelihood_ratio_p_value(ratio, variance, N):
	num = np.abs(ratio)
	denom = np.sqrt(2*np.pi*variance)
	normalised_ratio = num/denom
	p = 1-erf(normalised_ratio)
	return p, ratio




def log_likelihood_test(dist1, dist2):
	print len(dist1)
	print len(dist2)
	assert len(dist1)==len(dist2), 'Distributions compared must have same length'
	N = len(dist1)
	ratio = log_likelihood_ratio(dist1, dist2)
	variance =log_likelihood_variance(dist1, dist2)
	print "Log likelihood variance: ", variance
	return likelihood_ratio_p_value(ratio, variance, N)



def normalise_distribution(dist):
	total = np.sum(dist)
	norm_dist = dist/total
	# it does work, it's just a float 1.0 instead of integer 1
	#if sum(norm_dist)!=1:
	#	print "distribution failed to normalise properly"
	#	print "Sum! " ,sum(norm_dist)
	return norm_dist


if __name__=='__main__':
	data, n,bins,patches = get_saccade_distances('fixaton_scanpaths',return_hist_data=True)
	plot_saccade_distances(n, bins)

	N = len(data)
	xmin = 0.0001
	alpha = alpha_MLE(data,xmin)
	print "Alpha MLE calculated: " , alpha
	alpha_error = (alpha-1)/(np.sqrt(N))
	print "Alpha error" , alpha_error
	power_law = power_law_pdf(data, alpha, xmin)
	gaussian, mu, variance = gaussian_probabilities(data, xmin=xmin)
	p, ratio = log_likelihood_test(power_law, gaussian)
	print "Likelihood ratio: ", ratio
	print "P-value: " , p

	power_law_samples = sample_power_law_test(N, alpha)
	gaussian_samples = sample_gaussian(N, mu, np.sqrt(variance))
	lognormal_samples = sample_lognormal_mine(N, mu,np.sqrt(variance))
	print "lognormal samples tests"
	print N
	print mu
	print variance
	print lognormal_samples
	l = MLE_lambda(data)
	exp_samples = sample_exponential_mine(N, l)
	exps = exponential_pdf(data, l)
	print "exps"
	print exps
	gaussian, mu, variance = gaussian_probabilities(data, xmin=None)
	p, ratio = log_likelihood_test(gaussian, exps)
	print "Log likelihood test for gaussian vs exponential"
	print "Likelihood ratio: ", ratio
	print "P-value", p

	plaw_n, plaw_bins, _ = plot_frequency_histogram(power_law_samples, bins)
	print "power law histogram frequencies"
	print plaw_n
	gauss_n, gauss_bins, _ = plot_frequency_histogram(gaussian_samples,bins)
	print "gaussian histogram frquencies"
	print gauss_n
	lognorm_n, lognorm_bins, _ =plot_frequency_histogram(lognormal_samples, bins)
	print "log normal histogram frequencies"
	print lognorm_n
	exp_n, exp_bins,_ = plot_frequency_histogram(exp_samples,bins)
	print "exponential histogram frequencies"
	print exp_n
	plot_all_loglog(n, bins, power_law_samples, gaussian_samples, lognormal_samples, exp_samples)


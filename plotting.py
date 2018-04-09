#plotting functions to generate the various graphs!

import numpy as np
import matplotlib.pyplot as plt

def plot_saccade_distances(n,bins):
	fig = plt.figure()
	plt.loglog(bins[0:len(bins)-1], n, label='Saccade distance distribution frequency')
	plt.title('The frequency of saccade distances by distance')
	plt.xlabel('Log distance between saccades in pixels')
	plt.ylabel('Log number of saccades observed')
	plt.legend()
	fig.tight_layout()
	plt.show()
	return

def plot_all_loglog(n, bins, plaw_n,gauss_n, lognorm_n, exp_n):
	bins = bins[0:len(bins)-1]
	fig = plt.figure()
	plt.loglog(bins,n, label='Data frequencies')
	plt.loglog(bins, plaw_n, label='Power law frequencies')
	plt.loglog(bins, gauss_n,label='Gaussian frequencies')
	plt.loglog(bins, lognorm_n, label='Log normal frequencies')
	plt.loglog(bins, exp_n, label='Exponential frequencies')
	plt.title('Log-log plot of the data and various fitted distibutions')
	plt.xlabel('Log distance (in pixels) between fixations')
	plt.ylabel('Log number of fixations')
	plt.legend()
	fig.tight_layout()
	plt.show()
	return

def plot_frequency_histogram(samples, bins):
	fig = plt.figure()
	n, dist_bins, _ = plt.hist(samples, bins=bins)
	plt.title('Histogram of distribution frequencies vs distance')
	plt.xlabel('Saccade distance')
	plt.ylabel('Distribution sample frequency')
	fig.tight_layout()
	plt.show()
	return n, dist_bins, _
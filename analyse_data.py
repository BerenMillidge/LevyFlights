
#script for exploratory data analysis of the FixaTons dataset

from __future__ import division
import FixaTons as FT
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt

def tests():

	print FT.list.datasets()
	print FT.list.stimuli('SIENA12')

	DATASET_NAME = 'SIENA12'
	STIMULUS_NAME = 'land.jpg'
	SUBJECT_ID = 'GT_10022017'

	stimulus_matrix = FT.get.stimulus(DATASET_NAME, STIMULUS_NAME)
	saliency_map_matrix = FT.get.saliency_map(DATASET_NAME, STIMULUS_NAME)
	fixation_map_matrix = FT.get.fixation_map(DATASET_NAME, STIMULUS_NAME)

	print 'Stimulus dims = ', stimulus_matrix.shape
	print "saliency map dims = ", saliency_map_matrix.shape
	print "fixation map matrix = ", fixation_map_matrix.shape

	scanpath = FT.get.scanpath(DATASET_NAME, STIMULUS_NAME, subject = SUBJECT_ID)
	print scanpath.shape
	print scanpath
	print "this scanpath has ", len(scanpath), "fixations."

	#show the map
	FT.show.map(DATASET_NAME, STIMULUS_NAME, showSalMap=True, showFixMap=False, wait_time=5000, plotMaxDim=1024)

	#show a single scanpath
	FT.show.scanpath(DATASET_NAME, STIMULUS_NAME, subject=SUBJECT_ID,
		animation=True, wait_time=0, putLines=True, putNumbers = True,
		plotMaxDim=1024)

def show_map(dataset_name, stimulus_name):
	FT.show.map(dataset_name, stimulus_name, showSalMap=True, showFixMap=False, wait_time=5000, plotMaxDim=1024)
	return

def show_scanpath(dataset_name, stimulus_name, subject_id):
	FT.show.scanpath(dataset_name, stimulus_name, subject=subject_id,
		animation=True, wait_time=0, putLines=True, putNumbers = True,
		plotMaxDim=1024)
	return



def save(obj, fname):
	pickle.dump(obj, open(fname, 'wb'))


def load(fname):
	return pickle.load(open(fname, 'rb'))

def get_stimuli_info():
	datasets = FT.list.datasets()
	stimuli = []
	for dataset in datasets:
		stims = FT.list.stimuli(dataset)
		print "Num stimuli in dataset " + dataset + "  : " + str(len(stims))

def get_subject_info():
	scanpaths = load('fixaton_scanpaths')
	datasets = FT.list.datasets()
	subjects_per_dataset = {}
	for dataset in datasets:
		subjects =[]
		for scanpath in scanpaths:
			if scanpath['dataset'] == dataset:
				subjects.append(scanpath['subject_id'])

		subjects = np.array(subjects)
		subjects_per_dataset[dataset] = subjects

	print subjects_per_dataset
	for dataset in datasets:
		print "dataset: ", dataset
		print "num subjects: ", str(len(subjects_per_dataset[dataset]))
	save(subjects_per_dataset, 'subjects_per_dataset')

def get_num_scanpaths_and_fixations():
	scanpaths = load('fixaton_scanpaths')
	datasets = FT.list.datasets()
	for dataset in datasets:
		fixations = 0
		paths = 0
		for scanpath in scanpaths:
			if scanpath['dataset'] == dataset:
				fixations += len(scanpath['scanpath'])
				#print scanpath['scanpath'][0]
				paths +=1
		print "dataset: " + dataset
		print "num scanpaths: " + str(paths)
		print "num fixations: " + str(fixations)


def save_all_scanpaths():
	datasets = FT.list.datasets()
	#create a stimuli object for this
	stimuli = []
	for dataset in datasets:
		stims = FT.list.stimuli(dataset)
		for stim in stims:
			stimuli.append((stim, dataset))

	print stimuli

	#now get it
	scanpaths = []
	for stimulus in stimuli:
		stim, dataset = stimulus
		subjects = FT.list.subjects(dataset, stim)
		for subject in subjects:
			#create  a scanpath object with requisite metadata
			scanpath = {}
			scanpath['dataset'] = dataset
			scanpath['stimulus'] = stimulus
			scanpath['subject_id'] = subject
			scanpath['scanpath'] = FT.get.scanpath(dataset, stim, subject = subject)
			scanpaths.append(scanpath)

	#now I need to save the scanpaths
	print "scanpaths: ", len(scanpaths)
	save(scanpaths, 'fixaton_scanpaths')

def investigate_scanpath_lengths(scanpath_fname,save_name=None):
	scanpaths = load(scanpath_fname)
	lengths = []
	#do a loop
	for scanpath in scanpaths:
		sh = scanpath['scanpath'].shape
		assert sh[1]==4, 'Scanpath data is incomplete'
		lengths.append(sh[0]) # as that's the one
	lengths = np.array(lengths)
	avg = np.mean(lengths)
	var = np.var(lengths)
	print "Number of scanpaths: " , len(lengths)
	print "mean scanpath length: ", avg
	print "variance of scanpath lengths", var
	print "standard deviation of scanpath lengths", np.sqrt(var)

	#save
	if save_name is not None:
		np.save(save_name, lengths)
	#plot the histogram
	plt.hist(lengths)
	plt.title('Histogram of lengths of the scanpaths')
	plt.xlabel('Length of scanpath (in fixations)')
	plt.ylabel('Number of scanpaths')
	plt.show()


def euclidean_distance(p1, p2):
	assert len(p1)==len(p2), 'points must be of same dimension'
	total = 0
	for i in range(len(p1)):
		total += np.square(p1[i] - p2[i])
	return np.sqrt(total)

def euclidean_distance_unsafe(p1, p2):
	return np.sqrt(np.sum(np.square(p1-p2)))


# this ignores the timing info. Not sure how useful that is?
def get_saccade_distances(scanpath_fname, plot=True, save_name=None, info=True, return_hist_data=False):
	scanpaths = load(scanpath_fname)
	distances = []
	for scanpath in scanpaths:
		paths = scanpath['scanpath']
		length = paths.shape[0]
		for i in xrange(length-1):
			path1 = paths[i]
			p1 = path1[0:1]
			path2 = paths[i+1]
			p2 = path2[0:1]
			#append the distance
			dist = euclidean_distance(p1, p2)
			if dist <=10000:
				distances.append(dist)
			#distances.append(euclidean_distance(p1,p2))

	distances = np.array(distances)

	if info:
		length = len(distances)
		print "Number of scanpath distances calculated: ", length
		mean = np.mean(distances)
		print "Mean scanpath distance: " , mean
		variance = np.var(distances)
		print "Variance of scanpath distance: " , variance
		std = np.sqrt(variance)
		print "Standard deviation of scanpath distance: ", std
		max_distance = np.max(distances)
		print "Maximum scanpath distance: ", max_distance
		min_distance = np.min(distances)
		print "Minumum scanpath distance: ", min_distance
	
	#plot if necessary
	if plot:
		#n,bins,patches = plt.hist(distances, bins=15)
		#log_bins = np.logspace(np.log(0.01), np.log(2700),20)
		#print log_bins
		log_bins=20
		fig = plt.figure()
		n, bins, patches = plt.hist(distances, bins=log_bins)
		plt.title('Distribution of distances between successive scan paths')
		plt.xlabel('Distance in pixels between fixation')
		plt.ylabel('Frequency of occurence')
		fig.tight_layout()
		plt.show()

	if save_name is not None:
		np.save(save_name, distances)

	if return_hist_data:
		return distances, n,bins,patches

	return distances


def get_fixation_durations(scanpath_fname, plot=True, save_name=None, info=True, return_hist_data=False):
	scanpaths = load(scanpath_fname)
	differences = []
	for scanpath in scanpaths:
		paths = scanpath['scanpath']
		length = paths.shape[0]
		for i in xrange(length):
			path = paths[i]
			differences.append(path[3] - path[2])

	differences = np.array(differences)

	if info:
		length = len(differences)
		print "Number of fixation durations calculated: " , length
		mean = np.mean(differences)
		print "Mean duration of fixation: " , mean
		var = np.var(differences)
		print "Variance of fixation durations: " , var
		std = np.sqrt(var)
		print "Standard deviation of fixation durations: " , std
		max_duration = np.max(differences)
		print "Maximum fixation duration: " , max_duration
		min_duration = np.min(differences)
		print "Minumum fixation duration: " , min_duration

	if plot:
		n, bins, patches = plt.hist(differences)
		plt.title('Distribution of fixation durations')
		plt.show()

	if save_name is not None:
		np.save(save_name, differences)

	if return_hist_data:
		return differences, n,bins,patches

	return differences


def get_scanpath_durations(scanpath_fname, plot=True, save_name=None, info=True):
	scanpaths = load(scanpath_fname)
	differences = []
	for scanpath in scanpaths:
		paths = scanpath['scanpath']
		length = paths.shape[0]
		first = paths[0]
		last = paths[length-1]
		differences.append(last[3] - first[2])

	differences = np.array(differences)

	if info:
		length = len(differences)
		print "Number of scanpath durations calculated: " , length
		mean = np.mean(differences)
		print "Mean duration of scanpaths: " , mean
		var = np.var(differences)
		print "Variance of scanpath durations: " , var
		std = np.sqrt(var)
		print "Standard deviation of scanpath durations: " , std
		max_duration = np.max(differences)
		print "Maximum scanpath duration: " , max_duration
		min_duration = np.min(differences)
		print "Minumum scanpath duration: " , min_duration

	if plot:
		plt.hist(differences)
		plt.title('Distribution of scanpath durations')
		plt.show()

	if save_name is not None:
		np.save(save_name, differences)

	return differences


def get_middle_of_bins(bins):
	middles = []
	for i in xrange(len(bins)-1):
		start = bins[i]
		end = bins[i+1]
		div = (end - start)/2
		middle = start + div
		middles.append(middle)

	middles = np.array(middles)
	return middles

def log(x):
	#our safer log function
	for i in xrange(len(x)):
		if(x[i]==0):
			x[i]=0
		else: 
			x[i] = np.log(x[i])
	return x


def log_log_plot_mine(x,y, xlabel, ylabel, title):
	print "In log log plot"
	print x
	print y
	#x = np.log(np.log(x))
	#y = np.log(np.log(y))
	x =log(x)
	y=log(y)
	print x
	print y
	fig = plt.figure()
	plt.plot(x,y)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.show()


def log_log_plot(x,y, xlabel, ylabel,title):
	fig = plt.figure()
	plt.loglog(x,y)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.show()



if __name__ =='__main__':
	
	investigate_scanpath_lengths('fixaton_scanpaths')
	get_stimuli_info()
	get_subject_info()
	get_num_scanpaths_and_fixations()

	distances = get_saccade_distances('fixaton_scanpaths')
	durations = get_fixation_durations('fixaton_scanpaths')
	durations = get_scanpath_durations('fixaton_scanpaths')
	distances, n,bins,patches = get_saccade_distances('fixaton_scanpaths',return_hist_data=True)
	#print type(n)
	#print len(n)
	#print type(bins)
	#print len(bins)
	#print type(patches)
	#print len(patches)
	#middles = get_middle_of_bins(bins)
	#print bins
	#print bins[0:len(bins)-2]
	#middles = bins[0:len(bins)-1]
	#print type(middles)
	#print len(middles)
	#log_log_plot_mine(middles, n, 'Log Distance between saccades', 'Log Number of saccades','Log log plot of distance between saccades vs number of saccades')
	#plt.loglog(bins[0:len(bins)-1], n)
	#plt.show()
import numpy as np

biquad = np.genfromtxt('./bqrcfir.csv', delimiter=',')[2::]
#	reshape to regroup rectangular impulses by rising + falling edge, per each axis
biquad = biquad.reshape((biquad.size / 12, 3, 2, 2))
biquad_times = np.array([ [ 1e6 * (edges[1][0] - edges[0][0]) for edges in axis ] for axis in biquad ])
biquad_means = np.array([ np.mean(biquad_times[:,axis]) for axis in np.arange(3) ])
biquad_stds = np.array([ np.std(biquad_times[:,axis]) for axis in np.arange(3) ])
biquad_mean_total = np.mean(biquad_times)
biquad_std_total = np.std(biquad_times)

fkf = np.genfromtxt('./fkf.csv', delimiter=',')[2::]
fkf = fkf.reshape((fkf.size / 12, 3, 2, 2))
fkf_times = np.array([ [ 1e6 * (edges[1][0] - edges[0][0]) for edges in axis ] for axis in fkf ])
fkf_means = np.array([ np.mean(fkf_times[:,axis]) for axis in np.arange(3) ])
fkf_stds = np.array([ np.std(fkf_times[:,axis]) for axis in np.arange(3) ])
fkf_mean_total = np.mean(fkf_times)
fkf_std_total = np.std(fkf_times)

per_axis_slowdowns = 100 * (fkf_means - biquad_means) / biquad_means
average_slowdown = 100 * (fkf_mean_total - biquad_mean_total) / biquad_mean_total

print 'Biquad RC+FIR2:\tROLL\tPITCH\tYAW'
print 'mean (us)\t', '\t'.join([ '%.4f' % val for val in biquad_means ])
print 'std (us)\t', '\t'.join([ '%.4f' % val for val in biquad_stds ])
print 'total mean (us)\t', '%.4f' % biquad_mean_total
print 'total std (us)\t', '%.4f' % biquad_std_total
print
print 'FKF:\t\tROLL\tPITCH\tYAW'
print 'mean (us)\t', '\t'.join([ '%.4f' % val for val in fkf_means ])
print 'std (us)\t', '\t'.join([ '%.4f' % val for val in fkf_stds ])
print 'total mean (us)\t', '%.4f' % fkf_mean_total
print 'total std (us)\t', '%.4f' % fkf_std_total
print
print 'FKF slowdown:\t', '\t'.join([ '%.2f%%' % percent for percent in per_axis_slowdowns ])
print 'FKF average slowdown:\t', '%.2f%%' % average_slowdown
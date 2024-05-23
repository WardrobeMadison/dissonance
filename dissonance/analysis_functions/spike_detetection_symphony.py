# spikeResults = SpikeDetector(response);
# spikeIndices = spikeResults.sp;

# [fresponse, noise] = obj.filterResponse(response);
# ax = gca();
# if(ax ~= obj.handles.primaryAxes)
# weight = noise;
# % thresholding the spikes
# thresholdedSpikes = abs(fresponse(spikeIndices)) >= abs(weight * obj.threshold);
# else
# weight = 1;
# % thresholding the spikes
# thresholdedSpikes = abs(response(spikeIndices)) >= abs(weight * obj.threshold);
# end
# spikeIndices = spikeIndices(thresholdedSpikes);

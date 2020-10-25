import bisect
from matchms.filtering import normalize_intensities
from matchms.filtering import require_minimum_number_of_peaks
from matchms.filtering import select_by_mz
from matchms.filtering import select_by_relative_intensity
#from matchms.filtering import reduce_to_number_of_peaks
#from matchms.filtering import add_losses

class Filter:
    def filter(self, spectrums, verbose=True):
        filtered = []
        # apply filters to each spectrum
        for s in spectrums:
            s = normalize_intensities(s)
            s = select_by_mz(s, mz_from=0, mz_to=1000)
            s = require_minimum_number_of_peaks(s, n_required=10)
            s = select_by_relative_intensity(s, intensity_from=0.01, intensity_to=1.0)
            if s is not None and self.has_frag(s, s.metadata['precursor_mz'], 0.2):
                filtered.append(s)
        if verbose:
            print( "Filtered %d down to %d" % ( len(spectrums), len(filtered) ) )
        return filtered


    # a new filter to check if there is a fragment within N ppm of the precursor
    def has_frag(spectrum, mz, tol, tol_units='absolute'):
        if tol_units == 'ppm':
            di = tol * mz / 1e6
        else:
            di = tol
        min_mz = mz - di
        max_mz = mz + di
        pos = bisect.bisect_right(spectrum.peaks[0], min_mz)
        pos2 = bisect.bisect_right(spectrum.peaks[0], max_mz)
        return pos != pos2
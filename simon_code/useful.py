class Peak(object):
    def __init__(self, mz, intensity):
        self.mz = mz
        self.intensity = intensity

def spec2peaks(spec):
    peaks = []
    for i,mz in enumerate(spec.peaks[0]):
        intensity = spec.peaks[1][i]
        peaks.append(Peak(mz, intensity))
    return peaks

def find_matches(peaks1, peaks2, ms2_tol):
    # find all the peaks in peaks that are within tol
    matches = []
    for p1 in peaks1:
        for p2 in peaks2:
            if abs(p1.mz - p2.mz) < ms2_tol:
                matches.append((p1,p2,p1.intensity*p2.intensity))
    matches.sort(key = lambda x: x[2], reverse = True)
    return matches
    
def normalise_peaks(peaks):
    max_intensity = max([p.intensity for p in peaks])
    new_peaks = []
    for peak in peaks:
        new_peaks.append(Peak(peak.mz, peak.intensity / max_intensity))
    return new_peaks

def greedy_cosine(spec1, spec2, ms2_tol=0.2, normalise = False):
    peaks1 = spec2peaks(spec1)
    peaks2 = spec2peaks(spec2)

    if normalise:
        peaks1 = normalise_peaks(peaks1)
        peaks2 = normalise_peaks(peaks2)


    
    matches = find_matches(peaks1, peaks2, ms2_tol)
    
    
    length1 = sum([p.intensity**2 for p in peaks1])
    length2 = sum([p.intensity**2 for p in peaks2])
    
    used = set()
    cos = 0
    n_matches = 0
    for p1, p2, i_prod in matches:
        if not p1 in used and not p2 in used:
            cos += i_prod
            used.add(p1)
            used.add(p2)
            n_matches += 1
    result = (n_matches, cos/(np.sqrt(length1)*np.sqrt(length2)))
    return result

def pass_cosine(spec1, spec2, ms2_tol=0.2, normalise = False):
    peaks1 = spec2peaks(spec1)
    peaks2 = spec2peaks(spec2)
    
    if normalise:
        peaks1 = normalise_peaks(peaks1)
        peaks2 = normalise_peaks(peaks2)

    length1 = sum([p.intensity**2 for p in peaks1])
    length2 = sum([p.intensity**2 for p in peaks2])


    n_matches = 0
    cos = 0
    for p1 in peaks1:
        best_match = None
        for p2 in peaks2:
            if abs(p1.mz - p2.mz) < ms2_tol:
                if best_match is None:
                    best_match = p2
                elif p2.intensity > best_match.intensity:
                    best_match = p2
        if best_match is not None:
            n_matches += 1
            cos += p1.intensity * best_match.intensity
    
    result = (n_matches, cos/(np.sqrt(length1)*np.sqrt(length2)))
    return result

    
print(greedy_cosine(spectrums_query[1], spectrums_query[1], normalise=True))
print(pass_cosine(spectrums_query[1], spectrums_query[1]))
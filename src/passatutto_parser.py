import os

name_overwrites = {
    "INCHI_AUX": "inchiaux",
    "SpectrumFile": "source_file",
    "LibraryName": "library_membership",
    "compound": "compound_name",
    "formula": "formula_smiles",
    "ionization": "adduct",
    "parentmass": "parent_mass"
}

cast_to = {
    "parent_mass": float,
    "charge": int,
    "precursor_mz": float,
}

def parse_passatuto(ms_file):
    json_format = {}
    peaks = False
    peaks_json = []
    for line in open(ms_file):
        if peaks:
            peaks_json.append(list(map(float, line.split())))
        elif line.startswith(">collision"):
            peaks = True
        elif line.strip():
            try:
                key, value = line[1:].strip().split(' ', 1)
            except ValueError:
                key = line[1:].strip()
                value = 'N/A'
            except Exception as e:
                print(ms_file,line,e)
                continue
            key = name_overwrites.get(key, key.lower())
            if key in cast_to:
                value = cast_to[key](value)
            json_format[key] = value
    json_format["peaks_json"] = peaks_json
    return json_format

def parse_passatuto_folder(folder_path):
    spectrums = []
    ms_files = os.listdir(folder_path)
    for i, file in enumerate( ms_files ):
        if file.endswith(".ms"):
            spectrum = parse_passatuto(os.path.join(folder_path,file))
            spectrums.append(spectrum)
        if i and not i % 100:
            print( "processed %d files" % i )
    return spectrums


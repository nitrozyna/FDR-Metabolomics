import os

class PassatuttoParser:
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

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def _parse(self,ms_file):
        json_format = {}
        peaks = False
        peaks_json = []
        for line in open(ms_file):
            if line.startswith(">collision"):
                peaks = True
            elif peaks and line.strip():
                peaks_json.append(list(map(float, line.split())))
            elif line.strip():
                try:
                    key, value = line[1:].strip().split(' ', 1)
                except ValueError:
                    key = line[1:].strip()
                    value = 'N/A'
                except Exception as e:
                    print(ms_file,line,e)
                    continue
                key = self.name_overwrites.get(key, key.lower())
                if key in self.cast_to:
                    value = self.cast_to[key](value)
                json_format[key] = value
        json_format["peaks_json"] = peaks_json
        return json_format

    def parse_folder(self, verbose=True):
        spectrums = []
        ms_files = os.listdir(self.folder_path)
        for i, file in enumerate( ms_files ):
            if file.endswith(".ms"):
                spectrum = self._parse(os.path.join(self.folder_path,file))
                spectrums.append(spectrum)
            if verbose and i and not i % 100:
                print( "processed %d files" % i )
        if verbose:
            print( "Finished parsing of %d spectra " % (i+1))
        return spectrums

class DecoyParserPassattuto:
    name_overwrites = {
        "ACCESSION:": "source_file",
        "MS$FOCUSED_ION: PRECURSOR_M/Z": "precursor_mz",
        "MS$FOCUSED_ION: PRECURSOR_TYPE": "adduct",
        "CH$NAME:": "compound_name",
        "CH$FORMULA:": "formula_smiles",
        "CH$EXACT_MASS:": "exact_mass",
    }

    cast_to = {
        "parent_mass": float,
        "precursor_mz": float,
        "exact_mass": float,
    }

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def _parse(self,ms_file):
        json_format = {}
        peaks = False
        peaks_json = []
        for line in open(ms_file):
            if line.strip() == "//":
                continue
            if line.startswith("PK$PEAK"):
                peaks = True
            elif peaks and line.strip():
                peaks_json.append(list(map(float, line.split()[:2])))
            elif line.strip():
                try:
                    key, value = line.strip().rsplit(' ', 1)
                except ValueError:
                    key = line.strip()
                    value = 'N/A'
                except Exception as e:
                    print(ms_file,line,e)
                    continue
                key = self.name_overwrites.get(key, key.lower())
                if key in self.cast_to:
                    value = self.cast_to[key](value)
                json_format[key] = value
        json_format["peaks_json"] = peaks_json
        return json_format

    def parse_folder(self, verbose=True):
        spectrums = []
        files = os.listdir(self.folder_path)
        for i, file in enumerate( files ):
            if file.endswith(".txt"):
                try:
                    spectrum = self._parse(os.path.join(self.folder_path,file))
                    spectrums.append(spectrum)
                except Exception as e:
                    print(file,e)
            if verbose and i and not i % 100:
                print( "processed %d files" % i )
        if verbose:
            print( "Finished parsing of %d spectra " % (i+1))
        return spectrums
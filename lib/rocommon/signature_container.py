import os

# Location signature class: stores a signature characterizing one location


class LocationSignature:

    def __init__(self, no_bins=360):
        self.sig = [0] * no_bins
        self.idx = 0

    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

# --------------------- File management class ---------------


class SignatureContainer():

    def __init__(self, size=5, path='', no_bins=360):
        self.size = size  # max number of signatures that can be stored
        self.filenames = []
        self.no_bins = no_bins

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append(path + 'loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if not os.path.isfile(self.filenames[n]):
                break
            n += 1

        if (n >= self.size):
            return -1
        else:
            return n

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close()

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature(no_bins=self.no_bins)
        ls.idx = index + 1
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(float(s))
            f.close()
        else:
            print "WARNING: Signature does not exist."

        return ls

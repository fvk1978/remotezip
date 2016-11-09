#!/usr/bin/env python

from get_remote_file import HTTP

import struct, os, time, zlib
[false, true]= range(2)

ZipError= 'ZIP file format error'

# constants for Zip file compression methods
# (other ZIP compression methods not supported)

zipFormats= {
  'store': 0,
  'deflate': 8
}

def is_zip_archive(str):
    """checking the magic number. Will not accept a ZIP archive with an ending comment."""
    try:
        fpin = open(filename, "rb")
        fpin.seek(-22, 2)	# Seek to end-of-file record
        endrec = fpin.read()
        fpin.close()
        if endrec[0:4] == "PK\005\006" and endrec[-2:] == "\000\000":
            return true	# file has correct magic number
    except:
        pass
    return false

def zip2date(d):
    """Return (year, month, day) for a date in zip format"""
    return (d>>9)+1980, (d>>5)&0xF, d&0x1F

def zip2time(t):
    """Return (hour, minute, second) for a time in zip format"""
    return t>>11, (t>>5)&0x3F, t&0x1F * 2

def date2zip(year, month, day):
    """Return 16-bit zip date for year, month, day"""
    return (year - 1980) << 9 | month << 5 | day

def time2zip(hour, minute, second):
    """Return 16-bit zip time for hour, minute, second"""
    return hour << 11 | minute << 5 | second / 2

class ZipFile:
    """Class with methods to open, read, write, close, list zip files"""
    # Here are some struct module formats for reading headers
    structEndArchive = "<4s4H2lH"		# 9 items, end of archive, 22 bytes
    stringEndArchive = "PK\005\006"	# magic number for end of archive record
    structCentralDir = "<4s4B4H3i5H2i"	# 19 items, central directory, 46 bytes
    stringCentralDir = "PK\001\002"	# magic number for central directory
    structFileHeader = "<4s2B4H3i2H"	# 12 items, file header record, 30 bytes
    stringFileHeader = "PK\003\004"	# magic number for file header

    def __init__(self, url, compression = zipFormats['deflate']):
        """Construct a ZipFile instance and open the ZIP file named 'filename' with mode read 'r', write 'w' or append 'a'."""
        if compression not in zipFormats.values():
            raise ZipError, 'Unsupported compression type ' + "'" + str(compression) + "'"
        self.TOC = {}	# Table of contents for the archive
        self.compression = compression	# Method of compression
        self.url = url
        self.offset = 0 # position in the file
        
        self.http_file = HTTP(self.url)
        self._getTOC()

    def _getTOC(self):
        """Read in the table of contents for the zip file"""
        er_start = self.http_file.content_len - 22   # Start of end-of-archive record
        endrec = self.http_file.get(er_start, self.http_file.content_len)
        if endrec[0:4] != self.stringEndArchive or endrec[-2:] != "\000\000":
            raise ZipError, "File is not a zip file, or ends with a comment"
        endrec = struct.unpack(self.structEndArchive, endrec)
        size_cd = endrec[5]		# bytes in central directory
        offset_cd = endrec[6]	# offset of central directory
        x = self.http_file.content_len - 22 - size_cd
        concat = x - offset_cd	# zero, unless zip was concatenated to another file
        self.offset = offset_cd + concat	# Position of start of central directory
        total = 0
        flist = []		# List of file header offsets
        
        while total < size_cd:
            centdir = self.read(46)
            total = total + 46
            if centdir[0:4] != self.stringCentralDir:
                raise ZipError, "Bad magic number for central directory"
            
            centdir = struct.unpack(self.structCentralDir, centdir)
            fname = self.read(centdir[12])
            extra = self.read(centdir[13])
            comment = self.read(centdir[14])
            total = total + centdir[12] + centdir[13] + centdir[14]
            flist.append(centdir[18])	# Offset of file header record
            
        toc = self.TOC	# Table of contents
        for offset in flist:
            self.offset = offset + concat
            fheader = self.read(30)
            if fheader[0:4] != self.stringFileHeader:
                raise ZipError, "Bad magic number for file header"
            fheader = struct.unpack(self.structFileHeader, fheader)
            fname = self.read(fheader[10])
            extra = self.read(fheader[11])
            time = zip2time(fheader[5])
            date = zip2date(fheader[6])
            toc[fname] = (self.offset, extra) + fheader[3:10] + (date, time)
            
    def read(self, size):
        if size == 0:
            return ''
        result = self.http_file.get(self.offset, self.offset + size - 1)
        self.offset += size
        return result
    
    def file_list(self):
        return self.TOC.keys()

# read -- read a file from zip and pass its contents to a stream in chunks of default size 10K

    def get(self, name, directory = './', chunk= 10240):
        data = self.TOC[name]
        self.offset = data[0]
        
        nbytes = data[7]
        format = data[3]
        if format not in zipFormats.values():
            raise ZipError, 'Unsupported compression method ' + "'" + str(data[3]) + "'"
        
        if format == zipFormats['deflate']:
            dc = zlib.decompressobj(-15)
        
        path = directory + name
        dir, fname = os.path.split(path)
        self._mkdir(dir)
        file = open(path, 'w') 
        crc = 0
        while nbytes > 0:
            length = min(chunk, nbytes)
            bytes = self.read(length)
            if format == zipFormats['deflate']:
                bytes = dc.decompress(bytes)
            crc = zlib.crc32(bytes, crc)
            file.write(bytes)
            nbytes = nbytes - length
        
        if format == zipFormats['deflate']:
            bytes = dc.decompress('Z') + dc.flush()
            if bytes:
                crc = zlib.crc32(bytes, crc)
                file.write(bytes)
        
        file.close() 
        
        if crc!=data[6]:
            raise ZipError, 'Bad CRC for file ' + "'" + name + "'"
        
        return
    
    def _mkdir(self, newdir):
        """works the way a good mkdir should :)
            - already exists, silently complete
            - regular file in the way, raise an exception
            - parent directory(ies) does not exist, make them as well
        """
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("a file with the same name as the desired " \
                        "dir, '%s', already exists." % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head):
                self._mkdir(head)
            #print "_mkdir %s" % repr(newdir)
            if tail:
                os.mkdir(newdir)
            
            
if __name__ == "__main__":
    #z = ZipFile('http://forum.fvk:81/3scan.zip')
    z = ZipFile('http://forum.fvk:81/CloneCD4.2.0.2.zip')
    print "=%s=" % z.file_list()
    z.get('Key.diz')
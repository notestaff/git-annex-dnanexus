#!/usr/bin/env python

from __future__ import print_function
import subprocess
import time
import json
import sys
import os
import os.path

import dxpy
import dxpy.bindings
import dxpy.bindings.dxfile_functions
import dxpy.bindings.dxdataobject_functions
from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError
from annexremote import UnsupportedRequest

DX_URI_PFX='dx://'

class DNAnexusRemote(SpecialRemote):
    def initremote(self):
        # initialize the remote, eg. create the folders
        # raise RemoteError if the remote couldn't be initialized
        pass

    def prepare(self):
        # prepare to be used, eg. open TCP connection, authenticate with the server etc.
        # raise RemoteError if not ready to use
        pass

    def transfer_store(self, key, filename):
        # store the file in `filename` to a unique location derived from `key`
        # raise RemoteError if the file couldn't be stored
        raise RemoteError('Cannot yet store files')

    def _dbg(self, *args):
        self.annex.debug(' '.join(map(str, args)))

    def _url_to_dxid(self, url):
        return os.path.splitext(url[len(DX_URI_PFX):].split('/')[0])[0]

    def transfer_retrieve(self, key, filename):
        # get the file identified by `key` and store it to `filename`
        # raise RemoteError if the file couldn't be retrieved
        urls = self.annex.geturls(key=key, prefix=DX_URI_PFX)
        url = [url for url in urls if self.claimurl(url)][0]
        self._dbg('STANDALONE transfer-retrieve: key=', key, 'filename=', filename, 'urls=', urls, 'url=', url)
        try:
            cmd = 'dx download --no-progress ' + self._url_to_dxid(url) + " -f -o '" + filename + "'"
            self._dbg('cmd=', cmd)
            dxpy.bindings.dxfile_functions.download_dxfile(dxid=self._url_to_dxid(url), filename=filename)
        except Exception as dx_exc:
            raise RemoteError('transfer_retrieve: Error running dx download cmd {}: {}'.format(cmd, dx_exc))

    def checkpresent(self, key):
        # return True if the key is present in the remote
        # return False if the key is not present
        # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error
        self._dbg('CHECKING PRESENCE OF KEY ', key)

        return any([self.checkurl(url) for url in self.annex.geturls(key=key, prefix=DX_URI_PFX)])
        #raise RemoteError('Cannot yet check by key')

    def whereis(self, key):
        self._dbg('WHEREIS: key=', key, 'urls=', self.annex.geturls(key=key,prefix=DX_URI_PFX))
        raise UnsupportedRequest('Not supporting whereis yet')
        
    def remove(self, key):
        # remove the key from the remote
        # raise RemoteError if it couldn't be removed
        # note that removing a not existing key isn't considered an error
        raise RemoteError('Cannot yet remove keys')

    def claimurl(self, url):
        return url.startswith(DX_URI_PFX)

    def checkurl(self, url):
        if not self.claimurl(url): raise RemoteError('Cannot check non-dx URL {}'.format(url))
        try:
            descr = dxpy.bindings.dxdataobject_functions.describe(self._url_to_dxid(url))
        except Exception as describe_exc:
            raise RemoteError('Could not run dx describe for {}: {}'.format(url, describe_exc))
        url_ext = os.path.splitext(url)[1]
        file_ext = os.path.splitext(descr['name'])[1]
        if url.endswith('/'):
            return [dict(size=descr['size'], filename=descr['name'],
                         url=url+descr['name'])]
        if url_ext == file_ext  or  True:
            return [dict(size=descr['size'], filename=descr['name'])]
        else:
            return [dict(size=descr['size'], filename=descr['name'],
                         url=url+file_ext)]

# end: class DNAnexusRemote(SpecialRemote)

# In your ``main`` function, link your remote to the master class and initialize the protocol:

def main():
    master = Master()
    remote = DNAnexusRemote(master)
    master.LinkRemote(remote)
    master.Listen()

if __name__ == "__main__":
    main()


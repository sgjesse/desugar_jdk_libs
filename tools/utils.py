# Copyright (c) 2019, the R8 project authors. Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

from shutil import rmtree
import tempfile

class TempDir(object):
 def __init__(self, prefix='', delete=True):
   self._temp_dir = None
   self._prefix = prefix
   self._delete = delete

 def __enter__(self):
   self._temp_dir = tempfile.mkdtemp(self._prefix)
   return self._temp_dir

 def __exit__(self, *_):
   if self._delete:
     rmtree(self._temp_dir, ignore_errors=True)


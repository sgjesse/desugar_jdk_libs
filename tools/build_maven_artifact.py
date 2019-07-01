#!/usr/bin/env python
# Copyright (c) 2017, the R8 project authors. Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.

import argparse
import hashlib
from os import makedirs
from os.path import join
from shutil import copyfile, make_archive
import sys
from string import Template
import utils

POMTEMPLATE = Template(
"""<project
    xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.android.tools</groupId>
  <artifactId>desugar_jdk_libs</artifactId>
  <version>$version</version>
  <name>Small subset of OpenJDK libraries</name>
  <description>
    This project contains a small subset of OpenJDK libraries simplified for use on older runtimes.

    This is not an official Google product.
  </description>
  <url>https://github.com/google/desugar_jdk_libs</url>
  <inceptionYear>2018</inceptionYear>
  <licenses>
    <license>
      <name>The GNU General Public License (GPL)</name>
      <url>https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html</url>
      <distribution>repo</distribution>
    </license>
  </licenses>
  <scm>
    <url>
      https://github.com/google/desugar_jdk_libs
    </url>
  </scm>
</project>
""")

NAME = 'desugar_jdk_libs'

def determine_version():
  # TODO(sgjesse): Handle this in a beter way.
  return '1.0.0'

def get_maven_path(version):
  return join('com', 'android', 'tools', 'desugar_jdk_libs', version)

def write_pom_file(version, pom_file):
  version_pom = POMTEMPLATE.substitute(version=version)
  with open(pom_file, 'w') as file:
    file.write(version_pom)

def hash_for(file, hash):
  with open(file, 'rb') as f:
    while True:
      # Read chunks of 1MB
      chunk = f.read(2 ** 20)
      if not chunk:
        break
      hash.update(chunk)
  return hash.hexdigest()

def write_md5_for(file):
  hexdigest = hash_for(file, hashlib.md5())
  with (open(file + '.md5', 'w')) as file:
    file.write(hexdigest)

def write_sha1_for(file):
  hexdigest = hash_for(file, hashlib.sha1())
  with (open(file + '.sha1', 'w')) as file:
    file.write(hexdigest)

def run(jar, out):
  # Create directory structure for this version.
  version = determine_version()
  with utils.TempDir() as tmp_dir:
    version_dir = join(tmp_dir, get_maven_path(version))
    makedirs(version_dir)
    # Write the pom file.
    pom_file = join(version_dir, NAME + '-' + version + '.pom')
    write_pom_file(version, pom_file)
    # Copy the jar to the output.
    target_jar = join(version_dir, NAME + '-' + version + '.jar')
    copyfile(jar, target_jar)
    # Create check sums.
    write_md5_for(target_jar)
    write_md5_for(pom_file)
    write_sha1_for(target_jar)
    write_sha1_for(pom_file)
    # Zip it up - make_archive will append zip to the file, so remove.
    assert out.endswith('.zip')
    base_no_zip = out[0:len(out)-4]
    make_archive(base_no_zip, 'zip', tmp_dir)

def parse_options(argv):
  result = argparse.ArgumentParser()
  result.add_argument('--jar', help='The jar file with the library')
  result.add_argument('--out', help='The zip file to output')
  return result.parse_args(argv)

def main(argv):
  options = parse_options(argv)
  jar = options.jar
  out = options.out
  if jar == None:
    print 'Need to supply jar with --jar.'
    exit(1)
  if out == None:
    print 'Need to supply output zip with --out.'
    exit(1)
  run(jar, out)

if __name__ == "__main__":
  exit(main(sys.argv[1:]))
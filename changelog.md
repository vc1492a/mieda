# Changelog
All notable changes to `mieda` will be documented in this Changelog.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) 
and adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.0.2 
### Added 
- Code that allows intervals in isolation to be added to the directed graph. 
- A parameter that allows the graph object (a NetworkX directed graph) 
to be returned from `Merge.union` instead of a list of intervals (thanks 
for the suggestion [Mark Hoffmann](https://github.com/mark-hoffmann)). 
- Tests for new features, possible scenarios such as duplicate intervals 
used in the input, and additional input types (integer and string indices).

### Changed 
- Updated the readme to include the bump to version `0.0.2`, examples on 
using MIEDA with integer or string indices, and a small change in 
format. The newly updated code also includes handling for duplicate 
input intervals. 
- Updated Jupyter notebooks in the `notebooks` directory, which contains 
examples against some identified use cases and speed profiling code.

## 0.0.1
### Added

- `mieda/intervals.py`, which includes all the functionality of MIEDA. 
- An `images` directory, which includes figures used throughout the 
repository. 
- An `examples` directory, which includes examples of how to use MIEDA.
- A `license.txt` file specifying the Apache 2.0 License. 
- A `readme.md` file that contains some basic information about the 
package and how to use it, and other related information. 
- Unit tests for the package's basic operations, achieving 100% 
coverage.
- A `requirements.txt` file specifying the package's dependencies, and 
relatedly a `requirements_ci.txt` file. 
- A `setup.py` file for installing the package. Lines commented will 
be used in the future for Github and PyPi. 
- A `.travis.yml` file for future use once the project has been cleared 
for open-source release. 
- A `.gitignore` file to keep things tidy. 
- A `notebooks` directory which includes notebooks containing analyses 
of the algorithm's behavior and, later, example use cases. 
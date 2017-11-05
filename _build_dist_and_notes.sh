# Build and install the NebulaBayes package

# The MANIFEST.in file tells Distutils what files to include in the source distribution
# It incldues the grid data files and documentation.
# The "package_data" argument to setup specifies the data required to be installed
# WITH the package itself.

# Run the build for the distribution:
# Compensate for a bug in "wheel" by removing "build"
# Also clean all the build working
rm -rf build dist src/NebulaBayes.egg-info
python setup.py sdist bdist_wheel


# Now there are dirs called "build" and dist"
# The "dist" dir contains a wheel we can install:
# pip install dist/NebulaBayes-0.88-py2.py3-none-any.whl
# pip uninstall NebulaBayes
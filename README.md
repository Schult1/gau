# gau - Geo API Utilities

Python utilities around different geo APIs in form of a python 3 package

## Aim

The aim of this package is to provide a basic set of functions and to address common use cases i.e.:

### API
* Call HERE APIs
* Call INRIX APIs

### Viewer
* Visualise API responses

### Misc

### Notebooks

Contained in 'gau/notebooks', give usage examples for the
various packages/modules.

## Requirements
APIs need credential which have to be saved as environment variables at the moment.
here: 'HERE_APP_ID', 'HERE_APP_CODE'
inrix: 'INRIX_VENDOR_ID', 'INRIX_CONSUMER_ID'

## Installation

If you want to install into a self-contained environment, create and enter a virtualenv or conda environment with the version of Python you wish to use.

Direct from GitHub installation using:

```
pip install --upgrade git+https://github.com/Schult1/gau.git
```

Alternatively `git clone` this repo and use:

```
pip install --upgrade -r requirements.txt
```

If you want a global install that will make the package available in your base python installation, simply run the
install command above.
  ```

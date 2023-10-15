coverage2GHChecksAnnotations.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/coverage2GHChecksAnnotations.py.svg)](https://libraries.io/github/KOLANICH/coverage2GHChecksAnnotations.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

Transforms coverage info from [coveragepy](https://github.com/nedbat/coveragepy) database into a `dict` with GitHub annotations to be sent to [`/repos/{owner}/{repo}/check-runs` endpoint](https://docs.github.com/en/free-pro-team@latest/rest/reference/checks#create-a-check-run).

It registers 2 console commands:

* `coverage2GHChecksAnnotations <coverage database file> <project name> <root dir of the project to generate relative paths>` generates the dict.

* `coverageReportGHChecksAnnotations <coverage database file> <project name> <root dir of the project to generate relative paths>` not just generates the dict, but also sends the data to GitHub using [miniGHAPI](https://codeberg.org/KOLANICH-libs/miniGHAPI.py) lib.

for convenience we have [a GitHub Action doing this](https://codeberg.org/KOLANICH-GHActions/coveragepyReport).

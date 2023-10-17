coverage2GHChecksAnnotations.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/coverage2GHChecksAnnotations.py.svg)](https://libraries.io/github/KOLANICH/coverage2GHChecksAnnotations.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py)

**We have moved to https://codeberg.org/KOLANICH-libs/coverage2GHChecksAnnotations.py (the namespace has changed to `KFmts`, which groups packages related to parsing or serialization), grab new versions there.**

Under the disguise of "better security" Micro$oft-owned GitHub has [discriminated users of 1FA passwords](https://github.blog/2023-03-09-raising-the-bar-for-software-security-github-2fa-begins-march-13/) while having commercial interest in success and wide adoption of [FIDO 1FA specifications](https://fidoalliance.org/specifications/download/) and [Windows Hello implementation](https://support.microsoft.com/en-us/windows/passkeys-in-windows-301c8944-5ea2-452b-9886-97e4d2ef4422) which [it promotes as a replacement for passwords](https://github.blog/2023-07-12-introducing-passwordless-authentication-on-github-com/). It will result in dire consequencies and is competely inacceptable, [read why](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

If you don't want to participate in harming yourself, it is recommended to follow the lead and migrate somewhere away of GitHub and Micro$oft. Here is [the list of alternatives and rationales to do it](https://github.com/orgs/community/discussions/49869). If they delete the discussion, there are certain well-known places where you can get a copy of it. [Read why you should also leave GitHub](https://codeberg.org/KOLANICH/Fuck-GuanTEEnomo).

---

Transforms coverage info from [coveragepy](https://github.com/nedbat/coveragepy) database into a `dict` with GitHub annotations to be sent to [`/repos/{owner}/{repo}/check-runs` endpoint](https://docs.github.com/en/free-pro-team@latest/rest/reference/checks#create-a-check-run).

It registers 2 console commands:

* `coverage2GHChecksAnnotations <coverage database file> <project name> <root dir of the project to generate relative paths>` generates the dict.

* `coverageReportGHChecksAnnotations <coverage database file> <project name> <root dir of the project to generate relative paths>` not just generates the dict, but also sends the data to GitHub using [miniGHAPI](https://codeberg.org/KOLANICH-libs/miniGHAPI.py) lib.

for convenience we have [a GitHub Action doing this](https://codeberg.org/KOLANICH-GHActions/coveragepyReport).

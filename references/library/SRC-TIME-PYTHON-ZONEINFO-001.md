---
source_id: "SRC-TIME-PYTHON-ZONEINFO-001"
title: "Python 3.12 zoneinfo documentation"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/bazi/sources/SRC-TIME-PYTHON-ZONEINFO-001.json"
capture_mode: "full"
aggregate_payload_sha256: "893a6e1d83e5d9580bd708f70ad2d20f24afd752c94edc39724ee8cd6e99cf21"
license: "PSF-2.0; documentation code examples also 0BSD"
---

# Python 3.12 zoneinfo documentation

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-TIME-PYTHON-ZONEINFO-001`
- Manifest: `systems/bazi/sources/SRC-TIME-PYTHON-ZONEINFO-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `Python 3.12.13`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `bazi`, `vedic-astrology`, `western-astrology`
- Lineages: `time-normalization`, `true-citra-common-v0.1`, `tropical-geocentric-v0.1`

## Rights envelope

- License: `PSF-2.0; documentation code examples also 0BSD`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `not_applicable`
- Evidence: Python documentation license permits use and derivative works subject to retained notices.

## Locator capture ledger

### Locator 1

- Registered: https://docs.python.org/3.12/library/zoneinfo.html
- Resolved: https://docs.python.org/3.12/library/zoneinfo.html
- Status: `captured`
- Media type: `text/html`
- SHA-256: `6e4f9e0bdfd0e9aae9f16fe2b4e1b272123e7eeda8546351223b22264971861e`

#### Parsed material

zoneinfo — IANA time zone support — Python 3.12.13 documentation



Theme Auto Light Dark

### [Table of Contents](../contents.html)

- [`zoneinfo`— IANA time zone support](#)

  - [Using`ZoneInfo`](#using-zoneinfo)
  - [Data sources](#data-sources)

    - [Configuring the data sources](#configuring-the-data-sources)

      - [Compile-time configuration](#compile-time-configuration)
      - [Environment configuration](#environment-configuration)
      - [Runtime configuration](#runtime-configuration)

  - [The`ZoneInfo`class](#the-zoneinfo-class)

    - [String representations](#string-representations)
    - [Pickle serialization](#pickle-serialization)

  - [Functions](#functions)
  - [Globals](#globals)
  - [Exceptions and warnings](#exceptions-and-warnings)

#### Previous topic

[`datetime`— Basic date and time types](datetime.html)

#### Next topic

[`calendar`— General calendar-related functions](calendar.html)

### This Page

- [Report a Bug](../bugs.html)
- [Show Source](https://github.com/python/cpython/blob/main/Doc/library/zoneinfo.rst)

### Navigation

- [index](../genindex.html)
- [modules](../py-modindex.html) |
- [next](calendar.html) |
- [previous](datetime.html) |
-
- [Python](https://www.python.org/) »
-

-
- [3.12.13 Documentation](../index.html) »
- [The Python Standard Library](index.html) »
- [Data Types](datatypes.html) »
- [`zoneinfo`— IANA time zone support]
-

|
- Theme Auto Light Dark |

# `zoneinfo`— IANA time zone support[¶](#module-zoneinfo)

Added in version 3.9.

**Source code:**[Lib/zoneinfo](https://github.com/python/cpython/tree/3.12/Lib/zoneinfo)

The[`zoneinfo`](#module-zoneinfo) module provides a concrete time zone implementation to support the IANA time zone database as originally specified in[**PEP 615**](https://peps.python.org/pep-0615/) . By default,[`zoneinfo`](#module-zoneinfo) uses the system’s time zone data if available; if no system time zone data is available, the library will fall back to using the first-party[tzdata](https://pypi.org/project/tzdata/) package available on PyPI.

See also

Module:[`datetime`](datetime.html#module-datetime)

Provides the[`time`](datetime.html#datetime.time) and[`datetime`](datetime.html#datetime.datetime) types with which the[`ZoneInfo`](#zoneinfo.ZoneInfo) class is designed to be used.

Package[tzdata](https://pypi.org/project/tzdata/)

First-party package maintained by the CPython core developers to supply time zone data via PyPI.

[Availability](intro.html#availability) : not Emscripten, not WASI.

This module does not work or is not available on WebAssembly platforms`wasm32-emscripten`and`wasm32-wasi`. See[WebAssembly platforms](intro.html#wasm-availability) for more information.

## Using`ZoneInfo`[¶](#using-zoneinfo)

[`ZoneInfo`](#zoneinfo.ZoneInfo) is a concrete implementation of the[`datetime.tzinfo`](datetime.html#datetime.tzinfo) abstract base class, and is intended to be attached to`tzinfo`, either via the constructor, the[`datetime.replace`](datetime.html#datetime.datetime.replace) method or[`datetime.astimezone`](datetime.html#datetime.datetime.astimezone) :

```text
>>> from zoneinfo import ZoneInfo
>>> from datetime import datetime, timedelta

>>> dt = datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("America/Los_Angeles"))
>>> print(dt)
2020-10-31 12:00:00-07:00

>>> dt.tzname()
'PDT'

```

Datetimes constructed in this way are compatible with datetime arithmetic and handle daylight saving time transitions with no further intervention:

```text
>>> dt_add = dt + timedelta(days=1)

>>> print(dt_add)
2020-11-01 12:00:00-08:00

>>> dt_add.tzname()
'PST'

```

These time zones also support the[`fold`](datetime.html#datetime.datetime.fold) attribute introduced in[**PEP 495**](https://peps.python.org/pep-0495/) . During offset transitions which induce ambiguous times (such as a daylight saving time to standard time transition), the offset from*before*the transition is used when`fold=0`, and the offset*after*the transition is used when`fold=1`, for example:

```text
>>> dt = datetime(2020, 11, 1, 1, tzinfo=ZoneInfo("America/Los_Angeles"))
>>> print(dt)
2020-11-01 01:00:00-07:00

>>> print(dt.replace(fold=1))
2020-11-01 01:00:00-08:00

```

When converting from another time zone, the fold will be set to the correct value:

```text
>>> from datetime import timezone
>>> LOS_ANGELES = ZoneInfo("America/Los_Angeles")
>>> dt_utc = datetime(2020, 11, 1, 8, tzinfo=timezone.utc)

>>> # Before the PDT -> PST transition
>>> print(dt_utc.astimezone(LOS_ANGELES))
2020-11-01 01:00:00-07:00

>>> # After the PDT -> PST transition
>>> print((dt_utc + timedelta(hours=1)).astimezone(LOS_ANGELES))
2020-11-01 01:00:00-08:00

```

## Data sources[¶](#data-sources)

The`zoneinfo`module does not directly provide time zone data, and instead pulls time zone information from the system time zone database or the first-party PyPI package[tzdata](https://pypi.org/project/tzdata/) , if available. Some systems, including notably Windows systems, do not have an IANA database available, and so for projects targeting cross-platform compatibility that require time zone data, it is recommended to declare a dependency on tzdata. If neither system data nor tzdata are available, all calls to[`ZoneInfo`](#zoneinfo.ZoneInfo) will raise[`ZoneInfoNotFoundError`](#zoneinfo.ZoneInfoNotFoundError) .

### Configuring the data sources[¶](#configuring-the-data-sources)

When`ZoneInfo(key)`is called, the constructor first searches the directories specified in[`TZPATH`](#zoneinfo.TZPATH) for a file matching`key`, and on failure looks for a match in the tzdata package. This behavior can be configured in three ways:

-

The default[`TZPATH`](#zoneinfo.TZPATH) when not otherwise specified can be configured at[compile time](#zoneinfo-data-compile-time-config) .

-

[`TZPATH`](#zoneinfo.TZPATH) can be configured using[an environment variable](#zoneinfo-data-environment-var) .

-

At[runtime](#zoneinfo-data-runtime-config) , the search path can be manipulated using the[`reset_tzpath()`](#zoneinfo.reset_tzpath) function.

#### Compile-time configuration[¶](#compile-time-configuration)

The default[`TZPATH`](#zoneinfo.TZPATH) includes several common deployment locations for the time zone database (except on Windows, where there are no “well-known” locations for time zone data). On POSIX systems, downstream distributors and those building Python from source who know where their system time zone data is deployed may change the default time zone path by specifying the compile-time option`TZPATH`(or, more likely, the[`configure flag --with-tzpath`](../using/configure.html#cmdoption-with-tzpath) ), which should be a string delimited by[`os.pathsep`](os.html#os.pathsep) .

On all platforms, the configured value is available as the`TZPATH`key in[`sysconfig.get_config_var()`](sysconfig.html#sysconfig.get_config_var) .

#### Environment configuration[¶](#environment-configuration)

When initializing[`TZPATH`](#zoneinfo.TZPATH) (either at import time or whenever[`reset_tzpath()`](#zoneinfo.reset_tzpath) is called with no arguments), the`zoneinfo`module will use the environment variable`PYTHONTZPATH`, if it exists, to set the search path.

PYTHONTZPATH[¶](#envvar-PYTHONTZPATH)

This is an[`os.pathsep`](os.html#os.pathsep) -separated string containing the time zone search path to use. It must consist of only absolute rather than relative paths. Relative components specified in`PYTHONTZPATH`will not be used, but otherwise the behavior when a relative path is specified is implementation-defined; CPython will raise[`InvalidTZPathWarning`](#zoneinfo.InvalidTZPathWarning) , but other implementations are free to silently ignore the erroneous component or raise an exception.

To set the system to ignore the system data and use the tzdata package instead, set`PYTHONTZPATH=""`.

#### Runtime configuration[¶](#runtime-configuration)

The TZ search path can also be configured at runtime using the[`reset_tzpath()`](#zoneinfo.reset_tzpath) function. This is generally not an advisable operation, though it is reasonable to use it in test functions that require the use of a specific time zone path (or require disabling access to the system time zones).

## The`ZoneInfo`class[¶](#the-zoneinfo-class)

*class*zoneinfo. ZoneInfo (*key*)[¶](#zoneinfo.ZoneInfo)

A concrete[`datetime.tzinfo`](datetime.html#datetime.tzinfo) subclass that represents an IANA time zone specified by the string`key`. Calls to the primary constructor will always return objects that compare identically; put another way, barring cache invalidation via[`ZoneInfo.clear_cache()`](#zoneinfo.ZoneInfo.clear_cache) , for all values of`key`, the following assertion will always be true:

```text
a = ZoneInfo(key)
b = ZoneInfo(key)
assert a is b

```

`key`must be in the form of a relative, normalized POSIX path, with no up-level references. The constructor will raise[`ValueError`](exceptions.html#ValueError) if a non-conforming key is passed.

If no file matching`key`is found, the constructor will raise[`ZoneInfoNotFoundError`](#zoneinfo.ZoneInfoNotFoundError) .

The`ZoneInfo`class has two alternate constructors:

*classmethod*ZoneInfo. from_file (*fobj*,*/*,*key = None*)[¶](#zoneinfo.ZoneInfo.from_file)

Constructs a`ZoneInfo`object from a file-like object returning bytes (e.g. a file opened in binary mode or an[`io.BytesIO`](io.html#io.BytesIO) object). Unlike the primary constructor, this always constructs a new object.

The`key`parameter sets the name of the zone for the purposes of[`__str__()`](../reference/datamodel.html#object.__str__) and[`__repr__()`](../reference/datamodel.html#object.__repr__) .

Objects created via this constructor cannot be pickled (see[pickling](#pickling) ).

*classmethod*ZoneInfo. no_cache (*key*)[¶](#zoneinfo.ZoneInfo.no_cache)

An alternate constructor that bypasses the constructor’s cache. It is identical to the primary constructor, but returns a new object on each call. This is most likely to be useful for testing or demonstration purposes, but it can also be used to create a system with a different cache invalidation strategy.

Objects created via this constructor will also bypass the cache of a deserializing process when unpickled.

Caution

Using this constructor may change the semantics of your datetimes in surprising ways, only use it if you know that you need to.

The following class methods are also available:

*classmethod*ZoneInfo. clear_cache (***,*only_keys = None*)[¶](#zoneinfo.ZoneInfo.clear_cache)

A method for invalidating the cache on the`ZoneInfo`class. If no arguments are passed, all caches are invalidated and the next call to the primary constructor for each key will return a new instance.

If an iterable of key names is passed to the`only_keys`parameter, only the specified keys will be removed from the cache. Keys passed to`only_keys`but not found in the cache are ignored.

Warning

Invoking this function may change the semantics of datetimes using`ZoneInfo`in surprising ways; this modifies module state and thus may have wide-ranging effects. Only use it if you know that you need to.

The class has one attribute:

ZoneInfo. key[¶](#zoneinfo.ZoneInfo.key)

This is a read-only[attribute](../glossary.html#term-attribute) that returns the value of`key`passed to the constructor, which should be a lookup key in the IANA time zone database (e.g.`America/New_York`,`Europe/Paris`or`Asia/Tokyo`).

For zones constructed from file without specifying a`key`parameter, this will be set to`None`.

Note

Although it is a somewhat common practice to expose these to end users, these values are designed to be primary keys for representing the relevant zones and not necessarily user-facing elements. Projects like CLDR (the Unicode Common Locale Data Repository) can be used to get more user-friendly strings from these keys.

### String representations[¶](#string-representations)

The string representation returned when calling[`str`](stdtypes.html#str) on a[`ZoneInfo`](#zoneinfo.ZoneInfo) object defaults to using the[`ZoneInfo.key`](#zoneinfo.ZoneInfo.key) attribute (see the note on usage in the attribute documentation):

```text
>>> zone = ZoneInfo("Pacific/Kwajalein")
>>> str(zone)
'Pacific/Kwajalein'

>>> dt = datetime(2020, 4, 1, 3, 15, tzinfo=zone)
>>> f"{dt.isoformat()} [{dt.tzinfo}]"
'2020-04-01T03:15:00+12:00 [Pacific/Kwajalein]'

```

For objects constructed from a file without specifying a`key`parameter,`str`falls back to calling[`repr()`](functions.html#repr) .`ZoneInfo`’s`repr`is implementation-defined and not necessarily stable between versions, but it is guaranteed not to be a valid`ZoneInfo`key.

### Pickle serialization[¶](#pickle-serialization)

Rather than serializing all transition data,`ZoneInfo`objects are serialized by key, and`ZoneInfo`objects constructed from files (even those with a value for`key`specified) cannot be pickled.

The behavior of a`ZoneInfo`file depends on how it was constructed:

-

`ZoneInfo(key)`: When constructed with the primary constructor, a`ZoneInfo`object is serialized by key, and when deserialized, the deserializing process uses the primary and thus it is expected that these are expected to be the same object as other references to the same time zone. For example, if`europe_berlin_pkl`is a string containing a pickle constructed from`ZoneInfo("Europe/Berlin")`, one would expect the following behavior:

```text
>>> a = ZoneInfo("Europe/Berlin")
>>> b = pickle.loads(europe_berlin_pkl)
>>> a is b
True

```

-

`ZoneInfo.no_cache(key)`: When constructed from the cache-bypassing constructor, the`ZoneInfo`object is also serialized by key, but when deserialized, the deserializing process uses the cache bypassing constructor. If`europe_berlin_pkl_nc`is a string containing a pickle constructed from`ZoneInfo.no_cache("Europe/Berlin")`, one would expect the following behavior:

```text
>>> a = ZoneInfo("Europe/Berlin")
>>> b = pickle.loads(europe_berlin_pkl_nc)
>>> a is b
False

```

-

`ZoneInfo.from_file(fobj, /, key=None)`: When constructed from a file, the`ZoneInfo`object raises an exception on pickling. If an end user wants to pickle a`ZoneInfo`constructed from a file, it is recommended that they use a wrapper type or a custom serialization function: either serializing by key or storing the contents of the file object and serializing that.

This method of serialization requires that the time zone data for the required key be available on both the serializing and deserializing side, similar to the way that references to classes and functions are expected to exist in both the serializing and deserializing environments. It also means that no guarantees are made about the consistency of results when unpickling a`ZoneInfo`pickled in an environment with a different version of the time zone data.

## Functions[¶](#functions)

zoneinfo. available_timezones ( )[¶](#zoneinfo.available_timezones)

Get a set containing all the valid keys for IANA time zones available anywhere on the time zone path. This is recalculated on every call to the function.

This function only includes canonical zone names and does not include “special” zones such as those under the`posix/`and`right/`directories, or the`posixrules`zone.

Caution

This function may open a large number of files, as the best way to determine if a file on the time zone path is a valid time zone is to read the “magic string” at the beginning.

Note

These values are not designed to be exposed to end-users; for user facing elements, applications should use something like CLDR (the Unicode Common Locale Data Repository) to get more user-friendly strings. See also the cautionary note on[`ZoneInfo.key`](#zoneinfo.ZoneInfo.key) .

zoneinfo. reset_tzpath (*to = None*)[¶](#zoneinfo.reset_tzpath)

Sets or resets the time zone search path ([`TZPATH`](#zoneinfo.TZPATH) ) for the module. When called with no arguments,[`TZPATH`](#zoneinfo.TZPATH) is set to the default value.

Calling`reset_tzpath`will not invalidate the[`ZoneInfo`](#zoneinfo.ZoneInfo) cache, and so calls to the primary`ZoneInfo`constructor will only use the new`TZPATH`in the case of a cache miss.

The`to`parameter must be a[sequence](../glossary.html#term-sequence) of strings or[`os.PathLike`](os.html#os.PathLike) and not a string, all of which must be absolute paths.[`ValueError`](exceptions.html#ValueError) will be raised if something other than an absolute path is passed.

## Globals[¶](#globals)

zoneinfo. TZPATH[¶](#zoneinfo.TZPATH)

A read-only sequence representing the time zone search path – when constructing a`ZoneInfo`from a key, the key is joined to each entry in the`TZPATH`, and the first file found is used.

`TZPATH`may contain only absolute paths, never relative paths, regardless of how it is configured.

The object that`zoneinfo.TZPATH`points to may change in response to a call to[`reset_tzpath()`](#zoneinfo.reset_tzpath) , so it is recommended to use`zoneinfo.TZPATH`rather than importing`TZPATH`from`zoneinfo`or assigning a long-lived variable to`zoneinfo.TZPATH`.

For more information on configuring the time zone search path, see[Configuring the data sources](#zoneinfo-data-configuration) .

## Exceptions and warnings[¶](#exceptions-and-warnings)

*exception*zoneinfo. ZoneInfoNotFoundError[¶](#zoneinfo.ZoneInfoNotFoundError)

Raised when construction of a[`ZoneInfo`](#zoneinfo.ZoneInfo) object fails because the specified key could not be found on the system. This is a subclass of[`KeyError`](exceptions.html#KeyError) .

*exception*zoneinfo. InvalidTZPathWarning[¶](#zoneinfo.InvalidTZPathWarning)

Raised when[`PYTHONTZPATH`](#envvar-PYTHONTZPATH) contains an invalid component that will be filtered out, such as a relative path.

### [Table of Contents](../contents.html)

- [`zoneinfo`— IANA time zone support](#)

  - [Using`ZoneInfo`](#using-zoneinfo)
  - [Data sources](#data-sources)

    - [Configuring the data sources](#configuring-the-data-sources)

      - [Compile-time configuration](#compile-time-configuration)
      - [Environment configuration](#environment-configuration)
      - [Runtime configuration](#runtime-configuration)

  - [The`ZoneInfo`class](#the-zoneinfo-class)

    - [String representations](#string-representations)
    - [Pickle serialization](#pickle-serialization)

  - [Functions](#functions)
  - [Globals](#globals)
  - [Exceptions and warnings](#exceptions-and-warnings)

#### Previous topic

[`datetime`— Basic date and time types](datetime.html)

#### Next topic

[`calendar`— General calendar-related functions](calendar.html)

### This Page

- [Report a Bug](../bugs.html)
- [Show Source](https://github.com/python/cpython/blob/main/Doc/library/zoneinfo.rst)

«

### Navigation

- [index](../genindex.html)
- [modules](../py-modindex.html) |
- [next](calendar.html) |
- [previous](datetime.html) |
-
- [Python](https://www.python.org/) »
-

-
- [3.12.13 Documentation](../index.html) »
- [The Python Standard Library](index.html) »
- [Data Types](datatypes.html) »
- [`zoneinfo`— IANA time zone support]
-

|
- Theme Auto Light Dark |

©[Copyright](../copyright.html) 2001-2026, Python Software Foundation.
This page is licensed under the Python Software Foundation License Version 2.
Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License.
See[History and License](/license.html) for more information.

The Python Software Foundation is a non-profit corporation.[Please donate.](https://www.python.org/psf/donations/)

Last updated on Mar 07, 2026 (17:44 UTC).[Found a bug](/bugs.html) ?
Created using[Sphinx](https://www.sphinx-doc.org/) 8.2.3.

### Locator 2

- Registered: https://docs.python.org/3.12/license.html
- Resolved: https://docs.python.org/3.12/license.html
- Status: `captured`
- Media type: `text/html`
- SHA-256: `65fd1a0823ed62460ecfc3b4415631846f146fac571633cdaa2c9dc037e2385b`

#### Parsed material

History and License — Python 3.12.13 documentation



Theme Auto Light Dark

### [Table of Contents](contents.html)

- [History and License](#)

  - [History of the software](#history-of-the-software)
  - [Terms and conditions for accessing or otherwise using Python](#terms-and-conditions-for-accessing-or-otherwise-using-python)

    - [PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2](#python-software-foundation-license-version-2)
    - [BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0](#beopen-com-license-agreement-for-python-2-0)
    - [CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1](#cnri-license-agreement-for-python-1-6-1)
    - [CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2](#cwi-license-agreement-for-python-0-9-0-through-1-2)
    - [ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION](#zero-clause-bsd-license-for-code-in-the-python-documentation)

  - [Licenses and Acknowledgements for Incorporated Software](#licenses-and-acknowledgements-for-incorporated-software)

    - [Mersenne Twister](#mersenne-twister)
    - [Sockets](#sockets)
    - [Asynchronous socket services](#asynchronous-socket-services)
    - [Cookie management](#cookie-management)
    - [Execution tracing](#execution-tracing)
    - [UUencode and UUdecode functions](#uuencode-and-uudecode-functions)
    - [XML Remote Procedure Calls](#xml-remote-procedure-calls)
    - [test_epoll](#test-epoll)
    - [Select kqueue](#select-kqueue)
    - [SipHash24](#siphash24)
    - [strtod and dtoa](#strtod-and-dtoa)
    - [OpenSSL](#openssl)
    - [expat](#expat)
    - [libffi](#libffi)
    - [zlib](#zlib)
    - [cfuhash](#cfuhash)
    - [libmpdec](#libmpdec)
    - [W3C C14N test suite](#w3c-c14n-test-suite)
    - [Audioop](#audioop)
    - [asyncio](#asyncio)

#### Previous topic

[Copyright](copyright.html)

### This Page

- [Report a Bug](bugs.html)
- [Show Source](https://github.com/python/cpython/blob/main/Doc/license.rst)

### Navigation

- [index](genindex.html)
- [modules](py-modindex.html) |
- [previous](copyright.html) |
-
- [Python](https://www.python.org/) »
-

-
- [3.12.13 Documentation](index.html) »
- [History and License]
-

|
- Theme Auto Light Dark |

# History and License[¶](#history-and-license)

## History of the software[¶](#history-of-the-software)

Python was created in the early 1990s by Guido van Rossum at Stichting Mathematisch Centrum (CWI, see[https://www.cwi.nl](https://www.cwi.nl) ) in the Netherlands as a successor of a language called ABC. Guido remains Python’s principal author, although it includes many contributions from others.

In 1995, Guido continued his work on Python at the Corporation for National Research Initiatives (CNRI, see[https://www.cnri.reston.va.us](https://www.cnri.reston.va.us) ) in Reston, Virginia where he released several versions of the software.

In May 2000, Guido and the Python core development team moved to BeOpen.com to form the BeOpen PythonLabs team. In October of the same year, the PythonLabs team moved to Digital Creations, which became Zope Corporation. In 2001, the Python Software Foundation (PSF, see[https://www.python.org/psf/](https://www.python.org/psf/) ) was formed, a non-profit organization created specifically to own Python-related Intellectual Property. Zope Corporation was a sponsoring member of the PSF.

All Python releases are Open Source (see[https://opensource.org](https://opensource.org) for the Open Source Definition). Historically, most, but not all, Python releases have also been GPL-compatible; the table below summarizes the various releases.

 |

Release

 |

Derived from

 |

Year

 |

Owner

 |

GPL-compatible? (1)

 |

0.9.0 thru 1.2

 |

n/a

 |

1991-1995

 |

CWI

 |

yes

 |

1.3 thru 1.5.2

 |

1.2

 |

1995-1999

 |

CNRI

 |

yes

 |

1.6

 |

1.5.2

 |

2000

 |

CNRI

 |

no

 |

2.0

 |

1.6

 |

2000

 |

BeOpen.com

 |

no

 |

1.6.1

 |

1.6

 |

2001

 |

CNRI

 |

yes (2)

 |

2.1

 |

2.0+1.6.1

 |

2001

 |

PSF

 |

no

 |

2.0.1

 |

2.0+1.6.1

 |

2001

 |

PSF

 |

yes

 |

2.1.1

 |

2.1+2.0.1

 |

2001

 |

PSF

 |

yes

 |

2.1.2

 |

2.1.1

 |

2002

 |

PSF

 |

yes

 |

2.1.3

 |

2.1.2

 |

2002

 |

PSF

 |

yes

 |

2.2 and above

 |

2.1.1

 |

2001-now

 |

PSF

 |

yes

Note

-

GPL-compatible doesn’t mean that we’re distributing Python under the GPL. All Python licenses, unlike the GPL, let you distribute a modified version without making your changes open source. The GPL-compatible licenses make it possible to combine Python with other software that is released under the GPL; the others don’t.

-

According to Richard Stallman, 1.6.1 is not GPL-compatible, because its license has a choice of law clause. According to CNRI, however, Stallman’s lawyer has told CNRI’s lawyer that 1.6.1 is “not incompatible” with the GPL.

Thanks to the many outside volunteers who have worked under Guido’s direction to make these releases possible.

## Terms and conditions for accessing or otherwise using Python[¶](#terms-and-conditions-for-accessing-or-otherwise-using-python)

Python software and documentation are licensed under the Python Software Foundation License Version 2.

Starting with Python 3.8.6, examples, recipes, and other code in the documentation are dual licensed under the PSF License Version 2 and the[Zero-Clause BSD license](#bsd0) .

Some software incorporated into Python is under different licenses. The licenses are listed with code falling under that license. See[Licenses and Acknowledgements for Incorporated Software](#otherlicenses) for an incomplete list of these licenses.

### PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2[¶](#python-software-foundation-license-version-2)

```text
1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and
   the Individual or Organization ("Licensee") accessing and otherwise using this
   software ("Python") in source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, PSF hereby
   grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
   analyze, test, perform and/or display publicly, prepare derivative works,
   distribute, and otherwise use Python alone or in any derivative
   version, provided, however, that PSF's License Agreement and PSF's notice of
   copyright, i.e., "Copyright © 2001-2023 Python Software Foundation; All Rights
   Reserved" are retained in Python alone or in any derivative version
   prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on or
   incorporates Python or any part thereof, and wants to make the
   derivative work available to others as provided herein, then Licensee hereby
   agrees to include in any such work a brief summary of the changes made to Python.

4. PSF is making Python available to Licensee on an "AS IS" basis.
   PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF
   EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR
   WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE
   USE OF PYTHON WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
   FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF
   MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON, OR ANY DERIVATIVE
   THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material breach of
   its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any relationship
   of agency, partnership, or joint venture between PSF and Licensee.  This License
   Agreement does not grant permission to use PSF trademarks or trade name in a
   trademark sense to endorse or promote products or services of Licensee, or any
   third party.

8. By copying, installing or otherwise using Python, Licensee agrees
   to be bound by the terms and conditions of this License Agreement.

```

### BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0[¶](#beopen-com-license-agreement-for-python-2-0)

BEOPEN PYTHON OPEN SOURCE LICENSE AGREEMENT VERSION 1

```text
1. This LICENSE AGREEMENT is between BeOpen.com ("BeOpen"), having an office at
   160 Saratoga Avenue, Santa Clara, CA 95051, and the Individual or Organization
   ("Licensee") accessing and otherwise using this software in source or binary
   form and its associated documentation ("the Software").

2. Subject to the terms and conditions of this BeOpen Python License Agreement,
   BeOpen hereby grants Licensee a non-exclusive, royalty-free, world-wide license
   to reproduce, analyze, test, perform and/or display publicly, prepare derivative
   works, distribute, and otherwise use the Software alone or in any derivative
   version, provided, however, that the BeOpen Python License is retained in the
   Software, alone or in any derivative version prepared by Licensee.

3. BeOpen is making the Software available to Licensee on an "AS IS" basis.
   BEOPEN MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF
   EXAMPLE, BUT NOT LIMITATION, BEOPEN MAKES NO AND DISCLAIMS ANY REPRESENTATION OR
   WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE
   USE OF THE SOFTWARE WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

4. BEOPEN SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF THE SOFTWARE FOR
   ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF USING,
   MODIFYING OR DISTRIBUTING THE SOFTWARE, OR ANY DERIVATIVE THEREOF, EVEN IF
   ADVISED OF THE POSSIBILITY THEREOF.

5. This License Agreement will automatically terminate upon a material breach of
   its terms and conditions.

6. This License Agreement shall be governed by and interpreted in all respects
   by the law of the State of California, excluding conflict of law provisions.
   Nothing in this License Agreement shall be deemed to create any relationship of
   agency, partnership, or joint venture between BeOpen and Licensee.  This License
   Agreement does not grant permission to use BeOpen trademarks or trade names in a
   trademark sense to endorse or promote products or services of Licensee, or any
   third party.  As an exception, the "BeOpen Python" logos available at
   http://www.pythonlabs.com/logos.html may be used according to the permissions
   granted on that web page.

7. By copying, installing or otherwise using the software, Licensee agrees to be
   bound by the terms and conditions of this License Agreement.

```

### CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1[¶](#cnri-license-agreement-for-python-1-6-1)

```text
1. This LICENSE AGREEMENT is between the Corporation for National Research
   Initiatives, having an office at 1895 Preston White Drive, Reston, VA 20191
   ("CNRI"), and the Individual or Organization ("Licensee") accessing and
   otherwise using Python 1.6.1 software in source or binary form and its
   associated documentation.

2. Subject to the terms and conditions of this License Agreement, CNRI hereby
   grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
   analyze, test, perform and/or display publicly, prepare derivative works,
   distribute, and otherwise use Python 1.6.1 alone or in any derivative version,
   provided, however, that CNRI's License Agreement and CNRI's notice of copyright,
   i.e., "Copyright © 1995-2001 Corporation for National Research Initiatives; All
   Rights Reserved" are retained in Python 1.6.1 alone or in any derivative version
   prepared by Licensee.  Alternately, in lieu of CNRI's License Agreement,
   Licensee may substitute the following text (omitting the quotes): "Python 1.6.1
   is made available subject to the terms and conditions in CNRI's License
   Agreement.  This Agreement together with Python 1.6.1 may be located on the
   internet using the following unique, persistent identifier (known as a handle):
   1895.22/1013.  This Agreement may also be obtained from a proxy server on the
   internet using the following URL: http://hdl.handle.net/1895.22/1013".

3. In the event Licensee prepares a derivative work that is based on or
   incorporates Python 1.6.1 or any part thereof, and wants to make the derivative
   work available to others as provided herein, then Licensee hereby agrees to
   include in any such work a brief summary of the changes made to Python 1.6.1.

4. CNRI is making Python 1.6.1 available to Licensee on an "AS IS" basis.  CNRI
   MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF EXAMPLE,
   BUT NOT LIMITATION, CNRI MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY
   OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF
   PYTHON 1.6.1 WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

5. CNRI SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON 1.6.1 FOR
   ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF
   MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 1.6.1, OR ANY DERIVATIVE
   THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material breach of
   its terms and conditions.

7. This License Agreement shall be governed by the federal intellectual property
   law of the United States, including without limitation the federal copyright
   law, and, to the extent such U.S. federal law does not apply, by the law of the
   Commonwealth of Virginia, excluding Virginia's conflict of law provisions.
   Notwithstanding the foregoing, with regard to derivative works based on Python
   1.6.1 that incorporate non-separable material that was previously distributed
   under the GNU General Public License (GPL), the law of the Commonwealth of
   Virginia shall govern this License Agreement only as to issues arising under or
   with respect to Paragraphs 4, 5, and 7 of this License Agreement.  Nothing in
   this License Agreement shall be deemed to create any relationship of agency,
   partnership, or joint venture between CNRI and Licensee.  This License Agreement
   does not grant permission to use CNRI trademarks or trade name in a trademark
   sense to endorse or promote products or services of Licensee, or any third
   party.

8. By clicking on the "ACCEPT" button where indicated, or by copying, installing
   or otherwise using Python 1.6.1, Licensee agrees to be bound by the terms and
   conditions of this License Agreement.

```

### CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2[¶](#cwi-license-agreement-for-python-0-9-0-through-1-2)

```text
Copyright © 1991 - 1995, Stichting Mathematisch Centrum Amsterdam, The
Netherlands.  All rights reserved.

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appear in all copies and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of Stichting Mathematisch Centrum or CWI not be used in advertising or
publicity pertaining to distribution of the software without specific, written
prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO
EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE FOR ANY SPECIAL, INDIRECT
OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
SOFTWARE.

```

### ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION[¶](#zero-clause-bsd-license-for-code-in-the-python-documentation)

```text
Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

```

## Licenses and Acknowledgements for Incorporated Software[¶](#licenses-and-acknowledgements-for-incorporated-software)

This section is an incomplete, but growing list of licenses and acknowledgements for third-party software incorporated in the Python distribution.

### Mersenne Twister[¶](#mersenne-twister)

The`_random`C extension underlying the[`random`](library/random.html#module-random) module includes code based on a download from[http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/MT2002/emt19937ar.html](http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/MT2002/emt19937ar.html) . The following are the verbatim comments from the original code:

```text
A C-program for MT19937, with initialization improved 2002/1/26.
Coded by Takuji Nishimura and Makoto Matsumoto.

Before using, initialize the state by using init_genrand(seed)
or init_by_array(init_key, key_length).

Copyright (C) 1997 - 2002, Makoto Matsumoto and Takuji Nishimura,
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

 3. The names of its contributors may not be used to endorse or promote
    products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Any feedback is very welcome.
http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt.html
email: m-mat @ math.sci.hiroshima-u.ac.jp (remove space)

```

### Sockets[¶](#sockets)

The[`socket`](library/socket.html#module-socket) module uses the functions,`getaddrinfo()`, and`getnameinfo()`, which are coded in separate source files from the WIDE Project,[https://www.wide.ad.jp/](https://www.wide.ad.jp/) .

```text
Copyright (C) 1995, 1996, 1997, and 1998 WIDE Project.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of the project nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

```

### Asynchronous socket services[¶](#asynchronous-socket-services)

The`test.support.asynchat`and`test.support.asyncore`modules contain the following notice:

```text
Copyright 1996 by Sam Rushing

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and
its documentation for any purpose and without fee is hereby
granted, provided that the above copyright notice appear in all
copies and that both that copyright notice and this permission
notice appear in supporting documentation, and that the name of Sam
Rushing not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior
permission.

SAM RUSHING DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
NO EVENT SHALL SAM RUSHING BE LIABLE FOR ANY SPECIAL, INDIRECT OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

```

### Cookie management[¶](#cookie-management)

The[`http.cookies`](library/http.cookies.html#module-http.cookies) module contains the following notice:

```text
Copyright 2000 by Timothy O'Malley <timo@alum.mit.edu>

               All Rights Reserved

Permission to use, copy, modify, and distribute this software
and its documentation for any purpose and without fee is hereby
granted, provided that the above copyright notice appear in all
copies and that both that copyright notice and this permission
notice appear in supporting documentation, and that the name of
Timothy O'Malley  not be used in advertising or publicity
pertaining to distribution of the software without specific, written
prior permission.

Timothy O'Malley DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS, IN NO EVENT SHALL Timothy O'Malley BE LIABLE FOR
ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

```

### Execution tracing[¶](#execution-tracing)

The[`trace`](library/trace.html#module-trace) module contains the following notice:

```text
portions copyright 2001, Autonomous Zones Industries, Inc., all rights...
err...  reserved and offered to the public under the terms of the
Python 2.2 license.
Author: Zooko O'Whielacronx
http://zooko.com/
mailto:zooko@zooko.com

Copyright 2000, Mojam Media, Inc., all rights reserved.
Author: Skip Montanaro

Copyright 1999, Bioreason, Inc., all rights reserved.
Author: Andrew Dalke

Copyright 1995-1997, Automatrix, Inc., all rights reserved.
Author: Skip Montanaro

Copyright 1991-1995, Stichting Mathematisch Centrum, all rights reserved.

Permission to use, copy, modify, and distribute this Python software and
its associated documentation for any purpose without fee is hereby
granted, provided that the above copyright notice appears in all copies,
and that both that copyright notice and this permission notice appear in
supporting documentation, and that the name of neither Automatrix,
Bioreason or Mojam Media be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

```

### UUencode and UUdecode functions[¶](#uuencode-and-uudecode-functions)

The[`uu`](library/uu.html#module-uu) module contains the following notice:

```text
Copyright 1994 by Lance Ellinghouse
Cathedral City, California Republic, United States of America.
                       All Rights Reserved
Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation, and that the name of Lance Ellinghouse
not be used in advertising or publicity pertaining to distribution
of the software without specific, written prior permission.
LANCE ELLINGHOUSE DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL LANCE ELLINGHOUSE CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Modified by Jack Jansen, CWI, July 1995:
- Use binascii module to do the actual line-by-line conversion
  between ascii and binary. This results in a 1000-fold speedup. The C
  version is still 5 times faster, though.
- Arguments more compliant with Python standard

```

### XML Remote Procedure Calls[¶](#xml-remote-procedure-calls)

The[`xmlrpc.client`](library/xmlrpc.client.html#module-xmlrpc.client) module contains the following notice:

```text
    The XML-RPC client interface is

Copyright (c) 1999-2002 by Secret Labs AB
Copyright (c) 1999-2002 by Fredrik Lundh

By obtaining, using, and/or copying this software and/or its
associated documentation, you agree that you have read, understood,
and will comply with the following terms and conditions:

Permission to use, copy, modify, and distribute this software and
its associated documentation for any purpose and without fee is
hereby granted, provided that the above copyright notice appears in
all copies, and that both that copyright notice and this permission
notice appear in supporting documentation, and that the name of
Secret Labs AB or the author not be used in advertising or publicity
pertaining to distribution of the software without specific, written
prior permission.

SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.

```

### test_epoll[¶](#test-epoll)

The`test.test_epoll`module contains the following notice:

```text
Copyright (c) 2001-2006 Twisted Matrix Laboratories.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```

### Select kqueue[¶](#select-kqueue)

The[`select`](library/select.html#module-select) module contains the following notice for the kqueue interface:

```text
Copyright (c) 2000 Doug White, 2006 James Knight, 2007 Christian Heimes
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

```

### SipHash24[¶](#siphash24)

The file`Python/pyhash.c`contains Marek Majkowski’ implementation of Dan Bernstein’s SipHash24 algorithm. It contains the following note:

```text
<MIT License>
Copyright (c) 2013  Marek Majkowski <marek@popcount.org>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
</MIT License>

Original location:
   https://github.com/majek/csiphash/

Solution inspired by code from:
   Samuel Neves (supercop/crypto_auth/siphash24/little)
   djb (supercop/crypto_auth/siphash24/little2)
   Jean-Philippe Aumasson (https://131002.net/siphash/siphash24.c)

```

### strtod and dtoa[¶](#strtod-and-dtoa)

The file`Python/dtoa.c`, which supplies C functions dtoa and strtod for conversion of C doubles to and from strings, is derived from the file of the same name by David M. Gay, currently available from[https://web.archive.org/web/20220517033456/http://www.netlib.org/fp/dtoa.c](https://web.archive.org/web/20220517033456/http://www.netlib.org/fp/dtoa.c) . The original file, as retrieved on March 16, 2009, contains the following copyright and licensing notice:

```text
/****************************************************************
 *
 * The author of this software is David M. Gay.
 *
 * Copyright (c) 1991, 2000, 2001 by Lucent Technologies.
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose without fee is hereby granted, provided that this entire notice
 * is included in all copies of any software which is or includes a copy
 * or modification of this software and in all copies of the supporting
 * documentation for such software.
 *
 * THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
 * WARRANTY.  IN PARTICULAR, NEITHER THE AUTHOR NOR LUCENT MAKES ANY
 * REPRESENTATION OR WARRANTY OF ANY KIND CONCERNING THE MERCHANTABILITY
 * OF THIS SOFTWARE OR ITS FITNESS FOR ANY PARTICULAR PURPOSE.
 *
 ***************************************************************/

```

### OpenSSL[¶](#openssl)

The modules[`hashlib`](library/hashlib.html#module-hashlib) ,[`posix`](library/posix.html#module-posix) ,[`ssl`](library/ssl.html#module-ssl) ,[`crypt`](library/crypt.html#module-crypt) use the OpenSSL library for added performance if made available by the operating system. Additionally, the Windows and macOS installers for Python may include a copy of the OpenSSL libraries, so we include a copy of the OpenSSL license here. For the OpenSSL 3.0 release, and later releases derived from that, the Apache License v2 applies:

```text
                              Apache License
                        Version 2.0, January 2004
                     https://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions.

   "License" shall mean the terms and conditions for use, reproduction,
   and distribution as defined by Sections 1 through 9 of this document.

   "Licensor" shall mean the copyright owner or entity authorized by
   the copyright owner that is granting the License.

   "Legal Entity" shall mean the union of the acting entity and all
   other entities that control, are controlled by, or are under common
   control with that entity. For the purposes of this definition,
   "control" means (i) the power, direct or indirect, to cause the
   direction or management of such entity, whether by contract or
   otherwise, or (ii) ownership of fifty percent (50%) or more of the
   outstanding shares, or (iii) beneficial ownership of such entity.

   "You" (or "Your") shall mean an individual or Legal Entity
   exercising permissions granted by this License.

   "Source" form shall mean the preferred form for making modifications,
   including but not limited to software source code, documentation
   source, and configuration files.

   "Object" form shall mean any form resulting from mechanical
   transformation or translation of a Source form, including but
   not limited to compiled object code, generated documentation,
   and conversions to other media types.

   "Work" shall mean the work of authorship, whether in Source or
   Object form, made available under the License, as indicated by a
   copyright notice that is included in or attached to the work
   (an example is provided in the Appendix below).

   "Derivative Works" shall mean any work, whether in Source or Object
   form, that is based on (or derived from) the Work and for which the
   editorial revisions, annotations, elaborations, or other modifications
   represent, as a whole, an original work of authorship. For the purposes
   of this License, Derivative Works shall not include works that remain
   separable from, or merely link (or bind by name) to the interfaces of,
   the Work and Derivative Works thereof.

   "Contribution" shall mean any work of authorship, including
   the original version of the Work and any modifications or additions
   to that Work or Derivative Works thereof, that is intentionally
   submitted to Licensor for inclusion in the Work by the copyright owner
   or by an individual or Legal Entity authorized to submit on behalf of
   the copyright owner. For the purposes of this definition, "submitted"
   means any form of electronic, verbal, or written communication sent
   to the Licensor or its representatives, including but not limited to
   communication on electronic mailing lists, source code control systems,
   and issue tracking systems that are managed by, or on behalf of, the
   Licensor for the purpose of discussing and improving the Work, but
   excluding communication that is conspicuously marked or otherwise
   designated in writing by the copyright owner as "Not a Contribution."

   "Contributor" shall mean Licensor and any individual or Legal Entity
   on behalf of whom a Contribution has been received by Licensor and
   subsequently incorporated within the Work.

2. Grant of Copyright License. Subject to the terms and conditions of
   this License, each Contributor hereby grants to You a perpetual,
   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   copyright license to reproduce, prepare Derivative Works of,
   publicly display, publicly perform, sublicense, and distribute the
   Work and such Derivative Works in Source or Object form.

3. Grant of Patent License. Subject to the terms and conditions of
   this License, each Contributor hereby grants to You a perpetual,
   worldwide, non-exclusive, no-charge, royalty-free, irrevocable
   (except as stated in this section) patent license to make, have made,
   use, offer to sell, sell, import, and otherwise transfer the Work,
   where such license applies only to those patent claims licensable
   by such Contributor that are necessarily infringed by their
   Contribution(s) alone or by combination of their Contribution(s)
   with the Work to which such Contribution(s) was submitted. If You
   institute patent litigation against any entity (including a
   cross-claim or counterclaim in a lawsuit) alleging that the Work
   or a Contribution incorporated within the Work constitutes direct
   or contributory patent infringement, then any patent licenses
   granted to You under this License for that Work shall terminate
   as of the date such litigation is filed.

4. Redistribution. You may reproduce and distribute copies of the
   Work or Derivative Works thereof in any medium, with or without
   modifications, and in Source or Object form, provided that You
   meet the following conditions:

   (a) You must give any other recipients of the Work or
       Derivative Works a copy of this License; and

   (b) You must cause any modified files to carry prominent notices
       stating that You changed the files; and

   (c) You must retain, in the Source form of any Derivative Works
       that You distribute, all copyright, patent, trademark, and
       attribution notices from the Source form of the Work,
       excluding those notices that do not pertain to any part of
       the Derivative Works; and

   (d) If the Work includes a "NOTICE" text file as part of its
       distribution, then any Derivative Works that You distribute must
       include a readable copy of the attribution notices contained
       within such NOTICE file, excluding those notices that do not
       pertain to any part of the Derivative Works, in at least one
       of the following places: within a NOTICE text file distributed
       as part of the Derivative Works; within the Source form or
       documentation, if provided along with the Derivative Works; or,
       within a display generated by the Derivative Works, if and
       wherever such third-party notices normally appear. The contents
       of the NOTICE file are for informational purposes only and
       do not modify the License. You may add Your own attribution
       notices within Derivative Works that You distribute, alongside
       or as an addendum to the NOTICE text from the Work, provided
       that such additional attribution notices cannot be construed
       as modifying the License.

   You may add Your own copyright statement to Your modifications and
   may provide additional or different license terms and conditions
   for use, reproduction, or distribution of Your modifications, or
   for any such Derivative Works as a whole, provided Your use,
   reproduction, and distribution of the Work otherwise complies with
   the conditions stated in this License.

5. Submission of Contributions. Unless You explicitly state otherwise,
   any Contribution intentionally submitted for inclusion in the Work
   by You to the Licensor shall be under the terms and conditions of
   this License, without any additional terms or conditions.
   Notwithstanding the above, nothing herein shall supersede or modify
   the terms of any separate license agreement you may have executed
   with Licensor regarding such Contributions.

6. Trademarks. This License does not grant permission to use the trade
   names, trademarks, service marks, or product names of the Licensor,
   except as required for reasonable and customary use in describing the
   origin of the Work and reproducing the content of the NOTICE file.

7. Disclaimer of Warranty. Unless required by applicable law or
   agreed to in writing, Licensor provides the Work (and each
   Contributor provides its Contributions) on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
   implied, including, without limitation, any warranties or conditions
   of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
   PARTICULAR PURPOSE. You are solely responsible for determining the
   appropriateness of using or redistributing the Work and assume any
   risks associated with Your exercise of permissions under this License.

8. Limitation of Liability. In no event and under no legal theory,
   whether in tort (including negligence), contract, or otherwise,
   unless required by applicable law (such as deliberate and grossly
   negligent acts) or agreed to in writing, shall any Contributor be
   liable to You for damages, including any direct, indirect, special,
   incidental, or consequential damages of any character arising as a
   result of this License or out of the use or inability to use the
   Work (including but not limited to damages for loss of goodwill,
   work stoppage, computer failure or malfunction, or any and all
   other commercial damages or losses), even if such Contributor
   has been advised of the possibility of such damages.

9. Accepting Warranty or Additional Liability. While redistributing
   the Work or Derivative Works thereof, You may choose to offer,
   and charge a fee for, acceptance of support, warranty, indemnity,
   or other liability obligations and/or rights consistent with this
   License. However, in accepting such obligations, You may act only
   on Your own behalf and on Your sole responsibility, not on behalf
   of any other Contributor, and only if You agree to indemnify,
   defend, and hold each Contributor harmless for any liability
   incurred by, or claims asserted against, such Contributor by reason
   of your accepting any such warranty or additional liability.

END OF TERMS AND CONDITIONS

```

### expat[¶](#expat)

The[`pyexpat`](library/pyexpat.html#module-xml.parsers.expat) extension is built using an included copy of the expat sources unless the build is configured`--with-system-expat`:

```text
Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
                               and Clark Cooper

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```

### libffi[¶](#libffi)

The`_ctypes`C extension underlying the[`ctypes`](library/ctypes.html#module-ctypes) module is built using an included copy of the libffi sources unless the build is configured`--with-system-libffi`:

```text
Copyright (c) 1996-2008  Red Hat, Inc and others.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

```

### zlib[¶](#zlib)

The[`zlib`](library/zlib.html#module-zlib) extension is built using an included copy of the zlib sources if the zlib version found on the system is too old to be used for the build:

```text
Copyright (C) 1995-2011 Jean-loup Gailly and Mark Adler

This software is provided 'as-is', without any express or implied
warranty.  In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

3. This notice may not be removed or altered from any source distribution.

Jean-loup Gailly        Mark Adler
jloup@gzip.org          madler@alumni.caltech.edu

```

### cfuhash[¶](#cfuhash)

The implementation of the hash table used by the[`tracemalloc`](library/tracemalloc.html#module-tracemalloc) is based on the cfuhash project:

```text
Copyright (c) 2005 Don Owens
All rights reserved.

This code is released under the BSD license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
    copyright notice, this list of conditions and the following
    disclaimer in the documentation and/or other materials provided
    with the distribution.

  * Neither the name of the author nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

```

### libmpdec[¶](#libmpdec)

The`_decimal`C extension underlying the[`decimal`](library/decimal.html#module-decimal) module is built using an included copy of the libmpdec library unless the build is configured`--with-system-libmpdec`:

```text
Copyright (c) 2008-2020 Stefan Krah. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

```

### W3C C14N test suite[¶](#w3c-c14n-test-suite)

The C14N 2.0 test suite in the[`test`](library/test.html#module-test) package (`Lib/test/xmltestdata/c14n-20/`) was retrieved from the W3C website at[https://www.w3.org/TR/xml-c14n2-testcases/](https://www.w3.org/TR/xml-c14n2-testcases/) and is distributed under the 3-clause BSD license:

```text
Copyright (c) 2013 W3C(R) (MIT, ERCIM, Keio, Beihang),
All Rights Reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of works must retain the original copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the original copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name of the W3C nor the names of its contributors may be
  used to endorse or promote products derived from this work without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

```

### Audioop[¶](#audioop)

The audioop module uses the code base in g771.c file of the SoX project.[https://sourceforge.net/projects/sox/files/sox/12.17.7/sox-12.17.7.tar.gz](https://sourceforge.net/projects/sox/files/sox/12.17.7/sox-12.17.7.tar.gz)

>

This source code is a product of Sun Microsystems, Inc. and is provided for unrestricted use. Users may copy or modify this source code without charge.

SUN SOURCE CODE IS PROVIDED AS IS WITH NO WARRANTIES OF ANY KIND INCLUDING THE WARRANTIES OF DESIGN, MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE OF DEALING, USAGE OR TRADE PRACTICE.

Sun source code is provided with no support and without any obligation on the part of Sun Microsystems, Inc. to assist in its use, correction, modification or enhancement.

SUN MICROSYSTEMS, INC. SHALL HAVE NO LIABILITY WITH RESPECT TO THE INFRINGEMENT OF COPYRIGHTS, TRADE SECRETS OR ANY PATENTS BY THIS SOFTWARE OR ANY PART THEREOF.

In no event will Sun Microsystems, Inc. be liable for any lost revenue or profits or other special, indirect and consequential damages, even if Sun has been advised of the possibility of such damages.

Sun Microsystems, Inc. 2550 Garcia Avenue Mountain View, California 94043

### asyncio[¶](#asyncio)

Parts of the[`asyncio`](library/asyncio.html#module-asyncio) module are incorporated from[uvloop 0.16](https://github.com/MagicStack/uvloop/tree/v0.16.0) , which is distributed under the MIT license:

```text
Copyright (c) 2015-2021 MagicStack Inc.  http://magic.io

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```

### [Table of Contents](contents.html)

- [History and License](#)

  - [History of the software](#history-of-the-software)
  - [Terms and conditions for accessing or otherwise using Python](#terms-and-conditions-for-accessing-or-otherwise-using-python)

    - [PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2](#python-software-foundation-license-version-2)
    - [BEOPEN.COM LICENSE AGREEMENT FOR PYTHON 2.0](#beopen-com-license-agreement-for-python-2-0)
    - [CNRI LICENSE AGREEMENT FOR PYTHON 1.6.1](#cnri-license-agreement-for-python-1-6-1)
    - [CWI LICENSE AGREEMENT FOR PYTHON 0.9.0 THROUGH 1.2](#cwi-license-agreement-for-python-0-9-0-through-1-2)
    - [ZERO-CLAUSE BSD LICENSE FOR CODE IN THE PYTHON DOCUMENTATION](#zero-clause-bsd-license-for-code-in-the-python-documentation)

  - [Licenses and Acknowledgements for Incorporated Software](#licenses-and-acknowledgements-for-incorporated-software)

    - [Mersenne Twister](#mersenne-twister)
    - [Sockets](#sockets)
    - [Asynchronous socket services](#asynchronous-socket-services)
    - [Cookie management](#cookie-management)
    - [Execution tracing](#execution-tracing)
    - [UUencode and UUdecode functions](#uuencode-and-uudecode-functions)
    - [XML Remote Procedure Calls](#xml-remote-procedure-calls)
    - [test_epoll](#test-epoll)
    - [Select kqueue](#select-kqueue)
    - [SipHash24](#siphash24)
    - [strtod and dtoa](#strtod-and-dtoa)
    - [OpenSSL](#openssl)
    - [expat](#expat)
    - [libffi](#libffi)
    - [zlib](#zlib)
    - [cfuhash](#cfuhash)
    - [libmpdec](#libmpdec)
    - [W3C C14N test suite](#w3c-c14n-test-suite)
    - [Audioop](#audioop)
    - [asyncio](#asyncio)

#### Previous topic

[Copyright](copyright.html)

### This Page

- [Report a Bug](bugs.html)
- [Show Source](https://github.com/python/cpython/blob/main/Doc/license.rst)

«

### Navigation

- [index](genindex.html)
- [modules](py-modindex.html) |
- [previous](copyright.html) |
-
- [Python](https://www.python.org/) »
-

-
- [3.12.13 Documentation](index.html) »
- [History and License]
-

|
- Theme Auto Light Dark |

©[Copyright](copyright.html) 2001-2026, Python Software Foundation.
This page is licensed under the Python Software Foundation License Version 2.
Examples, recipes, and other code in the documentation are additionally licensed under the Zero Clause BSD License.
See[History and License](/license.html) for more information.

The Python Software Foundation is a non-profit corporation.[Please donate.](https://www.python.org/psf/donations/)

Last updated on Mar 07, 2026 (17:44 UTC).[Found a bug](/bugs.html) ?
Created using[Sphinx](https://www.sphinx-doc.org/) 8.2.3.

## Manifest quality note

Primary documentation for ZoneInfo and fold semantics.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `893a6e1d83e5d9580bd708f70ad2d20f24afd752c94edc39724ee8cd6e99cf21`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.

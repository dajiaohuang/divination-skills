---
source_id: "SRC-ASTRONOMY-NOAA-SOLAR-001"
title: "General Solar Position Calculations"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "catalog/sources/SRC-ASTRONOMY-NOAA-SOLAR-001.json"
capture_mode: "full"
aggregate_payload_sha256: "48438fec3e56bdbd3b0e62d7d52e5d275adac34e31932d0fca29058251eb6ada"
license: "US-Government-Public-Domain"
---

# General Solar Position Calculations

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-ASTRONOMY-NOAA-SOLAR-001`
- Manifest: `catalog/sources/SRC-ASTRONOMY-NOAA-SOLAR-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `retrieved-2026-07-23`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `bazi`, `liuyao`, `qimen`, `ziwei`
- Lineages: `apparent-solar-time-noaa`

## Rights envelope

- License: `US-Government-Public-Domain`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: NOAA formula PDF and NOAA public-domain policy inspected.
- License notes: NOAA-created government information is generally public domain. Credit NOAA and do not imply endorsement.

## Locator capture ledger

### Locator 1

- Registered: https://gml.noaa.gov/grad/solcalc/solareqns.PDF
- Resolved: https://gml.noaa.gov/grad/solcalc/solareqns.PDF
- Status: `captured`
- Media type: `application/pdf`
- SHA-256: `7fa1fdb5f6b5c05ab1ec3ffde92e6fb2d5df98bf1a87055075ae2c3c1240a627`

#### Parsed material

General Solar Position Calculations
                                    NOAA Global Monitoring Division


First, the fractional year (γ) is calculated, in radians.

                                   2                      ℎ𝑜𝑢𝑟 − 12
                            γ =       ∗ (day_of_year − 1 +           )
                                  365                         24

(For leap years, use 366 instead of 365 in the denominator.)

From γ, we can estimate the equation of time (in minutes) and the solar declination angle (in
radians).

        eqtime = 229.18*(0.000075 + 0.001868cos(γ) – 0.032077sin(γ) – 0.014615cos(2γ)
               – 0.040849sin(2γ) )

        decl = 0.006918 – 0.399912cos(γ) + 0.070257sin(γ) – 0.006758cos(2γ) + 0.000907sin(2γ)
                – 0.002697cos(3γ) + 0.00148sin (3γ)

Next, the true solar time is calculated in the following two equations. First the time offset is
found, in minutes, and then the true solar time, in minutes.

        time_offset = eqtime + 4*longitude – 60*timezone

where eqtime is in minutes, longitude is in degrees (positive to the east of the Prime Meridian),
timezone is in hours from UTC (U.S. Mountain Standard Time = –7 hours).

        tst = hr*60 + mn + sc/60 + time_offset

where hr is the hour (0 - 23), mn is the minute (0 - 59), sc is the second (0 - 59).

The solar hour angle, in degrees, is:

        ha = (tst / 4) – 180

The solar zenith angle () can then be found from the hour angle (ha), latitude (lat) and solar
declination (decl) using the following equation:

        cos() = sin(lat)sin(decl) + cost(lat)cos(decl)cos(ha)

And the solar azimuth (θ, degrees clockwise from north) is found from:

                                                sin(𝑙𝑎𝑡) cos(𝜙) − sin(𝑑𝑒𝑐𝑙)
                         cos(180 − 𝜃) = −
                                                      cos(𝑙𝑎𝑡) sin(𝜙)
                                   Sunrise/Sunset Calculations


For the special case of sunrise or sunset, the zenith is set to 90.833 (the approximate correction for
atmospheric refraction at sunrise and sunset, and the size of the solar disk), and the hour angle
becomes:

                                         cos(90.833)
                   ℎ𝑎 = ±𝑎𝑟𝑐𝑐𝑜𝑠 {                        − tan(𝑙𝑎𝑡) tan(𝑑𝑒𝑐𝑙)}
                                      cos(𝑙𝑎𝑡) cos(𝑑𝑒𝑐𝑙)

where the positive number corresponds to sunrise, negative to sunset.

Then the UTC time of sunrise (or sunset) in minutes is:

       sunrise = 720 – 4*(longitude + ha) – eqtime

where longitude and hour angle are in degrees and the equation of time is in minutes.

Solar noon for a given location is found from the longitude (in degrees, positive to the east of the
Prime Meridian) and the equation of time (in minutes):

       snoon = 720 – 4*longitude – eqtime

### Locator 2

- Registered: https://gml.noaa.gov/grad/solcalc/calcdetails.html
- Resolved: https://gml.noaa.gov/grad/solcalc/calcdetails.html
- Status: `captured`
- Media type: `text/html; charset=UTF-8`
- SHA-256: `3da7e18c6d2a9e4b0070214cdda1ab3d6fa02c3e700f0b4964982e355ce891ef`

#### Parsed material

Solar Calculator - NOAA Global Monitoring Laboratory

[Skip to main content](#main)

An official website of the United States government[Here's how you know](#top-grey-exp)

**Official websites use .gov**

A**.gov**website belongs to an official government organization in the United States.

**Secure .gov websites use HTTPS**

A lock ( ) or**https://**means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

**Search

Search GML:



[Global Monitoring Laboratory](/)

[Menu](#)

- [Home](/)
- [About](#)

[About GML](/about/aboutgml.html)[Science Reviews](/review/)[Safety Program](/safety/)[Employment](/about/jobs.html)[Visiting](https://www.boulder.noaa.gov/outreach/tour-noaa-boulder/)[Contact Us](/about/contacts.html)[Intranet](https://sites.google.com/noaa.gov/oar-gml-intranet/home)

- [People](#)

[Organization](/about/orgchart.html)[Staff](/about/stafflist.html)[Employee Spotlight](/about/employees.html)

- [Research](#)

[Research Overview](/about/research.html)[Carbon Cycle Greenhouse Gases](/ccgg/)[Greenhouse gases and Ozone-depleting Substances](/hats/)[Ozone and Water Vapor](/ozwv/)[Global Radiation, Aerosols and Clouds](/grad/)[Publications](/publications/) Calibration Facilities[WMO Central Calibration Laboratory](/ccl/)[Central UV Calibration Facility](/grad/calfacil/)[Broadband Solar Calibration Facility](/grad/srf.html)[World Dobson Ozone Calibration Centre](/ozwv/dobson/)

- [Observing Networks](#)

Overview[Observations Overview](/about/networks.html)[Measurement Sites](/dv/site/)[Field Campaigns](/about/campaigns.html)

Atmospheric Baseline Observatories[Observatory Operations](/obop/)[Barrow, Alaska](/obop/brw/)[Mauna Loa, Hawaii](/obop/mlo/)[American Samoa](/obop/smo/)[South Pole](/obop/spo/)

Observing Networks[Greenhouse Gas Reference Network](/ccgg/about.html)[Halocarbons and Trace Gases](/hats/flask/flasks.html)[Surface Radiation](/grad/field.html)[Federated Aerosol Network](/aero/net/)[Ozone](/ozwv/network.php)[Water Vapor](/ozwv/wvap/)

- [Data & Products](#)

Data[Data & Products Portal](/data/)[Data Finder](/data/data.php)[ObsPack Data Products](/ccgg/obspack/)[Measurement Sites](/dv/site/)

Visualization & Tools[Data Viewer](/dv/iadv/)[South Pole Ozone Hole](/dv/spo_oz/)[Mauna Loa Apparent Transmission](/grad/mloapt.html)[Barrow Snow Melt Dates](/grad/snomelt.html)

Products[Greenhouse Gas Index](/aggi/)[Ozone Depletion Index](/odgi/)[Trends in CO 2 , CH 4 , N 2 O, SF 6](/ccgg/trends/)[Modeling](/modeling.html)

- [Information](#)

[News](/news/)[Seminars](/about/seminars.php)[Education/Outreach](/education/)[Student Opportunities](/interns/)[FAQ's](/education/faq_cat-1.html)[Publications](/publications/) Webcams[South Pole Webcam](/obop/spo/livecamera.html)[Mauna Loa Webcams](/obop/mlo/livecam/livecam.html)[Barrow Webcam](/obop/brw/livecamera.html) Global Monitoring Annual Conference[GMAC Conference](/gmac/)

**Search

Search GML:

## Solar Calculation Details

Important Notice: NOAA/GML Solar Calculator
Please be advised that the NOAA/GML Solar Calculator is no longer actively supported or maintained by our team. While the calculator remains available for use, we cannot guarantee its accuracy or functionality and will not be providing updates or technical support. We apologize for any inconvenience this may cause and appreciate your understanding.

### General

The calculations in the NOAA Sunrise/Sunset and Solar Position Calculators are based on equations from***Astronomical Algorithms***, by Jean Meeus. The sunrise and sunset results are theoretically accurate to within a minute for locations between +/- 72° latitude, and within 10 minutes outside of those latitudes. However, due to variations in atmospheric composition, temperature, pressure and conditions, observed values may vary from calculations.

The following spreadsheets can be used to calculate solar data for a day or a year at a specified site. They are available in Microsoft Excel and Open Office format. Please note that calculations in the spreadsheets are only valid for dates between 1901 and 2099, due to an approximation used in the Julian Day calculation. The web calculator does not use this approximation, and can report values between the years -2000 and +3000.

 |  | Microsoft Excel | Day | [NOAA_Solar_Calculations_day.xls](./NOAA_Solar_Calculations_day.xls) | Year | [NOAA_Solar_Calculations_year.xls](./NOAA_Solar_Calculations_year.xls)

 |  | Open Office | Day | [NOAA_Solar_Calculations_day.ods](./NOAA_Solar_Calculations_day.ods) | Year | [NOAA_Solar_Calculations_year.ods](./NOAA_Solar_Calculations_year.ods)

### Data for Litigation

The NOAA Solar Calculator is for research and recreational use only. NOAA cannot certify or authenticate sunrise, sunset or solar position data. The U.S. Government does not collect observations of astronomical data, and due to atmospheric conditions our calculated results may vary significantly from actual observed values.

For further information, please see the U.S. Naval Observatory's page[Astronomical Data Used for Litigation](https://aa.usno.navy.mil/faq/lawyers) .

### Historical Dates

For the purposes of these calculators the current[Gregorian calendar](./glossary.html#gregoriancalendar) is extrapolated backward through time. When using a date before 15 October, 1582, you will need to correct for this.

The year preceding year 1 in the calendar is year zero (0). The year before that is -1.

The approximations used in these programs are very good for years between 1800 and 2100. Results should still be sufficiently accurate for the range from -1000 to 3000. Outside of this range, results may be given, but the potential for error is higher.

### Atmospheric Refraction Effects

For sunrise and sunset calculations, we assume 0.833° of[atmospheric refraction](glossary.html#atmosphericrefraction) . In the solar position calculator, atmospheric refraction is modeled as:

 | Solar Elevation | [Approximate Atmospheric Refraction Correction](atmosrefr.gif) (°) | 85° to 90° | 0 | 5° to 85° |  | -0.575° to 5° |  | < -0.575° |

The effects of the atmosphere vary with atmospheric pressure, humidity and other variables. Therefore the solar position calculations presented here are approximate. Errors in sunrise and sunset times can be expected to increase the further away you are from the equator, because the sun rises and sets at a very shallow angle. Small variations in the atmosphere can have a larger effect.

Solar Calculation Resources:

- [NOAA Solar Calculator](./index.html)
- [Old Sunrise Calculator](./sunrise.html)
- [Old Solar Pos Calculator](./azel.html)

- [Solar Calculator Links](./sollinks.html)
- [Solar Calculator Glossary](./glossary.html)

- [Calculation Details](./calcdetails.html)
- [Time Zone Table](./timezone.html)

[Global Monitoring Laboratory](/)
»[U.S. Department of Commerce](https://www.commerce.gov/)
»[National Oceanic & Atmospheric Administration](https://www.noaa.gov/)
»[NOAA Research](https://research.noaa.gov/)

[Privacy Policy](https://www.noaa.gov/protecting-your-privacy) |[Accessibility](https://www.noaa.gov/accessibility) |[Disclaimer](/about/disclaimer.html) |[Disclaimer for External Links](https://www.noaa.gov/disclaimer) |[FOIA](https://www.noaa.gov/information-technology/foia) |[Usa.gov](https://www.usa.gov)

[**](https://www.facebook.com/NOAAResearch)[**](https://instagram.com/noaaresearch)
[Site Contents](/sitemap/)
[Contact Us](/about/contacts.html) |[Webmaster](mailto:webmaster.gml@noaa.gov)
[Take Our Survey](/survey/)

### Locator 3

- Registered: https://sos.noaa.gov/copyright/
- Resolved: https://sos.noaa.gov/copyright/
- Status: `captured`
- Media type: `text/html`
- SHA-256: `bd16519cc168377e2eb10e7c56f00ea0e2309619546461fd96742067fb5d7d00`

#### Parsed material

Copyright Information - Science On a Sphere

[Skip to Content](#main-content)

[Science On a Sphere](/)

- [About](/about/)
- [SOS](/sos/)
- [SOS Explorer](/sos-explorer/)
- [Education](/education/)
- [Catalog](/catalog/)
- [Support](/support/)

# Copyright Information

- [Home](/)
- [Copyright Information]

- [Copyright Information](/copyright/)

  - [Use of Digital Media created by NOAA](#use-of-digital-media-created-by-noaa)

    - [General Digital Media Conditions](#use-of-digital-media-created-by-noaa-general-digital-media-conditions)
    - [Specific Digital Media Conditions](#use-of-digital-media-created-by-noaa-specific-digital-media-conditions)

  - [Use of Digital Media created by sources other than NOAA](#use-of-digital-media-created-by-sources-other-than-noaa)
  - [Third Party Use of Digital Media](#third-party-use-of-digital-media)

“Digital Media” refers to datasets and visualizations (which includes but is not limited to raw data, rendered data, label files, and pictures), video and motion picture recordings, photography, and audio recordings.

## Use of Digital Media created by NOAA

[Permalink to Use of Digital Media created by NOAA](#use-of-digital-media-created-by-noaa)

### General Digital Media Conditions

[Permalink to General Digital Media Conditions](#use-of-digital-media-created-by-noaa-general-digital-media-conditions)

- In general, digital media created by NOAA is not copyrighted
- Digital media created by NOAA can be used for educational or informational purposes, including photo collections, textbooks, public exhibits and Internet web pages
- Some digital media may contain a Copyright Notice or other distribution restrictions as defined by the originator of the digital media. It the responsibility of the user to identify the digital media creator and to obtain permission before making use of this material
- Please acknowledge NOAA as the source of any used digital media, if not otherwise noted
- NOAA materials, digital media or otherwise, may not be used to state or imply the endorsement by NOAA or by any NOAA employee of a commercial product, service or activity, or used in any other manner that might mislead the public

### Specific Digital Media Conditions

[Permalink to Specific Digital Media Conditions](#use-of-digital-media-created-by-noaa-specific-digital-media-conditions)

#### Photography

[Permalink to Photography](#use-of-digital-media-created-by-noaa-specific-digital-media-conditions-photography)

If a recognizable person appears in a photograph, use for commercial purposes may infringe a right of privacy or publicity and permission should be obtained from the recognizable person.

#### Audio Recordings

[Permalink to Audio Recordings](#use-of-digital-media-created-by-noaa-specific-digital-media-conditions-audio-recordings)

An audio recording may be downloaded, excerpted or reproduced and distributed, without further permission from NOAA. However, use of a portion or segment of an audiotape, such as talent, narration or music, may infringe a right of publicity or copyright and permission should be obtained from the source.

#### Video and Motion Picture Recordings

[Permalink to Video and Motion Picture Recordings](#use-of-digital-media-created-by-noaa-specific-digital-media-conditions-video-and-motion-picture-recordings)

A recording may be reproduced and distributed without further permission from NOAA. Copyrighted music or footage, which is incorporated in a production, may not be used unless permission is obtained from the copyright owner. While in most instances using non-copyrighted segments is permitted, use for commercial purposes of a portion or segment containing talent or a recognizable person may infringe a right of publicity and permission should be obtained from the talent or recognizable person.

## Use of Digital Media created by sources other than NOAA

[Permalink to Use of Digital Media created by sources other than NOAA](#use-of-digital-media-created-by-sources-other-than-noaa)

Some digital media on the SOS public servers (web site or other) are owned by organizations or individuals other than NOAA. These owners have agreed to make their digital media available for educational, journalistic, and personal uses, but restrictions may be placed on other uses (commercial or otherwise). To obtain permission for use of the digital media, contact the digital media creator directly. In cases where the creator is not listed, please contact NOAA for further information. Ownership of datasets in the online Dataset Catalog by parties other than NOAA is noted in the table at the bottom of each catalog page.

## Third Party Use of Digital Media

[Permalink to Third Party Use of Digital Media](#third-party-use-of-digital-media)

As required by 17 U.S.C. 403, third parties producing copyrighted works consisting predominantly of the material produced by U.S. government agencies must provide notice with such work(s) identifying the U.S. Government material incorporated and stating that such material is not subject to copyright protection. The information on government web pages is in the public domain unless specifically annotated otherwise (copyright may be held elsewhere) and may therefore be used freely by the public.

Edited May 28, 2009

Search Search

## Science On a Sphere

- [Home](/)
- [About](/about/)
- [SOS](/sos/)
- [SOS Explorer](/sos-explorer/)
- [Education](/education/)
- [Catalog](/catalog/)
- [Support](/support/)

## About Us…

- [Accessibility](/accessibility/)
- [Contact Us](/contact/)
- [Copyright](/copyright/)
- [Disclaimer](/disclaimer/)
- [Handouts / Logos](/handouts-logos/)
- [News](/news/)
- [Privacy Policy](/privacy/)

## Find us on…

- [Facebook](https://www.facebook.com/scienceonasphere)
- [Instagram](https://www.instagram.com/scienceonasphere/)
- [YouTube](https://www.youtube.com/user/scienceonasphere)

Science On a Sphere® is a program within the[National Oceanic and Atmospheric Administration](https://noaa.gov/) supported by the[Office of Education](https://www.noaa.gov/office-education) in partnership with the[Global Systems Laboratory](https://gsl.noaa.gov/) .

© 2026 Science On a Sphere®

## Manifest quality note

Official approximate equation-of-time and true-solar-time equations. The result is an engineering approximation, not an ephemeris-grade SPA implementation.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `48438fec3e56bdbd3b0e62d7d52e5d275adac34e31932d0fca29058251eb6ada`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.

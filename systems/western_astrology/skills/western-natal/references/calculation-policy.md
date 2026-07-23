# Calculation policy

Use tropical geocentric true-ecliptic-of-date positions from pinned Astronomy Engine 2.1.19. Longitude is east-positive. Require an IANA time zone, local date/time without offset, latitude, and longitude. Reject DST gaps; require `fold` for repeated local times.

The default house system is whole-sign. Equal house must be explicitly requested. Do not calculate or approximate Placidus. The supported bodies are Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto. See the system `LINEAGE.md` for aspect orbs and omissions.

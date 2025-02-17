China Set: Stations - Wuhu Changelog
=========================

0.3.4 (Work-in-progress)
------------------------
Make parameters stable -- future changes to parameters should no longer mess up your existing settings. The functionality was introduced in 0.3.3 but the stability was accidentally broken in the same version, so 0.3.4 will be the first version to actually support this.

Removed 8bpp graphics and applied other optmization techniques to reduce NewGRF size.

0.3.3 (2025-01-27)
------------------------
Preliminary traditional Chinese support.

Fix the layout for big (>= 30 rows) stations. They are still imperfect due to technical limitations, but should be slightly more pleasing than before.

New parameters to choose between using company colours or pre-selected colours.

Optimize the size of the newGRF (3 MiB smaller than before).

0.3.2 (2024-12-18)
------------------------
Fix a cropping issue for preview sprites.

0.3.1 (2024-10-13)
------------------------
Platform and shelter parameters now also control the availability of platform tiles.

Make the modern Wuhu Station preview images shorter, so they fit in the preview window.

0.3.0 (2024-10-02)
------------------------
Add the 1934 Wuhu Station.

Add snow and escalator graphics for station buildings.

Designate station tiles without platforms as waypoints.

Add bus stops, road waypoints and objects (not included in 0.3.0 release) to use alongside the station.

Support older versions of OpenTTD.

Add more parameters to control what's available, and also reduce the UI clutter.

Bugfix: station templates with shelter type 2 sometimes included wrong shelter graphics.

0.2.2 (2024-06-14)
--------------------
Further fix for the climate-aware groundsprites: they didn't work with custom track NewGRFs.

Add parameter to control station introduction years.

0.2.1 (2024-06-02)
--------------------
Fix monorail and maglev graphics (broken by the climate-aware groundsprite).

0.2.0 (2024-05-31)
--------------------
Redesign graphics, now the station building is always built atop a concrete platform. Corresponding tiles ("concourse") are also made buildable.

Switch platform/shelter graphics to the new ones from China Set: Stations; support all existing combinations.

Rework templates, now it is guaranteed that any rectangle-shaped subset of a template also has a coherent look-and-feel, and the existence of any platform is remembered during such (de)construction.

Make groundsprites climate aware: now desert and snow tiles show the respective ground type correctly.

0.1.2 (2024-04-30)
--------------------
Fix traversability of fully-traversable templates.

0.1.1 (2024-04-29)
--------------------
Urgent quick fix for broken platform graphics.

0.1.0 (2024-04-29)
--------------------
Initial release. Adds the Wuhu Station (2015), featuring 12 station templates and 423 modular station tiles.

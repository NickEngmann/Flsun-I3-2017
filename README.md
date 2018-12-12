# Flsun-I3-2017
Nick's Reference Notes about the FLsun I3 (2017) Printer
![Printer](https://github.com/NickEngmann/Flsun-I3-2017/blob/master/images/version2-1.jpg)
## Link to Livestream
<a class="link" href="https://www.twitch.tv/nickyslickshaha" target="_blank">Livestream</a>

## Introduction
Buying a DIY kit and building my own 3D printer ended up being one of the most stressful projects I've ever embarked on. I ended up putting about 80 hours into a $200 kit, just to get the initial printer working.
This was due to roughly translated instructions, vague videos, and to be honest - a lot of inexperience on my part. So I decided to make this repo that details some of my journey incase it can help anyone else that wants to do something similar.

## Helpful links to begin.
I purchased the <a target="__blank" href="https://www.amazon.com/FLSUN-Printer-leveling-Desktop-Printing/dp/B01N6BEK4R/ref=cm_cr_arp_d_product_top?ie=UTF8">FLSun i3 2017 printer</a>. This is now one of the two printers I own. I personally would not recommend it at this time, but if you already have the printer, you might as well work on it to get it up and running!
You are probably going to need the instructions on how to assemble the printer, as well as helpful videos that can guide you through the process. While the Amazon kit came with <i>some</i> of the necessary documents, here is a list of everything I gathered during my assembly process.
![3D-Prints](https://github.com/NickEngmann/Flsun-I3-2017/blob/master/images/2.jpg)

# Various Instructions

## Assembly Instructions:
www.dropbox.com/s/r4itqksu4w9gef6/C%20assembly%20manual%20newest.pdf?dl=0

## Instructional Youtube Videos:
<a href="youtu.be/Ok7igmasvXQ">Part 1</a>
<a href="youtu.be/bGDFUZiFhco">Part 2</a>
<a href="youtu.be/PI1t_t1kJ3A">Part 3</a>
<a href="youtu.be/oagV9PlhO2M">Part 4</a>
<a href="youtu.be/7kDTEWIiLE8">Part 5</a>

## Board Connection Diagram:
Those videos are helpful to get the device assembled, but they dont tell you how to connect the various cables of the printer to the controller, refer to <a href="https://ibb.co/noyNLv"> this </a> if you need assistance with that

## Auto leveling Instructiuon:
Depending on your Auto-leveler you may want to go with different methods. At first I used the stock Auto leveler but I have recently upgraded to a BLTouch. The BLTouch is MUCH easier to use than the standard Auto-Leveler that comes with the system. If using the BLTouch use the firmware image MarlinBLTouch in the <a href="https://github.com/NickEngmann/Flsun-I3-2017/blob/master/firmware/MarlinBlTouch" target="__blank">firmware/MarlinBLTouch</a> folder.

#### Stock Auto leveler
You can find auto-leveling instructions <a href="www.dropbox.com/s/ksriv7bdjm1eave/How%20to%20use%20auto-leveling%20system%20for%20i3.zip?dl=0"> here</a> including text based instructions as well as a video.
This ended up being one of the most difficult portions for me. In the end I ended up resorting to a manual way of setting the auto-leveler. My advice is that it is best to adjust the auto-leveler sensor position with the nozzle very close to the bed.
Then the Z Offset is small and can be easily set using M851, M500, M501 and M503.
(Tip: Fix Bed Level Sensor in its lowest position, then move it down to activate and use old credit cards to measure the gap, sensor - bed, and nozzle-bed. Subtract nozzle gap and readjust sensor fixing.)
![Printer](https://github.com/NickEngmann/Flsun-I3-2017/blob/master/images/3.jpg)

### BL Touch
I purchased a BL Touch for my auto leveling and I couldn't be happier. The BLTouch is a servo enhanced leveler for precise leveling. In order to use it you have to upgrade your Marlin firmware on your FLSUN. <a href="https://www.youtube.com/watch?v=3gwWVFtdg-4">Here is a video</a> on how to set up and upgrade your Marlin firmware. The necessary firmware update file can be found in the "firmware" directory. You can also find the user manual on how to do a Marlin upgrade here.

***Important note on the Marlin Firmware upgrade!***
A lot of things can change with the firmware upgrade of a device. Make sure to take a glance at the configuration file whenever you do ANY firmware upgrade and make sure the correct things for your 3D printer are flagged :)

![Printer](https://github.com/NickEngmann/Flsun-I3-2017/blob/master/images/BLTouch.jpg)
# Various Printer Enhancements

One of the best things about owning a 3D printer is that you can print its own enhancements. Here are some of the enhancements I printed off for my printer in order to improve quality of prints and overall aesthetic:
<a href="https://www.thingiverse.com/thing:2481325">X-carriage Holder</a>
<a href="https://www.thingiverse.com/thing:2113492">Y-axis cable chain</a>
<a href="https://www.thingiverse.com/thing:2120148">Z-axis cable chain</a>
There are also a handful of things that I purchased in order to make the printer easier to use
<a href="https://www.amazon.com/ANYCUBIC-Ultrabase-Platform-Tempered-310x310mm/dp/B0777BS1RB/ref=sr_1_2?ie=UTF8&qid=1544593215&sr=8-2&keywords=anycubic+ultrabase">Ultrabase Anycubic Base Plate</a>
<a href="https://www.amazon.com/gp/product/B01FJ9LUO6/ref=oh_aui_search_detailpage?ie=UTF8&psc=1">Extra Smooth Filament Holder</a>

![Z-cable-chain](https://github.com/NickEngmann/Flsun-I3-2017/blob/master/images/version2-2.jpg)


## Community

Here are a few Facebook groups that I joined for added support through the process:
https://www.facebook.com/groups/FlsunCube/about/ </br>
https://www.facebook.com/groups/FLSUN3DP/?ref=br_rs </br>
https://www.facebook.com/groups/1855314194686705/?ref=br_rs </br>
https://www.facebook.com/groups/511992158981791/?ref=br_rs </br>
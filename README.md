# VATSIMvision
Counts planes in AOR using colour segmentation

## What?
![image](https://user-images.githubusercontent.com/51272243/153290841-16ed59fa-be9c-4972-945a-bc3ab39db0a1.png)


## How
A screencapture is started that searches for certain colours on your screen. When a track color has been detected it check whether the track is (partly) in the AOR. The AOR is Euroscope's active background color.

## Why
There's no use case.

## Limitations
A lot. Out of the boxs it only works for the Belux vacc setup: black active background and light blue velocity header. You'll may set this up on your own using "FindHSVvalues.py". 
Keep in mind the color for these tracks must be distinct.

It does not take vertical bounds into consideration. 

Tracks with STCA, AIW, and other warnings that change the color of velocity header, are not counted.

Overlapping velocity headers may be counted as one. 

## Those other files?
They're just there for me. You may use them. I used these files to create the main "CountinAOR.py" file.

# Minecraft server monitor
A set of small scripts providing the possibility to monitor the current amount of players online on a Minecraft server, store the data at a set time interval and display a graph of player activity throughout the day.

Note: Currently, the only supported way to monitor a server is to enter its URL address on **minecraft-mp.com**


# main.py
Uses: requests, BeautifulSoup4

This script allows you to create or choose a text file to store data, choose which server you want to check and decide between a single or periodic data read.
Data is stored in a JSON format.


# graph.py
Uses: matplotlib

Draws a graph of player activity based on the data present in the selected text file.


# merge.py
In case the data was stored in different files (for example, a single server was monitored on different devices), merge.py allows the user to merge two files into one.


# Important note: The data is not timestamped. Because of this, merging files that contain data reads from overlapping time periods will distort the final result.

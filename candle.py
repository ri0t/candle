__author__ = 'riot'

import sys
import os
from pprint import pprint
import datetime
import pytz
import pygame
import calendar
from icalendar import Calendar
import IPython

calendarfile = '/home/riot/STUFF/CALENDARS/Home.ics'
outfile = 'calendar.png'
width = 800
height = 600

year = 2014
month = 12
tz = pytz.utc

daywidth = (width + 5) / 7
weekheight = (height + 5) / 5
center = [width / 2.0, height / 2.0]
fontcolor = pygame.Color('#222222')
linecolor = pygame.Color('#555555')
backcolor = pygame.Color('#ffffff')
color_month = pygame.Color('#AAAAAA')
color_transparent = pygame.Color('#000000FF')

pygame.init()

ev_font_size = 12
day_font = pygame.font.SysFont("monospace", 12)
ev_font = pygame.font.SysFont("marvel", ev_font_size)
month_font = pygame.font.SysFont("marvel", 144)

screen = pygame.display.set_mode([width, height])
pygame.draw.rect(screen, backcolor, [0, 0, width, height])


templ_month = calendar.monthcalendar(year, month)

icalfile = open(calendarfile, "rb")
icaldata = Calendar.from_ical(icalfile.read())

events = {}
evs = []

for event in icaldata.walk("VEVENT"):
    eventtime = event['DTSTART'].dt
    #print "\n", event, "#"*5, "\n", eventtime

    if eventtime.year == year and eventtime.month == month:
        events[eventtime] = event
        #print event['SUMMARY']
        evs += [event]

def printev(ev):
    msg = ""
    for k,v in ev.iteritems():
        if k in ('DTSTART', 'DTEND'):
            v = v.dt
        msg += "[%-10s]: %s\n" % (k, v)

    print(msg)

for ev in evs:
    printev(ev)
    print("\n")

################ PAINTING ################

label_month = month_font.render(calendar.month_name[month], 1, color_month)
label_month = pygame.transform.rotate(label_month, 30)
label_month_center = (center[0] - label_month.get_width() / 2, center[1] - label_month.get_height() / 2)

screen.blit(label_month, label_month_center)

for no_week in range(5):
    pygame.draw.line(screen, linecolor, [0, weekheight * no_week], [width, weekheight * no_week], 1)
for no_day in range(7):
    pygame.draw.line(screen, linecolor, [no_day * daywidth, 0], [no_day * daywidth, height], 1)

for no_week, templ_week in enumerate(templ_month):
    y = no_week * weekheight + 5
    for no_day, templ_day in enumerate(templ_week):
        screen.set_clip([no_day*daywidth, no_week*weekheight, (no_day+1)*daywidth, (no_week+1)*weekheight])
        if templ_day != 0:
            x = no_day * daywidth + 5
            y_offset = 0

            label = day_font.render(str(templ_day), 1, fontcolor)
            screen.blit(label, (x, y))

            for ev in evs:
                ev_start = ev['DTSTART'].dt
                ev_end = ev['DTEND'].dt

                if ev_start.day == templ_day or (ev_start.day <= templ_day and ev_end.day > templ_day):
                    label = ev_font.render(str(ev['SUMMARY']), 1, fontcolor)

                    if y_offset == 0:
                        x_offset = 15
                    else:
                        x_offset = 0

                    screen.blit(label, (x + x_offset, y + y_offset), [0, 0, daywidth - x_offset - 5, ev_font_size])
                    y_offset += 10


screen = pygame.transform.rotate(screen, 90)

pygame.display.update()
pygame.display.flip()

pygame.image.save(screen, outfile)

while 1:
    pass


#!/usr/bin/env python3

import gi
gi.require_version('Playerctl', '1.0')
from gi.repository import Playerctl, GLib
import paho.mqtt.publish as pub
import sys
import datetime
import json

player_name = sys.argv[1]
topic = 'scotty/music'
broker = ''
auth = {'username': sys.argv[2], 'password' : sys.argv[3]} 

def publish(song):
  song['_timestamp'] = str(datetime.datetime.now())
  song_str = json.dumps(song)
  pub.single(topic=topic, payload=song_str, hostname=broker, auth=auth, retain=True)

def on_play(player):
  title = player.get_title()
  artist = player.get_artist() 
  album = player.get_album()
  song = {
    'title' : title,
    'artist' : artist,
    'album' : album 
  }
  publish(song)

if __name__ == '__main__':
  player = Playerctl.Player(player_name=player_name)
  player.on('play', on_play)

  # wait for events
  main = GLib.MainLoop()
  main.run()


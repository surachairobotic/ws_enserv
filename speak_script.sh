#!/bin/bash
say() { local IFS=+; "C:/Program Files/VideoLAN/VLC/vlc.exe" --aout wave "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=%22%E0%B8%AA%E0%B8%A7%E0%B8%B1%E0%B8%AA%E0%B8%94%E0%B8%B5%20%E0%B8%8A%E0%B8%B2%E0%B8%A7%E0%B9%82%E0%B8%A5%E0%B8%81%22&tl=th"; }
say $*
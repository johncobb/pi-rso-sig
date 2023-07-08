# Raspberry Pi Audio File (SYBA)


Detect USB Soundcard Device
Run following command an plugin in USB Sound Card device.
```console
sudo tail -f /var/log/messages
```

Check proper loading of kernel module.
```console
lsmod | grep snd_usb_audio
```

Display ALSA playback device
ALSA Card Id is "Pro or number 1. The ALSA Card has two devices:
0 - Dirst Device
1 - Second Device
```console
aplay -l
```

The ALSA Card has in-line microphone. List the ALSA capture device.
```console
arecord -l
```

## Verify ALSA playback
A female voice stating "Front left... front right." on both speakers (headphones) should be playing.
```console
speaker-test -Dhw:1,0 -c2 -twav
```



### References
https://www.instructables.com/Use-USB-Sound-Card-in-Raspberry-Pi/

http://alsa-project.org


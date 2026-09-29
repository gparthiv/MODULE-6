"""
Simulates the message flow from an AAOS "Play" tap down to the Audio HAL.
Prints logcat-style logs: MM-DD HH:MM:SS.mmm Level/Tag: Message
Uses only the Python standard library.
"""

import time
from datetime import datetime


def log(level, tag, message):
    """Print one logcat-style line, then pause briefly to mimic real latency."""
    now = datetime.now()
    timestamp = now.strftime("%m-%d %H:%M:%S.") + f"{now.microsecond // 1000:03d}"
    print(f"{timestamp} {level}/{tag}: {message}")
    time.sleep(0.1)


def main():
    print("--- AAOS Play-button message flow simulation ---\n")

    # Layer 1: HMI
    log("D", "InputReader", "Touch event received at (540, 960) - ACTION_DOWN")
    log("D", "InputReader", "Touch event dispatched to com.android.car.media")
    log("I", "CarMediaApp", "Play button clicked")
    log("I", "CarMediaApp", "Calling MediaController.getTransportControls().play()")

    # Layer 2: MediaSession
    log("I", "MediaSession", "onPlay() received from controller")
    log("I", "MediaSession", "Playback state -> STATE_PLAYING")
    log("I", "MediaSession", "Requesting audio focus for USAGE_MEDIA")

    # Layer 3: CarAudioService + AudioFlinger
    log("D", "CarAudioService", "requestAudioFocus() from com.android.car.media")
    log("D", "CarAudioService", "Checking active focus holders in zone 0...")
    log("D", "CarAudioService", "No conflicts found - AUDIOFOCUS_REQUEST_GRANTED")
    log("I", "AudioTrack", "Creating AudioTrack: 48000 Hz, stereo, PCM_16BIT")
    log("I", "AudioTrack", "AudioTrack.play() called")
    log("D", "AudioFlinger", "Track created, attached to MixerThread")
    log("D", "AudioFlinger", "Mixing PCM frames from active tracks")

    # Layer 4: Audio HAL
    log("D", "AudioHALSvc", "IStreamOut::write() called via AIDL (4096 bytes)")
    log("D", "AudioHALSvc", "Forwarding buffer to ALSA via pcm_write()")

    # Layer 5: Kernel
    log("D", "ALSA-Driver", "PCM buffer received on card 0, device 0")
    log("D", "ALSA-Driver", "DMA transfer started to audio codec")
    log("D", "ALSA-Driver", "Audio output active - sound playing on speakers")

    print("\n--- Simulation complete ---")


if __name__ == "__main__":
    main()
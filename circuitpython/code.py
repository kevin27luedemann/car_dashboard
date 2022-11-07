import time
import board
import busio
import board
import dotstar_featherwing
import font3
import time
import random

import adafruit_gps

normal          = (8,0,0)
slow            = (0,8,0)
fast            = (0,0,8)

def knots_to_kph(knots):
    return knots*1.852

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,500")

# Set up dotstar wing
wing = dotstar_featherwing.DotstarFeatherwing(board.D13, board.D11, 0.25)
wing.clear()
wing.show()

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    gps.update()

    current = time.monotonic()
    if current - last_print >= 0.5:
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix...")
            wing.clear()
            wing.show()
            continue
        #print("=" * 40)  # Print a separator line.
        #print(
        #    "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
        #        gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
        #        gps.timestamp_utc.tm_mday,  # struct_time object that holds
        #        gps.timestamp_utc.tm_year,  # the fix time.  Note you might
        #        gps.timestamp_utc.tm_hour,  # not get all data like year, day,
        #        gps.timestamp_utc.tm_min,  # month!
        #        gps.timestamp_utc.tm_sec,
        #    )
        #)
        #print("Latitude: {0:.6f} degrees".format(gps.latitude))
        #print("Longitude: {0:.6f} degrees".format(gps.longitude))
        #print(
        #    "Precise Latitude: {:2.}{:2.4f} degrees".format(
        #        gps.latitude_degrees, gps.latitude_minutes
        #    )
        #)
        #print(
        #    "Precise Longitude: {:2.}{:2.4f} degrees".format(
        #        gps.longitude_degrees, gps.longitude_minutes
        #    )
        #)
        #print("Fix quality: {}".format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        #if gps.satellites is not None:
        #    print("# satellites: {}".format(gps.satellites))
        #if gps.altitude_m is not None:
        #    print("Altitude: {} meters".format(gps.altitude_m))
        #if gps.speed_knots is not None:
        #    print("Speed: {} kph".format(knots_to_kph(gps.speed_knots)))
        #if gps.track_angle_deg is not None:
        #    print("Track angle: {} degrees".format(gps.track_angle_deg))
        #if gps.horizontal_dilution is not None:
        #    print("Horizontal dilution: {}".format(gps.horizontal_dilution))
        #if gps.height_geoid is not None:
        #    print("Height geoid: {} meters".format(gps.height_geoid))

        speed       = int(round(knots_to_kph(gps.speed_knots),0))
        wing.clear()
        if speed > 113 and speed <= 123:
            wing.shift_in_string(font3.font, "{:d}".format(speed), slow, 0.0)
        elif speed >= 131:
            wing.shift_in_string(font3.font, "{:d}".format(speed), fast, 0.0)
        else:
            wing.shift_in_string(font3.font, "{:d}".format(speed), normal, 0.0)
        wing.show()
        print()

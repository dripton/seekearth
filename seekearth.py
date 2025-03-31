#!/usr/bin/env python3


"""Find the direction and distance to the nearest sample of some metal or stone."""

import argparse
from collections import namedtuple, defaultdict
from pprint import pprint


def parse_prefix(prefix_path):
    map_to_prefix = {}
    with open(prefix_path) as fil:
        for line in fil:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(":")
                if len(parts) == 2:
                    map_name = parts[0].strip()
                    map_prefix = parts[1].strip()
                    map_to_prefix[map_name] = map_prefix
    return map_to_prefix


def parse_xyz(xyz_path):
    MapInfo = namedtuple("MapInfo", ["x0", "y0", "z", "x_scale", "y_scale"])
    map_to_info = {}
    with open(xyz_path) as fil:
        for line in fil:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(",")
                if len(parts) == 6:
                    map_name = parts[0].strip()
                    x0 = float(parts[1].strip())
                    y0 = float(parts[2].strip())
                    z = float(parts[3].strip())
                    x_scale = float(parts[4].strip())
                    y_scale = float(parts[5].strip())
                    info = MapInfo(x0, y0, z, x_scale, y_scale)
                    map_to_info[map_name] = info
    return map_to_info


def parse_rooms(rooms_path):
    map_to_room_to_xy = {}
    with open(rooms_path) as fil:
        for line in fil:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(":")
                if len(parts) == 3:
                    map_name = parts[0].strip()
                    room_name = parts[1].strip()
                    coords = parts[2].strip()
                    coords_parts = coords.split(",")
                    if len(coords_parts) == 2:
                        x = int(coords_parts[0].strip())
                        y = int(coords_parts[1].strip())
                        if map_name not in map_to_room_to_xy:
                            map_to_room_to_xy[map_name] = {}
                        map_to_room_to_xy[map_name][room_name] = (x, y)
    return map_to_room_to_xy


def parse_treasures(treasures_path):
    room_to_treasures = defaultdict(set)
    with open(treasures_path) as fil:
        for line in fil:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(":")
                if len(parts) == 2:
                    room_name = parts[0].strip()
                    treasures_str = parts[1].strip()
                    if treasures_str:
                        treasures_list = treasures_str.split(",")
                        for treasure in treasures_list:
                            treasure = treasure.strip()
                            if treasure:
                                room_to_treasures[room_name].add(treasure)
    return room_to_treasures


def find_all_room_coords(map_to_prefix, map_to_tuple, map_to_room_to_xy):
    room_to_coords = {}
    for map_name, room_to_xy in map_to_room_to_xy.items():
        prefix = map_to_prefix[map_name]
        map_info = map_to_tuple[map_name]
        for room, xy in room_to_xy.items():
            global_room = f"{prefix}-{room}"
            pixel_x, pixel_y = xy
            x = map_info.x0 + pixel_x * map_info.x_scale
            y = map_info.y0 + pixel_y * map_info.y_scale
            z = map_info.z
            room_to_coords[global_room] = (x, y, z)
    return room_to_coords


def find_distance_and_direction(coords1, coords2):
    x1, y1, z1 = coords1
    x2, y2, z2 = coords2
    delta_x = x2 - x1  # positive means go east
    delta_y = y2 - y1  # positive means go south
    delta_z = z2 - z1  # positive means go up
    distance = (delta_x**2 + delta_y**2 + delta_z**2) ** 0.5
    return distance, delta_x, delta_y, delta_z


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--treasures",
        "-t",
        action="store",
        help="path to treasures file",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        action="store",
        help="path to map prefixes file",
    )
    parser.add_argument(
        "--xyz",
        "-x",
        action="store",
        help="path to map xyz file",
    )
    parser.add_argument(
        "--rooms",
        "-r",
        action="store",
        help="room xy coordinates",
    )
    parser.add_argument(
        "--find",
        "-f",
        action="store",
        help="thing to find",
    )
    parser.add_argument(
        "--start",
        "-s",
        action="store",
        help="room to search from",
    )
    parser.add_argument(
        "--number",
        "-n",
        action="store",
        default=10,
        help="number of results to return",
    )
    args = parser.parse_args()
    # TODO print errors on missing args
    print(args)

    map_to_prefix = parse_prefix(args.prefix)
    map_to_tuple = parse_xyz(args.xyz)
    map_to_room_to_xy = parse_rooms(args.rooms)
    room_to_xyz = find_all_room_coords(
        map_to_prefix, map_to_tuple, map_to_room_to_xy
    )
    pprint(room_to_xyz)
    room_to_treasures = parse_treasures(args.treasures)
    pprint(room_to_treasures)

    dds = []
    start_coords = room_to_xyz[args.start]
    print(f"{start_coords=}")
    for room, treasures in room_to_treasures.items():
        if args.find in treasures:
            dd = find_distance_and_direction(start_coords, room_to_xyz[room])
            dds.append((dd[0], dd[1], dd[2], dd[3], room))
    dds.sort()
    print("distance  x_dir  y_dir  z_dir room")
    for dd in dds[: args.number]:
        print(f"{dd[0]:8.0f} {dd[1]:6.0f} {dd[2]:6.0f} {dd[3]:6.0f} {dd[4]}")


if __name__ == "__main__":
    main()

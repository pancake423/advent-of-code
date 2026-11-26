const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const gpa = init.gpa;
    const io = init.io;

    std.debug.print("Part one:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partOne(gpa, io, "example.txt", 10)});
    std.debug.print("Actual input: {d}\n", .{try partOne(gpa, io, "input.txt", 1000)});

    std.debug.print("Part two:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partTwo(gpa, io, "example.txt")});
    std.debug.print("Actual input: {d}\n", .{try partTwo(gpa, io, "input.txt")});
}

fn parseJunctionBoxes(gpa: std.mem.Allocator, io: std.Io, filename: []const u8) ![]Point {
    const cwd = std.Io.Dir.cwd();
    const file = try cwd.openFile(io, filename, .{});
    defer file.close(io);
    var buffer: [1024]u8 = undefined;
    var fr = file.reader(io, &buffer);
    var reader = &fr.interface;

    var token_buffer: [64]u8 = @splat(0);
    var token_size: usize = 0;
    var write_to: u8 = 0;
    var point_builder: Point = .init(0, 0, 0);
    var points: std.ArrayList(Point) = try .initCapacity(gpa, 1024);
    defer points.deinit(gpa);
    while (reader.takeByte() catch |err| switch (err) {
        error.EndOfStream => null,
        else => return err,
    }) |byte| {
        if (byte == '\n' or byte == ',') {
            const int_val = try std.fmt.parseFloat(f64, token_buffer[0..token_size]);
            switch (write_to) {
                0 => point_builder.x = int_val,
                1 => point_builder.y = int_val,
                2 => {
                    point_builder.z = int_val;
                    try points.append(gpa, point_builder);
                },
                else => unreachable,
            }
            write_to = @mod(write_to + 1, 3);
            token_size = 0;
            continue;
        }

        if (token_size >= token_buffer.len) {
            return error.TokenTooLong;
        }
        token_buffer[token_size] = byte;
        token_size += 1;
    }

    return try points.toOwnedSlice(gpa);
}

fn getSortedDistances(gpa: std.mem.Allocator, junction_boxes: []Point) ![]DistanceInfo {
    const num_boxes = junction_boxes.len;

    var distances_list: std.ArrayList(DistanceInfo) = try .initCapacity(gpa, 1024);
    defer distances_list.deinit(gpa);

    for (0..num_boxes - 1) |i| {
        for (i + 1..num_boxes) |j| {
            try distances_list.append(gpa, .{
                .distance = junction_boxes[i].distance(junction_boxes[j]),
                .i = i,
                .j = j,
            });
        }
    }

    const distances = try distances_list.toOwnedSlice(gpa);
    std.mem.sort(DistanceInfo, distances, {}, distanceLessThan);
    return distances;
}

fn connectCircuits(circuit_lookups: *std.AutoHashMap(usize, usize), circuits: *std.AutoHashMap(usize, Circuit), d: DistanceInfo) !void {
    // find the two circuits for this connection
    const c1_idx = circuit_lookups.get(d.i).?;
    const c2_idx = circuit_lookups.get(d.j).?;

    // std.debug.print("{d} -> {d}, {d} -> {d}\n", .{ d.i, c1_idx, d.j, c2_idx });

    // do nothing if junction boxes are already in the same circuit
    if (c1_idx == c2_idx) {
        return;
    }

    // merge them into one

    // remove c2
    const removed_circuit = circuits.get(c2_idx).?;
    _ = circuits.remove(c2_idx);

    // update lookups for junction boxes in c2 to point to c1
    var it = removed_circuit.iterator(.{});
    while (it.next()) |i| {
        try circuit_lookups.put(i, c1_idx);
    }

    // set c1 to be the union of c1 and c2
    try circuits.put(c1_idx, circuits.get(c1_idx).?.unionWith(removed_circuit));
}

fn partOne(gpa: std.mem.Allocator, io: std.Io, filename: []const u8, connections_to_make: usize) !usize {
    const junction_boxes = try parseJunctionBoxes(gpa, io, filename);
    defer gpa.free(junction_boxes);

    // 2. compute the distance between every pair of junction boxes
    // and sort the pairs from closest to farthest away.

    const distances = try getSortedDistances(gpa, junction_boxes);
    defer gpa.free(distances);

    // for (distances) |d| {
    //     std.debug.print("{d} {d} {d}\n", .{ d.distance, d.i, d.j });
    // }

    // we now know the distances between every pair of junction boxes.
    // now, we need to use that information to build circuits.
    //
    // we need to maintain:
    // a list of circuits, where each circuit is a set of junction box
    // indexes.
    // for faster lookups, a hash table of junction box id -> circuit id

    var circuit_lookups: std.AutoHashMap(usize, usize) = .init(gpa);
    defer circuit_lookups.deinit();
    var circuits: std.AutoHashMap(usize, Circuit) = .init(gpa);
    defer circuits.deinit();

    for (0..junction_boxes.len) |i| {
        var circuit: Circuit = .empty;
        circuit.set(i);
        try circuits.put(i, circuit);
        try circuit_lookups.put(i, i);
    }

    for (distances[0..connections_to_make]) |d| {
        try connectCircuits(&circuit_lookups, &circuits, d);
    }

    // OK, now we've built our map of circuits, and we can finally solve the problem.
    // dump the circuits into an array containing the number of items in each circuit.

    var circuit_sizes: []usize = try gpa.alloc(usize, circuits.count());
    defer gpa.free(circuit_sizes);

    var it = circuits.valueIterator();
    var idx: usize = 0;
    while (it.next()) |value| {
        circuit_sizes[idx] = value.count();
        idx += 1;
    }

    std.mem.sort(usize, circuit_sizes, {}, comptime std.sort.desc(usize));

    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2];
}

fn partTwo(gpa: std.mem.Allocator, io: std.Io, filename: []const u8) !f64 {
    const junction_boxes = try parseJunctionBoxes(gpa, io, filename);
    defer gpa.free(junction_boxes);

    const distances = try getSortedDistances(gpa, junction_boxes);
    defer gpa.free(distances);

    var circuit_lookups: std.AutoHashMap(usize, usize) = .init(gpa);
    defer circuit_lookups.deinit();
    var circuits: std.AutoHashMap(usize, Circuit) = .init(gpa);
    defer circuits.deinit();

    for (0..junction_boxes.len) |i| {
        var circuit: Circuit = .empty;
        circuit.set(i);
        try circuits.put(i, circuit);
        try circuit_lookups.put(i, i);
    }

    for (distances) |d| {
        try connectCircuits(&circuit_lookups, &circuits, d);
        if (circuits.count() == 1) {
            // only one circuit remaining means we solved the problem.
            return junction_boxes[d.i].x * junction_boxes[d.j].x;
        }
    }

    unreachable;
}

fn distanceLessThan(_: void, a: DistanceInfo, b: DistanceInfo) bool {
    return a.distance < b.distance;
}

/// bit set storing the indices of junction boxes in each circuit.
///
/// the puzzle input has exactly 1000 lines, but I used 1024 because
/// its a nice power of two.
const Circuit = std.bit_set.Static(1024);

// stores the distance between and indices of two junction boxes
const DistanceInfo = struct {
    i: usize,
    j: usize,
    distance: f64,
};

const Point = struct {
    x: f64,
    y: f64,
    z: f64,

    pub fn init(x: f64, y: f64, z: f64) Point {
        return .{
            .x = x,
            .y = y,
            .z = z,
        };
    }

    pub fn distance(a: Point, b: Point) f64 {
        return @sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) + (a.z - b.z) * (a.z - b.z));
    }

    pub fn debugPrint(self: Point) void {
        std.debug.print("({d}, {d}, {d})\n", .{ self.x, self.y, self.z });
    }
};

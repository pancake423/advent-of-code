const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;

    const example = try readFileToOwnedSlice(io, gpa, "example.txt");
    const input = try readFileToOwnedSlice(io, gpa, "input.txt");

    defer gpa.free(example);
    defer gpa.free(input);

    std.debug.print("Part one:\n", .{});
    std.debug.print("Example input: {d}\n", .{try solvePart1(gpa, example)});
    std.debug.print("Actual input: {d}\n\n", .{try solvePart1(gpa, input)});

    std.debug.print("Part two:\n", .{});
    std.debug.print("Example input: {d}\n", .{try solvePart2(gpa, example)});
    std.debug.print("Actual input: {d}\n\n", .{try solvePart2(gpa, input)});
}

/// returns the contents of a file relative to cwd() as a slice
/// of bytes owned by the caller.
///
/// surely there's a standard library function for this, but I
/// wasn't able to find it.
pub fn readFileToOwnedSlice(io: std.Io, gpa: std.mem.Allocator, filename: []const u8) ![]u8 {
    var file_contents: std.ArrayList(u8) = try .initCapacity(gpa, 1024);

    const cwd = std.Io.Dir.cwd();
    const file = try cwd.openFile(io, filename, .{ .mode = .read_only });
    defer file.close(io);

    var buf: [1024]u8 = undefined;
    var done_reading = false;
    var offset: usize = 0;
    while (!done_reading) {
        const bytes_read = try file.readPositionalAll(io, &buf, offset);
        if (bytes_read < buf.len) {
            done_reading = true;
        }
        offset += bytes_read;
        try file_contents.appendSlice(gpa, buf[0..bytes_read]);
    }

    return file_contents.toOwnedSlice(gpa);
}

/// slices the given input into a list of \n separated lines.
///
/// memory is only allocated for the slices themselves,
/// the backing items are references to the original memory
/// of input.
///
/// in other words, make sure the input memory is at least as long
/// lived as the return value of this function.
pub fn listOfLines(gpa: std.mem.Allocator, input: []const u8) ![][]const u8 {
    var lines: std.ArrayList([]const u8) = try .initCapacity(gpa, 1024);
    var line_start: usize = 0;
    var line_end: usize = 0;
    for (input) |char| {
        if (char != '\n') {
            line_end += 1;
            continue;
        }
        try lines.append(gpa, input[line_start..line_end]);
        line_start = line_end + 1;
        line_end = line_start;
    }

    return lines.toOwnedSlice(gpa);
}

pub fn solvePart1(gpa: std.mem.Allocator, input: []u8) !usize {
    const lines = try listOfLines(gpa, input);
    defer gpa.free(lines);

    var dial_position: i32 = 50;
    var times_at_zero: usize = 0;

    for (lines) |line| {
        if (line.len < 2) {
            continue;
        }

        const sign: i32 = if (line[0] == 'L') -1 else 1;
        const value: i32 = sign * try std.fmt.parseInt(i32, line[1..], 10);
        dial_position = @mod(dial_position + value, 100);

        if (dial_position == 0) {
            times_at_zero += 1;
        }
    }

    return times_at_zero;
}

pub fn solvePart2(gpa: std.mem.Allocator, input: []const u8) !usize {
    const lines = try listOfLines(gpa, input);
    defer gpa.free(lines);

    var dial_position: i32 = 50;
    var times_at_zero: usize = 0;

    for (lines) |line| {
        if (line.len < 2) {
            continue;
        }

        const sign: i32 = if (line[0] == 'L') -1 else 1;
        const rotation_distance: i32 = try std.fmt.parseInt(i32, line[1..], 10);

        var distance_to_zero = if (sign == -1) dial_position else 100 - dial_position;
        if (distance_to_zero == 0) {
            distance_to_zero = 100;
        }

        const end_dial_position = @mod(dial_position + sign * rotation_distance, 100);

        // account for any "round trips" around the dial that very large turn numbers make
        times_at_zero += @divFloor(@max(0, rotation_distance - distance_to_zero), 100);

        // do we cross zero at least once during this rotation?
        // the first crossing is not accounted for by the @divFloor step.
        if (rotation_distance >= distance_to_zero) {
            times_at_zero += 1;
        }
        dial_position = end_dial_position;
    }

    return times_at_zero;
}

test "edgiest case" {
    try std.testing.expectEqual(2, try solvePart2(std.testing.allocator, "R50\nR100\n"));
}

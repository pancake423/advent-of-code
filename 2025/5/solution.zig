const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;

    var example: PuzzleInput = try .initFromFile(io, gpa, "example.txt");
    try example.ranges.mergeRanges(gpa);
    defer example.deinit(gpa);

    var input: PuzzleInput = try .initFromFile(io, gpa, "input.txt");
    try input.ranges.mergeRanges(gpa);
    defer input.deinit(gpa);

    std.debug.print("Part one:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partOne(example)});
    std.debug.print("Actual input: {d}\n\n", .{try partOne(input)});

    std.debug.print("Part two:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partTwo(example.ranges)});
    std.debug.print("Actual input: {d}\n\n", .{try partTwo(input.ranges)});
}

fn partOne(input: PuzzleInput) !usize {
    var count_fresh: usize = 0;
    for (input.ids.items) |id| {
        if (input.ranges.inAny(id)) {
            count_fresh += 1;
        }
    }

    return count_fresh;
}

/// note that this function expects the input ranges to have already been merged.
/// if that assumption is violated, the answer it gives will almost certainly be wrong.
fn partTwo(ranges: Ranges(usize)) !usize {
    var count_fresh: usize = 0;
    for (ranges.range_starts.items, ranges.range_ends.items) |start, end| {
        count_fresh += end - start + 1; // range is inclusive on both ends, so this is a classic fencepost problem
    }

    return count_fresh;
}

const PuzzleInput = struct {
    const Self = @This();

    ranges: Ranges(usize),
    ids: std.ArrayList(usize),

    pub fn initFromFile(io: std.Io, gpa: std.mem.Allocator, filename: []const u8) !Self {
        var self: Self = .{
            .ranges = try .init(gpa),
            .ids = try .initCapacity(gpa, 1024),
        };
        errdefer self.deinit(gpa);

        const cwd = std.Io.Dir.cwd();
        const file = try cwd.openFile(io, filename, .{});
        defer file.close(io);

        var buffer: [1024]u8 = undefined;
        var reader = file.reader(io, &buffer);

        // read id ranges from input file
        while (try reader.interface.peekByte() != '\n') {
            const range_start = try std.fmt.parseInt(usize, try reader.interface.takeDelimiterExclusive('-'), 10);
            _ = try reader.interface.takeByte();
            const range_end = try std.fmt.parseInt(usize, try reader.interface.takeDelimiterExclusive('\n'), 10);
            _ = try reader.interface.takeByte();

            try self.ranges.addRange(gpa, range_start, range_end);
        }

        // read individual ids from input file
        while (try reader.interface.takeDelimiter('\n')) |line| {
            if (line.len == 0) {
                continue;
            }
            const id = try std.fmt.parseInt(usize, line, 10);
            try self.ids.append(gpa, id);
        }

        return self;
    }

    pub fn deinit(self: *Self, gpa: std.mem.Allocator) void {
        self.ranges.deinit(gpa);
        self.ids.deinit(gpa);
    }
};

/// stores a list of ranges and determines if a given number is within any of its ranges.
/// you could probably store this information in a more efficient manner (some sort of
/// binary decision tree?), but this is good enough for part 1 :)
fn Ranges(T: type) type {
    return struct {
        const Self = @This();

        range_starts: std.ArrayList(T),
        range_ends: std.ArrayList(T),

        pub fn init(gpa: std.mem.Allocator) !Self {
            return .{
                .range_starts = try .initCapacity(gpa, 1024),
                .range_ends = try .initCapacity(gpa, 1024),
            };
        }

        pub fn deinit(self: *Self, gpa: std.mem.Allocator) void {
            self.range_starts.deinit(gpa);
            self.range_ends.deinit(gpa);
        }

        /// adds a new range to the Ranges list.
        /// asserts that range_start <= range_end.
        pub fn addRange(self: *Self, gpa: std.mem.Allocator, range_start: T, range_end: T) !void {
            std.debug.assert(range_start <= range_end);
            try self.range_starts.append(gpa, range_start);
            try self.range_ends.append(gpa, range_end);
        }

        pub fn removeRange(self: *Self, idx: usize) void {
            // swapRemove is OK here because the order of ranges is unimportant.
            // the only really important property is that the pairs remain aligned.
            // swapRemove just puts the last item in the now empty slot
            // and shortens the list by one.
            _ = self.range_starts.swapRemove(idx);
            _ = self.range_ends.swapRemove(idx);
        }

        pub fn mergeRanges(self: *Self, gpa: std.mem.Allocator) !void {
            while (try self.mergeOneIfNecessary(gpa)) {}
        }

        fn mergeOneIfNecessary(self: *Self, gpa: std.mem.Allocator) !bool {
            for (0..self.range_starts.items.len) |i| {
                for (0..self.range_starts.items.len) |j| {
                    if (i == j) {
                        continue;
                    }
                    if (self.pairsOverlap(i, j)) {
                        try self.merge(gpa, i, j);
                        return true;
                    }
                }
            }

            return false;
        }

        fn merge(self: *Self, gpa: std.mem.Allocator, i: usize, j: usize) !void {
            const range_start = @min(self.range_starts.items[i], self.range_starts.items[j]);
            const range_end = @max(self.range_ends.items[i], self.range_ends.items[j]);

            try self.addRange(gpa, range_start, range_end);

            // removing the higher index first is important, otherwise the index of the
            // second item would shift.
            self.removeRange(@max(i, j));
            self.removeRange(@min(i, j));
        }

        fn pairsOverlap(self: *const Self, i: usize, j: usize) bool {
            const i_start = self.range_starts.items[i];
            const i_end = self.range_ends.items[i];
            const j_start = self.range_starts.items[j];
            const j_end = self.range_ends.items[j];

            return inRange(i_start, j_start, j_end) or inRange(i_end, j_start, j_end) or inRange(j_start, i_start, i_end) or inRange(j_end, i_start, i_end);
        }

        fn inRange(value: T, min: T, max: T) bool {
            std.debug.assert(min <= max);
            return value >= min and value <= max;
        }

        pub fn inAny(self: *const Self, value: T) bool {
            for (self.range_starts.items, self.range_ends.items) |start, end| {
                if (value >= start and value <= end) {
                    return true;
                }
            }

            return false;
        }
    };
}

test "non-overlapping ranges not merged" {
    const gpa = std.testing.allocator;

    var ranges: Ranges(usize) = try .init(gpa);
    defer ranges.deinit(gpa);

    try ranges.addRange(gpa, 0, 1);
    try ranges.addRange(gpa, 2, 3);
    try ranges.mergeRanges(gpa);

    try std.testing.expectEqualSlices(usize, &[_]usize{ 0, 2 }, ranges.range_starts.items);
    try std.testing.expectEqualSlices(usize, &[_]usize{ 1, 3 }, ranges.range_ends.items);
    try std.testing.expectEqual(4, partTwo(ranges));
}

test "fully interior range merged" {
    const gpa = std.testing.allocator;

    var ranges: Ranges(usize) = try .init(gpa);
    defer ranges.deinit(gpa);

    try ranges.addRange(gpa, 1, 2);
    try ranges.addRange(gpa, 0, 4);
    try ranges.mergeRanges(gpa);

    try std.testing.expectEqualSlices(usize, &[_]usize{0}, ranges.range_starts.items);
    try std.testing.expectEqualSlices(usize, &[_]usize{4}, ranges.range_ends.items);
    try std.testing.expectEqual(5, partTwo(ranges));
}

test "multiple overlapping ranges merged" {
    const gpa = std.testing.allocator;

    var ranges: Ranges(usize) = try .init(gpa);
    defer ranges.deinit(gpa);

    try ranges.addRange(gpa, 5, 10);
    try ranges.addRange(gpa, 1, 6);
    try ranges.addRange(gpa, 7, 12);
    try ranges.mergeRanges(gpa);

    try std.testing.expectEqualSlices(usize, &[_]usize{1}, ranges.range_starts.items);
    try std.testing.expectEqualSlices(usize, &[_]usize{12}, ranges.range_ends.items);
    try std.testing.expectEqual(12, partTwo(ranges));
}

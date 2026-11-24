const std = @import("std");

const Grid = @This();

cells: std.ArrayList(u8),
width: usize,
height: usize,

/// creates a new empty grid.
pub fn init(gpa: std.mem.Allocator) !Grid {
    return .{
        .cells = try .initCapacity(gpa, 1024),
        .width = 0,
        .height = 0,
    };
}

pub fn deinit(self: *Grid, gpa: std.mem.Allocator) void {
    self.cells.deinit(gpa);
}

fn assertInBounds(self: *const Grid, x: usize, y: usize) void {
    std.debug.assert(x >= 0);
    std.debug.assert(y >= 0);
    std.debug.assert(x < self.width);
    std.debug.assert(y < self.height);
}

pub fn get(self: Grid, x: usize, y: usize) u8 {
    self.assertInBounds(x, y);
    return self.cells.items[x + y * self.width];
}

pub fn set(self: *Grid, x: usize, y: usize, value: u8) void {
    self.assertInBounds(x, y);
    self.cells.items[x + y * self.width] = value;
}

/// initializes a new grid from the given filename (relative to cwd)
pub fn initFromFile(io: std.Io, gpa: std.mem.Allocator, filename: []const u8) !Grid {
    const cwd = std.Io.Dir.cwd();

    const file = try cwd.openFile(io, filename, .{ .mode = .read_only });
    defer file.close(io);

    var buffer: [1024]u8 = undefined;
    var reader = file.reader(io, &buffer);

    var grid: Grid = try .init(gpa);

    read_loop: while (true) {
        const byte = reader.interface.takeByte() catch |err| switch (err) {
            error.EndOfStream => break :read_loop,
            else => return err,
        };

        if (byte == '\n') {
            grid.height += 1;
            if (grid.width == 0) {
                grid.width = grid.cells.items.len;
            }
        } else {
            try grid.cells.append(gpa, byte);
        }
    }
    std.debug.assert(grid.width * grid.height == grid.cells.items.len);

    return grid;
}

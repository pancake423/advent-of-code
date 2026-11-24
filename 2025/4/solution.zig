const std = @import("std");
const assert = std.debug.assert;
const lossyCast = std.math.lossyCast;

const Grid = @import("lib/Grid.zig");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;

    std.debug.print("Part one:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partOne(io, gpa, "example.txt")});
    std.debug.print("Actual input: {d}\n\n", .{try partOne(io, gpa, "input.txt")});

    std.debug.print("Part two:\n", .{});
    std.debug.print("Example input: {d}\n", .{try partTwo(io, gpa, "example.txt")});
    std.debug.print("Actual input: {d}\n\n", .{try partTwo(io, gpa, "input.txt")});
}

fn partOne(io: std.Io, gpa: std.mem.Allocator, filename: []const u8) !usize {
    var grid: Grid = try .initFromFile(io, gpa, filename);
    defer grid.deinit(gpa);

    return countAccessible(&grid, false);
}

fn partTwo(io: std.Io, gpa: std.mem.Allocator, filename: []const u8) !usize {
    var grid: Grid = try .initFromFile(io, gpa, filename);
    defer grid.deinit(gpa);

    var total_removed: usize = 0;
    while (true) {
        const removed = countAccessible(&grid, true);
        std.debug.print("{d}\n", .{removed});
        total_removed += removed;
        if (removed == 0) {
            break;
        }
    }

    return total_removed;
}

/// counts the number of 'accessible' cells in the current grid.
/// an accessible cell is defined as a cell whose value is '@', with less
/// than four neighbors out of the 8 surrounding cells also being an '@'.
///
/// if replace is true, this will mutate the grid, setting these accessible
/// cells to '.' as it passes over the grid.
///
/// usually, it is incorrect to mutate the grid as you count (results in an
/// incorrect count at each iteration), but in this case it is OK
/// (optimal, even) to remove as you iterate. The reason why this works will
/// be left as a thought exercise for the reader.
///
/// (I figured it out on accident)
fn countAccessible(grid: *Grid, replace: bool) usize {
    var count_accessible: usize = 0;

    for (0..grid.height) |y| {
        for (0..grid.width) |x| {
            if (grid.get(x, y) != '@') {
                // std.debug.print("{c}", .{grid.get(x, y)});
                continue;
            }

            const count = countSurroundingCells(grid.cells.items, grid.width, grid.height, x, y);
            if (count < 4) {
                count_accessible += 1;
                if (replace) {
                    grid.set(x, y, '.');
                }
                // std.debug.print("x", .{});
            } else {
                // std.debug.print("{d}", .{count});
            }
        }
        // std.debug.print("\n", .{});
    }

    return count_accessible;
}

fn countSurroundingCells(cells: []u8, width: i128, height: i128, x: i128, y: i128) usize {
    var count: usize = 0;

    const deltas: [3]i128 = .{ -1, 0, 1 };
    for (deltas) |dx| {
        for (deltas) |dy| {
            if (dx == 0 and dy == 0) {
                continue;
            }
            const fx = x + dx;
            const fy = y + dy;

            if (fx < 0 or fy < 0 or fx >= width or fy >= height) {
                continue;
            }

            // lossyCast is safe because we know fx and fy are both >=0
            if (cells[lossyCast(usize, fx + fy * width)] == '@') {
                count += 1;
            }
        }
    }

    return count;
}

const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;
    const cwd = std.Io.Dir.cwd();
    const file = try cwd.openFile(io, "input.txt", .{ .mode = .read_only });
    defer file.close(io);

    var buffer: [4096]u8 = undefined;
    var file_reader = file.reader(io, &buffer);
    const reader = &file_reader.interface;

    var col_list = try ColumnList.init(gpa);
    defer col_list.deinit(gpa);

    var col_idx: usize = 0;
    while (try readNextToken(reader)) |token_info| {
        const token = token_info.value;
        // ignore sequential spaces
        if (token.len == 0) {
            continue;
        }

        if (col_idx == col_list.columns.items.len) {
            try col_list.addColumn(gpa);
        }

        var col = col_list.columns.items[col_idx];
        if (std.mem.eql(u8, token, "+")) {
            col.op = .add;
        } else if (std.mem.eql(u8, token, "*")) {
            col.op = .mul;
        } else {
            try col.data.append(gpa, try std.fmt.parseInt(usize, token, 10));
        }

        col_idx += 1;
        if (token_info.delimiter == '\n') {
            col_idx = 0;
        }
    }

    var grand_total: usize = 0;
    for (col_list.columns.items) |col| {
        switch (col.op) {
            .add => {
                var col_total: usize = 0;
                for (col.data.items) |n| {
                    col_total += n;
                }
                grand_total += col_total;
            },
            .mul => {
                var col_total: usize = 1;
                for (col.data.items) |n| {
                    col_total *= n;
                }
                grand_total += col_total;
            },
            .none => return error.ColumnMissingOperation,
        }
    }

    std.debug.print("{d}\n", .{grand_total});
}

const TokenInfo = struct {
    value: []u8,
    delimiter: u8,
};

fn readNextToken(reader: *std.Io.Reader) !?TokenInfo {
    const read_space: ?[]u8 = reader.peekDelimiterExclusive(' ') catch |err| switch (err) {
        error.EndOfStream => null,
        else => return err,
    };
    const read_newline: ?[]u8 = reader.peekDelimiterExclusive('\n') catch |err| switch (err) {
        error.EndOfStream => null,
        else => return err,
    };

    if (read_space == null and read_newline == null) {
        return null;
    } else if (read_space == null) {
        return .{
            .value = (try reader.takeDelimiter('\n')).?,
            .delimiter = '\n',
        };
    } else if (read_newline == null) {
        return .{
            .value = (try reader.takeDelimiter(' ')).?,
            .delimiter = ' ',
        };
    }

    if (read_space.?.len > read_newline.?.len) {
        return .{
            .value = (try reader.takeDelimiter('\n')).?,
            .delimiter = '\n',
        };
    } else {
        return .{
            .value = (try reader.takeDelimiter(' ')).?,
            .delimiter = ' ',
        };
    }
}

const Operation = enum { add, mul, none };

const Column = struct {
    data: std.ArrayList(usize),
    op: Operation,

    pub fn init(gpa: std.mem.Allocator) !Column {
        return .{
            .data = try .initCapacity(gpa, 1024),
            .op = .none,
        };
    }

    pub fn deinit(self: *Column, gpa: std.mem.Allocator) void {
        self.data.deinit(gpa);
    }
};

const ColumnList = struct {
    columns: std.ArrayList(*Column),

    pub fn init(gpa: std.mem.Allocator) !ColumnList {
        return .{
            .columns = try .initCapacity(gpa, 64),
        };
    }

    pub fn addColumn(self: *ColumnList, gpa: std.mem.Allocator) !void {
        const col = try gpa.create(Column);
        col.* = try .init(gpa);
        try self.columns.append(gpa, col);
    }

    pub fn deinit(self: *ColumnList, gpa: std.mem.Allocator) void {
        for (self.columns.items) |col| {
            col.deinit(gpa);
            gpa.destroy(col);
        }
        self.columns.deinit(gpa);
    }
};

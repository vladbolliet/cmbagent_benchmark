#!/bin/bash

# set the root directory (you can also pass this as an argument)
ROOT_DIR="/mnt/p/stage/cmbagent_benchmark/data/clean/usaco_tests"  # or replace with the full path like /mnt/.../usaco_tests

# Walk through each subdirectory
for problem_dir in "$ROOT_DIR"/*; do
    # Make sure it's a directory
    [ -d "$problem_dir" ] || continue

    echo "📂 Processing: $problem_dir"

    # Go through .in files
    for infile in "$problem_dir"/*.in; do
        [ -f "$infile" ] || continue
        base=$(basename "$infile" .in)

        # Skip if already renamed
        if [[ "$base" =~ ^I\.[0-9]+$ ]]; then
            continue
        fi

        new_infile="$problem_dir/I.$base"
        mv "$infile" "$new_infile"
        echo "🔄 Renamed: $infile -> $new_infile"
    done

    # Go through .out files
    for outfile in "$problem_dir"/*.out; do
        [ -f "$outfile" ] || continue
        base=$(basename "$outfile" .out)

        # Skip if already renamed
        if [[ "$base" =~ ^O\.[0-9]+$ ]]; then
            continue
        fi

        new_outfile="$problem_dir/O.$base"
        mv "$outfile" "$new_outfile"
        echo "🔄 Renamed: $outfile -> $new_outfile"
    done
done

echo "✅ Done."

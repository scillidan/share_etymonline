#!/bin/bash
# Authors: GPT-4o mini🧙‍♂️, scillidan🤡

awk '
BEGIN { RS=""; FS="\n"; count=0 }
/^[0-9]+ definitions found/ {
  print $0 "\n"
  next
}
{
  # filter out header line "From ..." if any
  filtered_count=0
  delete filtered_lines

  for(i=1; i<=NF; i++) {
    line = $i
    if(line ~ /^From .* \[.*\]:/) continue
    filtered_lines[++filtered_count] = line
  }

  if(filtered_count > 0) {
    count++
    # Extract leading whitespace (spaces or tabs) of first line
    match(filtered_lines[1], /^[ \t]*/)
    leadws = substr(filtered_lines[1], RSTART, RLENGTH)
    # Remove leading whitespace from first line to avoid double indent after printing
    sub(/^[ \t]*/, "", filtered_lines[1])
    # Print number line with original indentation and one space after the dot
    printf "%s%d. %s\n", leadws, count, filtered_lines[1]
    # Print the rest lines as-is (include their original indentation)
    for(j=2; j<=filtered_count; j++) print filtered_lines[j]
    print ""
  }
}
'

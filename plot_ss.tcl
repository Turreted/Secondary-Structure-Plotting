set outfile [open ./ss_frac.dat w]
set frame_num [molinfo top get numframes]

# TCL file to dump the secondary structure of a trajectory

set full [atomselect top "protein and name CA"]
set len [llength [$full get resid]]
$full delete

for {set i 0} {$i < $frame_num} {incr i} {
    animate goto $i
    set sel [atomselect top "protein and name CA"]
    mol ssrecalc top
    puts $outfile [$sel get structure]
    $sel delete
}
close $outfile

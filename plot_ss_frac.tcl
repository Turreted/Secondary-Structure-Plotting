set alpha_lookup {H G I}
set beta_lookup  {B b E}
set turn_lookup  {T}

set outfile [open ./ss_frac.dat w]
set frame_num [molinfo top get numframes]

set full [atomselect top "protein and name CA"]
set len [llength [$full get resid]]
$full delete

puts $outfile "Alpha,Beta,Turn,Other"

for {set i 0} {$i < $frame_num} {incr i} {
    animate goto $i
    set sel [atomselect top "protein and name CA"]
    mol ssrecalc top
    set struc_string [$sel get structure]

    set alpha 0
    set beta 0
    set turn 0
    set other 0

    # iterate through every residue in the protein
    foreach letter $struc_string {
        if {$letter in $alpha_lookup} {
            incr alpha 1
        } elseif {$letter in $beta_lookup} {
            incr beta 1
        } elseif {$letter in $turn_lookup} {
            incr turn 1
        } else {
            incr other 1
        }
    }

    set percent_alpha [expr {double($alpha) / double($len)}]
    set percent_beta [expr {double($beta) / double($len)}]
    set percent_turn [expr {double($turn) / double($len)}]
    set percent_other [expr {double($other) / double($len)}]

    puts $outfile "$percent_helix,$percent_beta,$percent_turn,$percent_other"
    $sel delete
}
close $outfile


## CPAC post script for correcting the Orientations and headers

Lenient:
First, to apply to all files in func that have space-MNI in their filepath - NOT restricted to files that end in _bold (like last time)
run 3dresample to RPI first(this will grab the bold masks as well, this time)

Now restrict only to space-MNI and ends with _bold:
change pixdim4 to the TR value (0.8)
(this will also get the whole-head bold this time)

Now restrict to reg- in the filepath:
spike regression operations - grabbing the regressor, running that inverting function, and applying 3dTproject with the spike regressor
(iirc, we used -polort 2 in the lenient rerun this time so we don't need to do it here)

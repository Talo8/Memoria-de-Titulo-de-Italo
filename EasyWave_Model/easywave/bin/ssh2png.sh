#!/bin/bash

EWPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../tools" && pwd )"
FONT=$EWPATH/FreeMonoBold.ttf

VMAX=0.5


while test $# -gt 0; do
  case "$1" in
    -h|--help)
	echo ""
	echo "Usage: ssh2png.cmd <timelabel|all> [scaleMax]"
	echo "   where optional scale is given in meters, default scale- from -0.5 to 0.5 m"
	echo "e.g., ssh2png.cmd 01800 10"
	echo "   to present data from eWave.2D.01800.ssh using 10 meter scale"
	echo "      ssh2png.cmd all"
	echo "   use 'all' to create a mpg-movie over all available time frames"        
	exit 0
        ;;
    -grd)
        shift
        if test $# -gt 0; then
       	  f=$1  
        else
          echo "Error: no grid specified."
          exit 1
        fi
        shift
        ;;
    *)
	break
	;;
  esac
done

# Check command line parameters
if [ $# -eq 1 ]; then
  SSHFILE=eWave.2D.$1.ssh
else
  echo "Error: no ssh file specified."
  exit 1
fi

# Check number of grd-files in current directory
# We assume presence of a single grd -- bathymetry
ngrids=0
if test "$f" = ""; then
  for f in *.grd
  do
    let ngrids+=1
  done
  if [ $ngrids -gt 1 ]; then
    echo "More than one grid. Do not know which one to use!"
    exit 2
  fi
fi

# Execute converter
if [ "$1" == "all" ]; then
  echo "Batch processing to movie"
  echo "Enter frame rate [fps]: "
  read fps
  nmb=0
  for s in *.ssh
  do
    let nmb+=1
    OUTFILE=ssh$(printf "%.3d" "$nmb")
    echo "$s -> $OUTFILE.png"
    $EWPATH/ew2png -grdB $f -palB $EWPATH/topo.cpt -transparency 0.01 -grdW $s -palW $EWPATH/ssh.rel.cpt -log -minmax -$VMAX $VMAX -legend scale+time -font $FONT -output $OUTFILE
    convert $OUTFILE.png -depth 8 $OUTFILE.png
  done
  OUTFILE=ssh.mp4
  if [ -f $OUTFILE ]
  then
    rm $OUTFILE
  fi
  echo "NOW: Merging frames into a movie file $OUTFILE"
  avconv -qscale 5 -r $fps -i ssh%3d.png $OUTFILE
  echo "NOW: Removing png-frames"
  rm ssh*.png
else
  $EWPATH/ew2png -grdB $f -palB $EWPATH/topo.cpt -transparency 0.01 -grdW $SSHFILE -palW $EWPATH/ssh.rel.cpt -log -minmax -$VMAX $VMAX -legend range+scale+time -font $FONT
fi


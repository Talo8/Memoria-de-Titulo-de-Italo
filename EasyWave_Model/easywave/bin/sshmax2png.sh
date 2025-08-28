#!/bin/bash

EWPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../tools" && pwd )"
SSHFILE=eWave.2D.sshmax
FONT=$EWPATH/FreeMonoBold.ttf

# Check command line parameters
VMIN=0.1
VMAX=10.

while test $# -gt 0; do
  case "$1" in
    -h|--help)
	echo ""
  	echo "Usage: sshmax2png.sh [scaleMin scaleMax]"
  	echo "   where optional scale is given in meters, default scale- from 0.1 to 10 m"
  	echo "   avoid using 0 as ScaleMin because of logarithmic scale!"
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
    -ssh)
	shift
	if test $# -gt 0; then
          SSHFILE=$1
        else
          echo "Error: no ssh file specified."
          exit 1
        fi
  esac
done

# Check number of grd-files in current directory
# We assume presence of a single grd -- bathymetry
ngrids=0
if test "$f" = ""; then
  for f in *.grd
  do
    ngrids=$((ngrids+1))
  done
  if [ $ngrids -gt 1 ]; then
    echo "More than one grid. Do not know which one to use!"
    exit 2
  fi
fi

# Execute converter
$EWPATH/ew2png -grdB $f -palB $EWPATH/topo4sshmaxBW.cpt -transparency 0.001 -grdW $SSHFILE -palW $EWPATH/sshmax.rel.cpt -log -minmax $VMIN $VMAX -legend scale+range -font $FONT


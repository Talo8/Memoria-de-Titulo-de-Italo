#!/bin/bash

EWPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../tools" && pwd )"
SSHFILE=eWave.poi.summary
FONT=$EWPATH/FreeMonoBold.ttf

while test $# -gt 0; do
  case "$1" in
    -h|--help)
	echo ""
	echo "Usage: poi2png.cmd poi-filename"
	echo "   e.g., poi2png.cmd poiIndonesia.poi"
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
  POIFILE=$1
else
  echo "Error: no poi file specified."
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
$EWPATH/poi2png -grdB $f -palB $EWPATH/topo4sshmaxBW.cpt -poi $POIFILE -ssh $SSHFILE -levels 0.1 0.5 3.0 -font $FONT

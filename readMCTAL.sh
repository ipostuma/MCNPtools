#
# Bash script to divide MCTAL files
# in multiple subfile, one for each
# tally
#
# These tally files are written into
# columns, therefore more readable 
# numpy.loadtxt
#
for VAR in "$@"; do
  DIR=$(dirname "${VAR}")
  echo $VAR
  scripts/TallyRead.py $VAR
  echo $DIR/mOut/
done

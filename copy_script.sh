while read p; do
  cp $1"$p" .
  echo $1"$p" copied!
done <list.txt

stacknames=`aws elasticbeanstalk list-available-solution-stacks | jq -r ".SolutionStacks[]" |sed 's/$/, /g' | tr -d "\n" | sed 's/^/      [/' | rev | sed 's/^ *,/]/' | rev`
defaultstackame=`aws elasticbeanstalk list-available-solution-stacks | jq -r ".SolutionStacks[]" |grep "PHP" |head -1`
cat $1 |sed -e "s/REPLACE_ME_SOLUTIONSTACKNAME/$stacknames/"|sed -e "s/REPLACE_ME_DEFAULT_SOLUTIONSTACKNAME/$defaultstackame/"

export changed_files=$(git diff --name-only $(git branch --show-current) $(git merge-base $(git branch --show-current) master) | grep -E '\.py$' )
if [[ $* == *--show-files* ]]; then
  for file in $changed_files
  do
    echo $file
  done
fi
python -m isort $changed_files
if [ "$changed_files" == "" ]; then
  exit 0
else
  python -m flake8 $changed_files
fi

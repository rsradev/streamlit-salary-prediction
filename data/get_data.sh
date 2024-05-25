#!/bin/bash

# Declare an array
my_array=(
"https://cdn.stackoverflow.co/files/jo7n4k8s/production/49915bfd46d0902c3564fd9a06b509d08a20488c.zip/stack-overflow-developer-survey-2023.zip"
)

# Loop through the array elements
for element in "${my_array[@]}"; do
    # Perform actions with each element
    wget $element
done

find . -name "*.zip" -exec unzip {} \;

rm *.zip
rm so_*.pdf
rm README_2023.txt
rm survey_results_schema.csv
exit 0

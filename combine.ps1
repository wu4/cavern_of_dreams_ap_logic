# yq.exe ea '{(filename): $item} | . as $item ireduce ({}; . * $item)' ./levels/*.yaml
yq ea '{(filename | match(\"levels\\(.+).yaml$\").captures[0].string): .} as $item ireduce ({}; . * $item)' (Get-ChildItem levels/*.yaml | ForEach-Object{$_.fullname}) -I=0 -o=json > levels.json
# yq.exe ea 'filename | match("^\./levels/(.+)\.yaml$").captures[0].string' ./levels/*.yaml
# (filename | match("^\./levels/(.+)\.yaml$").captures[0].string)
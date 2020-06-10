pandoc.exe "$PSScriptRoot/main.md" `
 -o test.pdf `
 --filter pandoc-mermaid `
 --filter pandoc-fignos `
 --filter pandoc-secnos `
 --template="D:\Github\Nibbler\designDocs\template.tex"
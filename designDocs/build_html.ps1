pandoc.exe "$PSScriptRoot/main.md" `
    -o test.html `
    --filter pandoc-fignos `
    --filter pandoc-secnos
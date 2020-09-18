$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"


$middle   = 0.12326
$quantity = 8000
$pair     = "ADAUSDT"

# $range      = 0.004
# $upper_band = $middle * (1+$range/1.5)
# $lower_band = $middle * (1-$range)
$upper_band = $middle * (1+$range/1.5)
$lower_band = $middle * (1-$range)
$balance    = $quantity*$middle

Write-Output $balance
Write-Output $upper_band
Write-Output $lower_band

python $command_path `
    --pair=$pair `
    --bounds="$upper_band $lower_band" `
    --balances="$balance" `
    --n_levels=8 `
    --noise="True" `
    --futures="True" `
    --close_orders="True" `
    --distribution="linear"
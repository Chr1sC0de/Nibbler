$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"

$upper_band = 11.6172
$lower_band =

python $command_path `
    --pair=BANDUSDT `
    --bounds="$upper_band $lower_band" `
    --balances="250 500 1000 2000" `
    --n_levels=9 `
    --futures="True"
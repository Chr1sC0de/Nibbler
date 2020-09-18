$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"

$upper_band = 13.91
$lower_band = 1

python $command_path `
    --pair=LINKUSDT `
    --bounds="$upper_band $lower_band" `
    --balances="200 400 800 1600 1600 3200" `
    --n_levels=30 `
    --futures="True" `
    --close_orders="True"
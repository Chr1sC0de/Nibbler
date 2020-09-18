$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"
$upper_band = 2.9653
$lower_band = $upper_band * 0.95
python $command_path `
    --pair=DOTUSDT `
    --bounds="$upper_band $lower_band" `
    --balances="200 250 300" `
    --n_levels=15
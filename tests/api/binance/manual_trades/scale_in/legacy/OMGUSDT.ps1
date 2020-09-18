$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"
$upper_band = 7.6817
$lower_band = $upper_band * 0.925
python $command_path `
    --pair=OMGUSDT `
    --bounds="$upper_band $lower_band" `
    --balances="100 200 300" `
    --n_levels=20 `
    --futures="True"


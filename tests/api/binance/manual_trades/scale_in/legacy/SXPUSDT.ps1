
$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"

$upper_bound=
$lower_bound

python $command_path `
    --pair=SXPUSDT `
    --bounds="2.4324 1" `
    --balances="100 300 600 1200" `
    --n_levels=9 `
    --futures="True"
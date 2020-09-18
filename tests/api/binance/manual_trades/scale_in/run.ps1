$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"


python $command_path `
    --pair=SXPUSDT `
    --bounds="1.20 0.5" `
    --balances="100 200 300 400" `
    --n_levels=5 `
    --noise="True" `
    --futures="False" `
    --close_orders="True" `
    --distribution="linear"
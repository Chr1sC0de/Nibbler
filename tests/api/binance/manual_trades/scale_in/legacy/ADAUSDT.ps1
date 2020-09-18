$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"

python $command_path `
    --pair=ADAUSDT `
    --bounds="0.12100 0.06957" `
    --balances="110 200 300 1000 2000 4000" `
    --n_levels=10
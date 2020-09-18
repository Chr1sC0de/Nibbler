$command_path="D:\Github\Nibbler\tests\api\binance\manual_trades\scale_in\scale.py"
python $command_path `
    --pair=MATICUSDT `
    --bounds="0.02222 0.01763" `
    --balances="55 55 100 175 225 400" `
    --n_levels=5

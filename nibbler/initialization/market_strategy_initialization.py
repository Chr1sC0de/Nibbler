import numpy as np

def MarketStrategyInitialization(
        BuySignal, SellSignal, Strategy,
        buy_kwargs, sell_kwargs, strategy_kwargs,
        n_population=8
):

    population = []

    for _ in np.arange(n_population):
        while True:
            try:
                population.append(
                    Strategy(
                        BuySignal.random_initialization(**buy_kwargs),
                        SellSignal.random_initialization(**sell_kwargs),
                        **strategy_kwargs
                    )
                )
                break
            except:
                pass

    return population
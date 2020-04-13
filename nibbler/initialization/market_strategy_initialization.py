import numpy as np
import time
def MarketStrategyInitialization(
        BuySignal, SellSignal, Strategy,
        buy_kwargs, sell_kwargs, strategy_kwargs,
        stop_calculator=None,
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
                time.sleep(0.0001)
                break

            except:
                pass

    return population
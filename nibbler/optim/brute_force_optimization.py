import numpy as np
import multiprocessing as mp
from tqdm import tqdm
from ..utils import splitList
from ..trading.signals.buy import SavitzkyGolayMinFilteredGrads
from ..trading.signals.sell import SavitzkyGolayMaxFilteredGrads
from ..trading.strategy.market import MarketLong

class BruteForceSingleDataset:

    def __init__(
            self, strategy_population):
        self.population = strategy_population

    def calculate_fitness(self, data, n_processors=8):
        if n_processors == 1:
            self.run_strategy(self.population, data)
        if n_processors > 1:
            q = mp.Manager().Queue()
            split_population = splitList(self.population, n_processors)
            processes = [
                mp.Process(target=self.run_mp, args=(strategies, data, q))
                for strategies in split_population
            ]
            [process.start() for process in processes]
            [process.join() for process in processes]
            managed_list = []
            while q.qsize() > 0:
                managed_list.extend(q.get())
            self.population = managed_list
            self.population.sort(key=lambda x: x.account_balance)

    @staticmethod
    def run_strategy(population, data):
        for strategy in tqdm(population):
            strategy.walk_dataset(data)
        return population

    @staticmethod
    def run_mp(subset_pop, data, shared):
        output = BruteForceSingleDataset.run_strategy(subset_pop, data)
        shared.put(output)


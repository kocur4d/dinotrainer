from pathos.multiprocessing import ProcessingPool as Pool

import agent

NUMBER_OF_AGENTS = 2
GENERATIONS = 1

class Simulation:
    def __init__(self, number_of_agents, number_of_generations):
        self.n_agents = number_of_agents
        self.n_gen = number_of_generations
        self.winners = []

    def setup(self):
        print('Generating initial population... ', 'agents: ', self.n_agents)
        self.population = [Agent(n, debug=True) for n in range(self.n_agents)]

    def run(self):
        current_gen = 1
        results = []
        print('Starting generation: ', current_gen, ' ...')
        while current_gen <= self.n_gen:
          pool = Pool(processes = self.n_agents)
          results = pool.map(lambda agent: agents.start(), self.population)

        self.winners = self.winners.append(max(results, key=lambda agent: agent.score()))


if __name__ == "__main__":
  print('START')
  sim = Simulation(NUMBER_OF_AGENTS, GENERATIONS)
  sim.setup()
  print('results', results)
  print('FINISH')

from pathos.multiprocessing import ProcessingPool as Pool

from agent import Agent

NUMBER_OF_AGENTS = 1
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
        print('Starting generation: ', current_gen, ' ...')
        print('Population: ', self.population, '...')
        while current_gen <= self.n_gen:
          pool = Pool(processes = self.n_agents)
          results = pool.map(lambda agent: agent.start(), self.population)
          print('Generation: ', current_gen, ' finished.')
          self.winners.append(max(results, key=lambda agent: agent['score']))
          current_gen = current_gen + 1



if __name__ == "__main__":
  print('START')
  sim = Simulation(NUMBER_OF_AGENTS, GENERATIONS)
  sim.setup()
  sim.run()
  print('winners', sim.winners)
  print('FINISH')

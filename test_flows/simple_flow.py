from time import sleep
from metaflow import FlowSpec, step

STABLE_SEED=73

# Set to false to get pseudo-random runtime behavior
DETERMINISTIC=False

# Set to true to process 25% of the entire creatures list
SHORT_CREATURES = True

CREATURES = [
            "bird",
            "bat",
            "cat",
            "dog",
            "giraffe",
            "porcupine",
            "whale",
            "sloth",
            "shark",
            "bear",
            "narwhal",
            "beaver",
            "hamster",
            "gerbil",
            "guppy",
            "eagle",
            "peacock",
            "wombat",
            "lynx",
            "ocelot",
            "dingo"
        ]

class SimpleFlow(FlowSpec):
    @step
    def start(self):
        import random
        import time
        self.run_osquery()
        if DETERMINISTIC:
            random.seed(STABLE_SEED)
        else:
            random.seed(time.time_ns())
        if SHORT_CREATURES:
            self.creatures = []
            target_size = int(len(CREATURES) / 4)
            while len(self.creatures) < target_size:
                c = random.choice(CREATURES)
                if c not in self.creatures:
                    self.creatures.append(c)
        else:
            self.creatures = CREATURES
        random.shuffle(self.creatures)
        self.spin_creatures = []
        self.scoring_divisor = random.randint(25, 100)
        self.compute_factorial(3, 500)
        self.next(self.load_dataset)

    @step
    def load_dataset(self):
        self.run_osquery()
        import random
        max_spin = int(len(self.creatures) / 2)
        if len(self.creatures) > 10:
            max_spin = int(len(self.creatures) / 4)
        spin_count = random.randint(2, max_spin)
        i = 0
        while i < spin_count:
            c = random.choice(self.creatures)
            if c not in self.spin_creatures:
                self.spin_creatures.append(c)
                i += 1
        self.compute_factorial(2, 500)
        self.next(self.optimize, foreach="creatures")

    @step
    def optimize(self):
        self.run_osquery()
        import random
        self.creature = self.input
        if self.input in self.spin_creatures:
            print(f"({self.input}) Spinning CPU")
            self.compute_factorial(random.randint(15, 100), random.randint(10, 90) + 990)
        else:
            self.compute_factorial(3, 500)
        if random.randint(1, 100) > 50:
            for i in range(0, 10000000):
                pass            
        self.score = random.randint(1, 24) / self.scoring_divisor
        self.next(self.join)

    @step
    def join(self, inputs):
        self.run_osquery()
        self.best = max(inputs, key=lambda x: x.score).creature
        self.compute_factorial(2, 500)
        self.next(self.end)

    @step
    def end(self):
        self.run_osquery()
        self.compute_factorial(3, 500)
        print(f"{self.best} won!")

    def compute_factorial(self, times, n):
        import random
        import time
        little_sleeps = [0.25, 0.5, 0.75, 0.8, 1.0, 1.5, 2.5, 4.0]
        big_sleeps = [1, 2, 5, 7]
        while times > 0:
            v = 0
            x = n
            while x > 0:
                if x % 100 == 0:
                    time.sleep(random.choice(little_sleeps))
                v += x
                x -= 1
            times -= 1
            if times > 1:
                time.sleep(random.choice(big_sleeps))

if __name__ == "__main__":
    SimpleFlow()
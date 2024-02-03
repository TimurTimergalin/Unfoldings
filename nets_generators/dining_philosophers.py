from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to as arc


def generate_dining_philosophers(n):
    net = PetriNet(f"Dining philosophers {n}")
    marking = Marking()

    chopsticks = [PetriNet.Place(f"chopstick{x}") for x in range(1, n + 1)]
    net.places.update(chopsticks)
    marking.update(chopsticks)

    for i in range(1, n + 1):
        chopstick1 = chopsticks[i - 1]
        chopstick2 = chopsticks[i % n]

        thinking = PetriNet.Place(f"thinking{i}")
        prepare_left = PetriNet.Place(f"prepare left{i}")
        prepare_right = PetriNet.Place(f"prepare right{i}")
        ready_left = PetriNet.Place(f"ready left{i}")
        ready_right = PetriNet.Place(f"ready right{i}")
        dining = PetriNet.Place(f"dining{i}")

        net.places.update((thinking, prepare_left, prepare_right, prepare_right, ready_left, ready_right, dining))
        marking[thinking] += 1

        prepare = PetriNet.Transition(name := f"prepare{i}", label=name)
        take_left = PetriNet.Transition(name := f"take left{i}", label=name)
        take_right = PetriNet.Transition(name := f"take right{i}", label=name)
        eat = PetriNet.Transition(name := f"eat{i}", label=name)
        think = PetriNet.Transition(name := f"think{i}", label=name)

        net.transitions.update((prepare, take_left, take_right, eat, think))

        arc(thinking, prepare, net)
        arc(prepare, prepare_left, net)
        arc(prepare, prepare_right, net)

        arc(prepare_left, take_left, net)
        arc(chopstick1, take_left, net)
        arc(take_left, ready_left, net)

        arc(prepare_right, take_right, net)
        arc(chopstick2, take_right, net)
        arc(take_right, ready_right, net)

        arc(ready_left, eat, net)
        arc(ready_right, eat, net)
        arc(eat, dining, net)

        arc(dining, think, net)
        arc(think, chopstick1, net)
        arc(think, chopstick2, net)
        arc(think, thinking, net)

    return net, marking

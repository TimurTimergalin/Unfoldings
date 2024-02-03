from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to as arc


def generate_mutual_exclusion(n):
    net = PetriNet(f"Mutual exclusion {n}")
    marking = Marking()

    mutex = PetriNet.Place("mutex")
    net.places.add(mutex)
    marking.update((mutex,))

    for i in range(1, n + 1):
        critical = PetriNet.Place(f"critical{i}")
        isolated = PetriNet.Place(f"isolated{i}")
        waiting = PetriNet.Place(f"waiting{i}")

        net.places.update((critical, isolated, waiting))
        marking.update((isolated,))

        capture = PetriNet.Transition(name := f"capture{i}", label=name)
        release = PetriNet.Transition(name := f"release{i}", label=name)
        await_ = PetriNet.Transition(name := f"await{i}", label=name)

        net.transitions.update((capture, release, await_))

        arc(mutex, capture, net)
        arc(waiting, capture, net)
        arc(capture, critical, net)

        arc(critical, release, net)
        arc(release, mutex, net)
        arc(release, isolated, net)

        arc(isolated, await_, net)
        arc(await_, waiting, net)

    return net, marking

from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to, add_place, add_transition


def generate_slotted_ring(n):
    net = PetriNet(f"Milner's scheduler {n}")

    def place(x):
        return add_place(net, x)

    def trans(x):
        return add_transition(net, x, x)

    def arc(f, t):
        return add_arc_from_to(f, t, net)

    marking = Marking()

    p1s = [place(f"p1_{x}") for x in range(1, n + 1)]
    p2s = [place(f"p2_{x}") for x in range(1, n + 1)]
    p10s = [place(f"p10_{x}") for x in range(1, n + 1)]

    marking.update(p10s)

    for i in range(1, n + 1):
        p1 = p1s[i - 1]
        p2 = p2s[i - 1]
        p10 = p10s[i - 1]

        np1 = p1s[i % n]
        np2 = p2s[i % n]
        pp10 = p10s[(i - 2) % n]

        p3, p4, p5, p6, p7, p8, p9 = (place(f"p{x}_{i}") for x in range(3, 10))
        marking[p7] += 1

        owner = trans(f"owner{i}")
        other = trans(f"other{i}")
        go_on = trans(f"go on{i}")
        write = trans(f"write{i}")
        give_free_slot = trans(f"gfs{i}")
        put_message_in_slot = trans(f"put{i}")
        int_ack = trans(f"int ack{i}")
        free = trans(f"free{i}")
        used = trans(f"used{i}")
        ack = trans(f"ack{i}")

        arc(p1, owner)
        arc(p1, other)

        arc(owner, p2)
        arc(p2, go_on)
        arc(p2, write)

        arc(go_on, p3)
        arc(p3, give_free_slot)

        arc(give_free_slot, p4)
        arc(put_message_in_slot, p4)
        arc(p4, ack)

        arc(other, p5)
        arc(write, p5)
        arc(p5, put_message_in_slot)

        arc(int_ack, p6)
        arc(p6, give_free_slot)
        arc(p6, put_message_in_slot)

        arc(give_free_slot, p7)
        arc(p7, free)

        arc(put_message_in_slot, p8)
        arc(p8, used)

        arc(free, p9)
        arc(used, p9)
        arc(p9, int_ack)

        arc(p10, free)
        arc(p10, used)

        arc(ack, pp10)
        arc(used, np1)
        arc(free, np2)

    return net, marking

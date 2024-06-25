import pm4py
from unfoldings.unfolding_algorithms import standard_algorithm
from unfoldings.decorations import *
from unfoldings.cutoff_settings import MarkCutoffSettings
from unfoldings.order_settings import BasicOrderSettings
from nets_generators import generate_dining_philosophers

net, m0 = generate_dining_philosophers(3)
decorations = ColorsDecorations(
    LabelsDecorations.standard(),
    starting_conditions="#aaffaa",
    cutoff_events="#ffaaaa"
)

events = []

pr = standard_algorithm(net, m0, BasicOrderSettings(), MarkCutoffSettings(), decorations, order_of_adding=events)
pm4py.view_petri_net(pr, decorations=decorations.get())

print(events)

rg = pm4py.objects.petri_net.utils.reachability_graph.construct_reachability_graph(net, m0)
print(f"Reachability graph: {len(rg.states)} states, {len(rg.transitions)} transitions")
print(f"Unfolding prefix: {len(pr.places)} conditions, {len(pr.transitions)} events, "
      f"{len(pr.cutoff_events)} cutoff events")


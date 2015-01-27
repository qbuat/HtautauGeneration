import ROOT

from rootpy.tree.filtering import EventFilter, EventFilterList
from rootpy.tree import Tree, TreeChain, TreeModel, TreeBuffer
from rootpy.extern.argparse import ArgumentParser
from rootpy.io import root_open
from rootpy import stl

from flat.models import *
from flat.filters import *
from flat.objects import define_objects
import flat.branches as branches

output = root_open('toto.root', 'recreate')
output.cd()
model = get_model()
outtree = Tree(name='Tree', model=model)
outtree.define_object(name='tau1', prefix='tau1_')
outtree.define_object(name='tau2', prefix='tau2_')
outtree.define_object(name='higgs', prefix='higgs_')
outtree.define_object(name='met', prefix='met_')

log.info(model)
def mc_weight_count(event):
    return event.mc_event_weight
count_funcs = {
    'mc_weight': mc_weight_count,
}
event_filters = EventFilterList([
        Higgs(
            count_funcs=count_funcs,
            tree=outtree),
        TrueTaus(
            count_funcs=count_funcs,
            tree=outtree),
        ClassifyDecay(
            count_funcs=count_funcs,
            tree=outtree),
        TrueJets(count_funcs=count_funcs),
        ])

files = ['prod_filter20/MC12.300004.PowhegPythia8_AU2CT10_ggH80_tautau_run1234/ntup.EVNT_300004_seed1234.root']

# peek at first tree to determine which branches to exclude
with root_open(files[0]) as test_file:
    test_tree = test_file.Get('truth')
    ignore_branches = test_tree.glob(branches.REMOVE)

chain = TreeChain(
    'truth', 
    files=files, 
    filters=event_filters,
    cache=True,
    cache_size=50000000,
    learn_entries=100,
    ignore_branches=ignore_branches)

define_objects(chain)


for event in chain:

    outtree.runnumber = event.RunNumber
    outtree.evtnumber = event.EventNumber
    outtree.weight = event.mc_event_weight
    # sort taus and jets in decreasing order by pT
    event.taus.sort(key=lambda tau: tau.pt, reverse=True)
    event.jets.sort(key=lambda jet: jet.pt, reverse=True)

    tau1, tau2 = event.taus
    TrueTauBlock.set(outtree, tau1, tau2)
    FourMomentum.set(outtree.higgs, outtree.higgs.fourvect)
    outtree.Fill(reset=-1)
    

output.cd()
outtree.FlushBaskets()
outtree.Write()

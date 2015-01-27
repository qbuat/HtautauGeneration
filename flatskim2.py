import ROOT

from rootpy.tree.filtering import EventFilter, EventFilterList
from rootpy.tree import Tree, TreeChain, TreeModel, TreeBuffer
from rootpy.extern.argparse import ArgumentParser
from rootpy.io import root_open
from rootpy import stl

from flat.models import *
from flat.filters import *
from flat.objects import define_objects


output = root_open('toto.root', 'recreate')
output.cd()
model = get_model()
outtree = Tree(name='Tree', model=model)
outtree.define_object(name='tau1', prefix='tau1_')
outtree.define_object(name='tau2', prefix='tau2_')

event_filters = EventFilterList([
        TrueTaus(),
        TrueJets(),
        Higgs(tree=outtree),
        ])

files = ['prod_filter20/MC12.300004.PowhegPythia8_AU2CT10_ggH80_tautau_run1234/ntup.EVNT_300004_seed1234.root']
chain = TreeChain('truth', files=files, filters=event_filters)
define_objects(chain)


for event in chain:

    # sort taus and jets in decreasing order by pT
    event.taus.sort(key=lambda tau: tau.pt, reverse=True)
    event.jets.sort(key=lambda jet: jet.pt, reverse=True)

    tau1, tau2 = event.taus
    TrueTauBlock.set(outtree, tau1, tau2)
    outtree.Fill(reset=-1)


output.cd()
outtree.FlushBaskets()
outtree.Write()

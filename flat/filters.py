import ROOT

from rootpy.tree.filtering import *
from rootpy.extern.hep import pdg

from math import *
from .units import GeV
from . import utils
from . import log; log = log[__name__]


class TrueTaus(EventFilter):

    def __init__(self, **kwargs):
        super(TrueTaus, self).__init__(**kwargs)

    def passes(self, event):
        event.taus.select(
            lambda tau: tau.status == 2 and event.mc[tau.parent_index].pdgId == 25)
        return len(event.taus) == 2

class TrueJets(EventFilter):

    def __init__(self, **kwargs):
        super(TrueJets, self).__init__(**kwargs)
        
    def passes(self, event):
        # The number of anti kt R = 0.4 truth jets with pT>25 GeV, not
        # originating from the decay products of the Higgs boson.
        # Start from the AntiKt4Truth collection. Reject any jet with pT<25
        # GeV. Reject any jet withing dR < 0.4 of any electron, tau, photon or
        # parton (directly) produced in the Higgs decay.
        event.jets.select(lambda jet: jet.pt >= 25 * GeV and \
                              not any([tau for tau in event.taus if
                                       utils.dR(jet.eta, jet.phi,
                                                tau.eta, tau.phi) < 0.4]))


class Higgs(EventFilter):

    def __init__(self, tree, **kwargs):
        super(HiggsPT, self).__init__(**kwargs)
        self.tree = tree
        self.status = (62, 195)
        
    def passes(self, event):
        pt = 0
        higgs = None
        status = self.status
        # find the Higgs
        for mc in event.mc:
            if mc.pdgId == 25 and mc.status in status:
                pt = mc.pt
                higgs = mc
                break
        if higgs is None:
            raise RuntimeError("Higgs not found!")

        event.higgs = higgs
        return True

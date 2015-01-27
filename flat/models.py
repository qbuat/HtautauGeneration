"""
TreeModels common to both lephad and hadhad analyses
"""
from ROOT import TLorentzVector

from rootpy.tree import TreeModel, FloatCol, IntCol, BoolCol, CharCol
from rootpy.vector import LorentzRotation, LorentzVector, Vector3, Vector2
from rootpy import log
ignore_warning = log['/ROOT.TVector3.PseudoRapidity'].ignore(
    '.*transvers momentum.*')


class EventModel(TreeModel):
    runnumber = IntCol()
    evtnumber = IntCol()
    hadhad = IntCol() # 1 or 0
    lephad = IntCol() # 1 or 0
    leplep = IntCol() # 1 or 0
    channel = IntCol() # 1 (hh), 2 (lh), 3(hh)

class FourMomentum(TreeModel):
    pt = FloatCol()
    p = FloatCol()
    et = FloatCol()
    e = FloatCol()
    eta = FloatCol(default=-1111)
    phi = FloatCol(default=-1111)
    m = FloatCol()

    @classmethod
    def set(cls, this, other):
        if isinstance(other, TLorentzVector):
            vect = other
        else:
            vect = other.fourvect
        this.pt = vect.Pt()
        this.p = vect.P()
        this.et = vect.Et()
        this.e = vect.E()
        this.m = vect.M()
        with ignore_warning:
            this.phi = vect.Phi()
            this.eta = vect.Eta()

class TrueMet(FourMomentum):
    @classmethod
    def set(cls, this, tau1, tau2):
        met1 = tau1.fourvect - tau1.fourvect_vis
        met2 = tau2.fourvect - tau2.fourvect_vis
        FourMomentum.set(this, met1 + met2)

class TrueTau(FourMomentum + FourMomentum.prefix('vis_')):
    nProng = IntCol(default=-1111)
    nPi0 = IntCol(default=-1111)
    charge = IntCol()
    flavor = CharCol()
    pdgId = IntCol(default=-1111)
    @classmethod
    def set_vis(cls, this, other):
        if isinstance(other, TLorentzVector):
            vect = other
        else:
            vect = other.fourvect
        this.vis_pt = vect.Pt()
        this.vis_p = vect.P()
        this.vis_et = vect.Et()
        this.vis_e = vect.E()
        this.vis_m = vect.M()
        with ignore_warning:
            this.vis_phi = vect.Phi()
            this.vis_eta = vect.Eta()

class TrueTauBlock(TrueTau.prefix('tau1_') + TrueTau.prefix('tau2_') + TrueMet.prefix('met_')):
    
    dR_taus = FloatCol()
    dEta_taus = FloatCol()
    dPhi_taus = FloatCol()
    
    dPhi_taus_met = FloatCol()
    dPhi_tau1_met = FloatCol()
    dPhi_tau2_met = FloatCol()

    pt_sum_taus_met = FloatCol()
    pt_tot_taus_met = FloatCol()

    pt_sum_tau1_tau2 = FloatCol() # TO BE SET
    pt_tot_tau1_tau2 = FloatCol() # TO BE SET
    pt_ratio_tau1_tau2 = FloatCol()

    transverse_mass_tau1_tau2 = FloatCol() # TO BE SET
    transverse_mass_tau1_met = FloatCol() # TO BE SET
    transverse_mass_tau2_met = FloatCol() # TO BE SET

    @classmethod 
    def set(cls, tree, tau1, tau2):
        tree_object = tree.tau1
        TrueTau.set(tree_object, tau1.fourvect)
        TrueTau.set_vis(tree_object, tau1.fourvect_vis)
        tree_oject = tree.tau2
        TrueTau.set(tree_object, tau2.fourvect)
        TrueTau.set_vis(tree_object, tau2.fourvect_vis)
        tree_object = tree.met
        TrueMet.set(tree_object, tau1, tau2)

        vis_tau1 = tau1.fourvect_vis
        vis_tau2 = tau1.fourvect_vis
        tree.dR_taus = vis_tau1.DeltaR(vis_tau2)
        tree.dEta_taus = abs(vis_tau1.Eta() - vis_tau2.Eta())
        tree.dPhi_taus = abs(vis_tau1.DeltaPhi(vis_tau2))
        if vis_tau2.Pt() != 0:
            tree.pt_ratio_tau1_tau2 = vis_tau1.Pt() / vis_tau2.Pt()
        else:
            tree.pt_ratio_tau1_tau2 = 0


def get_model():
    model = EventModel + TrueTauBlock + FourMomentum.prefix('higgs')
    return model

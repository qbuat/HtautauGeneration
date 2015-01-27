from ROOT import TLorentzVector

from rootpy.tree import TreeModel, FloatCol, IntCol, BoolCol, CharCol
from rootpy.vector import LorentzRotation, LorentzVector, Vector3, Vector2
from rootpy.extern.hep import pdg
from rootpy import log
ignore_warning = log['/ROOT.TVector3.PseudoRapidity'].ignore(
    '.*transvers momentum.*')

from .taudecay import TauDecay

class EventModel(TreeModel):
    runnumber = IntCol()
    evtnumber = IntCol()
    weight = FloatCol()
    hadhad = IntCol() # 1 or 0
    lephad = IntCol() # 1 or 0
    leplep = IntCol() # 1 or 0
    
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
    def set(cls, this, miss1, miss2):
        FourMomentum.set(this, miss1 + miss2)

class TrueTau(FourMomentum + FourMomentum.prefix('vis_')):
    nProng = IntCol(default=-1111)
    nPi0 = IntCol(default=-1111)
    charge = IntCol()
    flavor = CharCol()
    pdgId = IntCol(default=-1111)
    index = IntCol()
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


        TrueTau.set(tree.tau1, tau1.fourvect)
        TrueTau.set(tree.tau2, tau2.fourvect)

        tau1_decay = TauDecay(tau1)
        tau2_decay = TauDecay(tau2)

        TrueTau.set_vis(tree.tau1, tau1_decay.fourvect_vis)
        TrueTau.set_vis(tree.tau2, tau2_decay.fourvect_vis)


        tree.tau1.index = tau1.index
        tree.tau1.charge = tau1.charge
        tree.tau1.flavor = 'l' if tau1_decay.leptonic else 'h'
        if tree.tau1.flavor == 'l':
            tree.tau1.pdgId = pdg.mu if tau1_decay.leptonic_muon else pdg.e
        else:
            tree.tau1.nProng = tau1_decay.nprong
            tree.tau1.nPi0s = tau1_decay.nneutrals
        
        tree.tau2.index = tau2.index
        tree.tau2.charge = tau2.charge
        tree.tau2.charge = tau2.charge
        tree.tau2.flavor = 'l' if tau2_decay.leptonic else 'h'
        if tree.tau2.flavor == 'l':
            tree.tau2.pdgId = pdg.mu if tau2_decay.leptonic_muon else pdg.e
        else:
            tree.tau2.nProng = tau2_decay.nprong
            tree.tau2.nPi0s = tau2_decay.nneutrals


        TrueMet.set(tree.met, tau1_decay.fourvect_missing, tau2_decay.fourvect_missing)

        vis_tau1 = tau1_decay.fourvect_vis
        vis_tau2 = tau1_decay.fourvect_vis
        tree.dR_taus = vis_tau1.DeltaR(vis_tau2)
        tree.dEta_taus = abs(vis_tau1.Eta() - vis_tau2.Eta())
        tree.dPhi_taus = abs(vis_tau1.DeltaPhi(vis_tau2))
        if vis_tau2.Pt() != 0:
            tree.pt_ratio_tau1_tau2 = vis_tau1.Pt() / vis_tau2.Pt()
        else:
            tree.pt_ratio_tau1_tau2 = 0


def get_model():
    model = EventModel + TrueTauBlock + FourMomentum.prefix('higgs_')
    return model

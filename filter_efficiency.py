


MASSES = range(60, 205, 5)

EFFS_GGH = [
    0.0970214,
    0.121563,
    0.147029,
    0.172998,
    0.203194,
    0.22777,
    0.257334,
    0.272257,
    0.304266,
    0.314505,
    0.34139,
    0.352908,
    0.37255,
    0.390016,
    0.411083,
    0.418796,
    0.447989,
    0.45294,
    0.471476,
    0.475692,
    0.483232,
    0.499351,
    0.513769,
    0.526981,
    0.528653,
    0.542064,
    0.553526,
    0.552364,
    0.565739,
]

EFFS_VBF = [
    0.18761,
    0.200924,
    0.217893,
    0.238209,
    0.253846,
    0.276579,
    0.289503,
    0.30656,
    0.330077,
    0.344614,
    0.363689,
    0.385743,
    0.404302,
    0.408063,
    0.43163,
    0.442243,
    0.456288,
    0.474068,
    0.48572,
    0.490004,
    0.503119,
    0.515464,
    0.521376,
    0.541067,
    0.546807,
    0.554139,
    0.566572,
    0.577367,
    0.580181,
]

from rootpy.plotting import Graph, Canvas, Legend
from rootpy.plotting.style import set_style
from rootpy import ROOT

set_style('ATLAS', shape='rect')
ROOT.gROOT.SetBatch(True)

gr_vbf = Graph(len(MASSES))
gr_ggh = Graph(len(MASSES))

for ip, (m, eff_vbf, eff_ggh) in enumerate(zip(MASSES, EFFS_VBF, EFFS_GGH)):
    gr_vbf.SetPoint(ip, m, eff_vbf)
    gr_ggh.SetPoint(ip, m, eff_ggh)


gr_vbf.title = 'VBFH#rightarrow #tau#tau'
gr_vbf.color = 'red'
gr_vbf.xaxis.title = 'm_H [GeV]'
gr_vbf.yaxis.title = 'Filter Efficiency'
gr_vbf.yaxis.SetRangeUser(0, 0.6)
gr_ggh.title = 'ggH#rightarrow #tau#tau'
gr_ggh.color = 'blue'
gr_ggh.xaxis.title = 'm_{H} [GeV]'

c = Canvas()
gr_vbf.Draw('APL')
gr_ggh.Draw('SAMEPL')
leg = Legend([gr_vbf, gr_ggh], pad=c, anchor='upper left')
leg.Draw('same')
c.SaveAs('filter_eff.png')

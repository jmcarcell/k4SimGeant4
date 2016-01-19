from Gaudi.Configuration import *
from Configurables import ApplicationMgr, HepMCReader, HepMCDumper, FCCDataSvc

albersevent = FCCDataSvc("EventDataSvc")

reader = HepMCReader("Reader", Filename="../example_MyPythia.dat")
reader.DataOutputs.hepmc.Path = "hepmc"

from Configurables import HepMCConverter
hepmc_converter = HepMCConverter("Converter")
hepmc_converter.DataInputs.hepmc.Path="hepmc"
hepmc_converter.DataOutputs.genparticles.Path="allGenParticles"
hepmc_converter.DataOutputs.genvertices.Path="allGenVertices"

from Configurables import G4SimSvc, G4GdmlDetector
det = G4GdmlDetector("G4GdmlDetector", gdml = "../Sim/SimG4Common/gdml/example.xml")
geantservice = G4SimSvc("G4SimSvc", detector=det, physicslist="G4FtfpBert", actions="G4FullSimActions")
geantservice.addTool(det)

from Configurables import G4SimAlg, G4SaveTrackerHits, G4SaveCalHits
savetrackertool = G4SaveTrackerHits("G4SaveTrackerHits")
savetrackertool.DataOutputs.trackClusters.Path = "clusters"
savetrackertool.DataOutputs.trackHits.Path = "hits"
savetrackertool.DataOutputs.trackHitsClusters.Path = "hitClusterAssociation"
geantsim = G4SimAlg("G4SimAlg",
                        outputs = ["G4SaveTrackerHits/G4SaveTrackerHits"] )
geantsim.DataInputs.genParticles.Path="allGenParticles"

from Configurables import AlbersWrite, AlbersOutput
out = AlbersOutput("out",
                   OutputLevel=DEBUG)
out.outputCommands = ["keep *"]

ApplicationMgr( TopAlg = [reader, hepmc_converter, geantsim, out],
                EvtSel = 'NONE',
                EvtMax   = 1,
                ExtSvc = [podioevent, geantservice], # order! geo needed by geant
                OutputLevel=DEBUG
 )

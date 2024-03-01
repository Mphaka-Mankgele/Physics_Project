import opengate as gate
from scipy.spatial.transform import Rotation  # used to describe a rotation matrix
import numpy as np
import rootReader as read

def create_simulation():
    # create the simulation
    sim = gate.Simulation()

    # main options
    sim.g4_verbose = False
    sim.g4_verbose_level = 1
    sim.visu = True
    sim.visu_type = "vrml"
    sim.visu_verbose = False
    sim.number_of_threads = 1
    sim.random_engine = "MersenneTwister"
    sim.random_seed = "auto"

    # Units
    m = gate.g4_units.m
    eV = gate.g4_units.eV
    keV = gate.g4_units.keV
    MeV = gate.g4_units.MeV
    mm = gate.g4_units.mm
    Bq = gate.g4_units.Bq
    
    # Setting the world size
    world = sim.world
    world.size = [3 * m, 3 * m, 3 * m]
    world.material = "G4_AIR"

    # add a simple crystal volume
    crystal = sim.add_volume("Box", "Crystal")
    cm = gate.g4_units.cm
    crystal.size = [20 * cm, 20 * cm, 10 * cm]
    crystal.translation = [[0 * cm, -50 * cm, 0],
                       [0 * cm, -50 * cm, 10*cm],
                       [-20 * cm, -50 * cm, 0],
                       [-20 * cm, -50 * cm, 10*cm],
                       [0 * cm, 50 * cm, 0],
                       [0 * cm, 50 * cm, 10*cm],
                       [-20 * cm, 50 * cm, 0],
                       [-20 * cm, 50 * cm, 10*cm]]
    crystal.material = "G4_CADMIUM_TELLURIDE"

    # Source
    
    source = sim.add_source("GenericSource", "Default")
    source.particle = "gamma"
    source.position.type = "sphere"
    source.position.radius = 10 * mm
    source.position.translation = [0, 0, -14 * cm]
    source.energy.mono = 80 * keV
    source.direction.type = "momentum"
    source.direction.momentum = [0, 0, 1]
    source.activity = 200 * Bq 
    sec = gate.g4_units.second
    sim.run_timing_intervals = [[0, 2 * sec], [2* sec, 3 * sec]]
    
    # Physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics"
    sim.physics_manager.special_physics_constructors.G4OpticalPhysics = True

    
    # Detector
    actor = sim.add_actor("PhaseSpaceActor", "PhaseSpace")
    actor.mother = "Crystal"
    actor.attributes = [
        "KineticEnergy",
        "Weight",
        "PostPosition",
        "PrePosition",
        "ParticleName",
        "PreDirection",
        "PostDirection",
        "TimeFromBeginOfEvent",
        "GlobalTime",
        "LocalTime",
        "EventPosition",
    ]
    actor.output = "Results/info.root"
    f = sim.add_filter("ParticleFilter", "f")
    f.particle = "gamma"
    actor.filters.append(f)

    # add stat actor
    sim.add_actor("SimulationStatisticsActor", "Stats") 
    # start simulation
    sim.run()

if __name__ == "__main__":
    create_simulation()
    read.read_root_file("Results/info.root", "PhaseSpace")
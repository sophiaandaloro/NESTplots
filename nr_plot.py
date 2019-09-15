
import nestpy 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes


#Detector identification
detector = nestpy.DetectorExample_XENON10()
# detector = nestpy.VDetector()

# Performing NEST calculations according to the given detector example       
nc = nestpy.NESTcalc(detector) #can also be left empty    


#GetInteractionObject grabs the number for the interaction you want so you don't have to always reference the dictionary. Just type e.g., 'ion'
#It just changes the name to a number for nestpy to do its work.
def GetInteractionObject(name):
    name = name.lower()
    
    if name == 'er':
        raise ValueError("For 'er', specify either 'gammaray' or 'beta'")
    
    nest_interaction_number = dict(
        nr=0,
        wimp=1,
        b8=2,
        dd=3,
        ambe=4,
        cf=5,
        ion=6,
        gammaray=7,
        beta=8,
        ch3t=9,
        c14=10,
        kr83m=11,
        nonetype=12,
    )
    
    interaction_object = nestpy.INTERACTION_TYPE(nest_interaction_number[name])
    return interaction_object

#Once you have interaction, you can get yields
#Begin with np.vectorize so that we can get yields over a range of interaction types/energies/drift fields.
@np.vectorize
def GetYieldsVectorized(interaction, yield_type, **kwargs):
    # This function does nc.GetYields for the various interactions and arguments we pass into it
    # TODO: Look at docstrings
    
    interaction_object = GetInteractionObject(interaction)
    
    if 'energy' in kwargs.keys():
        if interaction_object == GetInteractionObject('nr') and kwargs['energy'] > 3e2:
            return np.nan
    if interaction_object == GetInteractionObject('gammaray') and kwargs['energy'] > 3e3:
            return np.nan
    if interaction_object == GetInteractionObject('beta') and kwargs['energy'] > 3e3:
            return np.nan     
    yield_object = nc.GetYields(interaction = interaction_object, **kwargs)
    #this returns the yields for the type of yield we are considering be it ElectronYield or PhotonYield (an attribute of yield)
    return getattr(yield_object, yield_type)

#Gives us photon yield values
def PhotonYield(**kwargs):
    return GetYieldsVectorized(yield_type = 'PhotonYield', **kwargs)
#Gives electron yields    
def ElectronYield(**kwargs):
    return GetYieldsVectorized(yield_type = 'ElectronYield', **kwargs)

def Yield(**kwargs):
    return {'photon' : PhotonYield(**kwargs),
            'electron' : ElectronYield(**kwargs),
           # What is missing?  Aren't there other parts of YieldObject?
           }


#we are able to do nestpy with 13 different interaction types and that's all we're going to use here.
# interaction_types = np.array(['nr','wimp','b8','dd','ambe','cf','ion', 'gammaray', 'beta', 'ch3t', 'c14', 'kr83m', 'nonetype'])

fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000] 

energies = np.logspace(-1, 4, 2000)
energies = np.broadcast_to(energies, (len(fields), len(energies))) 


# ## Nuclear Recoils
# The following are the energy and field ranges for nuclear recoil examples in the detector and interaction we set above. 


nr_electrons = ElectronYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies
nr_photons = PhotonYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies



def nr_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(figsize=(13.2,4.1))
    subplot1 = plt.subplot(121)
    subplot2 = plt.subplot(122)
    for i in range(0, len(driftFields)-2):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))   
        
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    
    subplot1.set_ylim(bottom=0)
    subplot2.set_ylim(bottom=0)
    
    subplot1.legend(loc='best', fontsize= 8, ncol=3)
    subplot1.set_xlabel('Recoil Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for Nuclear Recoils')
    subplot1.margins(0)         
    subplot2.legend(loc='best', fontsize= 8, ncol=3)    
    subplot2.set_xlabel('Recoil Energy [keV]')
    subplot2.set_title('Charge Yields for Nuclear Recoils')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 
    subplot2.margins(0)
    plt.savefig('nr_results.png')

nr_subplot(energies, nr_photons, nr_electrons, fields)
from opentrons import protocol_api, types
import pandas as pd
import numpy as np
import os

# metadata
metadata = {
    'protocolName': 'LIBRARY POOLING AND DILUTION',
    'author': 'Name <jason.andoy@g42.ai>',
    'description': 'LIBRARY POOLING AND DILUTION FOR OPENTRONS',
    'apiLevel': '2.10'
}
water_run = False
Source_positions = []
Target_positions = []
RSB_volumes = []
DNA_volumes = []
pool_volume = 15.0



# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    # DECLARE LABWARES/MODULES
    #### TIP RACKS
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '7')

    #### PLATES
    # TODO
    sample_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5')
    lobind_tubes = protocol.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', '6', label='Lobind Tubes')
    #### PIPETTES
    left_pipette = protocol.load_instrument('p20_multi_gen2', mount='left')
    right_pipette = protocol.load_instrument('p300_multi_gen2', mount='right')

    sample_plate_wells = sample_plate.wells()
    protocol.comment(str(len(sample_plate_wells)))

    # define tips
    def define_tip_positions_for_multi_pipette():
        """"
            This function defines tip position starting from H1 to A12 e.g. H1, G1, F1, E1, D1, C1, B1, A1
            in reference with the number of samples. it is given in a reverse order to pick up only a single
            tip using the multi channel pipette
            :returns list
        """
        well_position_letters = ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        well_position_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        tip_positions = []
        for a in well_position_numbers:
            if len(tip_positions) == 96:
                break
            for b in well_position_letters:
                ba = b + a
                tip_positions.append(ba)
        return tip_positions

    def library_pooling():
        tip_positions = define_tip_positions_for_multi_pipette()
        for index in range(96):
            while 0 <= index <= 23:
                left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]])
                left_pipette.aspirate(location=sample_plate_wells[index].bottom(),
                                      volume=pool_volume)
                left_pipette.dispense(location=lobind_tubes['A1'].bottom())

                if water_run:
                    left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                          home_after=False)
                else:
                    left_pipette.drop_tip(home_after=False)

                del tip_positions[0]

            while 23 <= index <= 47:
                left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]])
                left_pipette.aspirate(location=sample_plate_wells[index].bottom(),
                                      volume=pool_volume)
                left_pipette.dispense(location=lobind_tubes['B1'].bottom())

                if water_run:
                    left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                          home_after=False)
                else:
                    left_pipette.drop_tip(home_after=False)

                del tip_positions[0]

            while 47 <= index <= 71:
                left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]])
                left_pipette.aspirate(location=sample_plate_wells[index].bottom(),
                                      volume=pool_volume)
                left_pipette.dispense(location=lobind_tubes['C1'].bottom())

                if water_run:
                    left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                          home_after=False)
                else:
                    left_pipette.drop_tip(home_after=False)

                del tip_positions[0]

            while 71 <= index <= 95:
                left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]])
                left_pipette.aspirate(location=sample_plate_wells[index].bottom(),
                                      volume=pool_volume)
                left_pipette.dispense(location=lobind_tubes['D1'].bottom())

                if water_run:
                    left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                          home_after=False)
                else:
                    left_pipette.drop_tip(home_after=False)

                del tip_positions[0]


    # IF YOU WANT TO CANCEL A STEP BELOW JUST ADD '#'
    # protocol.pause('Add Mastermix to resvoir')
    library_pooling()

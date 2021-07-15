from opentrons import protocol_api, types
import pandas as pd
import numpy as np
import os

# metadata
metadata = {
    'protocolName': 'PRE LIBRARY PREP NORMALIZATION',
    'author': 'Name <jason.andoy@g42.ai>',
    'description': 'PRE LIBRARY PREP NORMALIZATION FOR OPENTRONS',
    'apiLevel': '2.10'
}
water_run = False
Source_positions = []
Target_positions = []
RSB_volumes = []
DNA_volumes = []
mm_volume = 199.0
DNA_volume = 1.0

file_input_ot2 = '/data/user_files/input.csv'
file_input_local = 'C:/Users/Administrator/PycharmProjects/ILLUMINA_Opentrons/OT2CEP20210331B_DNA_EXT/Protocols/PreLibrary_Prep_Normalization/96input.csv'

df = pd.read_csv(file_input_ot2)

for i in range(len(df)):
    Source_positions.append(df['Source'][i])
    Target_positions.append(df['Target'][i])
    RSB_volumes.append(df['RSB_volume'][i])
    DNA_volumes.append(df['DNA_volume'][i])


# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    # DECLARE LABWARES/MODULES
    #### TIP RACKS
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '7')

    #### PLATES
    # TODO
    rsb_source = protocol.load_labware('thermofisher_reservoir', '8')
    sample_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '5')
    empty_plate = protocol.load_labware('opentrons_96_aluminumblock_biorad_wellplate_200ul', '6', label='SEMI SKIRTED PLATE')
    #### PIPETTES
    left_pipette = protocol.load_instrument('p20_multi_gen2', mount='left')
    right_pipette = protocol.load_instrument('p300_multi_gen2', mount='right')

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
            if len(tip_positions) == len(df):
                break
            for b in well_position_letters:
                ba = b + a
                tip_positions.append(ba)
        print('Number of Samples: ', len(df))
        print('Number of Tips: ', len(tip_positions))
        return tip_positions

    def sample_plate_aliquoting():
        tip_positions = define_tip_positions_for_multi_pipette()
        for index in range(len(df)):
            left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]])
            left_pipette.aspirate(location=sample_plate[Source_positions[index]].bottom(),
                                  volume=DNA_volumes[index])
            left_pipette.dispense(location=empty_plate[Target_positions[index]].bottom())

            if water_run:
                left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                      home_after=False)
            else:
                left_pipette.drop_tip(home_after=False)

            del tip_positions[0]

    def rsb_aliquoting():
        tip_positions = define_tip_positions_for_multi_pipette()
        for index in range(len(df)):
            left_pipette.pick_up_tip(location=tiprack_20ul[tip_positions[0]].bottom())
            left_pipette.aspirate(location=rsb_source['D1'],
                                  volume=RSB_volumes[index])
            left_pipette.dispense(location=empty_plate[Target_positions[index]].bottom())

            if water_run:
                left_pipette.drop_tip(location=tiprack_20ul[tip_positions[0]],
                                      home_after=False)
            else:
                left_pipette.drop_tip(home_after=False)

            del tip_positions[0]

    def only_sample_mixing():
        protocol.comment('ONLY SAMPLE MIXING')
        d = 0
        for j in range(int(len(Source_positions) / 8)):
            right_pipette.pick_up_tip()
            right_pipette.mix(repetitions=15,
                              volume=200.0,
                              location=dna_source_plate[Target_positions[d]].bottom(2),
                              rate=10.0)
            right_pipette.blow_out(location=dna_source_plate[Target_positions[d]].bottom(8))
            right_pipette.touch_tip()
            right_pipette.aspirate(volume=10,
                                   location=dna_source_plate[Target_positions[d]].top(),
                                   rate=10.0)
            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            d = d + 8

    def dna_aliquot():
        protocol.comment('DNA ALIQUOT')
        i = 0
        for j in range(int(len(Source_positions) / 8)):
            left_pipette.pick_up_tip()
            left_pipette.aspirate(volume=DNA_volume,
                                  location=dna_source_plate[Source_positions[i]].bottom(3.5))
            protocol.delay(seconds=1)
            left_pipette.dispense(volume=DNA_volume,
                                  location=nunc_target_plate[Target_positions[i]].bottom(0.3),
                                  rate=30.0)
            # POSITION OFFSETS
            bottom_location = nunc_target_plate[Target_positions[i]].bottom(0.4)
            right_offset = bottom_location.move(types.Point(x=2, y=0, z=0))
            left_pipette.move_to(location=right_offset)
            left_pipette.blow_out(location=right_offset)
            i = i + 8
            if water_run:
                left_pipette.return_tip(home_after=False)
            else:
                left_pipette.drop_tip(home_after=False)

    def master_mix_aliquot():
        protocol.comment('MASTER MIX ALIQUOT')
        g = 0
        for j in range(int(len(Source_positions) / 8)):
            right_pipette.pick_up_tip()
            right_pipette.aspirate(volume=mm_volume,
                                   location=mm_source['A1'].bottom(0.2))
            protocol.delay(seconds=0.5)
            right_pipette.dispense(volume=mm_volume,
                                   location=nunc_target_plate[Target_positions[g]].bottom(1),
                                   rate=10.0)
            right_pipette.mix(repetitions=6,
                              volume=150.0,
                              location=nunc_target_plate[Target_positions[g]].bottom(1),
                              rate=10.0)
            right_pipette.blow_out(location=nunc_target_plate[Target_positions[g]].bottom(1))
            if water_run:
                right_pipette.return_tip(home_after=False)
            else:
                right_pipette.drop_tip(home_after=False)
            g = g + 8

    #### COMMANDS ####
    # if water_run:
    #     protocol.set_rail_lights(True)
    # else:
    #     protocol.set_rail_lights(False)

    # IF YOU WANT TO CANCEL A STEP BELOW JUST ADD '#'
    # only_sample_mixing()
    # dna_aliquot()
    # protocol.pause('Add Mastermix to resvoir')
    # master_mix_aliquot()\
    sample_plate_aliquoting()
    rsb_aliquoting()

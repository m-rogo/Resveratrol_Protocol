from opentrons import protocol_api

metadata = {
    'protocolName': 'Resveratrol production using high rate enzymes',
    'author': 'Matthew Rogan',
    'apiLevel': '2.2'
}


def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", 2)
    tiprack_20 = protocol.load_labware("opentrons_96_tiprack_20ul", 1)
    tiprack_300 = protocol.load_labware("opentrons_96_tiprack_300ul", 4)
    tuberack_1 = protocol.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap", 5)
    tuberack_2 = protocol.load_labware("opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical", 3)

    # Pipettes
    p300 = protocol.load_instrument("p300_single", "Left", tip_racks=[tiprack_300])
    p20 = protocol.load_instrument("p20_single_gen2", "Right", tip_racks=[tiprack_20])

    # Ensures liquids dispensed 10 mm above bottom of well to prevent contamination
    p300.well_bottom_clearance.dispense = 10
    p20.well_bottom_clearance.dispense = 10

    # buffers and enzyme volumes
    s30_buffer = [
        161, 165, 179, 183, 175, 166, 175, 179, 170, 175, 171, 165, 170, 170, 165, 174, 156, 174, 179, 174, 170, 166,
        161, 170, 166, 161, 170
    ]

    pal = [
        5, 10, 1, 1, 1, 10, 5, 5, 10, 5, 5, 1, 5, 1, 10, 1, 10, 10, 1, 1, 1, 5, 10, 10, 5, 10, 5
    ]

    four_cl = [
        10, 10, 5, 1, 5, 5, 5, 1, 1, 1, 5, 10, 10, 5, 1, 1, 10, 1, 1, 10, 10, 10, 5, 5, 5, 10, 1
    ]

    sts = [
        10, 1, 1, 1, 5, 5, 1, 1, 5, 5, 5, 10, 1, 10, 10, 10, 10, 1, 5, 1, 5, 5, 10, 1, 10, 5, 10
    ]

    # S30 buffer
    p300.transfer(s30_buffer,
                  tuberack_2['A1'],
                  plate.wells('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2',
                              'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4'),
                  touch_tip=True)  # Touches tip on side of the well to ensure no liquid on tip
    # ATP 2 ul each well
    p20.transfer(2, tuberack_1['A1'], plate.columns('1', '2', '3'), touch_tip=True)
    p20.transfer(2, tuberack_1['A1'], plate.wells('A4', 'B4', 'C4'), touch_tip=True)

    # CoA 2 ul each well
    p20.transfer(2, tuberack_1['A2'], plate.columns('1', '2', '3'), touch_tip=True)
    p20.transfer(2, tuberack_1['A2'], plate.wells('A4', 'B4', 'C4'), touch_tip=True)

    # Malonyl-CoA 8 ul each well
    p20.transfer(8, tuberack_1['A3'], plate.columns('1', '2', '3'), touch_tip=True)
    p20.transfer(8, tuberack_1['A3'], plate.wells('A4', 'B4', 'C4'), touch_tip=True)
    # PAL ul
    p20.transfer(pal,
                 tuberack_1['A5'],
                 plate.wells('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2',
                             'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4'),
                 touch_tip=True)
    # 4CL ul
    p20.transfer(four_cl,
                 tuberack_1['A6'],
                 plate.wells('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2',
                             'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4'),
                 touch_tip=True)
    # STS ul
    p20.transfer(sts,
                 tuberack_1['B1'],
                 plate.wells('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2',
                             'H2', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4'),
                 touch_tip=True)

    # L-tyrosine 2 ul each well
    p20.transfer(2, tuberack_1['A4'], plate.columns('1', '2', '3'),
                 mix_after=(3, 20),
                 new_tip='always')  # no need for touch tip as new tip after mix. Mix_after means liquid in wells mixed

    p20.transfer(2, tuberack_1['A4'], plate.wells('A4', 'B4', 'C4'),
                 mix_after=(3, 20),
                 new_tip='always')

    protocol.comment('Protocol complete!')

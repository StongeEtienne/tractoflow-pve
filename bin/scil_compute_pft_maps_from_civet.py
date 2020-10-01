#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute include and exclude maps, and the seeding interface mask from partial
volume estimation (PVE) maps outputed from CIVET. Maps should have values in [0,1], gm+wm+csf=1 in
all voxels of the brain, gm+wm+csf=0 elsewhere.

References: Girard, G., Whittingstall K., Deriche, R., and Descoteaux, M.
(2014). Towards quantitative connectivity analysis: reducing tractography
biases. Neuroimage.

Etienne St-Onge
"""

from __future__ import division

import argparse
import logging

import numpy as np
import nibabel as nib

from scilpy.io.utils import (
    add_overwrite_arg, assert_inputs_exist, assert_outputs_exists)


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('wm', help='White matter PVE map (nifti). '
                              'From CIVET classify/*pve_exactwm* output.')
    p.add_argument('gm', help='Grey matter PVE map (nifti). '
                              'From CIVET classify/*pve_exactgm* output.')
    p.add_argument('csf', help='Cerebrospinal fluid PVE map (nifti). '
                               'From CIVET classify/*pve_exactcsf* output.')
    p.add_argument('sc', help='Sub-cortical gray matter structure (nifti). '
                              'From CIVET classify/*pve_exactsc* output.')

    p.add_argument('--include', required=True, help='Output include map (nifti).')
    p.add_argument('--exclude', required=True, help='Output exclude map (nifti).')
    p.add_argument('--interface', required=True, help='Output interface mask (nifti).')

    p.add_argument('--threshold', type=float, default=0.1,
                   help='Minimum gm and wm PVE values in a voxel to be '
                        'in to the interface. [0.1]')

    p.add_argument('--sc_include_val', type=float, default=0.3,
                   help='Sub-cortical include value: 0 is like white matter,'
                        ' 1 is like gray matter. [0.1]')

    add_overwrite_arg(p)
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    assert_inputs_exist(parser, [args.wm, args.gm, args.csf])
    assert_outputs_exists(parser, args,
                          [args.include, args.exclude, args.interface])

    # Load volume
    wm_img = nib.load(args.wm)
    img_affine = wm_img.affine
    img_shape = wm_img.shape

    wm_pve = wm_img.get_data()
    gm_pve = nib.load(args.gm).get_data()
    csf_pve = nib.load(args.csf).get_data()
    sc_pve = nib.load(args.sc).get_data()

    # distribute  Sub-cortical to white/gray matter
    gm_ratio = args.sc_include_val
    wm_pve += (1.0 - gm_ratio) * sc_pve
    gm_pve += gm_ratio * sc_pve

    # Background
    background = np.ones(img_shape)
    background[gm_pve > 0.0] = 0.0
    background[wm_pve > 0.0] = 0.0
    background[csf_pve > 0.0] = 0.0

    # Interface
    interface = np.zeros(img_shape)
    interface[gm_pve >= args.threshold] = 1.0
    interface[wm_pve < args.threshold] = 0.0

    # Include Exclude maps
    include_map = gm_pve
    include_map[background > 0.0] = 1.0

    exclude_map = csf_pve

    nib.Nifti1Image(include_map.astype('float32'),
                    img_affine).to_filename(args.include)
    nib.Nifti1Image(exclude_map.astype('float32'),
                    img_affine).to_filename(args.exclude)
    nib.Nifti1Image(interface.astype('float32'),
                    img_affine).to_filename(args.interface)


if __name__ == "__main__":
    main()

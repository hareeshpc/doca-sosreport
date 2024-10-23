# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES.
# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, IndependentPlugin


class HBN(Plugin, IndependentPlugin):

    short_desc = 'HBN (Host Based Networking)'
    plugin_name = "hbn"
    vsctl = "ovs-vsctl"
    packages = ('hbn-repo',)

    def setup(self):
        self.add_copy_spec([
            '/etc/mellanox',
            '/var/log/doca/hbn',
            '/var/lib/hbn/etc/cumulus',
            '/var/log/containers',
            self.path_join('/var/log', 'sfc-install.log'),
            self.path_join('/tmp', 'sf_devices'),
            self.path_join('/tmp', 'sfr_devices'),
            self.path_join('/tmp', 'sfc-activated'),
        ])

        self.add_journal(units="sfc")
        self.add_journal(units="sfc-state-propagation")

        self.add_cmd_output([
            f"{self.vsctl} -t 5 list Open_vSwitch .",
            f"{self.vsctl} -t 5 show",
            "crictl ps -a",
            "mlnx-sf -a show",
            "mlnx-sf -a show --json --pretty",
        ])

# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder

from _util import load_public, load_private, dump_cert, write


def generate_ca_cert(base_year, quiet=False):
    if not quiet:
        write('Generating ca cert ... ', end='')

    public_key = load_public('ca')
    private_key = load_private('ca')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'Codex Non Sufficit LLC',
            'common_name': 'Codex Non Sufficit Bad RSA CA',
        },
        public_key
    )
    builder.self_signed = True
    builder.ca = True
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 10, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(private_key)

    dump_cert('ca', certificate)

    if not quiet:
        write('done')

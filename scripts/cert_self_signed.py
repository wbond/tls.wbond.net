# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder

from _util import load_public, load_private, dump_cert, write


def generate_self_signed_cert(domain, base_year, quiet=False):
    if not quiet:
        write('Generating self-signed cert ... ', end='')

    full_domain = 'self-signed.{}'.format(domain)
    public_key = load_public('host')
    private_key = load_private('host')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'Codex Non Sufficit LLC',
            'common_name': full_domain,
        },
        public_key
    )
    builder.self_signed = True
    builder.subject_alt_domains = [full_domain]
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(private_key)

    dump_cert('self-signed', certificate)

    if not quiet:
        write('done')

# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder

from _util import load_public, load_private, load_cert, dump_cert, write


def generate_expired_1963_cert(domain, quiet=False):
    if not quiet:
        write('Generating expired-1963 cert ... ', end='')

    full_domain = 'expired-1963.{}'.format(domain)
    ca_private_key = load_private('ca')
    ca_cert = load_cert('ca')
    public_key = load_public('host')

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
    builder.issuer = ca_cert
    builder.subject_alt_domains = [full_domain]
    builder.begin_date = datetime(1962, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(1963, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('expired-1963', certificate)

    if not quiet:
        write('done')

# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder

from _util import load_public, load_private, load_cert, dump_cert, write


def generate_bad_key_usage_cert(domain, base_year, quiet=False):
    if not quiet:
        write('Generating bad-key-usage cert ... ', end='')

    full_domain = 'bad-key-usage.{}'.format(domain)
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
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.key_usage = set(['crl_sign'])
    builder.extended_key_usage = set(['email_protection'])
    certificate = builder.build(ca_private_key)

    dump_cert('bad-key-usage', certificate)

    if not quiet:
        write('done')

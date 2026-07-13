# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from datetime import datetime

from asn1crypto.util import timezone
from certbuilder import CertificateBuilder
from crlbuilder import CertificateListBuilder

from _util import load_public, load_private, load_cert, dump_cert, dump_crl, write


def generate_client_certs(domain, base_year, quiet=False):
    ca_private_key = load_private('ca')
    ca_cert = load_cert('ca')
    ca2_private_key = load_private('ca2')
    ca2_cert = load_cert('ca2')
    public_key = load_public('client')
    crl_url = 'http://crls.{}:9991/client.crl'.format(domain)

    # Certificate that is valid
    if not quiet:
        write('Generating good client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'Codex Non Sufficit LLC',
            'common_name': 'Codex Non Sufficit TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('client-good', certificate)

    if not quiet:
        write('done')

    # Certificate that has expired
    if not quiet:
        write('Generating expired client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Expired TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    builder.begin_date = datetime(base_year - 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('client-expired', certificate)

    if not quiet:
        write('done')

    # Certificate that is not yet valid
    if not quiet:
        write('Generating future client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Future TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    builder.begin_date = datetime(base_year + 3, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 4, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('client-future', certificate)

    if not quiet:
        write('done')

    # Certificate issued by untrusted CA
    if not quiet:
        write('Generating untrusted client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Untrusted TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca2_cert
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 3, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca2_private_key)

    dump_cert('client-untrusted', certificate)

    if not quiet:
        write('done')

    # Certificate that has a weak signature
    if not quiet:
        write('Generating weak client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Weak TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    # Hack since API doesn't allow selection of weak algo
    builder._hash_algo = 'md5'
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 3, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    certificate = builder.build(ca_private_key)

    dump_cert('client-weak', certificate)

    if not quiet:
        write('done')

    # Certificate that has bad key usage
    if not quiet:
        write('Generating bad key usage client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Bad Key Usage TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 3, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.key_usage = set(['crl_sign'])
    builder.extended_key_usage = set(['email_protection'])
    certificate = builder.build(ca_private_key)

    dump_cert('client-bad-key-usage', certificate)

    if not quiet:
        write('done')

    # Certificate that has been revoked
    if not quiet:
        write('Generating revoked client cert ... ', end='')

    builder = CertificateBuilder(
        {
            'country_name': 'US',
            'state_or_province_name': 'New Hampshire',
            'locality_name': 'Plymouth',
            'organization_name': 'TLS Client Certificates Limited',
            'common_name': 'Revoked TLS Client Certificate',
        },
        public_key
    )
    builder.issuer = ca_cert
    builder.crl_url = crl_url
    builder.begin_date = datetime(base_year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    builder.end_date = datetime(base_year + 3, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    revoked_certificate = builder.build(ca_private_key)

    dump_cert('client-revoked', revoked_certificate)

    if not quiet:
        write('done')

    crl_number = 1000
    crl_builder = CertificateListBuilder(
        crl_url,
        ca_cert,
        crl_number
    )

    crl_builder.add_certificate(
        revoked_certificate.serial_number,
        datetime(base_year, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
        'key_compromise'
    )

    certificate_list = crl_builder.build(ca_private_key)
    dump_crl('client', certificate_list)

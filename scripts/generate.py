# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import datetime

from keys import generate_ca_keys, generate_ca2_keys, generate_host_keys, generate_client_keys

from cert_ca import generate_ca_cert
from cert_ca2 import generate_ca2_cert
from cert_domain_match import generate_domain_match_cert
from cert_wildcard import generate_wildcard_cert
from cert_san_match import generate_san_match_cert
from cert_no_san import generate_no_san_cert
from cert_expired import generate_expired_cert
from cert_expired_1963 import generate_expired_1963_cert
from cert_future import generate_future_cert
from cert_weak_sig import generate_weak_sig_cert
from cert_auth import generate_auth_cert
from cert_bad_key_usage import generate_bad_key_usage_cert

from certs_client import generate_client_certs

from _util import generate_dh_params, get_arg


def generate_keys(quiet=False):
    generate_ca_keys(quiet)
    generate_ca2_keys(quiet)
    generate_host_keys(quiet)
    generate_client_keys(quiet)


def generate_domain_certs(domain, base_year, quiet=False):
    generate_domain_match_cert(domain, base_year, quiet)
    generate_wildcard_cert(domain, base_year, quiet)
    generate_san_match_cert(domain, base_year, quiet)
    generate_no_san_cert(domain, base_year, quiet)
    generate_expired_cert(domain, base_year, quiet)
    generate_expired_1963_cert(domain, quiet)
    generate_future_cert(domain, base_year, quiet)
    generate_weak_sig_cert(domain, base_year, quiet)
    generate_auth_cert(domain, base_year, quiet)
    generate_bad_key_usage_cert(domain, base_year, quiet)
    generate_client_certs(domain, base_year, quiet)


def generate_certs(domain, base_year, quiet=False):
    generate_ca_cert(base_year, quiet)
    generate_ca2_cert(base_year, quiet)
    generate_domain_certs(domain, base_year, quiet)


if __name__ == '__main__':
    domain = get_arg(1)
    regen_domain_certs = domain == '--regen-domain-certs'
    regen_all_certs = domain == '--regen-certs'
    if regen_domain_certs or regen_all_certs:
        domain = get_arg(2)
    if domain is None:
        domain = 'tls.wbond.net'

    base_year = datetime.date.today().year

    if regen_domain_certs:
        generate_domain_certs(domain, base_year)
    elif regen_all_certs:
        generate_certs(domain, base_year)
    else:
        generate_keys()
        generate_certs(domain, base_year)
        generate_dh_params('dhparam')
        generate_dh_params('dhparam-1024', size=1024)

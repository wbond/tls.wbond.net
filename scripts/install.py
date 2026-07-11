# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import shutil
import sys
from os import path

if sys.version_info < (3,):
    from codecs import open


def abort(message, code):
    print(message, file=sys.stderr)
    sys.exit(code)


def get_arg(num):
    if num > len(sys.argv) - 1:
        return None
    value = sys.argv[num]
    if sys.version_info < (3,):
        value = value.decode('utf-8')
    return value


if __name__ == '__main__':
    overwrite = False

    num = 1
    nginx_conf_dir = get_arg(num)

    if nginx_conf_dir == 'overwrite':
        overwrite = True
        num += 1
        nginx_conf_dir = get_arg(num)

    num += 1
    nginx_ssl_dir = get_arg(num)

    num += 1
    wwwroot_dir = get_arg(num)

    if not nginx_conf_dir or not nginx_ssl_dir or not wwwroot_dir:
        abort(
            'Usage: install.py ["overwrite"] {nginx_conf_dir} '
            '{nginx_ssl_dir} {wwwroot_dir}',
            1
        )

    root_dir = path.dirname(path.dirname(path.abspath(__file__)))

    src_tls_conf_path = path.join(root_dir, 'nginx', 'conf', 'tls.conf')
    src_certs_dir = path.join(root_dir, 'certs')
    src_wwwroot_dir = path.join(root_dir, 'nginx', 'wwwroot')

    dest_tls_conf_path = path.join(nginx_conf_dir, 'tls.conf')
    dest_certs_dir = path.join(nginx_ssl_dir, 'tls_certs')
    dest_wwwroot_dir = path.join(wwwroot_dir, 'tls_wwwroot')

    if not path.isdir(nginx_conf_dir):
        message = (
            'Error: nginx_conf_dir "{}" does not exist or is not a directory'
        ).format(nginx_conf_dir)
        abort(message, 2)

    if not path.isdir(nginx_ssl_dir):
        message = (
            'Error: nginx_ssl_dir "{}" does not exist or is not a directory'
        ).format(nginx_ssl_dir)
        abort(message, 3)

    if not path.isdir(wwwroot_dir):
        message = (
            'Error: wwwroot_dir "{}" does not exist or is not a directory'
        ).format(wwwroot_dir)
        abort(message, 4)

    if not overwrite:
        if path.exists(dest_tls_conf_path):
            message = (
                'Error: "{}" already exists, perhaps the "overwrite" parameter '
                'was omitted?'
            ).format(dest_tls_conf_path)
            abort(message, 5)

        if path.exists(dest_certs_dir):
            message = (
                'Error: "{}" already exists, perhaps the "overwrite" parameter '
                'was omitted?'
            ).format(dest_certs_dir)
            abort(message, 6)

        if path.exists(dest_wwwroot_dir):
            message = (
                'Error: "{}" already exists, perhaps the "overwrite" parameter '
                'was omitted?'
            ).format(dest_wwwroot_dir)
            abort(message, 7)

    with open(src_tls_conf_path, 'r', encoding='utf-8') as f:
        tls_conf = f.read()
        tls_conf = tls_conf.replace('wwwroot', dest_wwwroot_dir)
        tls_conf = tls_conf.replace('../../certs', dest_certs_dir)

    with open(dest_tls_conf_path, 'w', encoding='utf-8') as f:
        f.write(tls_conf)

    if overwrite:
        if path.exists(dest_certs_dir):
            shutil.rmtree(dest_certs_dir)
        if path.exists(dest_wwwroot_dir):
            shutil.rmtree(dest_wwwroot_dir)

    shutil.copytree(src_certs_dir, dest_certs_dir)
    shutil.copytree(src_wwwroot_dir, dest_wwwroot_dir)

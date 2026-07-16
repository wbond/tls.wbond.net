# tls.wbond.net

A server that serves up various bad (and good) TLS certificates and
configurations for the sake of testing.

 - [Domains](#domains)
 - [Running Locally](#running-locally)
 - [Installing](#installing)
 - [Generating New Certificates](#generating-new-certificates)

## Domains

Various "good" configurations:

 - [domain-match.tls.wbond.net:10000](https://domain-match.tls.wbond.net:10000)
 - [wildcard-match.tls.wbond.net:10001](https://wildcard-match.tls.wbond.net:10001)
 - [san-match.tls.wbond.net:10002](https://san-match.tls.wbond.net:10002)
 - [required-auth.tls.wbond.net:10003](https://required-auth.tls.wbond.net:10003)
 - [optional-auth.tls.wbond.net:10004](https://optional-auth.tls.wbond.net:10004)
 - [dh1024.tls.wbond.net:10005](https://dh1024.tls.wbond.net:10005)
 - [no-san.tls.wbond.net:10006](https://no-san.tls.wbond.net:10006)

Various "bad" configurations:

 - [expired-1963.tls.wbond.net:11000](https://expired-1963.tls.wbond.net:11000)
 - [future.tls.wbond.net:11001](https://future.tls.wbond.net:11001)
 - [domain-mismatch.tls.wbond.net:11002](https://domain-mismatch.tls.wbond.net:11002)
 - [san-mismatch.tls.wbond.net:11003](https://san-mismatch.tls.wbond.net:11003)
 - [weak-sig.tls.wbond.net:11004](https://weak-sig.tls.wbond.net:11004)
 - [bad-key-usage.tls.wbond.net:11005](https://bad-key-usage.tls.wbond.net:11005)
 - [expired.tls.wbond.net:11006](https://expired.tls.wbond.net:11006)
 - [wildcard.mismatch.tls.wbond.net:11007](https://wildcard.mismatch.tls.wbond.net:11007)
 - [rc4.tls.wbond.net:11008](https://rc4.tls.wbond.net:11008)
 - [rc4-md5.tls.wbond.net:11009](https://rc4-md5.tls.wbond.net:11009)
 - [dh512.tls.wbond.net:11010](https://dh512.tls.wbond.net:11010)
 - [self-signed.tls.wbond.net:11011](https://self-signed.tls.wbond.net:11011)

## CA Certificate

In order to properly test TLS connections, the CA certificate used for the
various domains will need to be added to the trust store/list used by the
code or application being tested.

The CA certificate is located at [certs/ca.crt](certs/ca.crt).

## Running Locally

To use the certificates for testing, `nginx` must be installed. All
of the domains run on non-privileged ports for ease-of-use.

To start nginx, execute:

```bash
bash ./scripts/local.sh
```

## Running with Docker

A `Dockerfile` and `docker-entrypoint.sh` are included so the full set of
bad (and good) TLS endpoints can be run on any machine with Docker
installed, without installing nginx, socat or any other dependencies on the
host.

Build the image:

```bash
docker build -t tls .
```

Run the container (mapping all endpoints to the host):

```bash
docker run -d --name tls \
  -p 9990-9992:9990-9992 \
  -p 10000-10006:10000-10006 \
  -p 11000-11011:11000-11011 \
  tls
```

The endpoints are then reachable on the host at the same ports listed in the
[Domains](#domains) section above, e.g. `https://domain-match.tls.wbond.net:10000`.

The image runs natively on both `linux/amd64` and `linux/arm64` (Apple
Silicon). It includes prebuilt `socat` binaries for each architecture, and
`docker-entrypoint.sh` selects the matching one at runtime, so no emulation is
required on either platform.

## Installing

To install the nginx configuration, web files and certificates on a server,
invoke the following command:

```bash
python scripts/install.py {nginx_conf_dir} {nginx_ssl_dir} {wwwroot_dir}
```

 - `{nginx_conf_dir}` should be a folder to copy the `tls.conf` file into
 - `{nginx_ssl_dir}` should be a folder in which to create a subfolder named
   `tls_certs`, which will contain all certificates, keys and related
   files
 - `{wwwroot_dir}` should be a folder in which to create a subfolder named
   `tls_wwwroot` which will contain the webfiles

The values provided will be used to customize the `tls.conf` file. All that
is necessary will be to add an `include` directive into the main `nginx.conf`:

```
http {
    ...

    include  relative/path/to/tls.conf;
}
```

By default, the install script will not overwrite existing files/directories.
To have existing files and folders replaced, add the `overwrite` parameter to
the arguments:

```bash
python scripts/install.py overwite {nginx_conf_dir} {nginx_ssl_dir} {wwwroot_dir}
```

Additionally, socat will need to be configured to run on port 10003 using
the configuration from [scripts/local.sh](scripts/local.sh). This allows proper
testing of a host requiring client certificates. Unfortunately nginx does not
allow requiring certificates at the TLS protocol level.

## Generating New Certificates

New certificates and keys can be generated if you wish to run your own instance
of the domains.

### Dependencies

Python 2.6, 2.7 or 3.2+ with the following packages:

 - [asn1crypto](https://github.com/wbond/asn1crypto)
 - [oscrypto](https://github.com/wbond/oscrypto)
 - [certbuilder](https://github.com/wbond/certbuilder)
 - [crlbuilder](https://github.com/wbond/crlbuilder)

The simplest way to install them is:

```bash
pip install certbuilder crlbuilder
```

### Commands

To generate all keys and certificates, execute the following, replacing
`{domain}` with the domain name you with to use:

```bash
python scripts/generate.py {domain}
```

If only domain certs need to be regenerated, use:

```bash
python scripts/generate.py --regen-certs {domain}
```

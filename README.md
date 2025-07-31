# Kurtosis Config

This repository contains configuration files for [Kurtosis](https://docs.kurtosis.com/install).

## Quick Start

To run a configuration, use the following command:

```bash
kurtosis --enclave ENCLAVE_NAME run github.com/ethpandaops/ethereum-package --args-file configs/<config-file.yaml>
```

For example, to run the `2507pectra.yaml` configuration, you would use:

```bash
kurtosis --enclave ENCLAVE_NAME run github.com/ethpandaops/ethereum-package --args-file configs/2507pectra.yaml
```

## Configurations

- `configs/2310.yaml`
- `configs/2405.yaml`
- `configs/2411.yaml`
- `configs/2507pectra.yaml`

## Common Commands


- Inspect enclave

```bash
kurtosis enclave inspect ENCLAVE_NAME
```

- Check logs of a specific service (use -f for continuous output)

```bash
kurtosis service logs ENCLAVE_NAME SERVICE_NAME
```

- Read ports and save to file

```bash
python utils/read_ports.py ENCLAVE_NAME
```

- Quick clear and remove enclaves

```bash
sh utils/clear_and_remove.sh ENCLAVE_NAME
```

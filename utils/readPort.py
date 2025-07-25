import re
import sys
import json


def main():
    in_user_services = False
    skip_header = False
    current_el_service = False
    ports = []
    el_ports = {}

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not in_user_services:
            if line.startswith(
                "========================================== User Services =========================================="
            ):
                in_user_services = True
                skip_header = True
            continue
        else:
            if skip_header:
                skip_header = False
                continue
            # Check for end of section (another ==== line)
            if line.startswith("=========================================="):
                in_user_services = False
                continue
            # Process lines here
            # Check if it's a new service line
            if re.match(r"^[a-f0-9]{12}\s+", line):
                # New service entry
                parts = re.split(r"\s{2,}", line.strip())
                if len(parts) >= 2:
                    name = parts[1]
                    if name.startswith("el-"):
                        current_el_service = True

                        # Collect port from this line
                        if len(parts) >= 3:
                            port_line = (name, parts[2])
                            # print(port_line)
                            ports.append(port_line)
                    else:
                        current_el_service = False
                else:
                    current_el_service = False
            else:
                # Check if it's a continuation line and we're in an el service
                if current_el_service and (
                    line.startswith(" ") or line.startswith("\t")
                ):
                    port_line = (name, line.strip())
                    ports.append(port_line)
                else:
                    current_el_service = False

    # Now parse the collected ports to extract the port numbers
    for name, port_line in ports:
        # Split into parts after '->'
        parts = port_line.split("->")
        if len(parts) < 2:
            continue
        address_part = parts[1].strip()
        # Check for 127.0.0.1:port
        match = re.search(r"127\.0\.0\.1:(\d+)", address_part)
        if match:
            el_ports[name + "-" + port_line[: port_line.find(":")]] = match.group(1)

    # print(ports)
    # Print the ports
    toSave = {}
    # i = 0
    # for client, port in el_ports.items():
    #     if client.endswith('-rpc') and not 'engine' in  client:
    #         i = i+1
    #         parts = client.split('-')
    #         if i < 4:
    #             toSave['GETH_MINER'+str(i)+'_RPC_PORT'] = port
    #             continue
    #         if i < 16:
    #             toSave['GETH_TX'+str(i-3)+'_RPC_PORT'] = port
    #             continue

    toSave["GETH_RPC_PORT"] = el_ports["el-1-geth-lighthouse-rpc"]
    toSave["BESU_RPC_PORT"] = el_ports["el-2-besu-lighthouse-rpc"]
    toSave["ERIGON_RPC_PORT"] = el_ports["el-3-erigon-lighthouse-ws-rpc"]
    toSave["NETHERMIND_RPC_PORT"] = el_ports["el-4-nethermind-lighthouse-rpc"]
    toSave["RETH_RPC_PORT"] = el_ports["el-5-reth-lighthouse-rpc"]
    for client, port in toSave.items():
        print(client, port)
    with open("utils/ports.json", "w") as f:
        json.dump(toSave, f, indent=True)


if __name__ == "__main__":
    main()

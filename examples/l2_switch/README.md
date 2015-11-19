# L2 Learning Switch

## Description

This program illustrates layer 2 learning switch.

The P4 program does the following:
- Source MAC address and ingress port of incoming packets are extracted and sent 
  to the CPU port using the `generate_digest()` action primitive
- the original packet is broadcast or forwarded to the appropriate port.

### Running the demo

We provide a small demo to let you test the program. It consists of the
following scripts:
- [run_demo.sh] (run_demo.sh): compile the P4 program and starts the switch,
  also configures the data plane by running the CLI [commands] (commands.txt)
- [receive.py] (receive.py): sniff packets on (eth0) and print a summary
  of them

To run the demo:
- start the switch and configure the tables and the mirroring session: `sudo
  ./run_demo.sh`
- send packets inside mininet `mininet> pingall`

This is a very simple example obviously. Feel free to build upon it.

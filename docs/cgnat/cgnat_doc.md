CGNAT Setup and CLI Behavior in German ISP NOC Simulation

Carrier-Grade NAT in German ISP Networks
Introduction to CGNAT and NAT Types
Carrier-Grade NAT (CGNAT), also known as Large-Scale NAT, is a solution to IPv4 address exhaustion that allows ISPs to share a single public IPv4 address among multiple customers by using NAT44 (IPv4-to-IPv4 network address translation on a large scale)
cisco.com
. In practice, residential users are assigned private IPv4 addresses (often in the special 100.64.0.0/10 range reserved for carriers) which are then translated to a shared public IPv4 in the provider’s network
wiki.mikrotik.com
. This effectively moves the NAT boundary from the home router into the ISP’s network. Major German ISPs like Deutsche Glasfaser have widely adopted CGNAT – for instance, Deutsche Glasfaser does not provide unique public IPv4 addresses to each user by default (users get IPv6 and a private IPv4 that is NATed in the backbone)
community.roonlabs.com
deutsche-glasfaser.de
. The result is that multiple customers’ traffic exits to the internet from the same public IPv4, distinguished only by port numbers. NAT44 refers to the one-to-many translation of IPv4 addresses (many private IPv4 hosts mapped to a public IPv4 with different ports). A specific scenario often seen with CGNAT is NAT444, nicknamed for the three different IPv4 address domains involved
en.wikipedia.org
. In a NAT444 deployment, a user’s device has a private IP (e.g. 192.168.1.x), which the home router NATs to an ISP-supplied private IP (e.g. 100.64.x.x); then the carrier’s CGNAT device NATs that to a public IPv4
wiki.mikrotik.com
. The “triple NAT” (customer LAN → ISP CGN → Internet) is transparent to the user except that inbound connections are not possible without special handling. Many German ISPs operate in a dual-stack or DS-Lite environment as well. Dual-Stack Lite (DS-Lite) uses an IPv6-access network: the customer receives an IPv6 address and no public IPv4. Any IPv4 traffic from the customer is encapsulated over IPv6 and then translated via NAT44 at the ISP’s AFTR (Address Family Transition Router) device
en.fritz.com
. This is common in IPv6-ready networks (e.g. used by some cable operators and FTTH providers) to cope with IPv4 scarcity. Another variant, NAT64, translates IPv6 client traffic to IPv4 servers (often used in mobile networks or ISP core networks as IPv6 adoption grows)
alcatelunleashed.com
. However, in German fixed-line networks the primary mode is NAT44/NAT444 for IPv4 with increasing reliance on native IPv6 for end-to-end connectivity.
CGNAT Devices and Network Roles
CGNAT can be implemented on various types of carrier-grade networking devices, each fitting a role in the ISP architecture:
Broadband Network Gateways (BNGs): The BNG (also called BRAS in DSL networks) is the aggregation router where subscriber sessions terminate (PPPoE or IPoE/DHCP sessions). Modern BNG routers often support integrated CGNAT functionality. For example, Cisco ASR 9000 series or Nokia 7750 SR BNGs can perform NAT44 on subscriber traffic as part of their services
cisco.com
. In this model, each BNG at the network edge might translate the private IPv4 addresses of its connected subscribers to public addresses. This distributed approach localizes NAT to the edge and is scalable by adding NAT capacity per BNG. BNGs manage thousands of subscribers, so NAT features are designed to handle high session counts and integrate with subscriber management (e.g. tying NAT records to subscriber IDs). Nokia’s BNG (SR OS) and Cisco’s BNG both support CGNAT, ensuring IPv4 address sharing is handled either directly on the line cards or via service modules.
Core and Edge Routers: Core routers in an ISP backbone typically focus on high-speed packet forwarding and MPLS, and may not perform NAT themselves. However, edge routers (those connecting toward the internet or between regions) can host NAT services if equipped appropriately. In some networks, a high-end router at the network boundary is configured with CGNAT for all outgoing traffic. For example, a Juniper MX series router with a services card (SPC) can run CGNAT at the edge, or a Cisco ASR 1000/CRS with CGN service modules can act as the NAT device. These routers essentially function as centralized CGNAT appliances when deployed in that role. The core network routes subscriber traffic (still using private IPs) towards the routers or appliances that perform the NAT before egress to the public internet.
Dedicated CGNAT Appliances: Many ISPs use purpose-built CGNAT devices or software appliances in their network. These include solutions like A10 Networks Thunder CGN and F5 BIG-IP CGNAT, or Cisco’s legacy Carrier-Grade Services Engines. These appliances are optimized for handling millions of concurrent NAT translations and high throughput. They often sit at aggregation points or datacenters. For instance, an ISP might deploy a cluster of A10 Thunder CGN devices in a central location (sometimes referred to as a NAT farm or CGNAT pool) that all BNGs feed into. These devices typically offer robust features: deterministic NAT, logging exports, integrated DDoS protection for the NAT pool, etc. They run their own OS and have CLI/web interfaces specific to NAT operations.
Carrier-Grade Firewalls: In some cases, ISPs leverage high-performance firewalls to achieve CGNAT functionality, effectively combining security filtering with NAT. Examples include large Fortinet or Juniper SRX clusters configured for large-scale NAT, or even Linux-based solutions for smaller ISPs. These are not as common in major ISPs due to the extreme scale required, but smaller providers or specific network segments might use them. A firewall-based CGNAT will have the same inside-private to outside-public translation but with the addition of firewall policies. The CLI (or GUI) in this case would be firewall-specific (e.g. Juniper’s JunoOS security hierarchy or FortiOS commands). The advantage is enhanced security controls per user/session; the downside can be scale limitations compared to purpose-built CGNAT routers.
Each of these devices plays a role in the network topology:
The BNG is often the first IP hop for customers and can either do NAT itself or forward traffic to a CGNAT device deeper in the network. For example, Deutsche Glasfaser has Nokia BNGs and core routers; those Nokia routers (running SR OS) handle subscriber IPv4 via CGNAT in the backbone
deutsche-glasfaser.de
. In such a case, the BNG provides the subscriber with an address (likely a 100.64/10 address) and the translation happens as traffic exits the provider network.
Core routers ensure connectivity and may implement policy routing or tunneling to get subscriber traffic to the CGNAT appliance or service. They generally don’t require NAT-specific configuration except to make sure the private address space is not leaked externally (e.g. implement filters so 100.64.0.0/10 or other RFC1918 do not escape un-NATed).
CGNAT appliances or edge routers doing NAT will typically sit at peering or uplink points. They have interfaces on the inside (ISP network, carrying private source IPs) and outside (public internet). They maintain the NAT tables and perform the translations in real time. These devices need substantial CPU/TCAM resources or specialized ASICs to handle translation lookups for every packet.
CLI Conventions by Vendor: The exact CLI used to configure and manage CGNAT depends on the vendor:
Cisco IOS / IOS-XE / IOS-XR: Cisco routers use the familiar IOS-style NAT commands. Interfaces are designated ip nat inside or ip nat outside. Typically an ACL defines the inside address range, and a NAT pool or interface is used for the outside. For example, on a Cisco IOS XE router one might configure: ip nat pool CGN-POOL 198.51.100.1 198.51.100.10 prefix-length 24 and then ip nat inside source list 100 pool CGN-POOL overload to map an ACL (matching inside private subnets) to a pool of public addresses with port overload. This is how dynamic NAT44 is set up in IOS
cisco.com
. In IOS-XR (used on ASR9000, etc.), the configuration is slightly different (CGNAT is configured under a services namespace and one enables NAT44 CGN mode globally with ip nat settings mode cgn), but the general principles are the same. Cisco CLI also provides verification commands like show ip nat translations, which lists active NAT entries (inside local to inside global address mapping)
cisco.com
, and show ip nat statistics for summary stats
cisco.com
. On IOS-XR, one might use show nat64 translations or show services nat44 port-block, etc., depending on the feature set. The command structure remains textual and familiar to network engineers.
Nokia SR OS: Nokia’s Service Router OS (used on 7750 SR, 7450, etc.) has a hierarchical CLI. NAT is configured under the context of a service (like a VPRN for the BNG or a global service for the NAT appliance role). You would define NAT inside and outside settings. For instance, one would create a NAT outside pool of public IPv4 addresses (with a command under configure service nat such as outside pool ISP-Pool address <range>) and a nat-policy that ties an inside (private side) to that pool. In the nat-policy, you can specify the translation mode (large-scale NAT44, deterministic or not, etc.), set port block sizes or limits, and assign any filtering or exclusions. Nokia supports L2-aware NAT (integrating with subscriber sessions so that when a user disconnects, their NAT mappings can be cleared immediately)
alcatelunleashed.com
. The CLI might look like: configure service vprn 300 nat inside source-nat policy "NAT44-Policy" to apply a NAT policy to a given VPRN (which would be the BNG instance for subscribers). Monitoring on Nokia is done with commands like show service nat overview (to list all NAT pools and usage) or show service nat nat-policy "<name>" statistics to see active sessions, usage per pool, etc
infocenter.nokia.com
. Nokia also provides very detailed logging and even RADIUS accounting for NAT if enabled – for example, it can send vendor-specific RADIUS attributes with the subscriber’s public IP and port range when they log in, useful for logging and tracing
wiki.mikrotik.com
. The Nokia CLI differs from Cisco in syntax but covers similar concepts: defining inside/outside, pools, and viewing translation entries.
MikroTik RouterOS: MikroTik devices (like the CCR routers) use a Unix-like CLI where NAT is configured under the /ip firewall nat menu. Each NAT rule can match certain parameters and specify an action. For CGNAT, the configuration is essentially the same as any source NAT (masquerade) setup, just applied to the ISP’s subscriber network. For example, a MikroTik CGNAT rule could be:
shell
Copy
Edit
/ip firewall nat add chain=srcnat src-address=100.64.0.0/10 out-interface=WAN action=src-nat to-addresses=198.51.100.1-198.51.100.4
This would translate any packets from the carrier’s CGNAT address space 100.64.0.0/10 to an address in the public range 198.51.100.1-198.51.100.4, using port overload
wiki.mikrotik.com
. MikroTik also supports specifying to-ports if one wanted to restrict or static-map port ranges, but by default it will auto-select ports (usually from 1024–65535). The CLI on RouterOS also provides print and print stats commands to inspect the NAT rules. For example, ip firewall nat print stats will show how many packets/bytes have been translated by each rule
wiki.mikrotik.com
. To monitor connections, one would use /ip firewall connection print which lists all current connection tracking entries (including srcnat/dstnat info). MikroTik doesn’t use the term “CGNAT” in configuration – you simply configure NAT for the private ranges as needed
wiki.mikrotik.com
. From an operational standpoint, an admin might check the number of connections per user by filtering that connection table (e.g. count connections from a particular 100.64.x.x address).
Other vendor CLIs: For completeness, other vendors like Juniper use a service-set model for CGNAT on MX series routers. The Junos CLI would involve configuring a NAT rule-set, then applying it to a service set on an interface. For example, set services nat pool CGN-POOL address-range 203.0.113.0/26 port automatic and then set services service-set CGN-NAT nat rules CGN-RULE pool CGN-POOL address-mapping random. Monitoring is via show services nat statistics or similar. On Fortinet devices, CGNAT is configured with firewall policies and VIPs, or using a feature called NAT46/NAT64 for carrier NAT – the CLI uses config firewall ippool and config system nat with large PAT port ranges. Each platform has its nuances, but generally one defines the address pools, enables NAT on the relevant interfaces, and then monitors the session table.
In summary, the devices used for CGNAT in German ISP networks range from high-end routers (Cisco, Nokia, Juniper) acting as BNGs or dedicated NAT nodes, to standalone appliances. The CLI differs (IOS vs. SR OS vs. RouterOS), but all provide commands to configure NAT pools, set inside/outside interfaces, and view translations and stats. Next, we’ll delve into how these devices manage port allocations, session limits, and logging – critical aspects for large-scale NAT.
Port Allocation and Session Management in CGNAT
Port Allocation Methods: A critical aspect of CGNAT design is how TCP/UDP port numbers are allocated for translations. Each public IPv4 address has 65,536 TCP ports and the same number of UDP ports available. CGNAT devices manage these ports as a shared resource among many customers. There are a few strategies for allocation:
Dynamic Port Allocation (Random Port NAT): This is the traditional PAT (Port Address Translation) behavior. Whenever a new connection from a subscriber needs a public socket, the CGNAT picks any free port on one of the public IPs in the pool. This maximizes utilization – in theory a single public IP could be fully used (over 64k concurrent flows if spread across many users)
community.juniper.net
. However, dynamic allocation means the CGNAT has no fixed relationship of subscribers to port ranges; any port could belong to any user at any time. This yields the highest address sharing efficiency (more users per IP) but has a downside in terms of record-keeping: it generates a high volume of logging, since every new flow could get a different port and the mapping of private→public:port must be logged for traceback
community.juniper.net
. It’s also called non-deterministic NAT. Security is considered “high” in the sense that ports are randomized and not predictable
community.juniper.net
 (reducing chances of certain attacks or user collisions). Dynamic allocation is often the default mode if not configured otherwise.
Deterministic or Static Port Block Allocation: To alleviate logging and manageability issues, ISPs often use a Port-Block Allocation (PBA) strategy. In this approach, each subscriber is pre-allocated a block of ports on a given public IP (or multiple blocks on multiple IPs). For example, Subscriber A might always use ports 10000–10999 on public IP 203.0.113.1, and Subscriber B uses ports 11000–11999 on the same IP, etc. This is referred to as deterministic NAT when the mapping is fixed by algorithm, or simply bulk port allocation when done on the fly in chunks. The key benefit is drastic reduction in logging: instead of logging every flow, the CGNAT only logs the assignment of a block to a user
cisco.com
 (or in fully deterministic schemes, logging can be nearly eliminated because the assignment is pre-known). According to a Juniper CGNAT study, dynamic NAT logging is “high” volume, whereas NAT with PBA has low log volume and fully deterministic NAT can have null (no) logging required
community.juniper.net
. This is because for deterministic NAT, the ISP knows that (for example) Customer X with internal IP 10.0.0.5 will always use public IP 203.0.113.1 and ports 10000-10127 (a block of 128 ports) – so if a query comes in from law enforcement, the mapping can be derived without having stored every connection
documents.rtbrick.com
community.juniper.net
. PBA is effectively a middle ground: the first time a subscriber initiates traffic, they get assigned a block (say 128 ports) on a particular public IP, and the system logs that one event
community.juniper.net
. All flows from that user will use ports out of that block (the CGNAT ensures this), until perhaps they need another block (then a second log entry is made). This reduces logging by orders of magnitude
community.juniper.net
. Many CGNAT platforms implement PBA under various names: Cisco calls it Bulk Port Allocation
cisco.com
, Juniper calls it port block allocation with “user quotas”, and it’s aligned with IETF RFCs like 7422 which recommend such approaches
wiki.mikrotik.com
.
Port Reservation and Patterns: With PBA or deterministic NAT, often a block size is chosen (common ones are 64, 128, 256, or 1024 ports per block). Sometimes a “step” or spacing can be configured to avoid contiguous port ranges (for instance, a scattered allocation might give each user ports in increments of, say, 8 or 16 apart to reduce the chance two users get adjacent port numbers, which can help certain applications). Cisco’s CGNAT allows defining a block size and a step (e.g., block of 100 ports with step of 100 gives a sort of round-robin distribution across the 64k range)
cisco.com
. Nokia and Juniper similarly allow configuration of block sizes and the number of blocks per user. Deterministic NAT typically requires choosing a fixed number of users that share an IP – for example, if each user gets 1024 ports, then at most 64 users share one IPv4 (64×1024 = 65536). If each gets 2048 ports, up to 32 users per IP, etc. The number is usually a power of 2 to align blocks nicely (64, 128, 256, etc., fitting 2^x)
community.juniper.net
. This ratio is a business decision: fewer users per IP (larger port blocks each) means better performance per user (less chance of port exhaustion) but uses more public IP addresses. More users per IP (small blocks) conserves IPs but risks users hitting their port limit.
Endpoint-Independent vs. Endpoint-Dependent Mapping: Another technical detail is how the CGNAT handles multiple connections from the same internal endpoint. Endpoint-Independent Mapping (EIM) means once a host’s internal IP:port is mapped to a public IP:port, it will reuse that mapping for all flows to any destination (until it closes). Endpoint-Dependent (Address and Port Dependent) means each new destination may get a new mapping. Many CGNATs use endpoint-independent mapping for consistency (and to better support peer-to-peer protocols)
data.nag.wiki
data.nag.wiki
. This is configurable in some devices and can slightly alter port usage patterns (but it’s more about NAT behavior for applications than resource allocation).
In practice, German ISPs have been reported to use port block strategies. For example, one carrier’s setup might give each customer a set of ~2,000 ports, resulting in about a 1:32 sharing ratio on each public IP
reddit.com
. Real-world data suggests an average residential user at a given moment might only have a few hundred active flows (e.g. web browsing, streaming, some apps)
reddit.com
, so a block of 1024 or 2048 ports is usually sufficient and rarely all used. Power users (torrents, many IoT devices, etc.) might come closer to the limit, so ISPs choose the block size and number of blocks to allow (some allow multiple blocks if the first fills up). If a user tries to exceed their allotted ports and no more are available, the CGNAT will typically drop the new sessions (and may send an ICMP error – some devices send “ICMP port unreachable” back when no port can be allocated, or a specific signal that NAT quota is exceeded). For instance, A10’s CGNAT can be configured with user-quota commands to limit ports per user (e.g. 1000 TCP, 1000 UDP) and then an overall session limit
data.nag.wiki
data.nag.wiki
. On Cisco, there’s a concept of max translations per host that can be set, and Juniper’s CGNAT has max-session-per-subscriber as a config option in the service-set
reddit.com
reddit.com
. Session Limits: Beyond port blocks, CGNAT devices often enforce absolute session limits per subscriber. A “session” in NAT terms is usually a flow (a unique 5-tuple of inside IP, inside port, outside IP, outside port, protocol). The session limit could coincide with port limits (since typically one flow uses one port), but sometimes they count differently (e.g. ICMP might count as a session without using a “port” in the TCP/UDP sense). ISPs set these limits to prevent any single subscriber from opening an unreasonable number of connections (which could be due to malware or misconfiguration). As noted, a common ballpark is 1000–2000 sessions per subscriber for residential service
reddit.com
. Some stricter setups use ~500 or even as low as 256, but those can impact heavy users. Conversely, some networks anticipating many IoT or concurrent apps might allow 4000+ per user
reddit.com
. The limits may also vary by subscriber type – e.g. business customers might be put on a different CGNAT or given a public IP because NAT limits would interfere with their needs (as one engineer quipped, “I wouldn’t put business customers behind NAT…might as well give them a real IP”
reddit.com
). Technically, on devices like Juniper or A10, these limits are configured in the NAT policy (Juniper user-max-session or A10 user-quota session 5000 as in the config guide
data.nag.wiki
data.nag.wiki
). Logging and Monitoring: One of the biggest challenges with CGNAT is maintaining logs to comply with legal and operational requirements. In Germany and other countries, ISPs must be able to identify the user of an IP address at a given time. With CGNAT, this means logging which customer had which public IP and port at what time
wiki.mikrotik.com
. All major CGNAT solutions have built-in logging mechanisms:
Syslog Logging: The CGNAT device can emit a syslog message for each NAT translation event (creation and deletion). This typically includes the internal IP:port, translated public IP:port, and timestamp. For example, Cisco IOS will, when NAT logging is enabled, produce syslogs like %IOSNAT: Built TCP connection for inside 10.0.0.5:34567 to outside 203.0.113.1:55234 (mapping id etc.). Because of volume, Cisco introduced High-Speed Logging (HSL) which is a binary-structured logging that can be exported at high rates to a collector
cisco.com
. Instead of regular text syslog, HSL uses NetFlow or IPFIX to export NAT records in a condensed form. This dramatically improves logging performance and reduces load on the router compared to processing thousands of syslog text lines per second.
Bulk/Batched Logging: As described earlier, using port blocks can reduce log messages. Cisco’s “Bulk Port Allocation” feature explicitly was made to “reduce the volume of NAT log messages by allocating a block of global ports instead of a single port”, so it logs only at block allocation time
cisco.com
. In other words, if a user opens one connection or 100 connections within the same block of 128 ports, a single log entry covers it. The log would say (for example) that 10.0.0.5 was allocated ports 55000-55127 on 203.0.113.1 at time X
cisco.com
. Only if they go beyond 128 and get a second block would a new log entry be generated. This is aligned with the RFC 7422 idea mentioned in MikroTik’s documentation: “deterministically map customer addresses to public addresses + port ranges” to significantly cut down logging
wiki.mikrotik.com
.
Deterministic (No Logging): In a fully deterministic CGNAT, the mapping algorithm is known (often a formula using the customer’s private IP or some user ID to assign a specific port range on a specific public IP). In this case, the system might log nothing during operation – it only needs to store the algorithm or seed info. However, in practice, many ISPs still log the assignments periodically or at session start for safety. But deterministic NAT essentially means the customer’s IP or line ID is hashed or mapped to a public IP:port block and only changes if the network config changes, not every session
documents.rtbrick.com
community.juniper.net
. This provides traceability without per-connection logs.
Retention and Volume: It’s not uncommon for CGNAT logs to be millions of entries per day even with optimizations. ISPs usually have a log retention policy (maybe keeping records 3 months, 6 months, etc., depending on regulations). The logs are often stored in compressed binary form. Specialized log collectors or even big data systems (Elasticsearch clusters or Hadoop) might be used to index these NAT logs for quick retrieval when needed (e.g., when authorities present a query for “who used IP x.x.x.x on date/time with port P”). Logging is a critical part of CGNAT planning; some ISPs measure that log generation and handling is one of the main costs of running CGNAT.
Monitoring Commands: Operators will use various CLI commands to monitor CGNAT in real time. Common ones:
show ... translations (to list current NAT entries, often filtered by inside or outside address).
show ... statistics (to see counts of active sessions, peak usage, etc.).
On some systems, show ... pool (to see how many IPs/ports are free or in use in each pool).
Nokia SR OS, for example, has show service nat pool <name> detail to display how many ports are in use and how many subscribers are assigned per public IP. Juniper has show services nat pool usage showing how many of the 64k ports are allocated on each address, and show services nat subscribers to list per-subscriber usage if subscriber awareness is on.
Cisco’s IOS-XE show ip nat statistics will reveal things like: total active translations, hits, misses, expired translations, and even how many translations have been done since last clear
cisco.com
. It also breaks down the pool usage (e.g., which addresses in the pool are in use).
Operators also monitor translation failure counts – e.g. if a user hit a port limit, the NAT device may have a counter for “port allocation failures” or “sessions dropped due to limit”. Cisco has counters for “number of dropped [packets] due to no translation” or similar in show nat statistics. These help identify if the NAT is over capacity.
Logging verification: sometimes commands like show logging or specific monitor start commands are used to ensure NAT logging is functioning. For example, Cisco might use debug ip nat detailed in a lab to see logs, whereas Juniper might use monitor start nat-log to capture live translations.
In summary, CGNAT devices implement sophisticated port allocation schemes (dynamic vs. block vs. deterministic) to balance address efficiency with logging manageability
community.juniper.net
. Session limits protect the network and ensure fair sharing of ports
reddit.com
. And extensive logging capabilities (with high-speed exports and aggregated records) are used to keep track of the many-to-one address mappings in a carrier environment
cisco.com
. All these features are exposed via the device CLI for configuration and monitoring – allowing network engineers in a NOC to simulate or manage the CGNAT as part of their daily operations.
CGNAT Configuration and CLI Examples
Let’s look at some typical configuration snippets and commands on the CLI for different platforms, reflecting how an engineer might set up and check CGNAT in a lab or simulator:
Cisco IOS Example: Suppose we have an ISP router and we want to configure CGNAT for subscribers who have addresses in 10.0.0.0/8 (could be any private range or the CGNAT 100.64/10 range). We also have a pool of public IPv4 addresses 198.51.100.1–198.51.100.63 to use for the translations. On a Cisco IOS or IOS-XE router, the config might be:
cisco
Copy
Edit
ip nat pool CGN_POOL 198.51.100.1 198.51.100.63 prefix-length 26
access-list 1 permit 10.0.0.0 0.255.255.255
! The ACL 1 matches subscriber source IPs.
ip nat inside source list 1 pool CGN_POOL overload
!
interface GigabitEthernet0/0 
  description Towards_Subscribers
  ip address 10.255.255.1 255.0.0.0 
  ip nat inside
interface GigabitEthernet0/1 
  description Towards_Internet
  ip address 203.0.113.2 255.255.255.0
  ip nat outside
This defines a NAT pool and uses an ACL to identify inside traffic, then enables NAT overload (PAT) for that traffic to the pool. The interfaces are marked as inside or outside accordingly. Once running, you can use show ip nat translations to see entries. For example, it might show:
sql
Copy
Edit
Router# **show ip nat translations**
Pro Inside global         Inside local          Outside local         Outside global
--- 198.51.100.5:40001    10.1.2.3:50001        93.184.216.34:443     93.184.216.34:443
--- 198.51.100.5:40002    10.1.2.3:50002        142.250.185.78:443    142.250.185.78:443
--- 198.51.100.7:35000    10.1.5.7:12345        151.101.1.69:80       151.101.1.69:80
(etc...)
Here you see inside local (subscriber) addresses and ports mapped to inside global (public) addresses and ports
cisco.com
. show ip nat statistics would report how many translations are active, e.g.:
yaml
Copy
Edit
Router# **show ip nat statistics**
Total active translations: 2534 (outdoors 1300, indoors 1234)
Peak translations: 4000
--- Inside interfaces: GigabitEthernet0/0
--- Outside interfaces: GigabitEthernet0/1
Hits: 23456789  Misses: 1200
CEF Translated packets: 34567890, CEF Punted packets: 0
Expired translations: 987654, ... 
If using IOS-XR (like ASR9k), the syntax is different (NAT is configured under cgn process), but the show commands are analogous (e.g. show nat pool-stats etc.). Cisco IOS devices also support features like NAT pool grouping, bulk port allocation config (ip nat settings mode cgn and then ip nat inside source list 1 pool CGN_POOL block-size 128 in newer IOS), and NAT64 config if needed (IOS supports NAT64 and DNS64 configuration for v6-v4 translation).
Nokia SR OS Example: On a Nokia 7750 SR acting as a CGNAT (either as part of a BNG or a standalone service router), configuration is done in the context of services. A simplified view could be:
bash
Copy
Edit
A:BNG# configure service vprn 100
A:BNG/vprn[100]# nat outside pool "CGN-POOL" 
A:BNG/vprn[100]#  address-range 198.51.100.1 mask 255.255.255.192
A:BNG/vprn[100]# exit
A:BNG/vprn[100]# nat inside
A:BNG/vprn[100 nat]#  large-scale enable
A:BNG/vprn[100 nat]#  nat-policy "NAT44-POLICY" create
A:BNG/vprn[100 nat nat-policy "NAT44-POLICY"]# inside-prefix 10.0.0.0/8
A:BNG/vprn[100 nat nat-policy "NAT44-POLICY"]# translate address select-from-pool "CGN-POOL"
A:BNG/vprn[100 nat nat-policy "NAT44-POLICY"]# port-block size 128 deterministic
A:BNG/vprn[100 nat nat-policy "NAT44-POLICY"]# exit
A:BNG/vprn[100 nat]# inside prefix 10.0.0.0/8 subscriber-interface "ge-1/1/1"
A:BNG/vprn[100 nat]#  nat-policy "NAT44-POLICY"
This is a hypothetical snippet to illustrate: we create an outside pool of public addresses, enable large-scale NAT (LSN44), define a NAT policy that maps an inside prefix to that pool, with a port-block size of 128 (perhaps deterministic mapping)
documents.rtbrick.com
, and then apply that policy to the subscriber interface. In reality, Nokia’s config is quite detailed, supporting things like nat-classifiers, inside routing instances, etc., but the above captures the idea. Monitoring might involve:
show service nat overview: which would list pools and how many addresses/ports used
infocenter.nokia.com
.
show service nat sessions: to list active sessions (this might show entries similar to Cisco’s, with private/public pairs).
show service nat statistics: summary of total translations, failures, etc.
If deterministic, show service nat subscriber 10.0.0.5 might directly tell which public IP and port range that subscriber has.
Nokia also allows enabling NAT logs to syslog or to a separate logging server, with configurable formats (e.g., it can log in a compact binary or text format similar to Cisco’s HSL). In the CLI, you might see under configure log some configuration for NAT logging (like a log event for “nat-address-allocation”).
MikroTik RouterOS Example: Given MikroTik’s approach is to treat CGNAT as regular NAT, one might set up a Mikrotik CCR as follows:
csharp
Copy
Edit
/ip address add address=100.64.0.1/10 interface=bridge-customers
/ip address add address=198.51.100.1/30 interface=ether1-public
/ip firewall nat add chain=srcnat src-address=100.64.0.0/10 action=masquerade out-interface=ether1-public
This effectively says: any source IP in 100.64.0.0/10 leaving via the public interface will be NATed to the router’s own public IP (198.51.100.1) using masquerade (PAT). If we had multiple public IPs, we could use action=src-nat to-addresses=<range> as mentioned earlier. MikroTik does not inherently know about subscribers, so it can’t automatically divide ports per user without some scripting. However, RouterOS v7 does support a concept called src-address-list in NAT rules, so an advanced config could pre-group subscribers and assign them different rules (though that’s manual). In most cases, Mikrotik will just randomly assign ports as needed (dynamic NAT). The monitoring might involve:
/ip firewall connection print where src-address~"100.64." to see active connections from CGNAT space.
/ip firewall nat print stats to see how many connections have matched the NAT rule (this gives a total, not per user)
wiki.mikrotik.com
.
/system resource print to monitor CPU (since NAT can be CPU-intensive on software routers).
If logs are needed, enabling connection logging would overwhelm the device, so instead one might rely on the fact that the masquerade action can maintain an internal table which is the connection tracking table itself. For legal logging, Mikrotik doesn’t have a built-in solution; an external system would have to query connection tracking or use a feature called Netflow (Traffic Flow in Mikrotik) to export connection data.
Juniper Junos Example (for contrast): Configuring CGNAT on a Juniper MX with SPC involves creating a rule and a service set. For example:
pgsql
Copy
Edit
set services nat pool CGN-POOL address 198.51.100.1/26 port automatic
set services nat pool CGN-POOL address pooling paired               (paired pooling to keep one user to one IP if desired)
set services nat rule CGN-RULE match-direction input
set services nat rule CGN-RULE term 1 from source-address 10.0.0.0/8 
set services nat rule CGN-RULE term 1 then translated pool CGN-POOL
set services service-set CGN-SET nat-rule CGN-RULE
set services service-set CGN-SET interface-service inside service-domain inside-nat
set services service-set CGN-SET interface-service outside service-domain outside-nat
Then applying that service-set to an interface facing subscribers:
pgsql
Copy
Edit
set interfaces xe-0/0/1 unit 0 family inet service input service-set CGN-SET
This is just illustrative. One would also configure security log mode event for NAT to log events or use Juniper’s MS-SPC logging which can log to a remote server. Monitoring with Junos CLI:
show services nat pool CGN-POOL usage (shows how many addresses and ports in use).
show services stateful-firewall nat44 sessions (lists active sessions if stateful firewall/NAT is being used).
show services accounting might show per-subscriber usage if subscriber management is integrated.
Also Junos has a feature called CGNAT Port Block Allocation (very similar to others) where commands like set services nat pool CGN-POOL port block-size 128 and port block-algorithm deterministic can be used, along with set services nat log-aggregation for logging one event per block (Juniper supports something called secured port block allocation which ensures logs are only at block events
reddit.com
).
The above examples highlight the CLI flavor of each vendor. For a Fiberglass NOC simulator, one might simulate a mix of these: e.g., a Cisco IOS-XR BNG with some sample NAT config and outputs, a Nokia SR OS node with its style of config and show outputs, and a Mikrotik CLI for a smaller segment. The goal would be to make the simulation realistic by using the actual commands and outputs network engineers expect.
Common CGNAT Deployment Topologies
Network topology plays a big role in how CGNAT is implemented and managed:
Single-NAT vs. Double-NAT Architecture: In many deployments, the only NAT occurs at the CGNAT device in the provider network (the customer’s router might be in bridge mode or if it is doing NAT, it’s a NAT444 scenario). German ISPs often supply routers (like Fritz!Box) that by default will do NAT for the home network, resulting in a double NAT (NAT444). However, some ISP configurations (especially DS-Lite) put the CPE in a state where it doesn’t NAT the IPv4 at all but sends it over IPv6 to the CGNAT – effectively making the carrier NAT the only NAT (aside from any local firewall). In NAT444 topologies, both customer router and CGNAT perform NAT. This can break certain applications (e.g., a user can no longer reliably port-forward through two layers of NAT without protocols like UPnP or PCP). ISPs generally try to mitigate issues by educating users about IPv6 (for example, Deutsche Glasfaser suggests using IPv6 for inbound connections since IPv4 is CGNAT). The Mikrotik wiki explicitly lists the drawbacks of NAT444: increased state in provider’s router, issues with peer-to-peer (two users behind same public IP connecting), necessity for extra logging, and breaking inbound connections and some protocols
wiki.mikrotik.com
wiki.mikrotik.com
.
Edge (Distributed) NAT Topology: Here, each edge router/BNG performs NAT for the users connected to it. Imagine an ISP with 10 regional BNG routers – each one could have its own pool of public IPv4 addresses and NAT its subscribers’ traffic. The advantages are: scalability (the NAT load is spread out), and if one router fails, it only affects that region’s NAT. It also localizes the traffic – for instance, user A and user B behind the same BNG might even communicate with each other via the private addresses internally without hitting NAT, if the network is configured to allow hairpin or local routing. The drawback is operational complexity: you have multiple translation tables (one per BNG) rather than a single point to query for “who had IP X at time T”. It also potentially uses IPs slightly less efficiently because each BNG might have spare capacity that can’t be shared with others. In practice, many ISPs started with distributed NAT (since they enabled it in the BNG as a quick solution), and some later migrated to centralized solutions for easier management.
Centralized NAT Farm Topology: In this design, all (or many) subscriber flows are forwarded to a central CGNAT cluster. This cluster could be a pair of powerful routers or appliances. Traffic can be forwarded to it using routing tricks: for example, assign the subscribers private IPs out of a certain range and have a route for that range pointing to the CGNAT appliance (where the appliance sees it as inside traffic). Alternatively, use tunneling: some BNGs forward all IPv4 traffic via L2TP or GRE tunnels to the NAT farm. The NAT farm then sends it out to internet and the return traffic comes back and is tunneled to the BNG, then to the user. Central NAT farms simplify public address management – one big pool to maintain – and simplify logging (one place to collect logs). They also allow easier scaling by adding more appliances to the cluster (if the design supports load sharing). On the other hand, they introduce an extra path for the traffic, which can add latency and a potential single point of failure if not designed with redundancy. ISPs mitigate that by having multiple NAT farm sites (e.g., one per major city or region) so traffic doesn’t travel too far and there’s backup if one site goes down.
High Availability and Redundancy: Regardless of topology, CGNAT must be highly available. Common approaches:
Deploy NAT devices in pairs (stateful failover). Some vendors support state replication between two units: if one fails, the backup takes over with minimal session loss. For example, F5 BIG-IP CGNAT can mirror NAT states. Cisco had something called Box-to-Box HA for NAT, but it’s limited; more often, they rely on routing failover.
In a distributed model, each BNG might have two route paths out – if the primary NAT service card fails, traffic could be rerouted to a secondary NAT (possibly a different device).
In centralized model, typically a cluster of appliances behind a load balancer or using equal-cost multipath is used. They might partition by subscriber source subnet or hash of IP so that each flow consistently hits the same NAT node (important, because if packets of the same flow go to different NAT units without a shared state, the flow breaks).
Use of anycast IPs for the public pool is an advanced strategy: e.g., two NAT sites advertising the same pool prefix and relying on routing to split users between them. This is tricky but some large ISPs do similar for load distribution (though usually not for stateful NAT – anycast is more common in stateless or load-balancing scenarios).
Example – NAT444 at the Edge: Consider a simplified diagram of NAT444 where the ISP has not deployed IPv6. The customers have home routers doing NAT 192.168.x.x → 100.64.x.x (ISP assigns 100.64.1.3 to Customer A’s WAN, 100.64.1.2 to Customer B’s WAN, etc.). Then the ISP’s CGNAT device (could be at the BNG or a dedicated router) takes those 100.64.0.0/10 addresses and maps them to public IP 200.100.5.1. In the diagram below, both customers end up appearing as 200.100.5.1 to the internet, differentiated by source port:
Illustration of a CGNAT deployment (NAT444 scenario) in which two customers (each with an ISP-assigned private WAN IP in 100.64.0.0/10) share the same public IPv4 address via the carrier’s NAT device. The CGNAT maintains a mapping of each customer’s flows by assigning them distinct source port ranges on the public IP
draytek.co.uk
draytek.co.uk
. In this example, Customer A (100.64.1.3) and Customer B (100.64.1.2) both egress with public IP 200.100.5.1, but Customer A’s traffic might use ports 55000-55999 while Customer B uses ports 56000-56999, ensuring uniqueness. In that diagram, inside the ISP, routes exist for 100.64.1.2 and .3 via the BNG or aggregation device. The CGNAT device has an inside interface handling 100.64.0.0/10 and an outside interface with IP 200.100.5.1. It translates flows and keeps state: e.g., Customer A’s PC 192.168.0.10 → (NAT at home) → 100.64.1.3:50000 → (CGNAT) → 200.100.5.1:55000 to access some internet server. Customer B might coincidentally also have a device using port 50000 internally, which becomes 100.64.1.2:50000, and the CGNAT could translate that to 200.100.5.1:56000 externally. The CGNAT table links 100.64.1.3:50000 ↦ 200.100.5.1:55000 for Customer A, and 100.64.1.2:50000 ↦ 200.100.5.1:56000 for Customer B
draytek.co.uk
draytek.co.uk
. When replies come from the internet to 200.100.5.1:55000, the CGNAT knows it belongs to 100.64.1.3:50000 (Customer A) and forwards it accordingly. This is the essence of large-scale NAT.
Central NAT Farm Example: If the ISP instead used a centralized NAT farm, the BNGs might not give out 100.64 addresses at all; they could give say 10.x.x.x addresses and route all 10.0.0.0/8 to the NAT farm. The NAT farm router has many public IPs and performs NAT for all regions. Users from different regions could share the same public IP (since all traffic converges there). The topology would include robust backhaul links from BNGs to the NAT farm to handle the aggregated traffic.
Topology for DS-Lite: In DS-Lite, the customer CPE encapsulates IPv4 packets into IPv6 and sends them to the AFTR. The AFTR is essentially the CGNAT device (often located at a central site). The topology here is an IPv6-only access network; the NAT exists only once at the AFTR. The CPE’s WAN IPv4 is a dummy (often 192.0.0.2/ DHCPv6-derived) that is not actually used except within the tunnel. Operationally, DS-Lite can simplify support calls (the user clearly doesn’t have a real IPv4, so port-forwarding must be done via PCP or not at all), but it requires the ISP network to fully support IPv6.
Monitoring and Management in Topologies: In an ISP NOC, engineers will monitor CGNAT resources across the topology. In a distributed model, they might poll each BNG for NAT usage. In a central model, they focus on the NAT cluster. They will watch metrics like: public IP pool utilization (are we running out of ports on any IP?), overall throughput on NAT devices, CPU/memory on those devices (NAT state tables consume memory), and log collection systems (are logs coming in and being stored properly?). They also prepare procedures for when a NAT device needs maintenance: e.g., how to drain traffic from a CGNAT appliance (often you’d stop advertising its IP pool or withdraw a route so new sessions don’t go to it, then wait for existing sessions to expire).
In summary, CGNAT in a carrier network is not just a single box, but an entire environment of devices and topologies working together. German ISPs like Deutsche Glasfaser exemplify a modern deployment: IPv6 to the customer combined with CGNAT for IPv4, often centralized at the core
community.roonlabs.com
. Meanwhile, others (especially mobile operators) have been using large-scale NAT centralized in their packet core for years. The network topology can be tuned for the operator’s preferences: edge NAT for more distributed failure domains, or centralized NAT for easier management. Understanding these topologies is crucial for a NOC simulator to realistically model how and where a CLI command would be run – e.g., a command on a BNG vs. on a central CGNAT router – and what the output represents (local NAT sessions vs. global).
By combining all the above aspects – device types, NAT configurations, port management schemes, session limits, logging, CLI usage, and topology design – one can create a realistic simulation of a CGNAT environment in a fiber ISP’s NOC. For instance, the simulator could present a scenario where a user is having trouble with a service because of CGNAT, and the trainee would use the CLI to check NAT translations on a Cisco or Nokia router, observe the port block allocation, perhaps adjust a user’s session quota, or verify logs for a security inquiry. Each of the CLI snippets and behaviors described comes from real-world CGNAT operations, ensuring the simulation would be grounded in authenticity and technical accuracy. Sources:
Cisco Systems – Carrier-Grade NAT and BNG Documentation
cisco.com
cisco.com
cisco.com
Nokia (Alcatel-Lucent) – SR OS NAT Configuration and Command References
alcatelunleashed.com
infocenter.nokia.com
Juniper Networks – CGNAT Configuration Guides and Community Discussions
community.juniper.net
community.juniper.net
reddit.com
MikroTik Wiki – Carrier Grade NAT (NAT444) Overview and Configuration
wiki.mikrotik.com
wiki.mikrotik.com
wiki.mikrotik.com
Deutsche Glasfaser – Customer FAQ on CGNAT and IPv6
deutsche-glasfaser.de
community.roonlabs.com
RtBrick (Carrier BNG vendor) – CGNAT Implementation Overview
documents.rtbrick.com
documents.rtbrick.com
DrayTek Blog – Explanation of CGNAT Topology and Issues
draytek.co.uk
draytek.co.uk
Cisco IOS XE Guide – Bulk Port Allocation and Logging
cisco.com
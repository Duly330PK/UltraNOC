IP-Routing in deutschen Glasfasernetzen (am Beispiel Deutsche Glasfaser)
In modernen deutschen Glasfasernetzen – insbesondere im FTTH-Bereich (Fiber to the Home) – erfolgt die Datenübertragung vom Backbone bis zum Endkunden über eine mehrstufige, hierarchische Netzarchitektur. Dieser Bericht erläutert technisch präzise den Weg der Datenpakete vom Kernnetz über Aggregations- und Zugangsnetze bis hin zum Kundenanschluss. Dabei werden sowohl Layer-2- (L2) als auch Layer-3- (L3) Konzepte betrachtet, inklusive eingesetzter Protokolle (wie BGP, OSPF, VLAN, MPLS) und typischer Geräteklassen (z. B. Core-Router, Aggregation-Switches, Broadband Network Gateways/BNGs, OLTs und ONTs). Als Beispielnetz dient das Netz der Deutsche Glasfaser, wobei auch allgemeine Gegebenheiten im deutschen Markt berücksichtigt werden. Konkrete Praxisbeispiele – etwa zum Einsatz von Carrier-Grade NAT (CGNAT) bei Privatkunden – werden hervorgehoben, einschließlich der technischen Umsetzung, beteiligter Geräte, Einschränkungen (Portweiterleitung, NAT-Typen) sowie Unterschiede bei Geschäftsanschlüssen. Diagramme und Tabellen veranschaulichen die Struktur.
Übersicht der Netzarchitektur und Topologie
Ein typisches Glasfasernetz gliedert sich in Kernnetz (Backbone), Aggregationsnetz und Zugangsnetz (Access):
Kernnetz (Backbone): Das Rückgrat des Providers, bestehend aus hochperformanten Core-Routern, verbindet zentrale Knoten (z. B. Rechenzentren, große PoPs) miteinander. Es ist meist als MPLS-IP-Netz realisiert, welches die Hauptstandorte in Ring- oder vermaschten Topologien verbindet. Dieses Netz stellt hohe Kapazitäten (10 Gbit/s bis 100 Gbit/s+ Links) bereit und läuft oft auf Glasfaser-Routen durch ganz Deutschland. Über BGP (Border Gateway Protocol) koppelt der Provider sein Backbone an das globale Internet – z. B. über Peering-Punkte (wie DE-CIX in Frankfurt) und Transit-Anbieter. Die Deutsche Glasfaser betreibt beispielsweise das autonome System AS60294 mit BGP-Sessions zu mehreren Upstreams (z. B. Cogent/AS174, Telia/AS1299, Lumen/AS3356) und Peering über Austauschpunkte
bgp.he.net
bgp.he.net
. Innerhalb des Backbones sorgt ein IGP (Interior Gateway Protocol) wie OSPF oder IS-IS für die interne Routenverteilung und Redundanz. Häufig wird das Kernnetz als MPLS-Core betrieben, um VLANs/VPNs zu transportieren und Traffic-Engineering zu ermöglichen.
Aggregationsnetz (Backhaul/Distribution): Dieses verbindet regionale Zugangs-PoPs (Point of Presence) oder Central Offices mit dem Backbone. Hier kommen Aggregation-Switches bzw. Edge-Router zum Einsatz, die den Verkehr vieler Zugangselemente bündeln. Oft werden Metro-Ethernet-Switches oder Router mit MPLS-Fähigkeit genutzt. Die Aggregationsschicht termininiert L2-Verbindungen aus dem Access und leitet Pakete auf L3-Ebene ins Kernnetz. Typisch ist eine Baum-Topologie, bei der z. B. mehrere lokale OLT-Standorte an einen übergeordneten BNG-Standort angebunden sind (teils gestuft). Redundante 10G/100G-Uplinks oder Ringstrukturen sichern hierbei die Ausfallsicherheit. Für die interne Steuerung werden VLANs und ggf. Q-in-Q-Tunneling eingesetzt, um jeden Anschluss oder jede OLT-Route eindeutig zu identifizieren. Moderne Provider nutzen häufig MPLS in der Aggregation, sodass der BNG (Broadband Network Gateway) – also der Router an der Grenze zwischen Access und Core – als Label Edge Router (LER) fungiert
bundesnetzagentur.de
bundesnetzagentur.de
. So können Kundendaten als gelabelte MPLS-Pakete durch das Kernnetz geschleust werden, was ein effizientes Routing ermöglicht
bundesnetzagentur.de
bundesnetzagentur.de
. Interne Routing-Protokolle wie OSPF/IS-IS verteilen die Next-Hops, während LDP oder RSVP-TE Labels für MPLS pflegen.
Zugangsnetz (Access): Dies umfasst die Verbindung vom lokalen Knoten zum Endkunden. In FTTH-Netzen dominiert in Deutschland die PON-Technologie (Passive Optical Network) – konkret meist GPON (Gigabit PON) oder XGS-PON –, aber teils auch PtP-Ethernet (Point-to-Point) Lösungen. In einem PON teilen sich bis zu 32 oder 64 Haushalte einen Glasfaserausgang an einem OLT (Optical Line Terminal), über optische Splitter im Verteilnetz
research.rug.nl
research.rug.nl
. Das OLT steht in einer Vermittlungsstelle/Betriebsstelle des Providers und bündelt die Datenströme vieler Kunden auf einen oder wenige Uplink(s) Richtung Aggregation. Deutsche Telekom vergleicht das mit einem Trichter: Der OLT sammelt die Daten vieler Kunden und schickt sie gebündelt über eine gemeinsame Leitung ins schnelle Netz
telekom.com
telekom.com
. Am Kundengebäude endet die Glasfaser in einer ONT/ONU (Optical Network Termination/Unit), die das optische Signal in ein elektrisches (Ethernet) Signal wandelt
telekom.com
. Die ONT ist meist ein kleines Gerät (Glasfasermodem) beim Kunden, an das der Heimrouter (z. B. Fritzbox) angeschlossen wird. Der OLT und die ONTs kommunizieren nach GPON-Standard verschlüsselt und in zeitmultiplexierten Slots, damit jede ONT nur ihre eigenen Daten empfängt
telekom.com
telekom.com
. In PtP-Architekturen hingegen besitzt jeder Kunde eine eigene Faser bis zum PoP; hier dienen aktive L2-Switches (häufig dieselbe Hardware wie ein GPON-OLT, aber mit Punkt-zu-Punkt-Linecards) als Access Nodes. Deutsche Glasfaser setzt z. B. Nokia 7360 ISAM Systeme als OLT ein (für GPON, meist für Privathaushalte) und dieselbe Plattform mit Ethernet-Linecards für aktive PtP-Business-Anschlüsse
deutsche-glasfaser.de
deutsche-glasfaser.de
.
Die folgende Tabelle gibt einen Überblick über die Netzebenen, Funktionen und Protokolle:
Netzebene	Typische Geräte (Beispiel)	Wichtige Protokolle/Techniken	Funktionen und Bemerkungen
Kernnetz (Core)	Core-Router (z. B. Nokia 7750 SR<sup>1</sup>)	BGP (extern), MPLS, IGP (OSPF/IS-IS)	Backbone verbindet Knoten, weltweite IP-Routing via BGP
bgp.he.net
. MPLS beschleunigt Routing und ermöglicht VPN
bundesnetzagentur.de
.
Aggregation	Edge-Router/BNG, Metro-Ethernet-Switches	MPLS (LDP/TE), VLAN/Q-in-Q, Spanning-Tree	Bündelung vieler Access-Links, Weiterleitung ans Kernnetz. Oft als MPLS-Cloud realisiert, um VLANs der Kunden zu transportieren
bundesnetzagentur.de
.
Access (GPON)	OLT (z. B. Nokia 7360), Splitter, ONT (z. B. Genexis)	GPON (G.984x): TDMA, AES-Verschl.	Letzte Meile zum Kunden: OLT terminiert PON, teilt Bandbreite auf ONTs auf
research.rug.nl
. ONT konvertiert Lichtsignal zu Ethernet
telekom.com
.
Access (PtP)	Access-Switch (Nokia ISAM PtP Linecard), NT (7210 SAS, Cisco NCS)	Ethernet, VLAN, ggf. PPPoE	Direkte Glasfaser pro Kunde, meist für Business. VLAN pro Anschluss, aktive Ethernet-Technik (höhere Kosten, aber echte Entbündelung).

<small><sup>1</sup> Deutsche Glasfaser ersetzt im Backbone aktuell Router zweier Altanbieter durch Nokia-Geräte (laut Pressemitteilung) – vermutlich 7750 SR-Serie für Core/BNG
telcotitans.com
.</small>
Layer-2 im Zugangsnetz: VLANs und Service-Segmente
Im Access-Bereich werden Layer-2-Technologien genutzt, um die einzelnen Kundenanschlüsse voneinander zu trennen und in Richtung BNG zu transportieren. Insbesondere kommen VLANs (IEEE 802.1Q) zum Einsatz. In typischen GPON-Setups gibt es zwei gängige Modelle:
1:1 VLAN pro Kunde: Jeder Endkunde wird in einem eigenen VLAN bis zum BNG geführt
xrdocs.io
. Häufig wird dies mittels VLAN-Stacking (Q-in-Q) realisiert, da ein OLT-Port bis zu 64 ONTs bedient und VLAN-IDs (0–4095) begrenzt sind. Beispielsweise könnte pro OLT ein äußerer VLAN-Tag vergeben werden und pro Kunde ein innerer VLAN-Tag, um alle Kunden eines OLT getrennt zum BNG zu tunneln
documentation.nokia.com
. Dieses Modell bietet hohe Isolation, vereinfacht die Zuordnung und ermöglicht Policies pro Kunde
xrdocs.io
. Deutsche Glasfaser erlaubt z. B. maximal 5 MAC-Adressen pro VLAN-Interface, um zu verhindern, dass ein Privatanschluss unkontrolliert als Switch fungiert
deutsche-glasfaser.de
. Paketverkehr von darüber hinausgehenden MACs wird verworfen, was die Sicherheit erhöht
deutsche-glasfaser.de
.
N:1 VLAN (Shared VLAN): Alternativ werden mehrere Kunden in einem gemeinsamen VLAN geführt (typisch, wenn PPPoE verwendet wird, siehe unten). Dann identifiziert z. B. der PPPoE-Session-ID oder DHCP-Lease den Kunden. Dieses Modell ist einfacher zu konfigurieren, aber erfordert sorgfältige Isolation (z. B. per MAC-FFDB und ARP/Snooping, oder durch L3 im OLT). In PtP-Ethernet-Zugängen wird oft pro Kunde ein eigenes Interface am Access-Switch bereitgestellt, was einem 1:1 VLAN entspricht (physische Trennung).
In der Praxis bei Deutsche Glasfaser werden Privatkunden-FTTH-Anschlüsse typischerweise als DHCP-basiertes IPoE realisiert, ohne dass der Endkunde PPPoE nutzen muss. Das bedeutet: Die ONT des Kunden wird im OLT auf ein VLAN/Interface geschaltet, und der kundeneigene Router erhält per DHCP direkt eine IP-Konfiguration vom Provider. Die BNG-Systeme von DG unterstützen allerdings beide Verfahren: Im technischen Spezifikationsdokument werden IPoE (DHCPv4/v6) und PPPoE als mögliche Protokolle genannt
deutsche-glasfaser.de
deutsche-glasfaser.de
. Standard ist aber IPoE; PPPoE kommt nur in bestimmten Fällen zum Einsatz (etwa bei Wholesale/L2-Bitstrom-Angeboten, wo DG als Vorleister fungiert und die Verbindung via L2TP/PPP an einen fremden Provider übergeben wird). So bestätigte es auch der DG-Support: Selbst wenn Geschäftskunden eine feste IP haben, erfolgt die Einwahl „per DHCP-Verbindung“, nicht via PPPoE
community.sophos.com
. Nutzerberichte zeigen, dass DG für Internet keine PPPoE-Zugangsdaten vorgibt – man schließt den Router einfach an, teils nach Wartezeit wegen MAC-Adressen-Caching, und erhält automatisch die IP
reddit.com
reddit.com
. Nur die VoIP-Telefonie erfordert SIP-Zugangsdaten, keine PPPoE-Zugangsdaten
reddit.com
reddit.com
. Dies unterscheidet sich z. B. von der Telekom, wo traditionell PPPoE mit VLAN 7 genutzt wird. Multi-Service: In modernen Netzen können übers selbe Access auch Triple-Play-Dienste laufen: Internet, IPTV, VoIP. Oft werden dafür getrennte VLANs je Dienst definiert (z. B. ein VLAN für IPTV mit Multicast). BNGs unterstützen MEF-Services wie E-Line, E-LAN, um z. B. Layer2-VPNs für Geschäftskunden bereitzustellen
deutsche-glasfaser.de
. Deutsche Glasfaser erwähnt für Business (DGB) explizit MEF E-LAN/E-Line-Services
deutsche-glasfaser.de
 – etwa für Standortvernetzung – was auf eine MPLS-VPN-Architektur im Kernnetz hindeutet.
Layer-3 im Kern: Routing, BNG und MPLS
Die Layer-3-Schicht übernimmt die vermittlungstechnischen Aufgaben: Zuweisung von IP-Adressen, Routing der Pakete und Verbindung zum Internet. Ein zentrales Element ist der bereits genannte BNG (Broadband Network Gateway) – bei früheren Technologien auch BRAS (Broadband Remote Access Server) genannt. Der BNG befindet sich an der Schnittstelle zwischen dem Konzentrationsnetz (Aggregation) und dem IP-Kernnetz und vereint mehrere Funktionen
bundesnetzagentur.de
:
Kunden-Termination: Der BNG terminiert die Kundensessions. Bei IPoE erhält er die DHCP-Anfragen der Endgeräte und weist IP-Adressen zu; bei PPPoE terminieren hier die PPP-Sessions (Authentifizierung via RADIUS). Der BNG verarbeitet anschlussindividuelle Aspekte wie Zugangskontrolle, QoS-Profile und Accounting. In DG-Netzen ohne PPPoE läuft die Authentifizierung meist implizit über die physische Line ID/MAC, da keine Zugangsdaten nötig sind. Trotzdem werden RADIUS/DHCP-Systeme im Hintergrund genutzt, um z. B. festzulegen, ob ein Kunde eine private (CGNAT) oder öffentliche IP erhält, welche Bandbreite sein Tarif hat usw.
Traffic Aggregation und Switching: Eingehende Daten der Kunden (Upstream) treffen typischerweise als Ethernet-Frames oder PPP-Pakete ein. Der BNG bündelt diesen Ethernet-Upstream-Verkehr vieler Anschlüsse, prüft dessen Zulässigkeit (z. B. gegen Access-Listen, DHCP Option 82, Session-Limits) und leitet ihn dann auf der anderen Seite ins Kernnetz weiter
bundesnetzagentur.de
bundesnetzagentur.de
. In Gegenrichtung nimmt er die vom Kernnetz kommenden Pakete, entfernt ggf. Tunnel-Header oder Labels, und sendet sie über das Access-Ethernet zum richtigen Kundenanschluss
bundesnetzagentur.de
bundesnetzagentur.de
. In gewisser Weise fungiert der BNG gleichzeitig als L3-Router und L2-Switch: Er bearbeitet IP und kann aber auch VLAN-Zuweisungen.
MPLS Edge Router: Im Kontext MPLS versieht der BNG die ausgehenden Pakete mit einem MPLS-Label, um sie ins Kernnetz zu schicken
bundesnetzagentur.de
bundesnetzagentur.de
. Er ist also das Ingress LER (Label Edge Router). Ankommende MPLS-Pakete entlabelt er wieder (Egress LER). In früheren Modellen gab es separate Ethernet-Aggregations-Switches und dahinter separate MPLS-Router (LER) in einem IP-PoP – diese Funktionen sind beim BNG nun in einem Gerät zusammengeführt
bundesnetzagentur.de
bundesnetzagentur.de
. Der BNG in DG-Netzen übernimmt auch die Rolle eines IP-PoP für Bitstrom-Übergaben: Für Wholesale-Partner kann er Traffic als Layer-2-Bitstrom (Ethernet) ausleiten oder einspeisen
bundesnetzagentur.de
. Außerdem ist er oft Multicast-Replikator für IPTV-Dienste (bei Telekom Entertain übernimmt das BNG diese Aufgabe)
bundesnetzagentur.de
.
Auf dem BNG laufen L3-Routing-Protokolle: Er spricht einerseits IBGP/OSPF intern mit den Core-Routern, andererseits dient er als Default-Gateway für die Kunden. Kundenpakete mit externen Zielen werden an den BNG geschickt (ggf. via Standardroute auf CPE-Seite), dort anhand der Routingtabelle ins Kernnetz/Internet weitergeleitet. Core-Router verbinden die BNG-Standorte weiter über IBGP/OSPF mit dem Rest des Netzes. DG erneuert derzeit sein BNG-Setup – es werden z. B. Cisco/Juniper-BNGs durch Nokia 7750 (SR-Edge) ersetzt
telcotitans.com
thefreelibrary.com
. Backbone-Routing: Der Core-Ring von Deutsche Glasfaser ist über eigene Glasfaser-Trassen realisiert (DG baut in ländlichen Räumen aus, koppelt aber über zentrale Knoten z. B. in Frankfurt). Im Backbone werden Externe BGP Sessions zu anderen Netzen gepflegt. DG hat am DE-CIX Frankfurt eine aktive Peering-Präsenz (AS-DGW, selective peering) und tauscht dort Datenverkehr mit vielen Netzen aus
bgp.he.net
bgp.he.net
. Zusätzlich werden Transitverträge genutzt, um alle Präfixe zu erreichen (siehe oben AS174 etc.). Die Interne Reichweite („IGP domain“) bleibt auf das eigene Netz beschränkt – so werden Kundenprefixe via IBGP auf den BNGs announced und nur Default/Aggregate-Routen per OSPF/ISIS verteilt. Dank MPLS muss der Core nicht jeden Endkundenprefix kennen; er leitet anhand von Labels. Regulatorische Anforderungen: Deutsche Besonderheiten betreffen etwa die Routerfreiheit (Kunden dürfen eigene Router anschließen, weshalb PPPoE-Zugangsdaten offen gelegt werden müssten – DG umgeht dies durch DHCP ohne Login
reddit.com
). Auch muss bei behördlichen Anfragen nachvollziehbar sein, welcher Kunde wann welche IP hatte. Daher protokolliert DG bei CGNAT-Betrieb die Adress-/Port-Zuordnung (siehe unten). Die Bundesnetzagentur hat mit Einführung der BNG-Architektur das Modell der IP-PoPs angepasst: BNGs werden nun als Netzebene 2/3-Komponente im Kostenmodell berücksichtigt
bundesnetzagentur.de
. Insgesamt folgt die Netzstruktur gängigen Standards: NE3-Core, NE2-Access-Concentration (BNG), NE1-TAL (Glasfaser-Anschluss). Für FTTH-PtP-Netze betont die BNetzA die Entbündelungsmöglichkeit: hier können alternative Anbieter am ODF eigene Fasern übernehmen
monopolkommission.de
, während bei PtMP (PON) Bitstrom-Zugänge auf Layer 2 (BNG-Übergabe) genormt wurden (in Deutschland existieren ~900 BNG-Übergabepunkte für Layer-2-Bitstrom)
monopolkommission.de
monopolkommission.de
.
IP-Adressierung und CGNAT im Privatkundenanschluss
Ein zentrales Thema bei L3 ist die IP-Adressvergabe an Kunden. Aufgrund der Knappheit öffentlicher IPv4-Adressen setzen viele deutsche FTTH-Anbieter – darunter Deutsche Glasfaser – bei Privatkunden auf Carrier-Grade NAT (CGNAT)
deutsche-glasfaser.de
community.roonlabs.com
. Dabei erhält der Kunde keine eigene öffentliche IPv4-Adresse, sondern teilt sich eine mit mehreren anderen Anschlüssen. Technisch geschieht dies, indem der Kundenrouter vom Provider nur eine private IPv4 (oft aus 100.64.0.0/10) zugewiesen bekommt, und am BNG/Carrier-NAT werden die ausgehenden Verbindungen auf öffentliche IPv4 umgesetzt
deutsche-glasfaser.de
. Laut DG-FAQ ist CGNAT „notwendig“ aufgrund der zur Neige gehenden IPv4-Adressen
deutsche-glasfaser.de
. Ein Anspruch auf eine eigene IPv4-Adresse besteht nicht, wie z. B. Deutsche Giganetz Kunden klar mitteilte
heise.de
. Praktisch bedeutet dies: IPv4-Traffic eines Privatanschlusses läuft über eine geteilte öffentliche IP, die vom NAT-Gateway dynamisch zugewiesen wird
heise.de
. Typischerweise sind Dutzende Kunden pro IPv4 zusammengefasst. CGNAT-Implementierung: Häufig ist das BNG selbst mit einer CGNAT-Funktion ausgestattet (etwa modulare Router mit NAT-Servicekarten) oder es existieren dedizierte LSN (Large Scale NAT) Appliances im Backbone. DG erwähnt „im Backbone des Internetanbieters“ werde die private in eine öffentliche IPv4 umgeschrieben
deutsche-glasfaser.de
 – dies deutet darauf hin, dass zentral im Kernnetz NAT-Gateways betrieben werden. Der Kundenrouter merkt davon wenig: Er bekommt z. B. eine IP 100.x.x.x als WAN-Adresse und der BNG mappt dessen Verbindungen auf z. B. einen Portbereich einer öffentlichen IP. Manche ISPs reservieren jedem Kunden einen Port-Block (z. B. 4096 Ports bei 16 Kunden/IP)
reddit.com
, andere nutzen dynamische Zuordnung pro Fluss (sog. 3-Tuple oder 5-Tuple-Mapping)
reddit.com
. In jedem Fall ist die Anzahl gleichzeitig nutzbarer Ports begrenzt. DG hat nicht offiziell publiziert, wie viele Anschlüsse sich eine IPv4 teilen, aber der Bereich 100.64/10 legt CGNAT nahe. Ein Indikator: Vergleicht man die WAN-IP im Router mit der öffentlichen IP (via „What is my IP“), erkennt man CGNAT, wenn die WAN-IP eine 100.64.x.x ist und von der öffentlichen abweicht
purevpn.com
. IPv6-Einsatz: Als Ausgleich versorgen moderne Anbieter ihre Kunden mit IPv6-Konnektivität. Deutsche Glasfaser bietet Dual-Stack Lite ähnliches Verhalten: IPv4 läuft über CGN, aber IPv6 steht nativ zur Verfügung
community.roonlabs.com
. Kunden erhalten meist ein /56 oder /64-Präfix via DHCPv6 Prefix Delegation. Damit kann der Kunde eingehend über IPv6 erreicht werden, was viele Probleme umgeht. So erklärt es auch ein Heise-Ratgeber: Der Zugriff aufs Heimnetz unterwegs klappt mit IPv6, sofern Smartphone, Mobilfunknetz oder WLAN des Zugriffs IPv6 nutzen und die Geräte daheim IPv6 sprechen
heise.de
. Ist das nicht der Fall, hat man via IPv4 in der Tat keine direkte Erreichbarkeit des Heimanschlusses von außen
heise.de
heise.de
. Für solche Fälle werden Workarounds empfohlen, etwa einen Tunnel/VPN oder einen externen vServer als Proxy zu nutzen
heise.de
heise.de
. Einschränkungen durch CGNAT: Durch die doppelte NAT-Schicht (Lokales NAT im Heimrouter + Carrier-NAT beim Provider, sog. NAT444) ergeben sich mehrere technische Einschränkungen:
Portweiterleitung & Serverbetrieb: Klassisches Port-Forwarding im eigenen Router reicht nicht mehr aus, da der Carrier-NAT eingehende Verbindungen blockiert
community.roonlabs.com
community.roonlabs.com
. Selbst wenn man in der Fritzbox Ports freigibt, kommt der Traffic nicht bis zum Router, da der vorgelagerte NAT keine Zuordnung hat. Dienste wie VPN-Server, Webserver oder Smart-Home-Zugriff über IPv4 funktionieren daher nicht direkt. Die DG-Community bestätigt, dass traditionelles Port-Forwarding nicht mehr möglich ist
community.roonlabs.com
. Abhilfe schafft nur IPv6 oder spezielle Lösungen wie Port-Mapping-Dienste (feste-ip.net) oder VPN-Tunnel (z. B. Tailscale empfahl Roon Labs für DG-Kunden
community.roonlabs.com
).
NAT-Typ und Peer-to-Peer: Anwendungen wie Online-Gaming, VoIP oder P2P-Filesharing leiden unter CGNAT. Oft wird der NAT-Typ als „strikt“ klassifiziert, da ausgehende Verbindungen zwar funktionieren, aber eingehende Peer-Verbindungen schwierig sind. Viele CGNAT-Systeme verwenden symmetrisches NAT – d.h. Port-Mappings sind zieladressabhängig – was z. B. STUN/ICE (für WebRTC) oder Konsolen-Spiele nur erschwert umgehen können. In Gaming-Communities wird berichtet, dass CGNAT zu hoher Latenz und Problemen beim Matchmaking führen kann
linkedin.com
reddit.com
. Auch UDP-Lochstechen (hole punching) versagt, wenn beide Seiten hinter sym. NAT sind. Manche Provider unterstützen UPnP PCP (Port Control Protocol) auf dem Carrier-NAT, sodass der Kundenrouter Portzuweisungen anfragen kann; allerdings ist das bislang selten im Einsatz. DG setzt eher auf IPv6 als Lösung – so entfällt NAT für IPv6-Traffic.
Performance und IP-Blacklist: CGNAT fügt eine Verarbeitungsschicht hinzu; jedoch sind Carrier-NAT-Systeme für hohe Durchsätze ausgelegt. Geringfügig erhöht sich die Latenz und es kann in Spitzenzeiten zu Engpässen kommen. Ein Problem ist Shared-IP-Reputation: Wenn z. B. ein CGNAT-Nutzer Spam verschickt, landet die gemeinsame IPv4 evtl. auf Blacklists – damit sind auch unbeteiligte Kunden betroffen. Einige Online-Dienste (z. B. Banken) erkennen CGNAT-Adressen und blockieren Aktionen oder fordern zusätzliche Verifizierung, weil viele Nutzer unter einer IP auffallen. Auch Rate-Limits oder Captchas bei häufigen Anfragen können eher triggern, da der Traffic mehrerer Kunden aus einer IP kommt
reddit.com
reddit.com
. DG-Kunden berichteten zudem von IP-Wechseln beim NAT: Da keine eigene IP fest zugeteilt ist, kann sich die öffentliche IP ggf. öfter ändern, was z. B. laufende Verbindungen stören könnte (in Praxis aber selten, da NAT-Sessions gehalten werden).
Logging & Rechtliches: Um Missbrauch nachverfolgen zu können, muss der Anbieter bei CGNAT genau mitprotokollieren, welcher Kunde zu welchem Zeitpunkt mit welcher öffentlichen IP:Port-Kombination kommuniziert hat. In Deutschland schreibt das TKG vor, den Sicherheitsbehörden bei Anfrage Auskunft zu ermöglichen. Das erfordert riesige Logdaten auf Seiten des Providers. Manche ISPs schränken daher die Größe der Port-Range pro Kunde ein (um weniger Logging zu erzeugen). Beispielsweise wurde berichtet, dass ein ISP 4096 Ports pro Kunde vergab
reddit.com
 – damit muss er nur die Zuweisung dieses Blocks loggen, nicht jeden einzelnen Port. DG äußert sich dazu nicht öffentlich, aber es ist davon auszugehen, dass ein Logging-Konzept umgesetzt ist.
Unterschiede bei Geschäftsanschlüssen (Business vs. Privat)
Geschäftskunden erhalten in deutschen Netzen meist abweichende Konditionen, um professionelle Anforderungen zu erfüllen. Im Kontext von IP-Routing und Adressierung ergeben sich insbesondere bei Deutsche Glasfaser Business folgende Unterschiede:
Öffentliche IPv4-Adresse: Während Privatkunden keine eigene IPv4 bekommen, bieten Business-Tarife eine feste IPv4-Adresse an
deutsche-glasfaser.de
deutsche-glasfaser.de
. DG wirbt explizit damit: „Dank fester IPv4-Adresse sind sichere VPN-Verbindungen und Serverzugriffe möglich.“
deutsche-glasfaser.de
. In den Small-Business-Tarifen ist eine statische IPv4 inklusive
deutsche-glasfaser.de
deutsche-glasfaser.de
. Das heißt, der Anschluss wird nicht hinter CGNAT platziert, sondern der Router des Kunden erhält eine echte public IPv4. Dadurch entfallen die genannten NAT-Einschränkungen – Firmen können problemlos VPN-Gateways, Mailserver etc. betreiben. Größere Firmenkunden können auf Anfrage sogar zusätzliche IPv4-Subnetze (z. B. /29) bekommen
andysblog.de
, die dann auf den Anschluss geroutet werden. In solchen Fällen richtet DG technisch entweder PPPoE mit „Framed Route“ ein (d. h. die zusätzlichen IPs werden via RADIUS dem PPPoE zugeordnet) oder, da DG meist DHCP nutzt, wird eine statische Route vom BNG auf die Kundenschnittstelle gelegt. Letzteres erfordert, dass der Kundenrouter mit der DG-gestellten WAN-IP als Next-Hop das Subnetz verwenden kann. Einige Business-Kunden berichten, dass DG ihnen PPPoE-Zugangsdaten gab, um mehrere IPs zu handhaben
forum.netgate.com
 – dies scheint aber eher die Ausnahme und nicht für Standard-Business nötig, da auch per DHCP feste IPs verteilt werden können.
IPv6-Prefix: Sowohl Privat- als auch Business-Kunden erhalten bei DG IPv6. Bei Business ist aber ggf. ein größerer Prefix (z. B. /48) möglich, je nach Tarif. Öffentliche Einrichtungen können oft IPv6 genauso frei nutzen. IPv6 spielt hier aber keine Unterscheidung außer evtl. beim Support (Business-Support hilft bei IPv6-Konfiguration, Privatkunden müssen oft selbst Lösungen finden).
Routing & QoS: Business-Anschlüsse werden mit höherwertigen Service Levels betrieben. Das zeigt sich z. B. in garantierten Entstörzeiten (24/7 Support) und evtl. geringeren Überbuchungsfaktoren. Im PON haben alle zwar gleiche physische Bandbreite, aber Business-ONTs können auf separaten PON-Ports mit weniger Teilnehmern hängen oder Priorisierung erhalten. DG erwähnt zwar keine separaten OLTs mehr für Business (früher wurden bestimmte OLTs nur für DGB genutzt
deutsche-glasfaser.de
), aber Traffic Priorisierung und getrennte VLANs sind üblich (etwa eigene VLANs für Business, damit im Aggregationsswitch eine Trennung erfolgt). Der BNG kann QoS pro Kunde anwenden – Business-Kunden könnten z. B. höhere Priorität für bestimmte Dienste bekommen, falls vertraglich zugesichert.
Symmetrische Bandbreiten: Häufig sind Business-Tarife symmetrisch (gleich viel Up- und Download). Bei DG Small Business aktuell bis 600/300 Mbit/s (Down/Up)
deutsche-glasfaser.de
, was zwar noch asymmetrisch ist, aber höherer Upload als Privattarife (dort meist z. B. 1 Gbit/s down, 500 Mbit/s up). Größere Firmenanschlüsse können symmetrische Gbit bekommen
deutsche-glasfaser.de
. Technisch wirkt sich das aufs Routing kaum aus, außer dass die Scheduler im BNG entsprechend konfiguriert sind (keine abendliche Download-Bevorzugung wie bei Privattarifen). BNGs führen hierarchisches Queuing pro Kunde und Dienstklasse durch, um Fairness zu garantieren
research.rug.nl
research.rug.nl
 – für Business werden strengere Garantien eingehalten.
Redundanz und Routing: Geschäftskunden erhalten oft redundante CPE oder zweite Leitungen (z. B. Backup über LTE oder zweiten Fiber Port) auf Wunsch. Aus Sicht des IP-Routings kann ein Business-Kunde auch eine BGP-Session mit dem Provider fahren (bei größeren Anschlüssen mit eigenem AS). DG bietet für Carrier und Großkunden sicher solche Optionen (nicht im Standard-SMB, aber via Carrier Services). Diese spezifischen Routen sind dann statisch oder via BGP im BNG/Edge-Router konfiguriert.
Spezielle Dienste: Zusätzlich zum blanken Internet bieten Business-Tarife oft VPN-Layer2 oder Standortvernetzung über das Providernetz an. Dafür nutzt DG wie erwähnt MEF E-Line/E-LAN Services, was praktisch mittels MPLS L2VPN umgesetzt wird. Routing-technisch sind solche Kunden in separaten VRFs auf dem BNG/PE-Router, damit deren Netze isoliert sind. Dies geht über den normalen Internet-Routingpfad hinaus, sei aber der Vollständigkeit erwähnt.
Zusammenfassend unterscheidet sich das Routing bei Geschäftskunden vor allem durch die öffentliche Adressierung und fehlendes NAT. Ein Firmenanschluss bei DG verhält sich wie klassischer DSL: der Router hat eine offizielle IP und ist vollwertiger Teil des Internets. Privatkunden sind dagegen „ein Stück hinter dem Netz versteckt“ – ausgehende Verbindungen gehen, aber eingehend muss auf IPv6 ausgewichen werden. Die Netztopologie hingegen (OLT → BNG → Backbone) ist für beide identisch, wenngleich Business-Kunden in der Umsetzung bevorzugte Pfade/Ressourcen erhalten können.
Fazit und Ausblick
Die IP-Routing-Infrastruktur deutscher Glasfasernetze ist komplex, aber nach klaren Schichten aufgebaut. Deutsche Glasfaser exemplifiziert den modernen Ansatz: ein MPLS-basiertes Kernnetz mit BNG an der Netzperipherie, VLAN-basierte Access-Anbindung und konsequenter Einsatz von Dual-Stack (IPv6) mit CGNAT für IPv4 im Massenkundensegment. Layer-2-Technologien wie GPON und VLAN sorgen für effiziente Ausnutzung der Glasfaser und Isolation, während Layer-3-Protokolle – BGP, OSPF, etc. – globale und lokale Routen steuern. Die Wahl zwischen CGNAT und echten IPs spiegelt die IPv4-Knappheit wider und führt zu einer Zweiklassengesellschaft: Privatkunden hinter NAT, Business mit Public-IP. Für die Zukunft ist zu erwarten, dass mit zunehmender IPv6-Verbreitung die Notwendigkeit von CGNAT sinkt. Regulatorisch könnten Anforderungen kommen, Privatkunden gegen Aufpreis eine öffentliche IP zu bieten – einige regionale Anbieter tun dies bereits als Option. Technisch jedoch bleibt das Rückgrat – das Backbone mit seinen Core-Routern und BNGs – das Herzstück, das den Datenstrom vom Endgerät über die Glasfaser bis ins weltweite Internet lenkt. Die beschriebene Architektur bildet die Grundlage, um Gigabit-Anschlüsse zuverlässig und skalierbar bereitzustellen. 
deutsche-glasfaser.de
deutsche-glasfaser.de
 Deutsche Glasfaser FAQ erklärt Carrier-Grade NAT (CGN) und stellt klar, dass Privatkunden keine eigene IPv4-Adresse erhalten. Aufgrund der IPv4-Knappheit wird die private Kunden-IP im Backbone in eine öffentliche IPv4 umgesetzt (CGNAT notwendig). Für typische Internetnutzung ist keine feste IP erforderlich, daher bietet DG in Privatkundentarifen keine feste IP an. 
community.roonlabs.com
 Roon Labs Support bestätigt, dass Deutsche Glasfaser flächendeckend CGNAT für IPv4 bei Residential-Kunden einsetzt. Klassisches Port-Forwarding funktioniert deshalb nicht – weder manuell noch via UPnP/NAT-PMP – da eingehende Verbindungen am Carrier-NAT scheitern. 
heise.de
 Heise-Bericht: In Anbieter-FAQs wird offen kommuniziert, dass im Privatkundenbereich CGNAT genutzt wird. IPv4-Verkehr läuft über eine Adresse, die sich mehrere Kunden teilen; ein Anspruch auf eigene IPv4-Adresse besteht nicht. 
heise.de
 Heise-Ratgeber: IPv6 ermöglicht trotz CGNAT den Zugriff aufs Heimnetz. DG-Kunden erhalten IPv6, sodass bei aktiviertem IPv6 auf Smartphone und im Heimnetz die Verbindung klappt. Andernfalls muss man auf einen externen vServer als IPv4-Proxy ausweichen. (Smart Home via CGNAT braucht also IPv6 oder Umwege.) 
community.sophos.com
 Erfahrungsbericht im Sophos-Forum: DG Business-Anschluss mit fester IP nutzt DHCP statt PPPoE. Der Nutzer versuchte PPPoE, erhielt aber vom DG-Support die Info, dass auch bei statischer IP die Verbindung per DHCP erfolgt. (Log zeigte PPPoE-Fehler, da PPPoE nicht nötig ist.) 
deutsche-glasfaser.de
deutsche-glasfaser.de
 Technische Spezifikation der Deutschen Glasfaser (DG Wholesale): Für Home (DGH) wird IPoE (DHCPv4/v6) unterstützt; PPPoE nur für bestimmte LNS/LAC-Szenarien. Für Business (DGB) ebenso IPoE und optional PPPoE oder statische Zuweisung. Es werden max. 5 Kunden-MAC-Adressen pro VLAN-Interface zugelassen – Überschüssige werden verworfen, Sicherheitsfunktionen greifen primär im Access Node/PE-Router. 
bundesnetzagentur.de
bundesnetzagentur.de
 Bundesnetzagentur (WIK) zur BNG-Architektur: Der BNG konzentriert den Verkehr aus Kundenanschlüssen ins MPLS-IP-Routernetz und bearbeitet anschlussindividuelle Aspekte. Er bündelt eingehenden Ethernet-Upstream, prüft die Zulässigkeit und versieht ihn ausgangsseitig mit einem geeigneten Label, um ihn ins MPLS-Netz weiterzuleiten. Aus der Gegenrichtung entfernt er das Label und gibt den Traffic über Ethernet an den Endkundenanschluss. Der BNG vereint die Funktionen eines Ethernet-Switches, eines BRAS und eines Label Edge Routers (LER) in einem Gerät. 
research.rug.nl
 Kundel et al. beschreiben eine typische FTTH-Topologie: Die Kunden-PPPoE-Sessions werden am BNG terminiert, welcher die Grenze zum MPLS-gerouteten ISP-Kernnetz bildet. Der OLT hat eine Ethernet-PtP-Verbindung zum BNG, bei GPON werden bis zu 64 Kunden an einem OLT-Port zusammengeführt und dann gemeinsam zum BNG übergeben. (Zudem werden Beispiele FTTB/FTTC angeführt, aber für FTTH ist relevant: GPON OLT bündelt optisch -> Ethernet zum BNG.) 
deutsche-glasfaser.de
 Deutsche Glasfaser Small Business Tarife: Hervorhebung, dass durch die feste IPv4-Adresse VPN-Verbindungen und Serverzugriffe möglich sind. Business-Kunden erhalten einen Glasfaseranschluss mit hoher Bandbreite und fester IP, ideal für mehrere Mitarbeiter und stabile Anbindung. (Im Tarifvergleich sind feste IPv4-Adressen als Feature aufgeführt.)
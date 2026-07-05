import pytest
from unittest.mock import Mock, patch
import json
from urllib import error
import netifaces
import socket
from scapy.all import IP, TCP, UDP, ICMP, Ether

from tproc import TrafficProcessor


@pytest.fixture
def mock_interface_info():
    """Mock netifaces to return a fake IP and MAC for a specific interface."""
    with patch("netifaces.ifaddresses") as mock_ifaddrs:
        mock_ifaddrs.return_value = {
            netifaces.AF_INET: [{"addr": "192.168.1.100"}],
            netifaces.AF_LINK: [{"addr": "aa:bb:cc:dd:ee:ff"}],
        }
        yield mock_ifaddrs


@pytest.fixture
def mock_hostname_resolution():
    """Mock socket.gethostbyname to return fixed IPs for CNSS and TARGET."""
    with patch("socket.gethostbyname") as mock_gethostbyname:
        def side_effect(hostname):
            if hostname == "cnss":
                return "10.0.0.2"
            if hostname == "mock_target":
                return "8.8.8.8"
            raise socket.gaierror("Unknown host")
        mock_gethostbyname.side_effect = side_effect
        yield mock_gethostbyname


def test_initialization_with_interface(mock_interface_info, mock_hostname_resolution):
    tp = TrafficProcessor(interface="eth0", output_url="http://test", delay=0.5)

    assert tp.gate_ip == "192.168.1.100"
    assert tp.target_ip == "8.8.8.8"
    assert tp.cnss_ip == "10.0.0.2"
    assert tp.interface == "eth0"
    assert tp.output_url == "http://test"
    assert tp.delay == 0.5
    assert tp.packet_cnt == 0
    assert tp.incoming_packets == 0
    assert tp.outgoing_packets == 0
    assert tp.gate_ip in tp.ip_tracker.ignore_ips


def test_packet_handler_statistics(mock_interface_info, mock_hostname_resolution):
    tp = TrafficProcessor(interface="eth0", output_url="http://test")
    # Override IPs to known test values
    tp.gate_ip = "192.168.1.100"
    tp.target_ip = "8.8.8.8"
    tp.cnss_ip = "10.0.0.2"

    # Incoming TCP packet (dport 80 is not a management port)
    pkt_in = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP(sport=12345, dport=80)
    # Outgoing UDP packet – use a non‑management source port (not 53)
    pkt_out = Ether() / IP(src="8.8.8.8", dst="192.168.1.1") / UDP(sport=12345, dport=12345)
    # Incoming ICMP packet
    pkt_icmp = Ether() / IP(src="1.1.1.1", dst="192.168.1.100") / ICMP()

    tp.packet_handler(pkt_in)
    tp.packet_handler(pkt_out)
    tp.packet_handler(pkt_icmp)

    assert tp.packet_cnt == 3
    assert tp.bytes_cnt == len(pkt_in) + len(pkt_out) + len(pkt_icmp)
    assert tp.tcp_cnt == 1
    assert tp.udp_cnt == 1
    assert tp.icmp_cnt == 1
    assert tp.other_cnt == 0

    assert tp.incoming_packets == 2   # TCP and ICMP have dst==gate_ip
    assert tp.outgoing_packets == 1   # UDP has src==target_ip
    assert tp.incoming_bytes == len(pkt_in) + len(pkt_icmp)
    assert tp.outgoing_bytes == len(pkt_out)

    # Verify IP tracker was updated
    assert len(tp.ip_tracker.data) > 0


def test_post_json_success_and_failure():
    tp = TrafficProcessor(output_url="http://localhost:8000")
    mock_stats = {
        "timestamp": "2023-01-01T00:00:00",
        "total_packets": 100,
        "total_bytes": 5000,
        "incoming_packets": 60,
        "outgoing_packets": 40,
        "incoming_bytes": 3000,
        "outgoing_bytes": 2000,
        "packets_per_second": 10.0,
        "bytes_per_second": 500.0,
        "tcp_packets": 70,
        "udp_packets": 20,
        "icmp_packets": 10,
        "other_packets": 0,
        "top_ips": [],
        "status": "online"
    }
    with patch.object(tp, "get_stats", return_value=mock_stats):
        with patch("urllib.request.urlopen") as mock_urlopen:
            # Success case
            mock_response = Mock()
            mock_response.getcode.return_value = 200
            mock_response.read.return_value = b'{"status":"ok"}'
            mock_urlopen.return_value.__enter__.return_value = mock_response

            status, body = tp.post_json()
            assert status == 200
            assert body == '{"status":"ok"}'

            args, kwargs = mock_urlopen.call_args
            request = args[0]
            assert request.get_method() == "POST"
            assert request.headers.get("Content-type") == "application/json"
            data = json.loads(request.data.decode())
            assert "timestamp" in data
            assert data["status"] == "online"

            # HTTP error case
            mock_urlopen.reset_mock()
            error_response = Mock()
            error_response.read.return_value = b'{"error":"bad request"}'
            mock_urlopen.side_effect = error.HTTPError(
                url="http://localhost:8000", code=400, msg="Bad Request",
                hdrs={}, fp=error_response
            )

            status, body = tp.post_json()
            assert status == 400
            assert body == '{"error":"bad request"}'

            # Non‑HTTP exception
            mock_urlopen.reset_mock()
            mock_urlopen.side_effect = ConnectionError("Network unreachable")
            with pytest.raises(ConnectionError):
                tp.post_json()

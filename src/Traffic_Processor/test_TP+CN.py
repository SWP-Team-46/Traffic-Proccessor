import pytest
from unittest.mock import Mock, patch
import json
from urllib import error
import socket
from scapy.all import IP, TCP, UDP, ICMP, Ether
from tproc import TrafficProcessor


def test_initialization_with_interface():
    """Test that TrafficProcessor initializes attributes correctly."""
    with patch("socket.gethostbyname") as mock_gethostbyname:
        def side_effect(hostname):
            if hostname == "cnss":
                return "10.0.0.2"
            if hostname == "mock_target":
                return "8.8.8.8"
            raise socket.gaierror("Unknown host")
        mock_gethostbyname.side_effect = side_effect

        tp = TrafficProcessor(
            interface="eth0",
            output_url="http://test",
            delay=0.5
        )

        # Core attributes
        assert tp.interface == "eth0"
        assert tp.output_url == "http://test"
        assert tp.delay == 0.5

        # Resolved IPs
        assert tp.cnss_ip == "10.0.0.2"
        assert tp.target_ip is None   # No TARGET_HOSTNAME set

        # Counters start at zero
        assert tp.packet_cnt == 0
        assert tp.incoming_packets == 0
        assert tp.outgoing_packets == 0


def test_packet_handler_statistics():
    """Test packet_handler increments counters and determines direction correctly."""
    with patch("socket.gethostbyname") as mock_gethostbyname:
        def side_effect(hostname):
            if hostname == "cnss":
                return "10.0.0.2"
            if hostname == "mock_target":
                return "8.8.8.8"
            raise socket.gaierror("Unknown host")
        mock_gethostbyname.side_effect = side_effect

        tp = TrafficProcessor(interface="eth0", output_url="http://test")
        # Override target_ip to a known value for direction tests
        tp.target_ip = "192.168.1.100"   # Treat this as "our" IP
        tp.cnss_ip = None               # Disable management filter for test

        # Incoming TCP (dst == target_ip)
        pkt_in = Ether() / IP(src="10.0.0.1", dst="192.168.1.100") / TCP(sport=12345, dport=80)
        # Outgoing UDP (src == target_ip)
        pkt_out = Ether() / IP(src="192.168.1.100", dst="8.8.8.8") / UDP(sport=12345, dport=53)
        # Incoming ICMP (dst == target_ip)
        pkt_icmp = Ether() / IP(src="1.1.1.1", dst="192.168.1.100") / ICMP()

        # Process packets
        tp.packet_handler(pkt_in)
        tp.packet_handler(pkt_out)
        tp.packet_handler(pkt_icmp)

        # Global counters
        assert tp.packet_cnt == 3
        assert tp.bytes_cnt == len(pkt_in) + len(pkt_out) + len(pkt_icmp)
        assert tp.tcp_cnt == 1
        assert tp.udp_cnt == 1
        assert tp.icmp_cnt == 1
        assert tp.other_cnt == 0

        # Direction counters (based on target_ip)
        assert tp.incoming_packets == 2   # TCP and ICMP have dst==target_ip
        assert tp.outgoing_packets == 1   # UDP has src==target_ip
        assert tp.incoming_bytes == len(pkt_in) + len(pkt_icmp)
        assert tp.outgoing_bytes == len(pkt_out)

        # IP tracker was updated
        assert len(tp.ip_tracker.data) > 0


def test_post_json_success_and_failure():
    """Test post_json handles successful response and HTTP errors."""
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
                url="http://localhost:8000",
                code=400,
                msg="Bad Request",
                hdrs={},
                fp=error_response
            )
            status, body = tp.post_json()
            assert status == 400
            assert body == '{"error":"bad request"}'

            # Non‑HTTP exception
            mock_urlopen.reset_mock()
            mock_urlopen.side_effect = ConnectionError("Network unreachable")
            with pytest.raises(ConnectionError):
                tp.post_json()

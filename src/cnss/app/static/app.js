const statusDiode = document.getElementById("status-diode");
const primaryLabel = document.getElementById("primary-label");
const primaryValue = document.getElementById("primary-value");
const rateValue = document.getElementById("rate-value");
const packetTypes = document.getElementById("packet-types");
const modeButton = document.getElementById("mode-button");
const packetNodes = {
  tcp_packets: document.getElementById("tcp-packets"),
  udp_packets: document.getElementById("udp-packets"),
  icmp_packets: document.getElementById("icmp-packets"),
  other_packets: document.getElementById("other-packets"),
};

const params = new URLSearchParams(window.location.search);
const isLocalFrontend =
  window.location.protocol === "file:" ||
  (["localhost", "127.0.0.1"].includes(window.location.hostname) &&
    window.location.port !== "8080");
const defaultApiUrl = isLocalFrontend
  ? "http://localhost:8080/packets"
  : `${window.location.origin}/packets`;
const apiUrl = params.get("api") || defaultApiUrl;

const stats = {
  status: "offline",
  total_packets: 0,
  total_bytes: 0,
  packets_per_second: 0,
  bytes_per_second: 0,
  tcp_packets: 0,
  udp_packets: 0,
  icmp_packets: 0,
  other_packets: 0,
};

let pollTimer;
let mode = "bytes";

function formatNumber(value) {
  return Number(value || 0).toLocaleString();
}

function render() {
  const isOnline = stats.status === "online";
  const isPacketMode = mode === "packets";

  statusDiode.classList.toggle("offline", !isOnline);
  packetTypes.hidden = !isPacketMode;
  modeButton.textContent = isPacketMode ? "Show bytes" : "Show packets";

  primaryLabel.textContent = isPacketMode ? "Packets per second" : "Bytes per second";
  primaryValue.textContent = isPacketMode
    ? `${formatNumber(stats.packets_per_second)} packets/s`
    : `${formatNumber(stats.bytes_per_second)} B/s`;
  rateValue.textContent = isOnline
    ? isPacketMode
      ? `${formatNumber(stats.total_packets)} total packets`
      : `${formatNumber(stats.total_bytes)} total bytes`
    : "Waiting for backend data";

  Object.entries(packetNodes).forEach(([key, node]) => {
    node.textContent = formatNumber(stats[key]);
  });
}

function readPayload(payload) {
  Object.assign(stats, payload);
  render();
}

async function fetchStats() {
  try {
    const response = await fetch(apiUrl, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    readPayload(await response.json());
  } catch {
    stats.status = "offline";
    render();
  }
}

window.addEventListener("beforeunload", () => {
  window.clearInterval(pollTimer);
});

modeButton.addEventListener("click", () => {
  mode = mode === "bytes" ? "packets" : "bytes";
  render();
});

render();
fetchStats();
pollTimer = window.setInterval(fetchStats, 1000);

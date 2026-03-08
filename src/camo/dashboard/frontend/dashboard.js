async function loadDiagnostic() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const profileId = urlParams.get('id') || 'default';
        const res = await fetch(`http://127.0.0.1:8000/dashboard-api/profile-info/${profileId}`);
        const data = await res.json();

        const content = document.getElementById('content');

        const buildCard = (title, items) => {
            let html = `<div class="bg-white rounded shadow p-4"><h2 class="font-bold text-lg mb-3 border-b">${title}</h2><ul class="text-sm space-y-1">`;
            for (const [k, v] of Object.entries(items)) {
                html += `<li><span class="text-gray-600 font-semibold">${k}:</span> ${v}</li>`;
            }
            html += `</ul></div>`;
            return html;
        };

        content.innerHTML =
            buildCard('🌐 Network Info', {
                'Public IP': data.ip,
                'Country': data.country,
                'Timezone': data.timezone,
                'WebRTC IP': data.webrtcIP
            }) +
            buildCard('🖥️ Browser Info', {
                'Browser Engine': data.browser,
                'User Agent': data.userAgent,
                'Platform': data.platform
            }) +
            buildCard('⚙️ Fingerprint Summary', {
                'CPU Cores': data.cpu,
                'RAM (GB)': data.ram,
                'GPU Vendor': data.gpuVendor,
                'GPU Renderer': data.gpuRenderer,
                'Screen': data.screen
            }) +
            buildCard('🎨 Rendering Hashes', {
                'Canvas Hash': data.canvasHash,
                'WebGL Hash': data.webglHash,
                'Audio Hash': data.audioHash
            });

    } catch (err) {
        console.error(err);
        document.getElementById('content').innerHTML = '<div class="text-red-500">Failed to load diagnostic data. Ensure the CAMO backend is running.</div>';
    }
}

window.onload = loadDiagnostic;

const API_URL = 'http://127.0.0.1:8000';

new Vue({
    el: '#app',
    data: {
        activeTab: 'profiles',
        modalTab: 'general',
        profiles: [],
        installedVersions: [],
        availableVersions: [],
        loadingVersions: false,
        showCreateModal: false,
        isEditing: false,
        editingId: null,
        form: {
            name: '',
            tagsInput: '',
            os: 'windows',
            camoufox_version: '',
            fingerprint: null,
            useProxy: false,
            proxy: {
                type: 'http',
                host: '',
                port: 8080,
                username: '',
                password: ''
            }
        },
        testingProxy: false,
        proxyTestResult: ''
    },
    mounted() {
        this.fetchProfiles();
        this.fetchInstalledVersions();
        setInterval(this.updateStatuses, 5000);
    },
    methods: {
        // --- PROFILES ---
        async fetchProfiles() {
            try {
                const res = await axios.get(`${API_URL}/api/profiles`);
                this.profiles = res.data.map(p => ({ ...p, running: false }));
                this.updateStatuses();
            } catch (err) {
                console.error(err);
            }
        },
        async updateStatuses() {
            for (let profile of this.profiles) {
                try {
                    const res = await axios.get(`${API_URL}/api/profiles/${profile.id}/status`);
                    this.$set(profile, 'running', res.data.running);
                } catch (err) {
                    console.error(err);
                }
            }
        },
        openCreateModal() {
            this.showCreateModal = true;
            this.isEditing = false;
            this.editingId = null;
            this.modalTab = 'general';
            this.resetForm();
            this.generateFingerprintPreview();
        },
        closeModal() {
            this.showCreateModal = false;
            this.isEditing = false;
            this.editingId = null;
            this.proxyTestResult = '';
            this.resetForm();
        },
        resetForm() {
            this.form = {
                name: '',
                tagsInput: '',
                os: 'windows',
                camoufox_version: '',
                fingerprint: null,
                useProxy: false,
                proxy: { type: 'http', host: '', port: 8080, username: '', password: '' }
            };
        },
        async saveProfile() {
            const tags = this.form.tagsInput.split(',').map(t => t.trim()).filter(t => t);
            const proxyConfig = this.form.useProxy ? { ...this.form.proxy } : null;

            const payload = {
                name: this.form.name || 'Unnamed Profile',
                tags: tags,
                proxy: proxyConfig,
                os: this.form.os,
                camoufox_version: this.form.camoufox_version || null,
                fingerprint: this.form.fingerprint
            };

            try {
                if (this.isEditing) {
                    await axios.put(`${API_URL}/api/profiles/${this.editingId}`, payload);
                } else {
                    await axios.post(`${API_URL}/api/profiles`, payload);
                }
                this.closeModal();
                this.fetchProfiles();
            } catch (err) {
                console.error(err);
                alert("Error saving profile");
            }
        },
        editProfile(profile) {
            this.isEditing = true;
            this.editingId = profile.id;
            this.modalTab = 'general';

            this.form.name = profile.name;
            this.form.tagsInput = profile.tags ? profile.tags.join(', ') : '';
            this.form.os = profile.os;
            this.form.camoufox_version = profile.camoufox_version || '';
            this.form.fingerprint = profile.fingerprint;

            if (profile.proxy) {
                this.form.useProxy = true;
                this.form.proxy = { ...profile.proxy };
            } else {
                this.form.useProxy = false;
            }
            this.showCreateModal = true;
        },
        async deleteProfile(id) {
            if (confirm("Are you sure you want to delete this profile? All data will be lost.")) {
                try {
                    await axios.delete(`${API_URL}/api/profiles/${id}`);
                    this.fetchProfiles();
                } catch (err) {
                    console.error(err);
                }
            }
        },
        async cloneProfile(id) {
            try {
                await axios.post(`${API_URL}/api/profiles/${id}/clone`);
                this.fetchProfiles();
            } catch (err) {
                console.error(err);
                alert("Failed to clone profile");
            }
        },
        async startProfile(id) {
            try {
                await axios.post(`${API_URL}/api/profiles/${id}/launch`);
                const p = this.profiles.find(x => x.id === id);
                if (p) p.running = true;
            } catch (err) {
                console.error(err);
                alert(err.response?.data?.detail || "Failed to start profile");
            }
        },
        async stopProfile(id) {
            try {
                await axios.post(`${API_URL}/api/profiles/${id}/stop`);
                const p = this.profiles.find(x => x.id === id);
                if (p) p.running = false;
            } catch (err) {
                console.error(err);
            }
        },

        // --- FINGERPRINT ---
        async generateFingerprintPreview() {
            try {
                const res = await axios.post(`${API_URL}/api/fingerprint/generate`, { os: this.form.os });
                this.$set(this.form, 'fingerprint', res.data);
            } catch (err) {
                console.error("Fingerprint generation failed", err);
            }
        },

        // --- PROXY ---
        async pasteProxy() {
            try {
                const text = await navigator.clipboard.readText();
                let str = text.trim();
                let type = 'http';
                if (str.includes('://')) {
                    const parts = str.split('://');
                    type = parts[0];
                    str = parts[1];
                }
                const parts = str.split(':');
                if (parts.length >= 2) {
                    this.form.proxy.type = type;
                    this.form.proxy.host = parts[0];
                    this.form.proxy.port = parseInt(parts[1], 10);
                    if (parts.length >= 4) {
                        this.form.proxy.username = parts[2];
                        this.form.proxy.password = parts[3];
                    }
                }
            } catch (err) {
                console.error('Failed to read clipboard contents: ', err);
            }
        },
        async testProxy() {
            this.testingProxy = true;
            this.proxyTestResult = '';
            try {
                const res = await axios.post(`${API_URL}/api/proxy/test`, this.form.proxy);
                this.proxyTestResult = res.data.success ? 'Success' : 'Failed';
            } catch (err) {
                this.proxyTestResult = 'Failed';
            } finally {
                this.testingProxy = false;
            }
        },

        // --- VERSIONS ---
        async fetchInstalledVersions() {
            try {
                const res = await axios.get(`${API_URL}/api/camoufox/versions/installed`);
                this.installedVersions = res.data;
            } catch (err) {
                console.error(err);
            }
        },
        async fetchAvailableVersions() {
            this.loadingVersions = true;
            try {
                const res = await axios.get(`${API_URL}/api/camoufox/versions/available`);
                this.availableVersions = res.data;
            } catch (err) {
                console.error(err);
            } finally {
                this.loadingVersions = false;
            }
        },
        isInstalled(version) {
            return this.installedVersions.some(v => v.version === version);
        },
        async installVersion(version) {
            if (!confirm(`Installing Camoufox ${version} will download several hundreds of MBs. Proceed?`)) return;
            try {
                alert("Installation started in background. Please check terminal/logs. This takes time.");
                await axios.post(`${API_URL}/api/camoufox/versions/install`, { version });
                this.fetchInstalledVersions();
                alert(`Version ${version} installed successfully!`);
            } catch (err) {
                console.error(err);
                alert("Installation failed");
            }
        },
        async setDefaultVersion(version) {
            try {
                await axios.post(`${API_URL}/api/camoufox/versions/set-active`, { version });
                this.fetchInstalledVersions();
            } catch (err) {
                console.error(err);
            }
        },
        async uninstallVersion(version) {
            if (!confirm(`Are you sure you want to uninstall version ${version}?`)) return;
            try {
                await axios.delete(`${API_URL}/api/camoufox/versions/${version}`);
                this.fetchInstalledVersions();
            } catch (err) {
                console.error(err);
            }
        }
    }
});

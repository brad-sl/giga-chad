// ============================================
// Agent Orchestrator Dashboard - JavaScript
// ============================================

// ==================== State & Data ====================

const appState = {
    activeSection: 'overview',
    approvals: [
        {
            id: 'PROP-001',
            agent: 'Google Ads Manager',
            type: 'Campaign Budget Increase',
            proposal: 'Increase daily budget for "Summer Sales" campaign from $50 to $75',
            created: new Date(Date.now() - 2 * 60 * 60 * 1000),
            status: 'pending'
        },
        {
            id: 'PROP-002',
            agent: 'Crypto Trading Bot',
            type: 'Trade Execution',
            proposal: 'Execute BUY signal for SHIB/USD (0.5 position size, limit order at $0.0082)',
            created: new Date(Date.now() - 15 * 60 * 1000),
            status: 'pending'
        },
        {
            id: 'PROP-003',
            agent: 'Google Ads Manager',
            type: 'Keyword Addition',
            proposal: 'Add 12 high-intent keywords to "Enterprise" ad group',
            created: new Date(Date.now() - 45 * 60 * 1000),
            status: 'pending'
        },
        {
            id: 'PROP-004',
            agent: 'Crypto Trading Bot',
            type: 'Trade Execution',
            proposal: 'Execute SELL signal for BTC/USD (take profit at $67,500)',
            created: new Date(Date.now() - 8 * 60 * 60 * 1000),
            status: 'approved'
        },
    ],
    runs: [
        {
            id: 'RUN-047',
            agent: 'Crypto Trading Bot',
            started: new Date(Date.now() - 15 * 60 * 1000),
            duration: 120,
            status: 'running',
            result: 'Executing sentiment analysis...'
        },
        {
            id: 'RUN-046',
            agent: 'Google Ads Manager',
            started: new Date(Date.now() - 2 * 60 * 60 * 1000),
            duration: 450,
            status: 'success',
            result: 'Analyzed 5 campaigns, generated 2 proposals'
        },
        {
            id: 'RUN-045',
            agent: 'Crypto Trading Bot',
            started: new Date(Date.now() - 2.5 * 60 * 60 * 1000),
            duration: 85,
            status: 'success',
            result: 'Executed 1 BUY trade (DOGE), portfolio +$234.50'
        },
        {
            id: 'RUN-044',
            agent: 'Google Ads Manager',
            started: new Date(Date.now() - 6 * 60 * 60 * 1000),
            duration: 520,
            status: 'success',
            result: 'Analyzed 5 campaigns, generated 3 proposals'
        },
        {
            id: 'RUN-043',
            agent: 'Crypto Trading Bot',
            started: new Date(Date.now() - 6.5 * 60 * 60 * 1000),
            duration: 95,
            status: 'failed',
            result: 'API rate limit exceeded - retry queued'
        },
        {
            id: 'RUN-042',
            agent: 'Google Ads Manager',
            started: new Date(Date.now() - 10 * 60 * 60 * 1000),
            duration: 480,
            status: 'success',
            result: 'Analyzed 5 campaigns, generated 1 proposal'
        },
    ],
    activityLog: [
        { time: new Date(Date.now() - 5 * 60 * 1000), type: 'success', icon: '✅', title: 'Sentiment Analysis Complete', message: 'Processed 245 posts from X API, signal strength: 72%' },
        { time: new Date(Date.now() - 8 * 60 * 1000), type: 'info', icon: '🔔', title: 'Approval Requested', message: 'Google Ads: Increase budget for Summer Sales campaign' },
        { time: new Date(Date.now() - 12 * 60 * 1000), type: 'success', icon: '✅', title: 'Trade Executed', message: 'BUY DOGE/USD @ $0.0342, position size: 0.5, P&L: +$234.50' },
        { time: new Date(Date.now() - 25 * 60 * 1000), type: 'error', icon: '❌', title: 'API Error', message: 'Crypto: Rate limit exceeded, backoff 30s then retry' },
        { time: new Date(Date.now() - 35 * 60 * 1000), type: 'info', icon: '🔔', title: 'Agent Started', message: 'Google Ads Manager spawned - analyzing 5 accounts' },
        { time: new Date(Date.now() - 1 * 60 * 60 * 1000), type: 'success', icon: '✅', title: 'Campaign Analysis', message: 'Completed analysis for 5 campaigns, ROI avg: +12%' },
    ]
};

// ==================== Chart Configuration ====================

let performanceChart = null;
let statusChart = null;

function initializeCharts() {
    // Performance Chart
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceChart) performanceChart.destroy();
    
    performanceChart = new Chart(performanceCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Google Ads Runs',
                    data: [5, 7, 8, 6, 9, 4, 3],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                },
                {
                    label: 'Crypto Bot Runs',
                    data: [8, 12, 15, 18, 14, 16, 12],
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 12, weight: '500' }
                    }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#cbd5e1' },
                    grid: { color: 'rgba(71, 85, 105, 0.3)' }
                },
                x: {
                    ticks: { color: '#cbd5e1' },
                    grid: { color: 'rgba(71, 85, 105, 0.3)' }
                }
            }
        }
    });

    // Status Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusChart) statusChart.destroy();
    
    statusChart = new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Success', 'Failed', 'Running', 'Pending'],
            datasets: [{
                data: [44, 2, 1, 3],
                backgroundColor: [
                    '#10b981',
                    '#ef4444',
                    '#3b82f6',
                    '#f59e0b'
                ],
                borderColor: '#1e293b',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 12, weight: '500' },
                        padding: 15
                    }
                }
            }
        }
    });
}

// ==================== Utility Functions ====================

function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
}

function formatDuration(seconds) {
    if (seconds < 60) return `${seconds}s`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
    return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}

function updateTime() {
    const now = new Date();
    document.getElementById('timeDisplay').textContent = formatTime(now);
}

// ==================== Section Navigation ====================

function navigateToSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Mark nav link as active
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

    // Initialize charts if we're on overview
    if (sectionId === 'overview') {
        setTimeout(() => initializeCharts(), 100);
    }

    appState.activeSection = sectionId;
}

// ==================== Approval Queue ====================

function renderApprovals() {
    const tableBody = document.getElementById('approvalTableBody');
    const filterText = document.getElementById('filterInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;

    const filtered = appState.approvals.filter(approval => {
        const matchText = approval.agent.toLowerCase().includes(filterText) ||
                         approval.type.toLowerCase().includes(filterText) ||
                         approval.proposal.toLowerCase().includes(filterText);
        const matchStatus = !statusFilter || approval.status === statusFilter;
        return matchText && matchStatus;
    });

    tableBody.innerHTML = filtered.map(approval => `
        <tr>
            <td>${approval.id}</td>
            <td>${approval.agent}</td>
            <td>${approval.type}</td>
            <td style="max-width: 250px; white-space: normal;">${approval.proposal.substring(0, 50)}...</td>
            <td>${getTimeAgo(approval.created)}</td>
            <td>
                <span class="status-badge-small status-${approval.status}">
                    ${approval.status.charAt(0).toUpperCase() + approval.status.slice(1)}
                </span>
            </td>
            <td>
                ${approval.status === 'pending' ? `
                    <div class="btn-action">
                        <button class="btn btn-success btn-sm" onclick="approveProposal('${approval.id}')">Approve</button>
                        <button class="btn btn-danger btn-sm" onclick="rejectProposal('${approval.id}')">Reject</button>
                    </div>
                ` : '-'}
            </td>
        </tr>
    `).join('');
}

function approveProposal(proposalId) {
    const approval = appState.approvals.find(a => a.id === proposalId);
    if (approval) {
        approval.status = 'approved';
        addActivity('success', '✅', 'Proposal Approved', `${approval.agent}: ${approval.type} approved and queued for execution`);
        renderApprovals();
    }
}

function rejectProposal(proposalId) {
    const approval = appState.approvals.find(a => a.id === proposalId);
    if (approval) {
        approval.status = 'rejected';
        addActivity('error', '❌', 'Proposal Rejected', `${approval.agent}: ${approval.type} rejected`);
        renderApprovals();
    }
}

// ==================== Run History ====================

function renderRunHistory() {
    const tableBody = document.getElementById('historyTableBody');
    const filterText = document.getElementById('historyFilterInput').value.toLowerCase();
    const statusFilter = document.getElementById('historyStatusFilter').value;

    const filtered = appState.runs.filter(run => {
        const matchText = run.agent.toLowerCase().includes(filterText) ||
                         run.result.toLowerCase().includes(filterText);
        const matchStatus = !statusFilter || run.status === statusFilter;
        return matchText && matchStatus;
    });

    tableBody.innerHTML = filtered.map(run => `
        <tr>
            <td>${run.id}</td>
            <td>${run.agent}</td>
            <td>${formatDate(run.started)}</td>
            <td>${formatDuration(run.duration)}</td>
            <td>
                <span class="status-badge-small status-${run.status}">
                    ${run.status.charAt(0).toUpperCase() + run.status.slice(1)}
                </span>
            </td>
            <td>${run.result}</td>
            <td>
                <button class="btn btn-secondary btn-sm" onclick="showRunDetails('${run.id}')">Details</button>
            </td>
        </tr>
    `).join('');
}

function showRunDetails(runId) {
    const run = appState.runs.find(r => r.id === runId);
    if (!run) return;

    const modal = document.getElementById('detailsModal');
    document.getElementById('modalTitle').textContent = `Run Details: ${run.id}`;

    const logsExample = `[2026-03-04T20:15:23] Agent spawned with task
[2026-03-04T20:15:25] Connected to API
[2026-03-04T20:15:28] Fetching data...
[2026-03-04T20:16:30] Processing results
[2026-03-04T20:16:35] Generated output
[2026-03-04T20:16:37] Agent completed successfully`;

    document.getElementById('modalBody').innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Run ID:</span>
            <span class="detail-value">${run.id}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Agent:</span>
            <span class="detail-value">${run.agent}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Status:</span>
            <span class="detail-value">
                <span class="status-badge-small status-${run.status}">
                    ${run.status.charAt(0).toUpperCase() + run.status.slice(1)}
                </span>
            </span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Started:</span>
            <span class="detail-value">${formatDate(run.started)}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Duration:</span>
            <span class="detail-value">${formatDuration(run.duration)}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Result:</span>
            <span class="detail-value">${run.result}</span>
        </div>
        <div style="margin-top: 1rem;">
            <h4 style="margin-bottom: 0.5rem;">Logs:</h4>
            <div class="code-block">${logsExample}</div>
        </div>
    `;

    modal.classList.add('active');
}

// ==================== Activity Feed ====================

function renderActivityFeed() {
    const feed = document.getElementById('activityFeed');
    const filter = document.getElementById('activityFilter').value;

    const filtered = filter ? appState.activityLog.filter(a => {
        const typeMap = {
            'agent': ['success', 'info'],
            'approval': ['info'],
            'error': ['error']
        };
        return typeMap[filter] && typeMap[filter].includes(a.type);
    }) : appState.activityLog;

    feed.innerHTML = filtered.map(activity => `
        <div class="activity-item ${activity.type}">
            <div class="activity-icon">${activity.icon}</div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-message">${activity.message}</div>
                <div class="activity-time">${formatTime(activity.time)}</div>
            </div>
        </div>
    `).join('');
}

function addActivity(type, icon, title, message) {
    appState.activityLog.unshift({
        time: new Date(),
        type,
        icon,
        title,
        message
    });

    if (appState.activityLog.length > 50) {
        appState.activityLog.pop();
    }

    if (appState.activeSection === 'activity') {
        renderActivityFeed();
    }
}

// ==================== Modal Management ====================

function setupModalHandlers() {
    const modal = document.getElementById('detailsModal');
    const closeBtn = document.querySelector('.modal-close');

    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
}

// ==================== Event Listeners ====================

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateToSection(link.dataset.section);
        });
    });

    // Approval Queue Filters
    document.getElementById('filterInput').addEventListener('input', renderApprovals);
    document.getElementById('statusFilter').addEventListener('change', renderApprovals);

    // Run History Filters
    document.getElementById('historyFilterInput').addEventListener('input', renderRunHistory);
    document.getElementById('historyStatusFilter').addEventListener('change', renderRunHistory);

    // Activity Filter
    document.getElementById('activityFilter').addEventListener('change', renderActivityFeed);

    // Clear Activity Button
    document.getElementById('clearActivityBtn').addEventListener('click', () => {
        appState.activityLog = [];
        renderActivityFeed();
    });

    // Button handlers
    document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.textContent.includes('Trigger Run')) {
                const agentName = this.closest('.agent-detail-card')?.querySelector('h3').textContent;
                addActivity('info', '🚀', 'Agent Triggered', `${agentName} has been triggered and is starting...`);
            }
        });
    });
}

// ==================== Initialize ====================

function initialize() {
    // Set up event listeners
    setupEventListeners();
    setupModalHandlers();

    // Initial render
    renderApprovals();
    renderRunHistory();
    renderActivityFeed();
    initializeCharts();

    // Update time every second
    updateTime();
    setInterval(updateTime, 1000);

    // Add some simulated real-time activity
    setInterval(() => {
        const activities = [
            { type: 'success', icon: '✅', title: 'Sentiment Check Complete', message: 'X API data processed, SHIB signal: STRONG BUY' },
            { type: 'info', icon: '🔔', title: 'Campaign Pending Review', message: 'Google Ads: New optimization proposal ready for approval' },
            { type: 'success', icon: '💰', title: 'Trade Executed', message: 'DOGE/USD BUY @ $0.0345, position +$156.23' },
        ];
        
        if (Math.random() > 0.7) {
            const activity = activities[Math.floor(Math.random() * activities.length)];
            addActivity(activity.type, activity.icon, activity.title, activity.message);
        }
    }, 15000);
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}

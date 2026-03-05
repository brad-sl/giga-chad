# Agent Orchestrator Dashboard

A responsive, real-time dashboard UI for managing multi-agent orchestration platform. Built with vanilla HTML5, CSS3, and JavaScript (no build step required).

## Features

### 📊 Overview Dashboard
- **Metrics Cards**: Quick glance at system health
  - Active Agents (currently running)
  - Pending Approvals (awaiting human review)
  - Total Runs (this month)
  - Success Rate (last 30 days)

- **Performance Charts**
  - Line chart: Agent performance trends (last 7 days)
  - Doughnut chart: Run status distribution

- **Agent Status Panel**
  - Real-time status for each agent
  - Last run time, daily run count
  - Success rates and API quota usage

### ✋ Approval Queue
- Table view of pending proposals
- Filter by agent, type, or status
- **Actions**: Approve or Reject with single click
- Status badges: Pending, Approved, Rejected

### 📜 Run History
- Complete log of all agent executions
- Filter by agent or run status
- Click "Details" to see full logs and execution timeline
- Status indicators: Success, Failed, Running

### 🎯 Agent Management
- Detailed cards for each agent
- Status, uptime, API quota tracking
- Quick actions: Trigger Run, View Logs
- Next scheduled run information

### ⚡ Live Activity Feed
- Real-time updates as agents execute
- Color-coded by activity type (success, error, info)
- Filter by activity category
- Automatic scroll with newest items on top

## Getting Started

### No Installation Required
The dashboard is fully client-side. Just open `index.html` in a modern browser:

```bash
# macOS/Linux
open index.html

# Windows
start index.html

# Or use any web server
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## File Structure

```
dashboard/
├── index.html        # Main HTML structure
├── styles.css        # Responsive styling (dark theme)
├── app.js           # JavaScript logic & interactivity
├── assets/          # Images, icons, fonts (for future use)
│   ├── icons/
│   └── fonts/
└── README.md        # This file
```

## Architecture

### HTML (`index.html`)
- Semantic layout: Header, Sidebar, Main Content
- 5 main sections (Overview, Approval Queue, Run History, Agents, Live Activity)
- Modal dialog for detailed views
- Mobile-first responsive structure

### CSS (`styles.css`)
- CSS Variables for theming (colors, spacing, animations)
- Dark theme (professional, low-eye-strain)
- CSS Grid for layout
- Flexbox for components
- Media queries: Desktop (1024px+), Tablet (768px+), Mobile (<480px)
- Smooth transitions and animations

### JavaScript (`app.js`)
- Mock data: 3 proposals, 6 run history records, activity log
- Chart.js integration for metrics visualization
- Interactive filtering and search
- Section navigation
- Real-time updates (simulated every 15 seconds)
- Modal dialog management
- Responsive time display

## Data Structures

### Approvals
```javascript
{
  id: 'PROP-001',
  agent: 'Google Ads Manager',
  type: 'Campaign Budget Increase',
  proposal: 'Increase daily budget from $50 to $75',
  created: Date,
  status: 'pending' | 'approved' | 'rejected'
}
```

### Runs
```javascript
{
  id: 'RUN-047',
  agent: 'Crypto Trading Bot',
  started: Date,
  duration: 120,  // seconds
  status: 'running' | 'success' | 'failed',
  result: 'Execution summary text'
}
```

### Activities
```javascript
{
  time: Date,
  type: 'success' | 'error' | 'info',
  icon: '✅',
  title: 'Event Title',
  message: 'Detailed message'
}
```

## Customization

### Change Theme Colors
Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #6366f1;      /* Indigo */
    --success-color: #10b981;      /* Green */
    --error-color: #ef4444;        /* Red */
    --bg-primary: #0f172a;         /* Dark blue */
    /* ... more colors ... */
}
```

### Add More Agents
Update `appState.activityLog` in `app.js` and add agent cards in the "Agents" section.

### Connect to Real API
Replace mock data with actual WebSocket/API calls:

```javascript
// Instead of:
const approval = appState.approvals.find(...);

// Use:
const response = await fetch('/api/approvals/1');
const approval = await response.json();
```

## Responsive Design

### Desktop (1024px+)
- 2-column grid (sidebar + main content)
- Multi-column metric cards
- Full-width charts

### Tablet (768px+)
- Sidebar becomes horizontal nav bar
- Single-column charts
- Stacked metrics

### Mobile (<480px)
- Single column layout
- Vertical navigation
- Simplified cards
- Touch-friendly buttons

## Integration Points

### WebSocket for Live Updates
```javascript
const ws = new WebSocket('ws://api.example.com/events');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    addActivity(data.type, data.icon, data.title, data.message);
    renderActivityFeed();
};
```

### REST API for Data Fetch
```javascript
async function loadApprovals() {
    const res = await fetch('/api/approvals?status=pending');
    appState.approvals = await res.json();
    renderApprovals();
}
```

### Chart.js Data Binding
Charts automatically update when you modify the data and call:
```javascript
performanceChart.data.datasets[0].data = newData;
performanceChart.update();
```

## Performance Notes

- **No Build Step**: Loads Chart.js from CDN, all assets are local
- **Lightweight**: ~50KB total (HTML + CSS + JS)
- **Fast Rendering**: CSS Grid + Flexbox for layout calculations
- **Efficient Filtering**: Client-side, no server calls needed for search
- **Responsive Charts**: Chart.js handles scaling automatically

## Browser DevTools Tips

### Debug Filtering
Open console and try:
```javascript
// Filter approvals
appState.approvals = appState.approvals.filter(a => a.status === 'pending');
renderApprovals();

// Add test activity
addActivity('success', '✅', 'Test', 'This is a test activity');
renderActivityFeed();
```

### Update Mock Data
```javascript
// Add a new approval
appState.approvals.push({
    id: 'PROP-099',
    agent: 'New Agent',
    type: 'Test Action',
    proposal: 'This is a test proposal',
    created: new Date(),
    status: 'pending'
});
renderApprovals();
```

## Accessibility Features

- Semantic HTML5 elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Color contrast meets WCAG AA standards
- Responsive text sizing

## Future Enhancements

1. **Dark/Light Theme Toggle**
   - Add theme switcher in header
   - localStorage to persist preference

2. **Real-time Sync**
   - WebSocket connection to backend
   - Auto-refresh on new data

3. **PDF Export**
   - Generate reports from visible data
   - Use jsPDF or similar library

4. **User Preferences**
   - Customizable dashboard widgets
   - Saved filters

5. **Advanced Analytics**
   - More detailed charts (Stochastic RSI, portfolio performance)
   - Trend analysis over time

6. **Notifications**
   - Browser notifications for critical alerts
   - Sound alerts for high-priority events

## Security Considerations

- **No sensitive data stored in HTML/CSS/JS**
- Credentials must be passed from backend only
- WebSocket connections should use WSS (secure)
- API calls should include auth headers
- Sanitize any user input before rendering

## Troubleshooting

### Charts Not Rendering
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify `initializeCharts()` is called

### Filters Not Working
- Check that filter elements have correct IDs
- Ensure `renderApprovals()` is called after filter change
- Verify data structure matches expectations

### Modal Not Appearing
- Check that modal element has `id="detailsModal"`
- Verify `modal.classList.add('active')` is called
- Check CSS for `.modal.active` display rules

## License

Part of the Agent Orchestrator Project (https://github.com/brad-sl/giga-chad)

## Support

For issues or questions about the dashboard, file an issue on GitHub or contact the development team.

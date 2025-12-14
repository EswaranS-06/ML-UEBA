import { InputSection } from './sections/input.js';
import { PipelineSection } from './sections/pipeline.js';
import { OutputSection } from './sections/output.js';
import { DatabaseSection } from './sections/database.js';
import { RunSection } from './sections/run.js';
import { LogsSection } from './sections/logs.js';
import { AgenticSection } from './sections/agent.js?v=final';

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();

    // Initialize Modules
    new InputSection();
    new PipelineSection();
    new OutputSection();
    new DatabaseSection();
    new RunSection();
    new LogsSection();
    new AgenticSection();
});

/* Navigation Logic */
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.panel');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));

            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Sidebar Collapse Logic
    const sidebar = document.querySelector('.sidebar');
    const header = document.querySelector('.sidebar-header');

    if (header && sidebar) {
        header.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            document.body.classList.toggle('sidebar-closed'); // Add global state class
        });
    }
}

// Global Logger (exposed for modules)
window.logAction = function (message) {
    const logContainer = document.getElementById('log-output');
    if (!logContainer) return;

    const div = document.createElement('div');
    div.className = 'log-line info';

    const now = new Date();
    const ts = `[${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}]`;

    div.innerHTML = `<span class="ts">${ts}</span> ${message}`;
    logContainer.appendChild(div);
    logContainer.scrollTop = logContainer.scrollHeight;
}

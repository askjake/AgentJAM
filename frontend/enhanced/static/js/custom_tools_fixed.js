// STATE MANAGEMENT
// ============================================================================

const CustomToolsState = {
    tools: [],
    currentTool: null,
    viewMode: 'grid', // 'grid' or 'list'
    currentCreationMethod: 'ai', // 'ai', 'code', or 'template'
    isLoading: false,
    generatedCode: ''
};

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize Custom Tools Management
 */
function initCustomTools() {
    console.log('Initializing Custom Tools Management...');
    
    // Load tools
    loadCustomTools();
    
    // Setup event listeners
    setupCustomToolsEventListeners();
    
    // Setup intervals
    setInterval(loadCustomTools, 30000); // Refresh every 30 seconds
}

/**
 * Setup all event listeners
 */
function setupCustomToolsEventListeners() {
    // Create tool button
    const createBtn = document.getElementById('create-tool-btn');
    if (createBtn) {
        createBtn.addEventListener('click', () => openCreateToolModal());
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refresh-tools-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => loadCustomTools());
    }
    
    // View toggle buttons
    document.querySelectorAll('.view-toggle').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const view = e.currentTarget.dataset.view;
            switchViewMode(view);
        });
    });
    
    // Search input
    const searchInput = document.getElementById('tools-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterTools(e.target.value);
        });
    }
    
    // Creation method tabs
    document.querySelectorAll('.creation-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            switchCreationMethod(e.currentTarget.dataset.method);
        });
    });
    
    // AI Generation
    const generateBtn = document.getElementById('generate-tool-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateToolWithAI);
    }
    
    // Save generated tool
    const saveGeneratedBtn = document.getElementById('save-generated-tool');
    if (saveGeneratedBtn) {
        saveGeneratedBtn.addEventListener('click', saveGeneratedTool);
    }
    
    // Regenerate tool
    const regenerateBtn = document.getElementById('regenerate-tool');
    if (regenerateBtn) {
        regenerateBtn.addEventListener('click', generateToolWithAI);
    }
    
    // Code editor save
    const saveCodeBtn = document.getElementById('save-code-tool');
    if (saveCodeBtn) {
        saveCodeBtn.addEventListener('click', saveCodeTool);
    }
    
    // Validate code
    const validateBtn = document.getElementById('validate-code-btn');
    if (validateBtn) {
        validateBtn.addEventListener('click', validateToolCode);
    }
    
    // Template selection
    document.querySelectorAll('.select-template-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const template = e.currentTarget.closest('.template-card').dataset.template;
            loadTemplate(template);
        });
    });
    
    // Tool details modal actions
    const saveChangesBtn = document.getElementById('save-tool-changes');
    if (saveChangesBtn) {
        saveChangesBtn.addEventListener('click', saveToolChanges);
    }
    
    const toggleStatusBtn = document.getElementById('toggle-tool-status');
    if (toggleStatusBtn) {
        toggleStatusBtn.addEventListener('click', toggleToolStatus);
    }
    
    const deleteBtn = document.getElementById('delete-tool-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', deleteTool);
    }
    
    const runTestBtn = document.getElementById('run-test-btn');
    if (runTestBtn) {
        runTestBtn.addEventListener('click', runToolTest);
    }
}

// ============================================================================
// TOOL LOADING & DISPLAY
// ============================================================================

/**
 * Load all custom tools from backend
 */
async function loadCustomTools() {
    if (CustomToolsState.isLoading) return;
    
    CustomToolsState.isLoading = true;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        CustomToolsState.tools = data.tools || [];
        
        console.log(`Loaded ${CustomToolsState.tools.length} custom tools`);
        
        // Update UI
        updateToolsStats();
        renderToolsGrid();
        
    } catch (error) {
        console.error('Error loading custom tools:', error);
        showNotification('Failed to load custom tools: ' + error.message, 'error');
    } finally {
        CustomToolsState.isLoading = false;
    }
}

/**
 * Update statistics display
 */
function updateToolsStats() {
    const total = CustomToolsState.tools.length;
    const active = CustomToolsState.tools.filter(t => t.active).length;
    const inactive = total - active;
    
    const totalEl = document.getElementById('total-tools-count');
    const activeEl = document.getElementById('active-tools-count');
    const inactiveEl = document.getElementById('inactive-tools-count');
    
    if (totalEl) totalEl.textContent = total;
    if (activeEl) activeEl.textContent = active;
    if (inactiveEl) inactiveEl.textContent = inactive;
}

/**
 * Render tools in grid or list view
 */
function renderToolsGrid() {
    const container = document.getElementById('custom-tools-container');
    if (!container) return;
    
    // Clear container
    container.innerHTML = '';
    
    // Set view mode class
    container.className = CustomToolsState.viewMode === 'grid' ? 
        'custom-tools-grid' : 'custom-tools-list';
    
    // Check if empty
    if (CustomToolsState.tools.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-tools"></i>
                <h4>No Custom Tools Yet</h4>
                <p>Create your first custom tool to get started</p>
                <button class="btn-primary" onclick="document.getElementById('create-tool-btn').click()">
                    <i class="fas fa-plus-circle"></i> Create Tool
                </button>
            </div>
        `;
        return;
    }
    
    // Render tools
    CustomToolsState.tools.forEach(tool => {
        const card = createToolCard(tool);
        container.appendChild(card);
    });
}

/**
 * Create a tool card element
 */
function createToolCard(tool) {
    const card = document.createElement('div');
    card.className = 'tool-card';
    card.dataset.toolName = tool.name;
    
    const statusClass = tool.active ? 'active' : 'inactive';
    const statusText = tool.active ? 'Active' : 'Inactive';
    const icon = getToolIcon(tool.category || 'custom');
    
    // Format modified date
    const modifiedDate = tool.modified ? 
        new Date(tool.modified).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }) : 'Unknown';
    
    card.innerHTML = `
        <div class="tool-card-header">
            <div class="tool-icon">
                <i class="fas ${icon}"></i>
            </div>
            <span class="tool-status-badge ${statusClass}">${statusText}</span>
        </div>
        <div class="tool-card-body">
            <h4>${tool.name}</h4>
            <p>${tool.description || 'No description provided'}</p>
            <div class="tool-meta">
                <span><i class="fas fa-clock"></i> ${modifiedDate}</span>
                <span><i class="fas fa-code"></i> ${tool.functions ? tool.functions.length : 0} functions</span>
            </div>
            <div class="tool-card-actions">
                <button class="tool-action-btn primary" onclick="openToolDetails('${tool.name}')">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="tool-action-btn" onclick="quickTestTool('${tool.name}')">
                    <i class="fas fa-vial"></i> Test
                </button>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Get appropriate icon for tool category
 */
function getToolIcon(category) {
    const icons = {
        'api': 'fa-plug',
        'data': 'fa-database',
        'file': 'fa-file-alt',
        'command': 'fa-terminal',
        'web': 'fa-globe',
        'webhook': 'fa-broadcast-tower',
        'custom': 'fa-wrench'
    };
    
    return icons[category] || icons['custom'];
}

/**
 * Switch between grid and list view
 */
function switchViewMode(mode) {
    CustomToolsState.viewMode = mode;
    
    // Update button states
    document.querySelectorAll('.view-toggle').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === mode);
    });
    
    // Re-render
    renderToolsGrid();
}

/**
 * Filter tools by search term
 */
function filterTools(searchTerm) {
    const term = searchTerm.toLowerCase();
    
    document.querySelectorAll('.tool-card').forEach(card => {
        const toolName = card.dataset.toolName.toLowerCase();
        const description = card.querySelector('.tool-card-body p').textContent.toLowerCase();
        
        const matches = toolName.includes(term) || description.includes(term);
        card.style.display = matches ? 'block' : 'none';
    });
}

// ============================================================================
// MODAL MANAGEMENT
// ============================================================================

/**
 * Open create tool modal
 */
function openCreateToolModal() {
    const modal = document.getElementById('create-tool-modal');
    if (modal) {
        modal.style.display = 'flex';
        
        // Reset form
        document.getElementById('ai-tool-name').value = '';
        document.getElementById('ai-tool-description').value = '';
        document.getElementById('ai-generated-preview').style.display = 'none';
        
        // Switch to AI tab
        switchCreationMethod('ai');
    }
}

/**
 * Switch creation method
 */
function switchCreationMethod(method) {
    CustomToolsState.currentCreationMethod = method;
    
    // Update tabs
    document.querySelectorAll('.creation-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.method === method);
    });
    
    // Show/hide panels
    document.querySelectorAll('.creation-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    document.getElementById(`${method}-creation-panel`).classList.add('active');
}

/**
 * Close modal
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// ============================================================================
// AI TOOL GENERATION
// ============================================================================

/**
 * Generate tool using AI
 */
async function generateToolWithAI() {
    const name = document.getElementById('ai-tool-name').value.trim();
    const description = document.getElementById('ai-tool-description').value.trim();
    const category = document.getElementById('ai-tool-category').value;
    
    if (!name || !description) {
        showNotification('Please provide both name and description', 'error');
        return;
    }
    
    // Validate name format
    if (!/^[a-z_][a-z0-9_]*$/.test(name)) {
        showNotification('Tool name must start with lowercase letter or underscore, and contain only lowercase letters, numbers, and underscores', 'error');
        return;
    }
    
    const generateBtn = document.getElementById('generate-tool-btn');
    const originalText = generateBtn.innerHTML;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    generateBtn.disabled = true;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description, category })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP ${response.status}`);
        }
        
        const data = await response.json();
        CustomToolsState.generatedCode = data.code;
        
        // Show preview
        document.getElementById('ai-generated-code').textContent = data.code;
        document.getElementById('ai-generated-preview').style.display = 'block';
        
        showNotification('Tool generated successfully!', 'success');
        
    } catch (error) {
        console.error('Error generating tool:', error);
        showNotification('Failed to generate tool: ' + error.message, 'error');
    } finally {
        generateBtn.innerHTML = originalText;
        generateBtn.disabled = false;
    }
}

/**
 * Save AI-generated tool
 */
async function saveGeneratedTool() {
    const name = document.getElementById('ai-tool-name').value.trim();
    const description = document.getElementById('ai-tool-description').value.trim();
    const category = document.getElementById('ai-tool-category').value;
    const code = CustomToolsState.generatedCode;
    
    if (!code) {
        showNotification('No generated code to save', 'error');
        return;
    }
    
    await createToolWithCode(name, code, description, category);
}

// ============================================================================
// CODE EDITOR TOOLS
// ============================================================================

/**
 * Validate tool code syntax
 */
async function validateToolCode() {
    const code = document.getElementById('code-tool-code').value.trim();
    
    if (!code) {
        showNotification('Please enter some code first', 'error');
        return;
    }
    
    const validateBtn = document.getElementById('validate-code-btn');
    const originalText = validateBtn.innerHTML;
    validateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validating...';
    validateBtn.disabled = true;
    
    try {
        // Try to create with dummy name to validate syntax
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: '__temp_validation__',
                code: code,
                description: 'Validation test'
            })
        });
        
        if (response.status === 400) {
            const error = await response.json();
            throw new Error(error.error);
        }
        
        showNotification('✓ Code syntax is valid', 'success');
        
    } catch (error) {
        showNotification('Syntax error: ' + error.message, 'error');
    } finally {
        validateBtn.innerHTML = originalText;
        validateBtn.disabled = false;
    }
}

/**
 * Save tool from code editor
 */
async function saveCodeTool() {
    const name = document.getElementById('code-tool-name').value.trim();
    const code = document.getElementById('code-tool-code').value.trim();
    const description = document.getElementById('code-tool-description').value.trim();
    const category = document.getElementById('code-tool-category').value;
    
    if (!name || !code) {
        showNotification('Please provide both name and code', 'error');
        return;
    }
    
    // Validate name
    if (!/^[a-z_][a-z0-9_]*$/.test(name)) {
        showNotification('Tool name must start with lowercase letter or underscore', 'error');
        return;
    }
    
    await createToolWithCode(name, code, description, category);
}

/**
 * Create a tool with provided code
 */
async function createToolWithCode(name, code, description, category) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, code, description, category })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP ${response.status}`);
        }
        
        showNotification(`Tool "${name}" created successfully!`, 'success');
        closeModal('create-tool-modal');
        loadCustomTools();
        
    } catch (error) {
        console.error('Error creating tool:', error);
        showNotification('Failed to create tool: ' + error.message, 'error');
    }
}

// ============================================================================
// TEMPLATE MANAGEMENT
// ============================================================================

/**
 * Load a template
 */
function loadTemplate(templateName) {
    const templates = {
        'api': `from typing import Dict, Any
import requests

def api_call_tool(url: str, method: str = 'GET', headers: Dict = None, data: Dict = None) -> Dict[str, Any]:
    """
    Make HTTP API calls to external services.
    
    Args:
        url: API endpoint URL
        method: HTTP method (GET, POST, PUT, DELETE)
        headers: Optional headers dictionary
        data: Optional request body
    
    Returns:
        Dictionary with status and response data
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers or {},
            json=data
        )
        
        return {
            'status': 'success',
            'status_code': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }`,
        
        'data': `from typing import Dict, Any, List
import json

def data_transformer(data: Any, transform_type: str = 'json_to_dict') -> Dict[str, Any]:
    """
    Transform data between different formats.
    
    Args:
        data: Input data to transform
        transform_type: Type of transformation (json_to_dict, dict_to_json, flatten, etc.)
    
    Returns:
        Dictionary with transformed data
    """
    try:
        if transform_type == 'json_to_dict':
            result = json.loads(data) if isinstance(data, str) else data
        elif transform_type == 'dict_to_json':
            result = json.dumps(data, indent=2)
        elif transform_type == 'flatten':
            result = _flatten_dict(data)
        else:
            result = data
        
        return {
            'status': 'success',
            'result': result
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def _flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)`,
        
        'file': `from typing import Dict, Any
import os

def file_parser(file_path: str, operation: str = 'read') -> Dict[str, Any]:
    """
    Parse and process different file types.
    
    Args:
        file_path: Path to file
        operation: Operation to perform (read, size, exists, lines)
    
    Returns:
        Dictionary with file data or operation result
    """
    try:
        if operation == 'read':
            with open(file_path, 'r') as f:
                content = f.read()
            return {'status': 'success', 'content': content}
        
        elif operation == 'size':
            size = os.path.getsize(file_path)
            return {'status': 'success', 'size_bytes': size}
        
        elif operation == 'exists':
            exists = os.path.exists(file_path)
            return {'status': 'success', 'exists': exists}
        
        elif operation == 'lines':
            with open(file_path, 'r') as f:
                lines = f.readlines()
            return {'status': 'success', 'line_count': len(lines), 'lines': lines}
        
        else:
            return {'status': 'error', 'error': f'Unknown operation: {operation}'}
            
    except Exception as e:
        return {'status': 'error', 'error': str(e)}`,
        
        'command': `from typing import Dict, Any
import subprocess

def command_runner(command: str, timeout: int = 30, shell: bool = True) -> Dict[str, Any]:
    """
    Execute system commands safely.
    
    Args:
        command: Command to execute
        timeout: Maximum execution time in seconds
        shell: Whether to use shell
    
    Returns:
        Dictionary with command output
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            'status': 'success',
            'return_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {'status': 'error', 'error': 'Command timed out'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}`,
        
        'webhook': `from typing import Dict, Any
import json

def webhook_handler(payload: Dict[str, Any], event_type: str = 'generic') -> Dict[str, Any]:
    """
    Process incoming webhook events.
    
    Args:
        payload: Webhook payload data
        event_type: Type of event (generic, github, gitlab, etc.)
    
    Returns:
        Dictionary with processed event data
    """
    try:
        if event_type == 'github':
            return _process_github_event(payload)
        elif event_type == 'gitlab':
            return _process_gitlab_event(payload)
        else:
            return {
                'status': 'success',
                'event_type': event_type,
                'payload': payload
            }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def _process_github_event(payload):
    return {
        'status': 'success',
        'platform': 'github',
        'action': payload.get('action'),
        'repo': payload.get('repository', {}).get('full_name')
    }

def _process_gitlab_event(payload):
    return {
        'status': 'success',
        'platform': 'gitlab',
        'event_type': payload.get('event_type'),
        'project': payload.get('project', {}).get('path_with_namespace')
    }`,
        
        'scraper': `from typing import Dict, Any
import requests
from bs4 import BeautifulSoup

def web_scraper(url: str, selector: str = None, extract: str = 'text') -> Dict[str, Any]:
    """
    Extract data from web pages.
    
    Args:
        url: URL to scrape
        selector: CSS selector to find elements
        extract: What to extract (text, links, tables)
    
    Returns:
        Dictionary with scraped data
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if extract == 'text':
            if selector:
                elements = soup.select(selector)
                result = [elem.get_text(strip=True) for elem in elements]
            else:
                result = soup.get_text(strip=True)
        
        elif extract == 'links':
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            result = links
        
        elif extract == 'tables':
            tables = []
            for table in soup.find_all('table'):
                rows = []
                for tr in table.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                    rows.append(cells)
                tables.append(rows)
            result = tables
        
        else:
            result = str(soup)
        
        return {
            'status': 'success',
            'url': url,
            'data': result
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}`
    };
    
    const template = templates[templateName];
    if (template) {
        // Switch to code editor panel
        switchCreationMethod('code');
        
        // Populate code
        document.getElementById('code-tool-code').value = template;
        document.getElementById('code-tool-name').value = `${templateName}_tool`;
        document.getElementById('code-tool-category').value = templateName === 'scraper' ? 'web' : templateName;
        
        showNotification(`Loaded ${templateName} template`, 'success');
    }
}

// ============================================================================
// TOOL DETAILS & EDITING
// ============================================================================

/**
 * Open tool details modal
 */
async function openToolDetails(toolName) {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${toolName}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const tool = await response.json();
        CustomToolsState.currentTool = tool;
        
        // Populate modal
        document.getElementById('tool-details-title').innerHTML = `
            <i class="fas fa-tools"></i> ${tool.name}
        `;
        document.getElementById('detail-tool-name').textContent = tool.name;
        document.getElementById('detail-tool-modified').textContent = new Date(tool.modified).toLocaleString();
        document.getElementById('detail-tool-functions').textContent = tool.functions ? tool.functions.join(', ') : 'None';
        document.getElementById('detail-tool-description').textContent = tool.description || 'No description';
        
        // Status badge
        const statusBadge = document.getElementById('detail-tool-status').querySelector('.status-badge');
        statusBadge.className = `status-badge ${tool.active ? 'active' : 'inactive'}`;
        statusBadge.textContent = tool.active ? 'Active' : 'Inactive';
        
        // Toggle button text
        document.getElementById('toggle-status-text').textContent = tool.active ? 'Deactivate' : 'Activate';
        
        // Load code
        const codeResponse = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${toolName}`);
        const codeData = await codeResponse.json();
        
        // Read the actual file content
        document.getElementById('detail-tool-code').value = codeData.code || '';
        
        // Show modal
        document.getElementById('tool-details-modal').style.display = 'flex';
        
    } catch (error) {
        console.error('Error loading tool details:', error);
        showNotification('Failed to load tool details', 'error');
    }
}

/**
 * Save tool changes
 */
async function saveToolChanges() {
    const toolName = CustomToolsState.currentTool.name;
    const code = document.getElementById('detail-tool-code').value;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${toolName}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error);
        }
        
        showNotification('Tool updated successfully', 'success');
        loadCustomTools();
        
    } catch (error) {
        console.error('Error saving tool:', error);
        showNotification('Failed to save tool: ' + error.message, 'error');
    }
}

/**
 * Toggle tool activation status
 */
async function toggleToolStatus() {
    const tool = CustomToolsState.currentTool;
    const action = tool.active ? 'deactivate' : 'activate';
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${tool.name}/${action}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        showNotification(`Tool ${action}d successfully`, 'success');
        closeModal('tool-details-modal');
        loadCustomTools();
        
    } catch (error) {
        console.error(`Error ${action}ing tool:`, error);
        showNotification(`Failed to ${action} tool`, 'error');
    }
}

/**
 * Delete tool
 */
async function deleteTool() {
    const tool = CustomToolsState.currentTool;
    
    if (!confirm(`Are you sure you want to delete "${tool.name}"? This will move it to trash.`)) {
        return;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${tool.name}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        showNotification('Tool deleted successfully', 'success');
        closeModal('tool-details-modal');
        loadCustomTools();
        
    } catch (error) {
        console.error('Error deleting tool:', error);
        showNotification('Failed to delete tool', 'error');
    }
}

/**
 * Run tool test
 */
async function runToolTest() {
    const tool = CustomToolsState.currentTool;
    const paramsText = document.getElementById('test-params').value.trim();
    
    let params = {};
    if (paramsText) {
        try {
            params = JSON.parse(paramsText);
        } catch (e) {
            showNotification('Invalid JSON in test parameters', 'error');
            return;
        }
    }
    
    const runBtn = document.getElementById('run-test-btn');
    const originalText = runBtn.innerHTML;
    runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    runBtn.disabled = true;
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/custom-tools/${tool.name}/test`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ params })
        });
        
        const result = await response.json();
        
        // Show results
        document.getElementById('test-results').style.display = 'block';
        document.getElementById('test-output').textContent = JSON.stringify(result, null, 2);
        
    } catch (error) {
        document.getElementById('test-results').style.display = 'block';
        document.getElementById('test-output').textContent = `Error: ${error.message}`;
    } finally {
        runBtn.innerHTML = originalText;
        runBtn.disabled = false;
    }
}

/**
 * Quick test tool (from card)
 */
async function quickTestTool(toolName) {
    // Open tool details and switch to test tab
    await openToolDetails(toolName);
    // Could scroll to test section or highlight it
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Show notification (reuse existing notification system)
 */
function showNotification(message, type = 'info') {
    // Use existing notification system if available
    if (typeof showToast === 'function') {
        showToast(message, type);
    } else {
        console.log(`[${type.toUpperCase()}] ${message}`);
        alert(message);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCustomTools);
} else {
    initCustomTools();
}

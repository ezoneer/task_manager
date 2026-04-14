// КОНФИГ
const API_BASE = 'http://localhost:8080';

// СОСТОЯНИЕ
let tasks = [];
let isLoading = false;
let error = null;
let modal = { open: false, editingTask: null };
let isAuthenticated = localStorage.getItem('isAuth') === 'true';
let authMode = 'login';

const appEl = document.getElementById('app');

// API
const api = {
  async request(endpoint, options = {}) {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      credentials: 'include'
    });

    if (!res.ok) {
      if (res.status === 401) {
        isAuthenticated = false;
        localStorage.removeItem('isAuth');
      }
      const err = await res.text();
      throw new Error(`${res.status}: ${err}`);
    }

    const text = await res.text();
    return text ? JSON.parse(text) : null;
  },

  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include'
    });
    if (!res.ok) throw new Error('Login failed');
    isAuthenticated = true;
    localStorage.setItem('isAuth', 'true');
    return res.json();
  },

  async register(email, password) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
      credentials: 'include'
    });
    if (!res.ok) throw new Error('Register failed');
    return res.json();
  },

  async logout() {
    try {
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      });
    } catch (e) {}
    isAuthenticated = false;
    localStorage.removeItem('isAuth');
  },

  async getTasks() {
    return this.request('/tasks/all');
  },

  async createTask(task) {
    return this.request('/tasks/add', {
      method: 'POST',
      body: JSON.stringify(task)
    });
  },

  async updateTask(taskId, task) {
    return this.request(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(task)
    });
  },

  async deleteTask(taskId) {
    return this.request(`/tasks/delete/${taskId}`, {
      method: 'DELETE'
    });
  }
};

// АВТОРИЗАЦИЯ
async function handleLogin(email, password) {
  try {
    await api.login(email, password);
    render();
    loadTasks();
  } catch (e) {
    alert('Login failed: ' + e.message);
  }
}

async function handleRegister(email, password) {
  try {
    await api.register(email, password);
    alert('Registered! Now login');
    authMode = 'login';
    render();
  } catch (e) {
    alert('Register failed: ' + e.message);
  }
}

async function handleLogout() {
  await api.logout();
  tasks = [];
  render();
}

// ЗАГРУЗКА
async function loadTasks() {
  if (!isAuthenticated) return;

  isLoading = true;
  error = null;
  render();
  try {
    tasks = await api.getTasks();
  } catch (e) {
    error = e.message;
  } finally {
    isLoading = false;
    render();
  }
}

// ДЕЙСТВИЯ С ЗАДАЧАМИ
async function handleCreate(taskData) {
  try {
    await api.createTask({
      title: taskData.title,
      description: taskData.description || '',
      priority: taskData.priority
    });
    // Вместо пуша — просто перезагружаем все задачи
    await loadTasks();
  } catch (e) {
    alert('Failed: ' + e.message);
  }
}

async function handleUpdate(taskId, updates) {
  try {
    await api.updateTask(taskId, updates);
    await loadTasks(); // Перезагружаем вместо ручного map
  } catch (e) {
    alert('Failed: ' + e.message);
  }
}

async function handleDelete(taskId) {
  if (!confirm('Delete?')) return;
  try {
    await api.deleteTask(taskId);
    await loadTasks(); // Перезагружаем
  } catch (e) {
    alert('Failed: ' + e.message);
  }
}

async function handleToggle(task) {
  await handleUpdate(task.id, { is_completed: !task.is_completed });
}

// СОРТИРОВКА
function getSorted() {
  return [...tasks].sort((a, b) => {
    if (a.is_completed !== b.is_completed) return a.is_completed ? 1 : -1;
    const order = { high: 0, medium: 1, low: 2 };
    return order[a.priority] - order[b.priority];
  });
}

// МОДАЛКА ЗАДАЧ
function openModal(task = null) {
  modal = { open: true, editingTask: task };
  render();
}

function closeModal() {
  modal.open = false;
  render();
}

async function saveModal(formData) {
  if (modal.editingTask) {
    await handleUpdate(modal.editingTask.id, formData);
  } else {
    await handleCreate(formData);
  }
  closeModal();
}

// РЕНДЕР ФОРМЫ ЛОГИНА
function renderAuthForm() {
  const container = document.createElement('div');
  container.style.cssText = 'max-width:400px;margin:100px auto;';

  const box = document.createElement('div');
  box.className = 'tasks-container';

  const title = document.createElement('h3');
  title.style.cssText = 'color:white;margin-bottom:1.5rem;font-size:1.5rem';
  title.textContent = authMode === 'login' ? 'Login' : 'Register';

  const emailInput = document.createElement('input');
  emailInput.type = 'email';
  emailInput.placeholder = 'Email';
  emailInput.style.cssText = 'width:100%;padding:0.8rem;margin-bottom:1rem;border-radius:1rem;background:#1e293b;border:1px solid #334155;color:white';

  const passInput = document.createElement('input');
  passInput.type = 'password';
  passInput.placeholder = 'Password';
  passInput.style.cssText = 'width:100%;padding:0.8rem;margin-bottom:1rem;border-radius:1rem;background:#1e293b;border:1px solid #334155;color:white';

  const btn = document.createElement('button');
  btn.className = 'btn-primary';
  btn.style.width = '100%';
  btn.textContent = authMode === 'login' ? 'Login' : 'Register';

  const toggleText = document.createElement('p');
  toggleText.style.cssText = 'color:#94a3b8;text-align:center;margin-top:1rem;font-size:0.9rem';
  toggleText.innerHTML = authMode === 'login'
    ? 'No account? <span style="color:#6366f1;cursor:pointer">Register</span>'
    : 'Have account? <span style="color:#6366f1;cursor:pointer">Login</span>';

  btn.addEventListener('click', () => {
    const email = emailInput.value.trim();
    const pass = passInput.value;
    if (!email || !pass) {
      alert('Fill all fields');
      return;
    }
    if (authMode === 'login') {
      handleLogin(email, pass);
    } else {
      handleRegister(email, pass);
    }
  });

  toggleText.querySelector('span').addEventListener('click', () => {
    authMode = authMode === 'login' ? 'register' : 'login';
    render();
  });

  box.appendChild(title);
  box.appendChild(emailInput);
  box.appendChild(passInput);
  box.appendChild(btn);
  box.appendChild(toggleText);
  container.appendChild(box);

  return container;
}

// РЕНДЕР КАРТОЧКИ
function renderTaskCard(task) {
  const card = document.createElement('div');
  card.className = `task-card ${task.is_completed ? 'completed' : ''}`;

  const header = document.createElement('div');
  header.className = 'card-header';

  const titleSection = document.createElement('div');
  titleSection.className = 'card-title-section';

  const checkboxWrapper = document.createElement('div');
  checkboxWrapper.className = 'checkbox-wrapper';
  const ch = document.createElement('input');
  ch.type = 'checkbox';
  ch.checked = task.is_completed;
  ch.addEventListener('change', () => handleToggle(task));
  checkboxWrapper.appendChild(ch);

  const titleSpan = document.createElement('span');
  titleSpan.className = 'card-title';
  titleSpan.textContent = task.title;

  titleSection.appendChild(checkboxWrapper);
  titleSection.appendChild(titleSpan);

  const badge = document.createElement('span');
  badge.className = `priority-badge priority-${task.priority}`;
  badge.textContent = task.priority;

  header.appendChild(titleSection);
  header.appendChild(badge);

  const desc = document.createElement('div');
  desc.className = 'card-desc';
  desc.textContent = task.description || 'No description';

  const actions = document.createElement('div');
  actions.className = 'card-actions';

  const editBtn = document.createElement('button');
  editBtn.className = 'btn-icon';
  editBtn.textContent = 'Edit';
  editBtn.addEventListener('click', () => openModal(task));

  const delBtn = document.createElement('button');
  delBtn.className = 'btn-icon btn-delete';
  delBtn.textContent = 'Delete';
  delBtn.addEventListener('click', () => handleDelete(task.id));

  actions.appendChild(editBtn);
  actions.appendChild(delBtn);

  card.appendChild(header);
  card.appendChild(desc);
  card.appendChild(actions);

  return card;
}

function renderModal() {
  if (!modal.open) return null;

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';

  const modalDiv = document.createElement('div');
  modalDiv.className = 'modal';

  const title = document.createElement('h3');
  title.textContent = modal.editingTask ? 'Edit Task' : 'New Task';

  const titleInput = document.createElement('input');
  titleInput.type = 'text';
  titleInput.placeholder = 'Task title';
  titleInput.value = modal.editingTask?.title || '';

  const descInput = document.createElement('input');
  descInput.type = 'text';
  descInput.placeholder = 'Description';
  descInput.value = modal.editingTask?.description || '';

  const prioritySelect = document.createElement('select');
  ['low', 'medium', 'high'].forEach(p => {
    const opt = document.createElement('option');
    opt.value = p;
    opt.textContent = p.charAt(0).toUpperCase() + p.slice(1);
    if (modal.editingTask?.priority === p) opt.selected = true;
    prioritySelect.appendChild(opt);
  });

  let completedCh = null;
  if (modal.editingTask) {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem';
    completedCh = document.createElement('input');
    completedCh.type = 'checkbox';
    completedCh.checked = modal.editingTask.is_completed;
    completedCh.style.width = 'auto';
    const label = document.createElement('label');
    label.textContent = 'Completed';
    label.style.cssText = 'color:#cbd5e1;font-size:0.9rem';
    wrap.appendChild(completedCh);
    wrap.appendChild(label);
    modalDiv.appendChild(wrap);
  }

  const actionsDiv = document.createElement('div');
  actionsDiv.className = 'modal-actions';

  const saveBtn = document.createElement('button');
  saveBtn.className = 'btn-modal-save';
  saveBtn.textContent = modal.editingTask ? 'Save' : 'Add';

  const cancelBtn = document.createElement('button');
  cancelBtn.className = 'btn-modal-cancel';
  cancelBtn.textContent = 'Cancel';

  saveBtn.addEventListener('click', () => {
    const newTitle = titleInput.value.trim();
    if (!newTitle) {
      alert('Title required');
      return;
    }
    const data = {
      title: newTitle,
      description: descInput.value.trim(),
      priority: prioritySelect.value
    };
    if (modal.editingTask && completedCh) {
      data.is_completed = completedCh.checked;
    }
    saveModal(data);
  });

  cancelBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', e => {
    if (e.target === overlay) closeModal();
  });

  actionsDiv.appendChild(saveBtn);
  actionsDiv.appendChild(cancelBtn);

  modalDiv.appendChild(title);
  modalDiv.appendChild(titleInput);
  modalDiv.appendChild(descInput);
  modalDiv.appendChild(prioritySelect);
  modalDiv.appendChild(actionsDiv);
  overlay.appendChild(modalDiv);

  setTimeout(() => titleInput.focus(), 50);

  return overlay;
}

// ГЛАВНЫЙ РЕНДЕР
function render() {
  appEl.innerHTML = '';

  if (!isAuthenticated) {
    appEl.appendChild(renderAuthForm());
    return;
  }

  const header = document.createElement('div');
  header.className = 'app-header';
  const h1 = document.createElement('h1');
  h1.textContent = 'Task Manager';

  const headerRight = document.createElement('div');
  headerRight.style.cssText = 'display:flex;gap:1rem';

  const addBtn = document.createElement('button');
  addBtn.className = 'btn-primary';
  addBtn.textContent = '+ New Task';
  addBtn.addEventListener('click', () => openModal());

  const logoutBtn = document.createElement('button');
  logoutBtn.className = 'btn-icon';
  logoutBtn.textContent = 'Logout';
  logoutBtn.addEventListener('click', handleLogout);

  headerRight.appendChild(addBtn);
  headerRight.appendChild(logoutBtn);
  header.appendChild(h1);
  header.appendChild(headerRight);
  appEl.appendChild(header);

  if (error) {
    const errDiv = document.createElement('div');
    errDiv.className = 'error-message';
    errDiv.textContent = `Error: ${error}`;
    appEl.appendChild(errDiv);
  }

  const container = document.createElement('div');
  container.className = 'tasks-container';

  const tasksHeader = document.createElement('div');
  tasksHeader.className = 'tasks-header';
  const h2 = document.createElement('h2');
  h2.textContent = 'All Tasks';
  const badge = document.createElement('span');
  badge.className = 'badge-count';
  badge.textContent = tasks.length;
  tasksHeader.appendChild(h2);
  tasksHeader.appendChild(badge);

  const taskList = document.createElement('div');
  taskList.className = 'task-list';

  if (isLoading) {
    const loadDiv = document.createElement('div');
    loadDiv.className = 'loading';
    loadDiv.textContent = 'Loading...';
    taskList.appendChild(loadDiv);
  } else if (tasks.length === 0) {
    const emptyDiv = document.createElement('div');
    emptyDiv.className = 'empty-message';
    emptyDiv.textContent = 'No tasks yet';
    taskList.appendChild(emptyDiv);
  } else {
    getSorted().forEach(t => taskList.appendChild(renderTaskCard(t)));
  }

  container.appendChild(tasksHeader);
  container.appendChild(taskList);
  appEl.appendChild(container);

  const modalEl = renderModal();
  if (modalEl) appEl.appendChild(modalEl);
}

// СТАРТ
if (isAuthenticated) {
  loadTasks();
} else {
  render();
}
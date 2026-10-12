/**
 * FitTrack - Frontend Application Logic
 * Pure ES6+ Vanilla JavaScript connecting with Flask REST endpoints
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global Application State
  const state = {
    currentPage: 'dashboard',
    theme: localStorage.getItem('fittrack_theme') || 'dark',
    goals: { daily_step_goal: 8000, weekly_workout_goal: 5, daily_water_goal: 2.5 },
    activeWorkoutId: null,
    deleteWorkoutCandidate: null,
    charts: {
      dashboardWeekly: null,
      analyticsSteps: null,
      analyticsCalories: null,
      analyticsDistribution: null
    }
  };

  // DOM Elements Cache
  const elements = {
    // Nav & Shell
    sidebar: document.getElementById('sidebar'),
    mobileMenuBtn: document.getElementById('mobileMenuBtn'),
    navItems: document.querySelectorAll('.nav-item, .mobile-nav-item'),
    pageViews: document.querySelectorAll('.page-view'),
    pageTitle: document.getElementById('pageTitle'),
    pageSubtitle: document.getElementById('pageSubtitle'),
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    toggleThemeSettingsBtn: document.getElementById('toggleThemeSettingsBtn'),
    themeIcon: document.getElementById('themeIcon'),
    themeLabel: document.getElementById('themeLabel'),
    apiStatusText: document.getElementById('apiStatusText'),
    currentDateBadge: document.getElementById('currentDateBadge'),
    headerQuickAddBtn: document.getElementById('headerQuickAddBtn'),

    // Dashboard
    dashSteps: document.getElementById('dashSteps'),
    dashDistance: document.getElementById('dashDistance'),
    dashCalories: document.getElementById('dashCalories'),
    dashDuration: document.getElementById('dashDuration'),
    dashWater: document.getElementById('dashWater'),
    dashWeeklyWorkouts: document.getElementById('dashWeeklyWorkouts'),
    dashStepProgressBar: document.getElementById('dashStepProgressBar'),
    dashStepProgressText: document.getElementById('dashStepProgressText'),
    dashWaterProgressBar: document.getElementById('dashWaterProgressBar'),
    dashWaterProgressText: document.getElementById('dashWaterProgressText'),
    dashWeeklyProgressBar: document.getElementById('dashWeeklyProgressBar'),
    dashWeeklyProgressText: document.getElementById('dashWeeklyProgressText'),
    dashboardRecentList: document.getElementById('dashboardRecentList'),
    viewAllWorkoutsLink: document.getElementById('viewAllWorkoutsLink'),

    // Workouts
    workoutSearchInput: document.getElementById('workoutSearchInput'),
    workoutTypeFilter: document.getElementById('workoutTypeFilter'),
    workoutDateFilter: document.getElementById('workoutDateFilter'),
    workoutSortBy: document.getElementById('workoutSortBy'),
    workoutSortOrder: document.getElementById('workoutSortOrder'),
    resetWorkoutFiltersBtn: document.getElementById('resetWorkoutFiltersBtn'),
    createNewWorkoutBtn: document.getElementById('createNewWorkoutBtn'),
    workoutsTableBody: document.getElementById('workoutsTableBody'),
    workoutsCountText: document.getElementById('workoutsCountText'),

    // Workout Form
    workoutForm: document.getElementById('workoutForm'),
    formWorkoutTitle: document.getElementById('formWorkoutTitle'),
    editWorkoutId: document.getElementById('editWorkoutId'),
    workoutTypeInput: document.getElementById('workoutTypeInput'),
    workoutDateInput: document.getElementById('workoutDateInput'),
    workoutDurationInput: document.getElementById('workoutDurationInput'),
    workoutCaloriesInput: document.getElementById('workoutCaloriesInput'),
    workoutDistanceInput: document.getElementById('workoutDistanceInput'),
    workoutNotesInput: document.getElementById('workoutNotesInput'),
    cancelWorkoutFormBtn: document.getElementById('cancelWorkoutFormBtn'),
    saveWorkoutBtn: document.getElementById('saveWorkoutBtn'),
    saveWorkoutBtnText: document.getElementById('saveWorkoutBtnText'),

    // Activity Tracker
    activityForm: document.getElementById('activityForm'),
    activityDateInput: document.getElementById('activityDateInput'),
    activityStepsInput: document.getElementById('activityStepsInput'),
    activityWaterInput: document.getElementById('activityWaterInput'),
    activityActiveMinsInput: document.getElementById('activityActiveMinsInput'),
    activityDistanceInput: document.getElementById('activityDistanceInput'),
    activityCaloriesInput: document.getElementById('activityCaloriesInput'),
    addWater250Btn: document.getElementById('addWater250Btn'),
    addWater500Btn: document.getElementById('addWater500Btn'),
    activityHistoryBody: document.getElementById('activityHistoryBody'),

    // Analytics
    anaTotalWorkouts: document.getElementById('anaTotalWorkouts'),
    anaAvgDuration: document.getElementById('anaAvgDuration'),
    anaTotalCalories: document.getElementById('anaTotalCalories'),
    anaTotalDistance: document.getElementById('anaTotalDistance'),
    analyticsGoalBars: document.getElementById('analyticsGoalBars'),

    // Goals & Settings
    goalsForm: document.getElementById('goalsForm'),
    goalStepInput: document.getElementById('goalStepInput'),
    goalWeeklyWorkoutsInput: document.getElementById('goalWeeklyWorkoutsInput'),
    goalWaterInput: document.getElementById('goalWaterInput'),
    resetDemoDataBtn: document.getElementById('resetDemoDataBtn'),

    // Modals
    workoutDetailsModal: document.getElementById('workoutDetailsModal'),
    modalWorkoutTitle: document.getElementById('modalWorkoutTitle'),
    modalWorkoutBody: document.getElementById('modalWorkoutBody'),
    closeWorkoutDetailsModal: document.getElementById('closeWorkoutDetailsModal'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),
    modalEditWorkoutBtn: document.getElementById('modalEditWorkoutBtn'),

    deleteConfirmModal: document.getElementById('deleteConfirmModal'),
    closeDeleteModal: document.getElementById('closeDeleteModal'),
    cancelDeleteBtn: document.getElementById('cancelDeleteBtn'),
    confirmDeleteBtn: document.getElementById('confirmDeleteBtn'),
    deleteWorkoutPreview: document.getElementById('deleteWorkoutPreview'),

    toastContainer: document.getElementById('toastContainer')
  };

  // ==========================================
  // Helper: Notification Toasts
  // ==========================================
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ==========================================
  // Theme Management
  // ==========================================
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('fittrack_theme', theme);

    if (theme === 'dark') {
      elements.themeIcon.textContent = '☀️';
      elements.themeLabel.textContent = 'Light Mode';
      if (elements.toggleThemeSettingsBtn) {
        elements.toggleThemeSettingsBtn.textContent = 'Switch to Light Mode';
      }
    } else {
      elements.themeIcon.textContent = '🌙';
      elements.themeLabel.textContent = 'Dark Mode';
      if (elements.toggleThemeSettingsBtn) {
        elements.toggleThemeSettingsBtn.textContent = 'Switch to Dark Mode';
      }
    }

    // Refresh charts with updated theme colors
    refreshAllCharts();
  }

  function toggleTheme() {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  }

  // ==========================================
  // Routing & View Navigation
  // ==========================================
  const pageMetadata = {
    'dashboard': {
      title: 'Dashboard',
      subtitle: 'Track your daily momentum, physical activity, and workout milestones'
    },
    'workouts': {
      title: 'Workouts History',
      subtitle: 'Comprehensive training log with search, type filters, and date sorting'
    },
    'add-workout': {
      title: 'Workout Logger',
      subtitle: 'Record a completed workout session to update dashboard metrics'
    },
    'activity': {
      title: 'Daily Activity Tracker',
      subtitle: 'Log and monitor step counts, active calories, and daily hydration'
    },
    'analytics': {
      title: 'Fitness Analytics',
      subtitle: 'Long-term trends, training distributions, and performance averages'
    },
    'goals': {
      title: 'Goals & Settings',
      subtitle: 'Configure daily step targets, weekly goals, and laboratory options'
    }
  };

  function navigateTo(pageId) {
    if (!pageMetadata[pageId]) pageId = 'dashboard';
    state.currentPage = pageId;

    // Update Nav Buttons
    elements.navItems.forEach(item => {
      if (item.getAttribute('data-page') === pageId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Toggle Views
    elements.pageViews.forEach(view => {
      if (view.id === `view-${pageId}`) {
        view.classList.add('active');
      } else {
        view.classList.remove('active');
      }
    });

    // Update Header
    const meta = pageMetadata[pageId];
    elements.pageTitle.textContent = meta.title;
    elements.pageSubtitle.textContent = meta.subtitle;

    // Close mobile drawer if opened
    elements.sidebar.classList.remove('mobile-open');

    // Trigger View Specific Data Fetch
    if (pageId === 'dashboard') loadDashboard();
    else if (pageId === 'workouts') loadWorkouts();
    else if (pageId === 'add-workout') prepareAddWorkoutForm();
    else if (pageId === 'activity') loadActivityView();
    else if (pageId === 'analytics') loadAnalyticsView();
    else if (pageId === 'goals') loadGoalsView();
  }

  // ==========================================
  // Health Check
  // ==========================================
  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      const data = await res.json();
      if (res.ok && data.status === 'healthy') {
        elements.apiStatusText.textContent = `API Online (${data.database})`;
      } else {
        elements.apiStatusText.textContent = 'API Degraded';
      }
    } catch {
      elements.apiStatusText.textContent = 'API Disconnected';
    }
  }

  // ==========================================
  // 1. Dashboard View
  // ==========================================
  async function loadDashboard() {
    try {
      const res = await fetch('/api/dashboard');
      if (!res.ok) throw new Error('Failed to fetch dashboard data');
      const json = await res.json();
      const { today, weekly_chart, recent_workouts } = json.data;

      // Update Today KPI cards
      elements.dashSteps.textContent = Number(today.steps).toLocaleString();
      elements.dashDistance.textContent = today.distance_km.toFixed(1);
      elements.dashCalories.textContent = Number(today.calories).toLocaleString();
      elements.dashDuration.textContent = today.workout_duration_minutes;
      elements.dashWater.textContent = today.water_intake_liters.toFixed(1);
      elements.dashWeeklyWorkouts.textContent = today.weekly_workout_count;

      // Progress bars
      elements.dashStepProgressBar.style.width = `${Math.min(100, today.step_goal_pct)}%`;
      elements.dashStepProgressText.textContent = `${today.step_goal_pct}% of ${Number(today.step_goal).toLocaleString()} goal`;

      elements.dashWaterProgressBar.style.width = `${Math.min(100, today.water_goal_pct)}%`;
      elements.dashWaterProgressText.textContent = `${today.water_goal_pct}% of ${today.water_goal} L`;

      elements.dashWeeklyProgressBar.style.width = `${Math.min(100, today.weekly_workout_pct)}%`;
      elements.dashWeeklyProgressText.textContent = `${today.weekly_workout_pct}% of ${today.weekly_workout_goal} sessions`;

      // Render Dashboard Weekly Chart
      renderDashboardWeeklyChart(weekly_chart);

      // Render Recent Workouts
      renderRecentWorkoutsList(recent_workouts);
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function renderRecentWorkoutsList(workouts) {
    if (!workouts || workouts.length === 0) {
      elements.dashboardRecentList.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">🏃</div>
          <p>No workouts recorded yet. Start by logging your first session!</p>
        </div>`;
      return;
    }

    elements.dashboardRecentList.innerHTML = workouts.map(w => {
      const typeClass = w.workout_type.replace(/\s+/g, '-');
      const icon = getWorkoutIcon(w.workout_type);
      return `
        <div class="recent-item" data-id="${w.id}">
          <div class="recent-item-left">
            <div class="workout-type-icon ${typeClass}">${icon}</div>
            <div>
              <div class="recent-item-title">${escapeHtml(w.workout_type)}</div>
              <div class="recent-item-meta">${w.workout_date} &bull; ${w.distance > 0 ? w.distance + ' km' : 'Indoor session'}</div>
            </div>
          </div>
          <div class="recent-item-stats">
            <div class="recent-item-cals">${w.calories} kcal</div>
            <div class="recent-item-dur">${w.duration} mins</div>
          </div>
        </div>`;
    }).join('');

    // Attach click listeners to open details modal
    elements.dashboardRecentList.querySelectorAll('.recent-item').forEach(el => {
      el.addEventListener('click', () => {
        const id = el.getAttribute('data-id');
        openWorkoutDetailsModal(id);
      });
    });
  }

  function renderDashboardWeeklyChart(chartData) {
    const ctx = document.getElementById('dashboardWeeklyChart');
    if (!ctx) return;

    if (state.charts.dashboardWeekly) {
      state.charts.dashboardWeekly.destroy();
    }

    const isDark = state.theme === 'dark';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
    const textColor = isDark ? '#9ca3af' : '#6b7280';

    state.charts.dashboardWeekly = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: 'Steps',
            data: chartData.steps,
            backgroundColor: 'rgba(16, 185, 129, 0.85)',
            borderRadius: 6,
            yAxisID: 'y'
          },
          {
            label: 'Calories (kcal)',
            data: chartData.calories,
            type: 'line',
            borderColor: '#f97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
            borderWidth: 3,
            tension: 0.35,
            fill: false,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: {
            labels: { color: textColor, font: { family: 'Plus Jakarta Sans', weight: 600 } }
          }
        },
        scales: {
          x: {
            grid: { color: gridColor },
            ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
          },
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            grid: { color: gridColor },
            ticks: { color: textColor },
            title: { display: true, text: 'Steps', color: textColor }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: textColor },
            title: { display: true, text: 'Calories (kcal)', color: textColor }
          }
        }
      }
    });
  }

  // ==========================================
  // 2. Workouts View (CRUD + History)
  // ==========================================
  async function loadWorkouts() {
    try {
      const type = elements.workoutTypeFilter.value;
      const dateVal = elements.workoutDateFilter.value;
      const search = elements.workoutSearchInput.value;
      const sortBy = elements.workoutSortBy.value;
      const order = elements.workoutSortOrder.value;

      const params = new URLSearchParams();
      if (type) params.append('type', type);
      if (dateVal) params.append('date', dateVal);
      if (search) params.append('search', search);
      if (sortBy) params.append('sort_by', sortBy);
      if (order) params.append('order', order);

      const res = await fetch(`/api/workouts?${params.toString()}`);
      if (!res.ok) throw new Error('Failed to retrieve workouts');
      const json = await res.json();
      const workouts = json.data;

      elements.workoutsCountText.textContent = `Showing ${workouts.length} workout${workouts.length === 1 ? '' : 's'}`;

      if (workouts.length === 0) {
        elements.workoutsTableBody.innerHTML = `
          <tr>
            <td colspan="8" class="empty-state">
              <div class="empty-state-icon">🔍</div>
              <p>No workouts match the current search or filter criteria.</p>
            </td>
          </tr>`;
        return;
      }

      elements.workoutsTableBody.innerHTML = workouts.map(w => {
        const typeClass = w.workout_type.replace(/\s+/g, '-');
        const icon = getWorkoutIcon(w.workout_type);
        return `
          <tr>
            <td><strong>#${w.id}</strong></td>
            <td>
              <span class="badge badge-pill badge-primary">
                ${icon} ${escapeHtml(w.workout_type)}
              </span>
            </td>
            <td>${w.workout_date}</td>
            <td><strong>${w.duration}</strong> min</td>
            <td><span style="color: var(--brand-calorie); font-weight:700;">${w.calories}</span> kcal</td>
            <td>${w.distance > 0 ? w.distance + ' km' : '—'}</td>
            <td><small class="text-muted">${escapeHtml(w.notes || '—')}</small></td>
            <td class="text-right">
              <div class="action-btn-group">
                <button class="btn-icon view-btn" data-id="${w.id}" title="View Details">👁️</button>
                <button class="btn-icon edit-btn" data-id="${w.id}" title="Edit Workout">✏️</button>
                <button class="btn-icon delete delete-btn" data-id="${w.id}" title="Delete Workout">🗑️</button>
              </div>
            </td>
          </tr>`;
      }).join('');

      // Wire Action Buttons
      elements.workoutsTableBody.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => openWorkoutDetailsModal(btn.getAttribute('data-id')));
      });
      elements.workoutsTableBody.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => openEditWorkoutForm(btn.getAttribute('data-id')));
      });
      elements.workoutsTableBody.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => openDeleteConfirmModal(btn.getAttribute('data-id')));
      });
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // 3. Add / Edit Workout Form
  // ==========================================
  function prepareAddWorkoutForm(workout = null) {
    elements.workoutForm.reset();
    document.querySelectorAll('.form-error').forEach(el => el.textContent = '');

    if (workout) {
      // Edit Mode
      state.activeWorkoutId = workout.id;
      elements.editWorkoutId.value = workout.id;
      elements.formWorkoutTitle.textContent = `Edit Workout #${workout.id}`;
      elements.saveWorkoutBtnText.textContent = 'Update Workout';
      elements.workoutTypeInput.value = workout.workout_type;
      elements.workoutDateInput.value = workout.workout_date;
      elements.workoutDurationInput.value = workout.duration;
      elements.workoutCaloriesInput.value = workout.calories;
      elements.workoutDistanceInput.value = workout.distance;
      elements.workoutNotesInput.value = workout.notes || '';
    } else {
      // Add Mode
      state.activeWorkoutId = null;
      elements.editWorkoutId.value = '';
      elements.formWorkoutTitle.textContent = 'Log a New Workout';
      elements.saveWorkoutBtnText.textContent = 'Save Workout';
      elements.workoutDateInput.value = new Date().toISOString().split('T')[0];
      elements.workoutDistanceInput.value = '0.0';
    }
  }

  async function openEditWorkoutForm(workoutId) {
    try {
      const res = await fetch(`/api/workouts/${workoutId}`);
      if (!res.ok) throw new Error('Workout not found');
      const json = await res.json();
      prepareAddWorkoutForm(json.data);
      navigateTo('add-workout');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function handleWorkoutFormSubmit(e) {
    e.preventDefault();

    // Client-side validation
    let hasError = false;
    const type = elements.workoutTypeInput.value;
    const dateVal = elements.workoutDateInput.value;
    const duration = parseInt(elements.workoutDurationInput.value, 10);
    const calories = parseInt(elements.workoutCaloriesInput.value, 10);
    const distance = parseFloat(elements.workoutDistanceInput.value) || 0.0;
    const notes = elements.workoutNotesInput.value.trim();

    if (!type) {
      document.getElementById('err-workoutType').textContent = 'Please select a workout type.';
      hasError = true;
    }
    if (!dateVal) {
      document.getElementById('err-workoutDate').textContent = 'Please choose a valid date.';
      hasError = true;
    }
    if (isNaN(duration) || duration <= 0) {
      document.getElementById('err-workoutDuration').textContent = 'Duration must be greater than 0.';
      hasError = true;
    }
    if (isNaN(calories) || calories < 0) {
      document.getElementById('err-workoutCalories').textContent = 'Calories must be 0 or higher.';
      hasError = true;
    }

    if (hasError) return;

    const payload = {
      workout_type: type,
      workout_date: dateVal,
      duration: duration,
      calories: calories,
      distance: distance,
      notes: notes
    };

    const isEdit = Boolean(elements.editWorkoutId.value);
    const url = isEdit ? `/api/workouts/${elements.editWorkoutId.value}` : '/api/workouts';
    const method = isEdit ? 'PUT' : 'POST';

    try {
      elements.saveWorkoutBtn.disabled = true;
      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || (data.errors ? data.errors.join(', ') : 'Submission failed'));
      }

      showToast(isEdit ? 'Workout updated successfully!' : 'Workout logged successfully!', 'success');
      elements.workoutForm.reset();
      navigateTo('workouts');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      elements.saveWorkoutBtn.disabled = false;
    }
  }

  // ==========================================
  // 4. Workout Details & Deletion Modals
  // ==========================================
  async function openWorkoutDetailsModal(workoutId) {
    try {
      const res = await fetch(`/api/workouts/${workoutId}`);
      if (!res.ok) throw new Error('Workout details not found');
      const json = await res.json();
      const w = json.data;

      state.activeWorkoutId = w.id;
      elements.modalWorkoutTitle.textContent = `${w.workout_type} Session Details`;
      elements.modalWorkoutBody.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:12px;">
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Workout ID</span> <strong>#${w.id}</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Type</span> <strong>${escapeHtml(w.workout_type)}</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Date</span> <strong>${w.workout_date}</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Duration</span> <strong>${w.duration} minutes</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Calories Burned</span> <strong style="color:var(--brand-calorie);">${w.calories} kcal</strong>
          </div>
          <div style="display:flex; justify-content:space-between; padding-bottom:8px; border-bottom:1px solid var(--border-subtle);">
            <span>Distance Covered</span> <strong>${w.distance} km</strong>
          </div>
          <div>
            <span style="display:block; margin-bottom:4px;">Notes & Observations:</span>
            <div style="padding:10px; border-radius:var(--radius-sm); background-color:var(--bg-surface-elevated); font-style:italic;">
              ${escapeHtml(w.notes || 'No notes entered for this session.')}
            </div>
          </div>
        </div>
      `;

      elements.workoutDetailsModal.classList.add('show');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function openDeleteConfirmModal(workoutId) {
    try {
      const res = await fetch(`/api/workouts/${workoutId}`);
      if (!res.ok) throw new Error('Workout not found');
      const json = await res.json();
      const w = json.data;

      state.deleteWorkoutCandidate = w.id;
      elements.deleteWorkoutPreview.innerHTML = `
        <strong>#${w.id} ${escapeHtml(w.workout_type)}</strong> &bull; ${w.workout_date} (${w.duration} mins, ${w.calories} kcal)
      `;
      elements.deleteConfirmModal.classList.add('show');
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function confirmDeleteWorkout() {
    if (!state.deleteWorkoutCandidate) return;
    try {
      const res = await fetch(`/api/workouts/${state.deleteWorkoutCandidate}`, {
        method: 'DELETE'
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || 'Deletion failed');

      showToast('Workout successfully deleted.', 'success');
      elements.deleteConfirmModal.classList.remove('show');
      state.deleteWorkoutCandidate = null;
      loadWorkouts();
      loadDashboard();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // 5. Activity Tracker View
  // ==========================================
  async function loadActivityView() {
    const todayStr = new Date().toISOString().split('T')[0];
    elements.activityDateInput.value = todayStr;

    // Fetch existing activity for today
    try {
      const res = await fetch(`/api/activity?date=${todayStr}`);
      const json = await res.json();
      if (json.data) {
        elements.activityStepsInput.value = json.data.steps;
        elements.activityWaterInput.value = json.data.water_intake;
        elements.activityActiveMinsInput.value = json.data.active_minutes;
        elements.activityDistanceInput.value = json.data.distance;
        elements.activityCaloriesInput.value = json.data.calories;
      } else {
        elements.activityStepsInput.value = '';
        elements.activityWaterInput.value = '';
        elements.activityActiveMinsInput.value = '';
        elements.activityDistanceInput.value = '';
        elements.activityCaloriesInput.value = '';
      }
    } catch (err) {
      console.error(err);
    }

    // Load recent history logs
    loadActivityHistory();
  }

  async function loadActivityHistory() {
    try {
      const res = await fetch('/api/activity?limit=10');
      const json = await res.json();
      const activities = json.data;

      if (!activities || activities.length === 0) {
        elements.activityHistoryBody.innerHTML = `
          <tr><td colspan="5" class="empty-state">No activity logs recorded.</td></tr>
        `;
        return;
      }

      elements.activityHistoryBody.innerHTML = activities.map(a => `
        <tr>
          <td><strong>${a.activity_date}</strong></td>
          <td>${Number(a.steps).toLocaleString()}</td>
          <td>${a.distance} km</td>
          <td>${a.water_intake} L</td>
          <td>${a.calories} kcal</td>
        </tr>
      `).join('');
    } catch (err) {
      console.error(err);
    }
  }

  async function handleActivityFormSubmit(e) {
    e.preventDefault();
    const payload = {
      activity_date: elements.activityDateInput.value,
      steps: parseInt(elements.activityStepsInput.value, 10) || 0,
      water_intake: parseFloat(elements.activityWaterInput.value) || 0.0,
      active_minutes: parseInt(elements.activityActiveMinsInput.value, 10) || 0,
      distance: parseFloat(elements.activityDistanceInput.value) || 0.0,
      calories: parseInt(elements.activityCaloriesInput.value, 10) || 0
    };

    try {
      const res = await fetch('/api/activity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.message || 'Failed to save activity');

      showToast('Daily activity updated successfully!', 'success');
      loadActivityHistory();
      loadDashboard();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // 6. Analytics View
  // ==========================================
  async function loadAnalyticsView() {
    try {
      const res = await fetch('/api/analytics');
      if (!res.ok) throw new Error('Failed to load analytics');
      const json = await res.json();
      const data = json.data;

      // Update KPIs
      elements.anaTotalWorkouts.textContent = data.total_workouts;
      elements.anaAvgDuration.textContent = data.avg_duration_minutes;
      elements.anaTotalCalories.textContent = Number(data.total_calories_burned).toLocaleString();
      elements.anaTotalDistance.textContent = data.total_distance_km.toFixed(1);

      // Render Charts
      renderAnalyticsCharts(data);

      // Render Goal Adherence Bars
      renderGoalAdherenceBars(data);
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  function renderAnalyticsCharts(data) {
    const isDark = state.theme === 'dark';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
    const textColor = isDark ? '#9ca3af' : '#6b7280';

    // 1. Steps Consistency Chart
    const stepsCtx = document.getElementById('analyticsStepsChart');
    if (stepsCtx) {
      if (state.charts.analyticsSteps) state.charts.analyticsSteps.destroy();
      state.charts.analyticsSteps = new Chart(stepsCtx, {
        type: 'bar',
        data: {
          labels: data.weekly_trends.labels,
          datasets: [{
            label: 'Steps Walked',
            data: data.weekly_trends.steps,
            backgroundColor: '#10b981',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor } }
          },
          plugins: {
            legend: { labels: { color: textColor } }
          }
        }
      });
    }

    // 2. Calorie Expenditure Chart
    const calCtx = document.getElementById('analyticsCaloriesChart');
    if (calCtx) {
      if (state.charts.analyticsCalories) state.charts.analyticsCalories.destroy();
      state.charts.analyticsCalories = new Chart(calCtx, {
        type: 'line',
        data: {
          labels: data.weekly_trends.labels,
          datasets: [{
            label: 'Calories Burned (kcal)',
            data: data.weekly_trends.calories,
            borderColor: '#f97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
            borderWidth: 3,
            tension: 0.35,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { grid: { color: gridColor }, ticks: { color: textColor } },
            y: { grid: { color: gridColor }, ticks: { color: textColor } }
          },
          plugins: {
            legend: { labels: { color: textColor } }
          }
        }
      });
    }

    // 3. Distribution Doughnut Chart
    const distCtx = document.getElementById('analyticsDistributionChart');
    if (distCtx) {
      if (state.charts.analyticsDistribution) state.charts.analyticsDistribution.destroy();
      state.charts.analyticsDistribution = new Chart(distCtx, {
        type: 'doughnut',
        data: {
          labels: data.distribution_chart.labels,
          datasets: [{
            data: data.distribution_chart.counts,
            backgroundColor: [
              '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4'
            ],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: { color: textColor }
            }
          }
        }
      });
    }
  }

  function renderGoalAdherenceBars(data) {
    const goals = data.goals;
    const rates = data.completion_rates;

    elements.analyticsGoalBars.innerHTML = `
      <div class="goal-bar-item">
        <div class="goal-bar-header">
          <span>Daily Step Target (${Number(goals.daily_step_goal).toLocaleString()} steps)</span>
          <strong>${rates.daily_step_goal_pct}%</strong>
        </div>
        <div class="goal-bar-track">
          <div class="goal-bar-fill" style="width: ${Math.min(100, rates.daily_step_goal_pct)}%; background-color: var(--brand-primary);"></div>
        </div>
      </div>

      <div class="goal-bar-item">
        <div class="goal-bar-header">
          <span>Weekly Workout Goal (${goals.weekly_workout_goal} sessions)</span>
          <strong>${rates.weekly_workout_goal_pct}%</strong>
        </div>
        <div class="goal-bar-track">
          <div class="goal-bar-fill" style="width: ${Math.min(100, rates.weekly_workout_goal_pct)}%; background-color: var(--brand-accent);"></div>
        </div>
      </div>

      <div class="goal-bar-item">
        <div class="goal-bar-header">
          <span>Daily Hydration Goal (${goals.daily_water_goal} L)</span>
          <strong>${rates.daily_water_goal_pct}%</strong>
        </div>
        <div class="goal-bar-track">
          <div class="goal-bar-fill" style="width: ${Math.min(100, rates.daily_water_goal_pct)}%; background-color: var(--brand-water);"></div>
        </div>
      </div>
    `;
  }

  // ==========================================
  // 7. Goals & Settings View
  // ==========================================
  async function loadGoalsView() {
    try {
      const res = await fetch('/api/goals');
      const json = await res.json();
      const g = json.data;

      state.goals = g;
      elements.goalStepInput.value = g.daily_step_goal;
      elements.goalWeeklyWorkoutsInput.value = g.weekly_workout_goal;
      elements.goalWaterInput.value = g.daily_water_goal;
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function handleGoalsFormSubmit(e) {
    e.preventDefault();
    const payload = {
      daily_step_goal: parseInt(elements.goalStepInput.value, 10),
      weekly_workout_goal: parseInt(elements.goalWeeklyWorkoutsInput.value, 10),
      daily_water_goal: parseFloat(elements.goalWaterInput.value)
    };

    try {
      const res = await fetch('/api/goals', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.message || 'Failed to update goals');

      state.goals = json.data;
      showToast('Goals updated successfully!', 'success');
      loadDashboard();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  async function handleResetDemoData() {
    if (!confirm('Are you sure you want to restore initial demo records? This will reseed your database with sample data.')) {
      return;
    }

    try {
      const res = await fetch('/api/reset', { method: 'POST' });
      const json = await res.json();
      if (!res.ok) throw new Error(json.message || 'Reset failed');

      showToast('FitTrack database reset successfully!', 'success');
      loadDashboard();
      if (state.currentPage === 'workouts') loadWorkouts();
      if (state.currentPage === 'analytics') loadAnalyticsView();
      if (state.currentPage === 'goals') loadGoalsView();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  // ==========================================
  // Utility Functions
  // ==========================================
  function getWorkoutIcon(type) {
    switch (type) {
      case 'Running': return '🏃';
      case 'Walking': return '🚶';
      case 'Cycling': return '🚴';
      case 'Strength Training': return '🏋️';
      case 'Yoga': return '🧘';
      default: return '⚡';
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function refreshAllCharts() {
    if (state.currentPage === 'dashboard') loadDashboard();
    else if (state.currentPage === 'analytics') loadAnalyticsView();
  }

  // ==========================================
  // Event Listeners Registration
  // ==========================================
  // Navigation
  elements.navItems.forEach(btn => {
    btn.addEventListener('click', () => {
      const page = btn.getAttribute('data-page');
      navigateTo(page);
    });
  });

  if (elements.headerQuickAddBtn) {
    elements.headerQuickAddBtn.addEventListener('click', () => {
      prepareAddWorkoutForm();
      navigateTo('add-workout');
    });
  }

  if (elements.createNewWorkoutBtn) {
    elements.createNewWorkoutBtn.addEventListener('click', () => {
      prepareAddWorkoutForm();
      navigateTo('add-workout');
    });
  }

  if (elements.viewAllWorkoutsLink) {
    elements.viewAllWorkoutsLink.addEventListener('click', () => navigateTo('workouts'));
  }

  // Theme Toggles
  elements.themeToggleBtn.addEventListener('click', toggleTheme);
  if (elements.toggleThemeSettingsBtn) {
    elements.toggleThemeSettingsBtn.addEventListener('click', toggleTheme);
  }

  // Mobile drawer toggle
  elements.mobileMenuBtn.addEventListener('click', () => {
    elements.sidebar.classList.toggle('mobile-open');
  });

  // Forms
  elements.workoutForm.addEventListener('submit', handleWorkoutFormSubmit);
  elements.cancelWorkoutFormBtn.addEventListener('click', () => navigateTo('workouts'));

  elements.activityForm.addEventListener('submit', handleActivityFormSubmit);
  elements.addWater250Btn.addEventListener('click', () => {
    const cur = parseFloat(elements.activityWaterInput.value) || 0;
    elements.activityWaterInput.value = (cur + 0.25).toFixed(2);
  });
  elements.addWater500Btn.addEventListener('click', () => {
    const cur = parseFloat(elements.activityWaterInput.value) || 0;
    elements.activityWaterInput.value = (cur + 0.50).toFixed(2);
  });

  elements.goalsForm.addEventListener('submit', handleGoalsFormSubmit);
  elements.resetDemoDataBtn.addEventListener('click', handleResetDemoData);

  // Workout Filter Inputs
  const debouncedWorkoutSearch = debounce(loadWorkouts, 300);
  elements.workoutSearchInput.addEventListener('input', debouncedWorkoutSearch);
  elements.workoutTypeFilter.addEventListener('change', loadWorkouts);
  elements.workoutDateFilter.addEventListener('change', loadWorkouts);
  elements.workoutSortBy.addEventListener('change', loadWorkouts);
  elements.workoutSortOrder.addEventListener('change', loadWorkouts);
  elements.resetWorkoutFiltersBtn.addEventListener('click', () => {
    elements.workoutSearchInput.value = '';
    elements.workoutTypeFilter.value = '';
    elements.workoutDateFilter.value = '';
    elements.workoutSortBy.value = 'workout_date';
    elements.workoutSortOrder.value = 'desc';
    loadWorkouts();
  });

  // Modals Close Handlers
  elements.closeWorkoutDetailsModal.addEventListener('click', () => elements.workoutDetailsModal.classList.remove('show'));
  elements.modalCloseBtn.addEventListener('click', () => elements.workoutDetailsModal.classList.remove('show'));
  elements.modalEditWorkoutBtn.addEventListener('click', () => {
    elements.workoutDetailsModal.classList.remove('show');
    openEditWorkoutForm(state.activeWorkoutId);
  });

  elements.closeDeleteModal.addEventListener('click', () => elements.deleteConfirmModal.classList.remove('show'));
  elements.cancelDeleteBtn.addEventListener('click', () => elements.deleteConfirmModal.classList.remove('show'));
  elements.confirmDeleteBtn.addEventListener('click', confirmDeleteWorkout);

  // Close modals when clicking backdrop
  window.addEventListener('click', (e) => {
    if (e.target === elements.workoutDetailsModal) elements.workoutDetailsModal.classList.remove('show');
    if (e.target === elements.deleteConfirmModal) elements.deleteConfirmModal.classList.remove('show');
  });

  function debounce(func, wait) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  // ==========================================
  // Initialization
  // ==========================================
  applyTheme(state.theme);
  checkHealth();
  const dateToday = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  elements.currentDateBadge.textContent = dateToday;
  navigateTo('dashboard');
});

// TP799 Learning Hub
// 修改課程只需要編輯 courses 陣列。status 可用：done / next / planned

const abilities = {
  mindset: {
    label: '目標與心態',
    icon: '🎯',
    color: '#b78a2a',
    desc: '目標設定、業務心態、自我要求與行動紀律。'
  },
  selfbrand: {
    label: '銷售自我與故事',
    icon: '🪪',
    color: '#1d4e89',
    desc: '銷售自我、故事行銷、個人信任感與專業形象。'
  },
  star: {
    label: '穩定績效系統',
    icon: '🏆',
    color: '#c87c35',
    desc: '富邦之星、固定活動量、長期服務與每月穩定產出。'
  },
  social: {
    label: '社群與開發',
    icon: '🧲',
    color: '#4f8f6b',
    desc: '社群開發、客戶開發、名單接觸與曝光轉換。'
  },
  grid: {
    label: '九宮格與需求拆解',
    icon: '🧩',
    color: '#7c5cc4',
    desc: '九宮格工具、需求盤點、家庭責任與問句設計。'
  },
  relationship: {
    label: '好感經營與議題轉換',
    icon: '🤝',
    color: '#b95858',
    desc: '好感型客戶經營、話題轉議題、關係深化與自然切入。'
  },
  claims: {
    label: '條款與理賠',
    icon: '📜',
    color: '#2f6f73',
    desc: '保單條款、理賠邏輯、案例說明與客戶權益。'
  },
  wealth: {
    label: '投資財富與高資產',
    icon: '📊',
    color: '#9b6a10',
    desc: '投資財富、高資產客戶、資產配置與財務規劃切入。'
  }
};

const statuses = {
  all: { label: '全部' },
  ready: { label: '互動筆記完成' },
  done: { label: '已上課・待整理' },
  next: { label: '下一堂' },
  planned: { label: '未開始' }
};

const courses = [
  {
    no: 1,
    date: '06/09',
    month: '06',
    title: '目標設定、心態調整',
    lecturer: '簡宏鈞',
    role: '處經理',
    status: 'done',
    ability: 'mindset',
    url: '',
    desc: '建立業務工作的目標感與心態底盤，把想要的結果拆成可追蹤的行動節奏。',
    tags: ['目標設定', '心態調整', '行動紀律']
  },
  {
    no: 2,
    date: '06/16',
    month: '06',
    title: '銷售自我',
    lecturer: '范毓斌',
    role: '業務經理',
    status: 'done',
    ability: 'selfbrand',
    url: '',
    desc: '讓客戶先認同你這個人，再認同觀念與保險，建立信任感與自我介紹架構。',
    tags: ['銷售自我', '信任感', '個人品牌']
  },
  {
    no: 3,
    date: '06/23',
    month: '06',
    title: '富邦之星',
    lecturer: '李孟珊',
    role: '業務經理',
    status: 'ready',
    ability: 'star',
    url: 'notes/fubon-star-0623/',
    assetType: 'interactive',
    linkLabel: '查看互動筆記',
    desc: '把富邦之星拆成可執行的穩定績效系統：認同、約訪主題、名單水池、客戶經營與 30 日行動。',
    tags: ['富邦之星', '穩定績效', '活動量', '客戶經營']
  },
  {
    no: 4,
    date: '06/30',
    month: '06',
    title: '社群開發',
    lecturer: '詹呂欣蓓',
    role: '行銷襄理',
    status: 'next',
    ability: 'social',
    url: '',
    desc: '把社群曝光變成名單接觸點，建立可持續的內容、互動與邀約節奏。',
    tags: ['社群開發', '內容經營', '名單接觸']
  },
  {
    no: 5,
    date: '07/07',
    month: '07',
    title: '九宮格（前）',
    lecturer: '陳昶宇',
    role: '行銷襄理',
    status: 'planned',
    ability: 'grid',
    url: '',
    desc: '九宮格前段：協助業務盤點客戶資訊、家庭責任、風險缺口與可延伸議題。',
    tags: ['九宮格', '需求盤點', 'KYC']
  },
  {
    no: 6,
    date: '07/14',
    month: '07',
    title: '好感型客戶經營',
    lecturer: '吳虹儀',
    role: '行銷襄理',
    status: 'planned',
    ability: 'relationship',
    url: '',
    desc: '用好感與服務建立長期關係，讓客戶願意持續互動、回訪與轉介紹。',
    tags: ['好感經營', '客戶關係', '服務節奏']
  },
  {
    no: 7,
    date: '07/21',
    month: '07',
    title: '客戶開發',
    lecturer: '王昱文',
    role: '業務襄理',
    status: 'planned',
    ability: 'social',
    url: '',
    desc: '建立客戶開發的來源、接觸理由與追蹤方式，讓名單能被持續推進。',
    tags: ['客戶開發', '名單來源', '追蹤']
  },
  {
    no: 8,
    date: '07/28',
    month: '07',
    title: '故事行銷',
    lecturer: '張恩煒',
    role: '行銷襄理',
    status: 'planned',
    ability: 'selfbrand',
    url: '',
    desc: '把產品、觀念與案例包裝成客戶聽得懂、記得住、願意分享的故事。',
    tags: ['故事行銷', '案例表達', '信任建構']
  },
  {
    no: 9,
    date: '08/04',
    month: '08',
    title: '話題轉議題',
    lecturer: '周純伃',
    role: '行銷經理',
    status: 'planned',
    ability: 'relationship',
    url: '',
    desc: '從日常聊天自然切到保險、財務、家庭責任與風險管理議題。',
    tags: ['話題轉議題', '聊天切入', '需求引導']
  },
  {
    no: 10,
    date: '08/11',
    month: '08',
    title: '條款理賠',
    lecturer: '鄭占禮',
    role: '處經理',
    status: 'planned',
    ability: 'claims',
    url: '',
    desc: '用條款與理賠案例強化專業信任，讓客戶理解保單真正能解決什麼問題。',
    tags: ['條款', '理賠', '案例說明']
  },
  {
    no: 11,
    date: '08/18',
    month: '08',
    title: '投資財富',
    lecturer: '洪敬忠',
    role: '分處經理',
    status: 'planned',
    ability: 'wealth',
    url: '',
    desc: '從投資與財富管理角度切入客戶需求，連結資產配置、保障與長期規劃。',
    tags: ['投資財富', '資產配置', '財務規劃']
  },
  {
    no: 12,
    date: '08/25',
    month: '08',
    title: '高資產客戶',
    lecturer: '鄭捷宇',
    role: '業務經理',
    status: 'planned',
    ability: 'wealth',
    url: '',
    desc: '學習高資產客戶的經營邏輯、議題設計、信任累積與後續服務節奏。',
    tags: ['高資產', '客戶經營', '財富議題']
  },
  {
    no: 13,
    date: '09/01',
    month: '09',
    title: '九宮格（後）',
    lecturer: '趙家詡',
    role: '行銷襄理',
    status: 'planned',
    ability: 'grid',
    url: '',
    desc: '九宮格後段：把前段盤點結果轉成建議方向、行動方案與可追蹤的成交節奏。',
    tags: ['九宮格', '建議方向', '成交節奏']
  }
];

const state = {
  search: '',
  status: 'all',
  ability: 'all'
};

const dom = {
  searchInput: document.querySelector('#searchInput'),
  statusChips: document.querySelector('#statusChips'),
  pathGrid: document.querySelector('#pathGrid'),
  courseMount: document.querySelector('#courseMount'),
  resultSummary: document.querySelector('#resultSummary'),
  resetButton: document.querySelector('#resetButton'),
  metricGrid: document.querySelector('#metricGrid'),
  progressPercent: document.querySelector('#progressPercent'),
  progressBar: document.querySelector('#progressBar')
};

function normalize(value) {
  return String(value ?? '').trim().toLowerCase();
}

function courseMatchesSearch(course) {
  if (!state.search) return true;
  const abilityLabel = abilities[course.ability]?.label ?? '';
  const haystack = [
    course.date,
    course.title,
    course.lecturer,
    course.role,
    course.desc,
    abilityLabel,
    ...(course.tags ?? [])
  ].map(normalize).join(' ');
  return haystack.includes(normalize(state.search));
}

function getFilteredCourses() {
  return courses.filter(course => {
    const statusOk = state.status === 'all' || course.status === state.status;
    const abilityOk = state.ability === 'all' || course.ability === state.ability;
    return statusOk && abilityOk && courseMatchesSearch(course);
  });
}

function groupByMonth(list) {
  return list.reduce((groups, course) => {
    groups[course.month] ||= [];
    groups[course.month].push(course);
    return groups;
  }, {});
}

function getStatusLabel(status) {
  return statuses[status]?.label ?? status;
}

function renderMetrics() {
  const total = courses.length;
  const classDone = courses.filter(course => ['ready', 'done'].includes(course.status)).length;
  const notesReady = courses.filter(course => course.status === 'ready').length;
  const next = courses.find(course => course.status === 'next');
  const percent = total === 0 ? 0 : Math.round((classDone / total) * 100);

  dom.progressPercent.textContent = `${percent}%`;
  dom.progressBar.style.width = `${percent}%`;

  const metrics = [
    { value: total, label: '總課程' },
    { value: classDone, label: '已上課' },
    { value: notesReady, label: '互動筆記' },
    { value: next ? next.date : '—', label: '下一堂日期' }
  ];

  dom.metricGrid.innerHTML = metrics.map(metric => `
    <div class="metric">
      <b>${metric.value}</b>
      <span>${metric.label}</span>
    </div>
  `).join('');
}
function renderStatusChips() {
  dom.statusChips.innerHTML = Object.entries(statuses).map(([key, status]) => {
    const count = key === 'all' ? courses.length : courses.filter(course => course.status === key).length;
    return `<button type="button" class="chip ${state.status === key ? 'is-active' : ''}" data-status="${key}">${status.label} ${count}</button>`;
  }).join('');
}

function renderAbilityMap() {
  const allActive = state.ability === 'all';
  const allCount = courses.length;
  const allCard = `
    <button type="button" class="path-card ${allActive ? 'is-active' : ''}" data-ability="all" style="color:#0d1b2a">
      <span class="path-icon">✨</span>
      <h3>全部能力</h3>
      <p>查看完整訓練地圖，不限制能力分類。</p>
      <span class="path-meta">${allCount} 堂課</span>
    </button>
  `;

  const abilityCards = Object.entries(abilities).map(([key, ability]) => {
    const count = courses.filter(course => course.ability === key).length;
    return `
      <button type="button" class="path-card ${state.ability === key ? 'is-active' : ''}" data-ability="${key}" style="color:${ability.color}">
        <span class="path-icon">${ability.icon}</span>
        <h3>${ability.label}</h3>
        <p>${ability.desc}</p>
        <span class="path-meta">${count} 堂課</span>
      </button>
    `;
  }).join('');

  dom.pathGrid.innerHTML = allCard + abilityCards;
}

function renderCourses() {
  const filtered = getFilteredCourses();
  const grouped = groupByMonth(filtered);
  const monthKeys = Object.keys(grouped).sort();

  dom.resultSummary.textContent = `目前顯示 ${filtered.length} / ${courses.length} 堂課。`;

  if (filtered.length === 0) {
    dom.courseMount.innerHTML = `
      <div class="empty-state">
        <strong>找不到符合條件的課程</strong>
        <span>換一個關鍵字，或清除篩選重新查看。</span>
      </div>
    `;
    return;
  }

  dom.courseMount.innerHTML = monthKeys.map(month => {
    const cards = grouped[month].map(course => renderCourseCard(course)).join('');
    return `
      <section class="month-section" aria-label="${month} 月課程">
        <div class="month-label">
          <strong>${month}</strong>
          <span>月課程</span>
        </div>
        <div class="course-grid">${cards}</div>
      </section>
    `;
  }).join('');
}

function renderCourseCard(course) {
  const ability = abilities[course.ability];
  const canOpen = Boolean(course.url);
  const fallbackLabel = {
    ready: '查看互動筆記',
    done: '待整理筆記',
    next: '即將上課',
    planned: '未開始'
  }[course.status] || '查看課程';
  const buttonLabel = canOpen ? (course.linkLabel || fallbackLabel) : fallbackLabel;
  const linkClass = canOpen ? 'course-link' : 'course-link is-disabled';
  const href = canOpen ? course.url : '#';
  const tags = (course.tags ?? []).map(tag => `<span class="tag">#${tag}</span>`).join('');

  return `
    <article class="course-card">
      <div class="course-topline">
        <span class="date-pill">${course.date}</span>
        <span class="status-badge status-${course.status}">${getStatusLabel(course.status)}</span>
      </div>
      <div>
        <h3 class="course-title">${course.no}. ${course.title}</h3>
        <p class="course-speaker">${course.lecturer}｜${course.role}</p>
      </div>
      <p class="course-desc">${course.desc}</p>
      <div class="tag-row">${tags}</div>
      <div class="course-footer">
        <span class="ability-label">${ability?.icon ?? '📌'} ${ability?.label ?? '未分類'}</span>
        <a class="${linkClass}" href="${href}" ${canOpen ? 'target="_blank" rel="noreferrer"' : 'aria-disabled="true"'}>${buttonLabel}</a>
      </div>
    </article>
  `;
}
function resetFilters() {
  state.search = '';
  state.status = 'all';
  state.ability = 'all';
  dom.searchInput.value = '';
  render();
}

function bindEvents() {
  dom.searchInput.addEventListener('input', event => {
    state.search = event.target.value;
    renderCourses();
  });

  dom.statusChips.addEventListener('click', event => {
    const button = event.target.closest('[data-status]');
    if (!button) return;
    state.status = button.dataset.status;
    renderStatusChips();
    renderCourses();
  });

  dom.pathGrid.addEventListener('click', event => {
    const button = event.target.closest('[data-ability]');
    if (!button) return;
    state.ability = button.dataset.ability;
    renderAbilityMap();
    renderCourses();
    document.querySelector('#courses')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  dom.resetButton.addEventListener('click', resetFilters);
}

function render() {
  renderMetrics();
  renderStatusChips();
  renderAbilityMap();
  renderCourses();
}

bindEvents();
render();

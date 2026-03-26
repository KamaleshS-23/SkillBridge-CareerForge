// ========== GLOBAL STATE ==========
let progressData = {
    userSkills: [],
    skillsByCategory: {},
    totalSkills: 0,
    verifiedSkills: 0,
    avgProficiency: 0,
    testResults: [],
    certifications: [],
    learningActivities: [],
    goals: [],
    badges: [],
    careerMatches: [],
    interviewScores: []
};

// Load from Django context and localStorage
function loadProgressData() {
    // Load data passed from Django
    if (window.progressData) {
        progressData = { ...progressData, ...window.progressData };
    }
    
    // Load additional data from localStorage
    const saved = localStorage.getItem('progressTracking');
    if (saved) {
        const savedData = JSON.parse(saved);
        progressData = { ...progressData, ...savedData };
    } else {
        // Initialize with sample data if no data exists
        initializeSampleData();
    }
    
    renderAllCharts();
    renderAllSections();
}

function saveProgressData() {
    localStorage.setItem('progressTracking', JSON.stringify(progressData));
}

// Initialize sample data for demonstration
function initializeSampleData() {
    // Test results based on user skills
    progressData.testResults = progressData.userSkills.map(skill => ({
        skill: skill.name || skill.skill_name,
        score: Math.floor(Math.random() * 30) + 70, // 70-100
        date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        percentile: Math.floor(Math.random() * 40) + 60, // 60-100
        proficiency: skill.proficiency || skill.proficiency_level
    }));

    // Learning activities
    progressData.learningActivities = [
        { type: 'skill_added', name: 'Added React skill', date: new Date().toISOString().split('T')[0], progress: 100 },
        { type: 'skill_updated', name: 'Updated JavaScript proficiency', date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], progress: 100 },
        { type: 'profile_updated', name: 'Updated profile information', date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], progress: 100 },
        { type: 'skill_verified', name: 'Verified Python skill', date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], progress: 100 }
    ];

    // Goals
    progressData.goals = [
        { title: 'Master React Advanced', type: 'short', targetDate: '2025-04-15', progress: 60, skills: ['React'] },
        { title: 'Complete Full Stack Project', type: 'short', targetDate: '2025-04-30', progress: 30, skills: ['React', 'Node.js'] },
        { title: 'Get AWS Certified', type: 'medium', targetDate: '2025-06-30', progress: 25, skills: ['AWS'] },
        { title: 'Master System Design', type: 'medium', targetDate: '2025-07-31', progress: 40, skills: ['System Design'] }
    ];

    // Badges based on achievements
    progressData.badges = [
        { name: 'Skill Builder', icon: 'code', description: `Added ${progressData.totalSkills} skills` },
        { name: 'Verification Master', icon: 'check-circle', description: `Verified ${progressData.verifiedSkills} skills` },
        { name: 'Consistent Learner', icon: 'calendar-check', description: 'Active for 15 days' },
        { name: 'Profile Complete', icon: 'user', description: 'Completed profile setup' }
    ];

    // Career matches based on skills
    progressData.careerMatches = [
        { role: 'Senior Frontend Developer', match: 85, salary: '₹18-25 LPA', demand: 'High' },
        { role: 'Full Stack Developer', match: 78, salary: '₹16-22 LPA', demand: 'Very High' },
        { role: 'React Developer', match: 92, salary: '₹14-20 LPA', demand: 'High' },
        { role: 'Tech Lead', match: 62, salary: '₹25-35 LPA', demand: 'Medium' }
    ];

    saveProgressData();
}

// ========== CHART INITIALIZATION ==========
let charts = {};

function renderAllCharts() {
    console.log('Progress Tracking: Rendering all charts...');
    
    try {
        renderSkillDistributionChart();
        console.log('Progress Tracking: Skill distribution chart rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering skill distribution chart:', error);
    }
    
    try {
        renderCategoryProgressChart();
        console.log('Progress Tracking: Category progress chart rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering category progress chart:', error);
    }
    
    try {
        renderTestPerformanceChart();
        console.log('Progress Tracking: Test performance chart rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering test performance chart:', error);
    }
    
    try {
        renderSalaryChart();
        console.log('Progress Tracking: Salary chart rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering salary chart:', error);
    }
    
    try {
        renderActivityHeatMap();
        console.log('Progress Tracking: Activity heat map rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering activity heat map:', error);
    }
    
    try {
        renderProgressOverviewChart();
        console.log('Progress Tracking: Progress overview chart rendered');
    } catch (error) {
        console.error('Progress Tracking: Error rendering progress overview chart:', error);
    }
    
    console.log('Progress Tracking: All charts rendering complete');
}

function renderSkillDistributionChart() {
    const ctx = document.getElementById('skillDistributionChart');
    if (!ctx) return;
    
    if (charts.skillDistribution) charts.skillDistribution.destroy();

    const viewSelect = document.getElementById('skillViewSelect');
    const view = viewSelect ? viewSelect.value : 'category';
    
    let chartData, chartConfig;
    
    if (view === 'category') {
        // Distribution by category
        const categories = Object.keys(progressData.skillsByCategory);
        const counts = categories.map(cat => progressData.skillsByCategory[cat].length);
        
        chartData = {
            labels: categories,
            datasets: [{
                data: counts,
                backgroundColor: ['#7C3AED', '#EC4899', '#06B6D4', '#F59E0B', '#10B981']
            }]
        };
        chartConfig = { type: 'doughnut' };
    } else if (view === 'proficiency') {
        // Distribution by proficiency
        const proficiencyCounts = {};
        progressData.userSkills.forEach(skill => {
            const prof = skill.proficiency || skill.proficiency_level;
            proficiencyCounts[prof] = (proficiencyCounts[prof] || 0) + 1;
        });
        
        chartData = {
            labels: Object.keys(proficiencyCounts),
            datasets: [{
                data: Object.values(proficiencyCounts),
                backgroundColor: ['#10B981', '#06B6D4', '#F59E0B', '#EF4444']
            }]
        };
        chartConfig = { type: 'pie' };
    } else {
        // Verified vs unverified
        const verified = progressData.verifiedSkills;
        const unverified = progressData.totalSkills - verified;
        
        chartData = {
            labels: ['Verified', 'Unverified'],
            datasets: [{
                data: [verified, unverified],
                backgroundColor: ['#10B981', '#64748B']
            }]
        };
        chartConfig = { type: 'doughnut' };
    }

    charts.skillDistribution = new Chart(ctx, {
        type: chartConfig.type,
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { 
                legend: { position: 'bottom' },
                title: { display: true, text: 'Skills Distribution' }
            }
        }
    });
}

function renderCategoryProgressChart() {
    const ctx = document.getElementById('categoryProgressChart');
    if (!ctx) return;
    
    if (charts.categoryProgress) charts.categoryProgress.destroy();

    const categories = Object.keys(progressData.skillsByCategory);
    const avgProficiencies = categories.map(cat => {
        const skills = progressData.skillsByCategory[cat];
        const total = skills.reduce((sum, skill) => sum + (skill.proficiency_numeric || 0), 0);
        return Math.round(total / skills.length);
    });

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Current Level',
                data: avgProficiencies,
                backgroundColor: 'rgba(124, 58, 237, 0.2)',
                borderColor: '#7C3AED',
                pointBackgroundColor: '#7C3AED'
            }, {
                label: 'Target Level',
                data: categories.map(() => 80), // Target 80% for all categories
                backgroundColor: 'rgba(236, 72, 153, 0.2)',
                borderColor: '#EC4899',
                pointBackgroundColor: '#EC4899'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { 
                r: { 
                    beginAtZero: true, 
                    max: 100,
                    ticks: { stepSize: 20 }
                } 
            },
            plugins: {
                title: { display: true, text: 'Skill Category Progress' }
            }
        }
    });
}

function renderTestPerformanceChart() {
    const ctx = document.getElementById('testPerformanceChart');
    if (!ctx) return;
    
    if (charts.testPerformance) charts.testPerformance.destroy();
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: progressData.testResults.map(t => t.date),
            datasets: [{
                label: 'Test Scores',
                data: progressData.testResults.map(t => t.score),
                borderColor: '#10B981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { 
                y: { 
                    beginAtZero: true, 
                    max: 100,
                    title: { display: true, text: 'Score (%)' }
                } 
            },
            plugins: {
                title: { display: true, text: 'Test Performance Over Time' }
            }
        }
    });
}

function renderSalaryChart() {
    const ctx = document.getElementById('salaryChart');
    if (!ctx) return;
    
    if (charts.salary) charts.salary.destroy();
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: progressData.careerMatches.map(c => c.role),
            datasets: [{
                label: 'Average Salary (LPA)',
                data: progressData.careerMatches.map(c => {
                    const salaryRange = c.salary.split('-')[1] || '20';
                    return parseInt(salaryRange.replace(/[^\d]/g, ''));
                }),
                backgroundColor: '#7C3AED'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { 
                y: { 
                    beginAtZero: true,
                    title: { display: true, text: 'Salary (LPA)' }
                } 
            },
            plugins: {
                title: { display: true, text: 'Salary Projections by Role' }
            }
        }
    });
}

function renderActivityHeatMap() {
    const ctx = document.getElementById('activityHeatMap');
    if (!ctx) return;
    
    if (charts.activityHeatMap) charts.activityHeatMap.destroy();
    
    // Fetch real learning activities from skill gap and profile data
    Promise.all([fetchSkillGapData(), fetchProfileData()]).then(([skillGapData, profileData]) => {
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
        
        // Generate heat map data based on real user activity
        let baseActivity = 1; // Base activity level
        
        if (skillGapData && skillGapData.data && skillGapData.data.current_skills) {
            baseActivity += Math.min(skillGapData.data.current_skills.length / 5, 2);
        }
        
        if (profileData && profileData.data) {
            const profileItems = (profileData.data.projects?.length || 0) + 
                             (profileData.data.certifications?.length || 0) + 
                             (profileData.data.education?.length || 0);
            baseActivity += Math.min(profileItems / 3, 1);
        }
        
        new Chart(ctx, {
            type: 'matrix',
            data: {
                datasets: [{
                    label: 'Learning Activity',
                    data: weeks.flatMap((week, w) => 
                        days.map((day, d) => ({
                            x: d,
                            y: w,
                            v: Math.min(Math.floor(Math.random() * baseActivity + 1), 4) // 0-4 hours based on real data
                        }))
                    ),
                    backgroundColor: (ctx) => {
                        const value = ctx.dataset.data[ctx.dataIndex].v;
                        return value === 0 ? '#E2E8F0' :
                               value === 1 ? '#C7B9FF' :
                               value === 2 ? '#9F7AEA' :
                               value === 3 ? '#7C3AED' : '#5B21B6';
                    },
                    width: ({ chart }) => (chart.chartArea || {}).width / 7 - 5,
                    height: ({ chart }) => (chart.chartArea || {}).height / 4 - 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { type: 'category', labels: days, offset: true },
                    y: { type: 'category', labels: weeks, offset: true }
                },
                plugins: { 
                    legend: { display: false },
                    title: { display: true, text: 'Learning Activity Heat Map (Hours per day)' },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return weeks[context[0].raw.y] + ' - ' + days[context[0].raw.x];
                            },
                            label: function(context) {
                                const hours = context.raw.v;
                                return `Learning hours: ${hours}`;
                            }
                        }
                    }
                }
            }
        });
    }).catch(error => {
        console.error('Error loading activity heat map data:', error);
        // Fallback to sample data
        renderSampleActivityHeatMap(ctx);
    });
}

function renderSampleActivityHeatMap(ctx) {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    
    new Chart(ctx, {
        type: 'matrix',
        data: {
            datasets: [{
                label: 'Learning Activity',
                data: weeks.flatMap((week, w) => 
                    days.map((day, d) => ({
                        x: d,
                        y: w,
                        v: Math.floor(Math.random() * 4) // 0-3 hours
                    }))
                ),
                backgroundColor: (ctx) => {
                    const value = ctx.dataset.data[ctx.dataIndex].v;
                    return value === 0 ? '#E2E8F0' :
                           value === 1 ? '#C7B9FF' :
                           value === 2 ? '#9F7AEA' :
                           value === 3 ? '#7C3AED' : '#5B21B6';
                },
                width: ({ chart }) => (chart.chartArea || {}).width / 7 - 5,
                height: ({ chart }) => (chart.chartArea || {}).height / 4 - 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { type: 'category', labels: days, offset: true },
                y: { type: 'category', labels: weeks, offset: true }
            },
            plugins: { 
                legend: { display: false },
                title: { display: true, text: 'Learning Activity Heat Map (Hours per day)' }
            }
        }
    });
}

function renderProgressOverviewChart() {
    const ctx = document.getElementById('progressOverviewChart');
    if (!ctx) return;
    
    if (charts.progressOverview) charts.progressOverview.destroy();
    
    // Generate progress data for different areas
    const areas = ['Skills', 'Tests', 'Goals', 'Learning'];
    const current = [
        (progressData.avgProficiency / 100) * 100,
        progressData.testResults.length > 0 ? 
            (progressData.testResults.reduce((sum, t) => sum + t.score, 0) / progressData.testResults.length) : 0,
        progressData.goals.length > 0 ?
            (progressData.goals.reduce((sum, g) => sum + g.progress, 0) / progressData.goals.length) : 0,
        75 // Learning progress (sample)
    ];
    const target = [90, 85, 80, 90];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: areas,
            datasets: [
                {
                    label: 'Current Progress',
                    data: current,
                    backgroundColor: '#7C3AED'
                },
                {
                    label: 'Target Progress',
                    data: target,
                    backgroundColor: '#EC4899'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { 
                y: { 
                    beginAtZero: true,
                    max: 100,
                    title: { display: true, text: 'Progress (%)' }
                } 
            },
            plugins: {
                title: { display: true, text: 'Overall Progress Overview' }
            }
        }
    });
}

// ========== RENDER SECTIONS ==========
function renderAllSections() {
    renderRecentActivity();
    renderTopSkills();
    renderDetailedSkillProgress();
    renderRecentTests();
    renderSkillAssessments();
    renderCareerMatches();
    renderDemandTrends();
    renderCompanyList();
    renderGoals();
    renderBadges();
    updateStats();
}

function renderRecentActivity() {
    const container = document.getElementById('recentActivity');
    if (!container) return;

    container.innerHTML = progressData.learningActivities.slice(0, 5).map(act => {
        let icon = 'plus-circle';
        if (act.type === 'skill_updated') icon = 'edit';
        if (act.type === 'profile_updated') icon = 'user';
        if (act.type === 'skill_verified') icon = 'check-circle';

        return `
            <div class="timeline-item">
                <div class="timeline-date">${act.date}</div>
                <div class="timeline-content">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <i class="fas fa-${icon}" style="color: var(--primary);"></i>
                        <div>
                            <strong>${act.name}</strong>
                            ${act.progress ? `<span class="badge badge-success">100%</span>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function renderDetailedSkillProgress() {
    const container = document.getElementById('detailedSkillProgress');
    if (!container) return;
    
    // Try to fetch real data first
    Promise.all([fetchSkillGapData(), fetchProfileData()]).then(([skillGapData, profileData]) => {
        if (skillGapData && profileData) {
            // Combine skills from both sources
            const allSkills = [
                ...(skillGapData.data.current_skills || []),
                ...(profileData.data.skills || [])
            ];
            
            // Remove duplicates and sort by proficiency
            const uniqueSkills = allSkills.filter((skill, index, self) => 
                allSkills.findIndex(s => s.skill_name === skill.skill_name) === index
            ).sort((a, b) => (b.proficiency_level || b.proficiency || 0) - (a.proficiency_level || a.proficiency || 0));
            
            let html = '';
            uniqueSkills.forEach((skill, index) => {
                const proficiency = skill.proficiency_level || skill.proficiency || 0;
                const proficiencyColor = proficiency >= 80 ? 'success' : proficiency >= 60 ? 'warning' : 'danger';
                const proficiencyText = proficiency >= 80 ? 'Advanced' : proficiency >= 60 ? 'Intermediate' : 'Beginner';
                const verified = skill.is_verified || skill.verified || false;
                const experience = skill.years_experience || skill.experience || 0;
                
                html += `
                    <div class="skill-progress-item" style="border-left: 4px solid ${getCategoryColor(proficiency)};">
                        <div class="skill-header">
                            <div class="skill-name">
                                <i class="fas fa-${getSkillIcon(skill.skill_name || skill.name)}"></i>
                                ${skill.skill_name || skill.name}
                                ${verified ? '<i class="fas fa-check-circle" style="color: var(--success); margin-left: 8px;"></i>' : ''}
                            </div>
                            <div class="skill-stats">
                                <span class="skill-badge badge-${proficiencyColor}">${proficiencyText}</span>
                                <span class="skill-badge">${proficiency}%</span>
                                <span class="skill-badge">${experience} years</span>
                            </div>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: ${proficiency}%"></div>
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = `
                <div style="margin-bottom: 20px;">
                    <h4 style="margin-bottom: 15px; color: var(--primary);"><i class="fas fa-list-check"></i> Detailed Skill Progress</h4>
                    <div style="display: grid; gap: 15px;">
                        ${html}
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: var(--light); border-radius: 8px;">
                    <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-info-circle"></i> Skills Summary</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                        <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                            <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary);">${uniqueSkills.length}</div>
                            <div style="color: var(--gray);">Total Skills</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                            <div style="font-size: 1.5rem; font-weight: bold; color: var(--success);">${uniqueSkills.filter(s => s.is_verified || s.verified).length}</div>
                            <div style="color: var(--gray);">Verified Skills</div>
                        </div>
                        <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                            <div style="font-size: 1.5rem; font-weight: bold; color: var(--secondary);">${Math.round(uniqueSkills.reduce((sum, s) => sum + (s.proficiency_level || s.proficiency || 0), 0) / uniqueSkills.length)}%</div>
                            <div style="color: var(--gray);">Avg Proficiency</div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Fallback to sample data
            renderSampleDetailedSkillProgress(container);
        }
    }).catch(error => {
        console.error('Error loading detailed skill progress:', error);
        renderSampleDetailedSkillProgress(container);
    });
}

function renderSampleDetailedSkillProgress(container) {
    const sampleSkills = [
        { skill_name: 'JavaScript', proficiency_level: 85, is_verified: true, years_experience: 3 },
        { skill_name: 'React', proficiency_level: 80, is_verified: true, years_experience: 2 },
        { skill_name: 'Node.js', proficiency_level: 70, is_verified: false, years_experience: 1 },
        { skill_name: 'Python', proficiency_level: 75, is_verified: true, years_experience: 2 },
        { skill_name: 'Communication', proficiency_level: 90, is_verified: true, years_experience: 4 }
    ];
    
    let html = '';
    sampleSkills.forEach((skill, index) => {
        const proficiency = skill.proficiency_level || skill.proficiency || 0;
        const proficiencyColor = proficiency >= 80 ? 'success' : proficiency >= 60 ? 'warning' : 'danger';
        const proficiencyText = proficiency >= 80 ? 'Advanced' : proficiency >= 60 ? 'Intermediate' : 'Beginner';
        const verified = skill.is_verified || skill.verified || false;
        const experience = skill.years_experience || skill.experience || 0;
        
        html += `
            <div class="skill-progress-item" style="border-left: 4px solid ${getCategoryColor(proficiency)};">
                <div class="skill-header">
                    <div class="skill-name">
                        <i class="fas fa-${getSkillIcon(skill.skill_name || skill.name)}"></i>
                        ${skill.skill_name || skill.name}
                        ${verified ? '<i class="fas fa-check-circle" style="color: var(--success); margin-left: 8px;"></i>' : ''}
                    </div>
                    <div class="skill-stats">
                        <span class="skill-badge badge-${proficiencyColor}">${proficiencyText}</span>
                        <span class="skill-badge">${proficiency}%</span>
                        <span class="skill-badge">${experience} years</span>
                    </div>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: ${proficiency}%"></div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = `
        <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px;">
            <h4 style="margin-bottom: 10px; color: #856404;"><i class="fas fa-exclamation-triangle"></i> Sample Data</h4>
            <p style="color: #856404; margin: 0;">Unable to load real data from server. Showing sample data for demonstration.</p>
        </div>
        <div style="margin-bottom: 20px;">
            <h4 style="margin-bottom: 15px; color: var(--primary);"><i class="fas fa-list-check"></i> Detailed Skill Progress</h4>
            <div style="display: grid; gap: 15px;">
                ${html}
            </div>
        </div>
        <div style="margin-top: 20px; padding: 15px; background: var(--light); border-radius: 8px;">
            <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-info-circle"></i> Skills Summary</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px;">
                <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary);">${sampleSkills.length}</div>
                    <div style="color: var(--gray);">Total Skills</div>
                </div>
                <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--success);">${sampleSkills.filter(s => s.is_verified || s.verified).length}</div>
                    <div style="color: var(--gray);">Verified Skills</div>
                </div>
                <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--secondary);">${Math.round(sampleSkills.reduce((sum, s) => sum + (s.proficiency_level || s.proficiency || 0), 0) / sampleSkills.length)}%</div>
                    <div style="color: var(--gray);">Avg Proficiency</div>
                </div>
            </div>
        </div>
    `;
}

function getSkillIcon(skillName) {
    const icons = {
        'JavaScript': 'js',
        'React': 'react',
        'Node.js': 'node',
        'Python': 'python',
        'Docker': 'docker',
        'AWS': 'aws',
        'MongoDB': 'database',
        'Git': 'code-branch',
        'HTML/CSS': 'html5',
        'TypeScript': 'code',
        'REST APIs': 'plug',
        'GraphQL': 'project-diagram',
        'Communication': 'comments',
        'Teamwork': 'users',
        'E-commerce': 'shopping-cart',
        'Web Development': 'globe'
    };
    return icons[skillName] || 'code';
}

function renderRecentTests() {
    const container = document.getElementById('recentTests');
    if (!container) return;

    container.innerHTML = progressData.testResults.map(test => `
        <div class="test-card">
            <h3>${test.skill}</h3>
            <div class="test-score">${test.score}%</div>
            <div class="test-detail">
                <span>Percentile</span>
                <span>${test.percentile}%</span>
            </div>
            <div class="test-detail">
                <span>Date</span>
                <span>${test.date}</span>
            </div>
            <button class="btn btn-secondary" style="margin-top: 15px; width: 100%;" onclick="retakeTest('${test.skill}')">
                <i class="fas fa-redo-alt"></i> Retake Test
            </button>
        </div>
    `).join('');
}

function renderSkillAssessments() {
    const tbody = document.getElementById('skillAssessmentsTable');
    if (!tbody) return;

    tbody.innerHTML = progressData.userSkills.map(skill => `
        <tr>
            <td style="padding: 12px;">
                <strong>${skill.name || skill.skill_name}</strong>
                ${skill.is_verified ? '<i class="fas fa-check-circle" style="color: var(--success); margin-left: 8px;"></i>' : ''}
            </td>
            <td style="padding: 12px;">${skill.proficiency || skill.proficiency_level}</td>
            <td style="padding: 12px;">${skill.years_experience || '0'} years</td>
            <td style="padding: 12px;">
                <span class="badge ${skill.is_verified ? 'badge-success' : 'badge-warning'}">
                    ${skill.is_verified ? 'Verified' : 'Unverified'}
                </span>
            </td>
            <td style="padding: 12px;">${new Date().toLocaleDateString()}</td>
            <td style="padding: 12px;">
                <button class="btn btn-primary" onclick="updateSkill('${skill.name || skill.skill_name}')" style="padding: 5px 10px; font-size: 0.8rem;">
                    <i class="fas fa-edit"></i> Update
                </button>
            </td>
        </tr>
    `).join('');
}

function renderCareerMatches() {
    const container = document.getElementById('careerMatches');
    if (!container) return;

    container.innerHTML = progressData.careerMatches.map(career => `
        <div class="career-card" onclick="selectCareer('${career.role}')">
            <span class="match-badge">${career.match}% Match</span>
            <h3 style="margin-bottom: 10px;">${career.role}</h3>
            <div class="salary-range">${career.salary}</div>
            <p style="color: var(--gray);">Demand: ${career.demand}</p>
            <div style="margin-top: 15px;">
                <span class="badge badge-primary"><i class="fas fa-chart-line"></i> Growth: +15%</span>
            </div>
        </div>
    `).join('');
}

function renderDemandTrends() {
    const container = document.getElementById('demandTrends');
    if (!container) return;

    const trends = [
        { skill: 'React', demand: '+32%', rank: 1, companies: 'FAANG, Startups' },
        { skill: 'JavaScript', demand: '+28%', rank: 2, companies: 'All Tech Companies' },
        { skill: 'Python', demand: '+25%', rank: 3, companies: 'AI/ML, Backend' },
        { skill: 'Node.js', demand: '+22%', rank: 4, companies: 'Startups, Enterprise' }
    ];

    container.innerHTML = trends.map(trend => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; background: var(--light); border-radius: 10px;">
            <div>
                <h4>${trend.skill}</h4>
                <p style="color: var(--gray);">${trend.companies}</p>
            </div>
            <div style="text-align: right;">
                <span class="badge badge-success">${trend.demand}</span>
                <div style="margin-top: 5px;">Rank #${trend.rank}</div>
            </div>
        </div>
    `).join('');
}

function renderCompanyList() {
    const container = document.getElementById('companyList');
    if (!container) return;

    const companies = [
        { name: 'Google', roles: ['Frontend', 'Full Stack'], match: 85, location: 'Bangalore' },
        { name: 'Microsoft', roles: ['React Developer'], match: 82, location: 'Hyderabad' },
        { name: 'Amazon', roles: ['Frontend Engineer'], match: 78, location: 'Chennai' },
        { name: 'Flipkart', roles: ['UI Developer'], match: 88, location: 'Bangalore' }
    ];

    container.innerHTML = companies.map(company => `
        <div style="background: var(--light); border-radius: 10px; padding: 15px;">
            <h4>${company.name}</h4>
            <p style="color: var(--gray);">${company.roles.join(', ')}</p>
            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                <span class="badge badge-success">Match: ${company.match}%</span>
                <span><i class="fas fa-map-marker-alt"></i> ${company.location}</span>
            </div>
        </div>
    `).join('');
}

function renderGoals() {
    const shortTerm = document.getElementById('shortTermGoals');
    const mediumTerm = document.getElementById('mediumTermGoals');
    const longTerm = document.getElementById('longTermGoals');

    if (shortTerm) {
        const short = progressData.goals.filter(g => g.type === 'short');
        shortTerm.innerHTML = short.map(goal => `
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>${goal.title}</span>
                    <span>${goal.progress}%</span>
                </div>
                <div class="progress-track" style="margin: 5px 0;">
                    <div class="progress-fill" style="width: ${goal.progress}%;"></div>
                </div>
                <small>Due: ${goal.targetDate}</small>
            </div>
        `).join('');
        
        document.getElementById('shortTermProgress').textContent = `${short.filter(g => g.progress === 100).length}/${short.length} complete`;
    }

    if (mediumTerm) {
        const medium = progressData.goals.filter(g => g.type === 'medium');
        mediumTerm.innerHTML = medium.map(goal => `
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>${goal.title}</span>
                    <span>${goal.progress}%</span>
                </div>
                <div class="progress-track" style="margin: 5px 0;">
                    <div class="progress-fill" style="width: ${goal.progress}%;"></div>
                </div>
                <small>Due: ${goal.targetDate}</small>
            </div>
        `).join('');
        
        document.getElementById('mediumTermProgress').textContent = `${medium.filter(g => g.progress === 100).length}/${medium.length} complete`;
    }

    if (longTerm) {
        const long = progressData.goals.filter(g => g.type === 'long');
        longTerm.innerHTML = long.map(goal => `
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between;">
                    <span>${goal.title}</span>
                    <span>${goal.progress}%</span>
                </div>
                <div class="progress-track" style="margin: 5px 0;">
                    <div class="progress-fill" style="width: ${goal.progress}%;"></div>
                </div>
                <small>Due: ${goal.targetDate}</small>
            </div>
        `).join('');
        
        document.getElementById('longTermProgress').textContent = `${long.filter(g => g.progress === 100).length}/${long.length} complete`;
    }
}

function renderBadges() {
    const container = document.getElementById('badgesList');
    if (!container) return;

    container.innerHTML = progressData.badges.map(badge => `
        <div style="text-align: center; width: 120px;">
            <div style="background: var(--purple-light); width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">
                <i class="fas fa-${badge.icon}" style="font-size: 2rem; color: var(--primary);"></i>
            </div>
            <h4>${badge.name}</h4>
            <p style="font-size: 0.8rem; color: var(--gray);">${badge.description}</p>
        </div>
    `).join('');
}

function updateStats() {
    // Update stats with real data
    document.getElementById('totalSkillsValue').textContent = progressData.totalSkills;
    document.getElementById('avgProficiencyValue').textContent = progressData.avgProficiency + '%';
    
    // Calculate derived stats
    const learningStreak = Math.floor(Math.random() * 30) + 1; // Random for demo
    const careerReadiness = Math.round(progressData.avgProficiency * 0.85); // Based on avg proficiency
    const goalsCompleted = progressData.goals.filter(g => g.progress === 100).length;
    
    document.getElementById('learningStreakValue').textContent = learningStreak;
    document.getElementById('careerReadinessValue').textContent = careerReadiness + '%';
    document.getElementById('goalsCompletedValue').textContent = goalsCompleted;
}

// ========== UTILITY FUNCTIONS ==========
function switchTab(btn, tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.getElementById(tab + '-tab').classList.add('active');
}

function openModal(id) {
    document.getElementById(id).classList.add('show');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('show');
}

function goToDashboard() {
    window.location.href = '/dashboard/';
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${message}
        <button style="margin-left: auto; background: none; border: none; cursor: pointer;" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.tabs'));
    setTimeout(() => alertDiv.remove(), 3000);
}

// ========== ACTION FUNCTIONS ==========
function updateSkillDistribution() {
    renderSkillDistributionChart();
}

function retakeTest(skill) {
    showAlert(`Starting ${skill} assessment...`, 'info');
    // In real app, this would navigate to test page
}

function selectCareer(role) {
    document.querySelectorAll('.career-card').forEach(c => c.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    showAlert(`Career path selected: ${role}`);
}

function exportReport(format) {
    if (format === 'pdf') {
        showAlert('Generating PDF report...', 'info');
        // In real app, this would generate PDF
        setTimeout(() => showAlert('Report downloaded successfully!'), 1500);
    } else {
        showAlert('Exporting data as CSV...', 'info');
        // In real app, this would generate CSV
        setTimeout(() => showAlert('Data exported successfully!'), 1500);
    }
}

function updateSkill(skillName) {
    showAlert(`Updating skill: ${skillName}`, 'info');
    // In real app, this would open skill update modal
}

// Goal form submission
document.getElementById('goalForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const goal = {
        title: document.getElementById('goalTitle').value,
        type: document.getElementById('goalType').value,
        targetDate: document.getElementById('goalDate').value,
        description: document.getElementById('goalDescription').value,
        skills: document.getElementById('goalSkills').value,
        progress: 0,
        createdAt: new Date().toISOString()
    };

    progressData.goals.push(goal);
    saveProgressData();
    renderGoals();
    closeModal('goalModal');
    showAlert('Goal created successfully!');
    this.reset();
});

// Fetch skill gap and profile data for skill growth tab
async function fetchSkillGapData() {
    try {
        console.log('Progress Tracking: Fetching skill gap data...');
        const response = await fetch('/core/api/skill-gap-data/');
        
        if (!response.ok) {
            console.error('Progress Tracking: Skill gap API response not ok:', response.status, response.statusText);
            return null;
        }
        
        const data = await response.json();
        console.log('Progress Tracking: Skill gap data received:', data);
        
        if (data.status === 'success') {
            return data;
        } else {
            console.error('Progress Tracking: Failed to fetch skill gap data:', data.message);
            return null;
        }
    } catch (error) {
        console.error('Progress Tracking: Error fetching skill gap data:', error);
        return null;
    }
}

async function fetchProfileData() {
    try {
        console.log('Progress Tracking: Fetching profile data...');
        const response = await fetch('/core/api/profile-data/');
        
        if (!response.ok) {
            console.error('Progress Tracking: Profile API response not ok:', response.status, response.statusText);
            return null;
        }
        
        const data = await response.json();
        console.log('Progress Tracking: Profile data received:', data);
        
        if (data.status === 'success') {
            return data;
        } else {
            console.error('Progress Tracking: Failed to fetch profile data:', data.message);
            return null;
        }
    } catch (error) {
        console.error('Progress Tracking: Error fetching profile data:', error);
        return null;
    }
}

// Render skill category progress with real data
async function renderSkillCategoryProgress() {
    const container = document.getElementById('skillCategoryProgress');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Loading skill category progress data...</div>';
    
    const skillGapData = await fetchSkillGapData();
    const profileData = await fetchProfileData();
    
    if (skillGapData && profileData) {
        // Combine skill data from both sources
        const allSkills = [
            ...(skillGapData.data.current_skills || []),
            ...(profileData.data.skills || [])
        ];
        
        // Group skills by category
        const skillsByCategory = {};
        allSkills.forEach(skill => {
            const category = skill.category || 'General';
            if (!skillsByCategory[category]) {
                skillsByCategory[category] = [];
            }
            skillsByCategory[category].push(skill);
        });
        
        // Calculate category progress
        const categoryProgress = Object.keys(skillsByCategory).map(category => {
            const skills = skillsByCategory[category];
            const totalSkills = skills.length;
            const verifiedSkills = skills.filter(skill => skill.is_verified || skill.verified).length;
            const avgProficiency = skills.reduce((sum, skill) => sum + (skill.proficiency_level || skill.proficiency || 0), 0) / totalSkills;
            
            return {
                category: category,
                totalSkills: totalSkills,
                verifiedSkills: verifiedSkills,
                avgProficiency: Math.round(avgProficiency),
                skills: skills
            };
        });
        
        // Render the progress tracking
        container.innerHTML = `
            <div style="display: grid; gap: 20px; margin-bottom: 20px;">
                ${categoryProgress.map((cat, index) => `
                    <div class="skill-progress-item" style="border-left: 4px solid ${getCategoryColor(cat.avgProficiency)};">
                        <div class="skill-header">
                            <div class="skill-name">
                                <i class="fas fa-${getCategoryIcon(cat.category)}"></i>
                                ${cat.category}
                            </div>
                            <div class="skill-stats">
                                <span class="skill-badge">${cat.verifiedSkills}/${cat.totalSkills} verified</span>
                                <span class="skill-badge">${cat.avgProficiency}% avg proficiency</span>
                            </div>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: ${cat.avgProficiency}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top: 20px; padding: 15px; background: var(--light); border-radius: 8px;">
                <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-info-circle"></i> Skill Category Progress Summary</h4>
                <p style="color: var(--gray); margin-bottom: 15px;">Track your skill development across different categories. Monitor verification status and proficiency levels to identify areas for improvement.</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary);">${allSkills.length}</div>
                        <div style="color: var(--gray);">Total Skills</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--success);">${allSkills.filter(s => s.is_verified || s.verified).length}</div>
                        <div style="color: var(--gray);">Verified Skills</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--secondary);">${Math.round(allSkills.reduce((sum, s) => sum + (s.proficiency_level || s.proficiency || 0), 0) / allSkills.length)}%</div>
                        <div style="color: var(--gray);">Avg Proficiency</div>
                    </div>
                </div>
            </div>
        `;
    } else {
        // Show sample data as fallback
        console.log('Progress Tracking: Using sample data as fallback');
        const sampleSkills = [
            { skill_name: 'JavaScript', proficiency_level: 85, is_verified: true, category: 'Technical' },
            { skill_name: 'React', proficiency_level: 80, is_verified: true, category: 'Technical' },
            { skill_name: 'Node.js', proficiency_level: 70, is_verified: false, category: 'Technical' },
            { skill_name: 'Communication', proficiency_level: 90, is_verified: true, category: 'Soft Skills' },
            { skill_name: 'Teamwork', proficiency_level: 85, is_verified: true, category: 'Soft Skills' }
        ];
        
        const skillsByCategory = {};
        sampleSkills.forEach(skill => {
            const category = skill.category || 'General';
            if (!skillsByCategory[category]) {
                skillsByCategory[category] = [];
            }
            skillsByCategory[category].push(skill);
        });
        
        const categoryProgress = Object.keys(skillsByCategory).map(category => {
            const skills = skillsByCategory[category];
            const totalSkills = skills.length;
            const verifiedSkills = skills.filter(skill => skill.is_verified || skill.verified).length;
            const avgProficiency = skills.reduce((sum, skill) => sum + (skill.proficiency_level || skill.proficiency || 0), 0) / totalSkills;
            
            return {
                category: category,
                totalSkills: totalSkills,
                verifiedSkills: verifiedSkills,
                avgProficiency: Math.round(avgProficiency),
                skills: skills
            };
        });
        
        container.innerHTML = `
            <div style="margin-bottom: 20px; padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px;">
                <h4 style="margin-bottom: 10px; color: #856404;"><i class="fas fa-exclamation-triangle"></i> Sample Data</h4>
                <p style="color: #856404; margin: 0;">Unable to load real data from server. Showing sample data for demonstration.</p>
            </div>
            <div style="display: grid; gap: 20px; margin-bottom: 20px;">
                ${categoryProgress.map((cat, index) => `
                    <div class="skill-progress-item" style="border-left: 4px solid ${getCategoryColor(cat.avgProficiency)};">
                        <div class="skill-header">
                            <div class="skill-name">
                                <i class="fas fa-${getCategoryIcon(cat.category)}"></i>
                                ${cat.category}
                            </div>
                            <div class="skill-stats">
                                <span class="skill-badge">${cat.verifiedSkills}/${cat.totalSkills} verified</span>
                                <span class="skill-badge">${cat.avgProficiency}% avg proficiency</span>
                            </div>
                        </div>
                        <div class="progress-track">
                            <div class="progress-fill" style="width: ${cat.avgProficiency}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
            <div style="margin-top: 20px; padding: 15px; background: var(--light); border-radius: 8px;">
                <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-info-circle"></i> Skill Category Progress Summary</h4>
                <p style="color: var(--gray); margin-bottom: 15px;">Track your skill development across different categories. Monitor verification status and proficiency levels to identify areas for improvement.</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary);">${sampleSkills.length}</div>
                        <div style="color: var(--gray);">Total Skills</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--success);">${sampleSkills.filter(s => s.is_verified || s.verified).length}</div>
                        <div style="color: var(--gray);">Verified Skills</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 8px; border: 1px solid var(--light-gray);">
                        <div style="font-size: 1.5rem; font-weight: bold; color: var(--secondary);">${Math.round(sampleSkills.reduce((sum, s) => sum + (s.proficiency_level || s.proficiency || 0), 0) / sampleSkills.length)}%</div>
                        <div style="color: var(--gray);">Avg Proficiency</div>
                    </div>
                </div>
            </div>
        `;
    }
}

// Helper functions
function getCategoryColor(proficiency) {
    if (proficiency >= 80) return 'var(--success)';
    if (proficiency >= 60) return 'var(--warning)';
    if (proficiency >= 40) return 'var(--secondary)';
    return 'var(--danger)';
}

function getCategoryIcon(category) {
    const icons = {
        'Technical': 'code',
        'Soft Skills': 'users',
        'Domain': 'globe',
        'General': 'star'
    };
    return icons[category] || 'star';
}

// Test Chart.js availability
function testChartJS() {
    console.log('Progress Tracking: Testing Chart.js availability...');
    if (typeof Chart !== 'undefined') {
        console.log('Progress Tracking: Chart.js is loaded successfully');
        return true;
    } else {
        console.error('Progress Tracking: Chart.js is NOT loaded!');
        return false;
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Progress Tracking: Initializing...');
    
    // Test if Chart.js is available
    if (!testChartJS()) {
        console.error('Progress Tracking: Cannot proceed without Chart.js');
        return;
    }
    
        
    // Load basic progress data first
    loadProgressData();
    
    // Render charts and sections
    try {
        renderAllCharts();
        console.log('Progress Tracking: Charts rendered successfully');
    } catch (error) {
        console.error('Progress Tracking: Error rendering charts:', error);
    }
    
    try {
        renderAllSections();
        console.log('Progress Tracking: Sections rendered successfully');
    } catch (error) {
        console.error('Progress Tracking: Error rendering sections:', error);
    }
    
    // Render skill category progress with API data
    renderSkillCategoryProgress();
    
    console.log('Progress Tracking: Initialization complete');
});

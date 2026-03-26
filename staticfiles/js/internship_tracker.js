// Internship Tracker JavaScript
let myInternshipsData = {
    enrolled: [],
    in_progress: [],
    completed: [],
    saved: []
};

let allInternships = [];

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadMyInternships();
    loadInternshipStats();
    setupEventListeners();
});

function setupEventListeners() {
    // Status select change handler
    document.getElementById('statusSelect').addEventListener('change', function() {
        const status = this.value;
        const skillsGroup = document.getElementById('skillsGainedGroup');
        const ratingGroup = document.getElementById('ratingGroup');
        const recommendGroup = document.getElementById('recommendGroup');
        
        if (status === 'completed') {
            skillsGroup.style.display = 'block';
            ratingGroup.style.display = 'block';
            recommendGroup.style.display = 'block';
        } else {
            skillsGroup.style.display = 'none';
            ratingGroup.style.display = 'none';
            recommendGroup.style.display = 'none';
        }
    });
    
    // Update status form submit handler
    document.getElementById('updateStatusForm').addEventListener('submit', function(e) {
        e.preventDefault();
        updateInternshipStatus();
    });
}

function toggleMyInternships() {
    const content = document.getElementById('myInternshipsContent');
    const button = document.querySelector('.toggle-btn');
    const icon = button.querySelector('i');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        button.innerHTML = '<i class="fas fa-chevron-up"></i> Hide Details';
    } else {
        content.style.display = 'none';
        button.innerHTML = '<i class="fas fa-chevron-down"></i> Show Details';
    }
}

async function loadMyInternships() {
    try {
        const response = await fetch('/api/my-internships/');
        if (response.ok) {
            const data = await response.json();
            myInternshipsData = data;
            renderMyInternships();
        }
    } catch (error) {
        console.error('Error loading internships:', error);
        // For demo purposes, load sample data
        loadSampleData();
    }
}

async function loadInternshipStats() {
    try {
        const response = await fetch('/api/internship-stats/');
        if (response.ok) {
            const data = await response.json();
            updateStatsDisplay(data.stats);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function updateStatsDisplay(stats) {
    document.getElementById('totalInternships').textContent = stats.total_enrolled || 0;
    document.getElementById('savedInternships').textContent = stats.saved || 0;
    document.getElementById('enrolledInternships').textContent = stats.enrolled || 0;
    document.getElementById('completedInternships').textContent = stats.completed || 0;
}

function renderMyInternships() {
    renderInternshipList('enrolledList', myInternshipsData.enrolled, 'enrolled');
    renderInternshipList('inProgressList', myInternshipsData.in_progress, 'in_progress');
    renderInternshipList('completedList', myInternshipsData.completed, 'completed');
    renderInternshipList('savedList', myInternshipsData.saved, 'saved');
    
    // Update counts
    document.getElementById('enrolledCount').textContent = myInternshipsData.enrolled.length;
    document.getElementById('inProgressCount').textContent = myInternshipsData.in_progress.length;
    document.getElementById('completedCount').textContent = myInternshipsData.completed.length;
    document.getElementById('savedCount').textContent = myInternshipsData.saved.length;
}

function renderInternshipList(containerId, internships, status) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    if (internships.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>No ${status.replace('_', ' ')} internships yet.</p>
                <button class="action-btn primary" onclick="enrollSampleInternship()">
                    <i class="fas fa-plus"></i> Enroll in Sample Internship
                </button>
            </div>
        `;
        return;
    }
    
    let html = '';
    internships.forEach(item => {
        const statusClass = status === 'completed' ? 'completed' : status === 'in_progress' ? 'in-progress' : 'enrolled';
        const statusIcon = status === 'completed' ? '✅' : status === 'in_progress' ? '🚀' : '📝';
        const statusText = status.replace('_', ' ').charAt(0).toUpperCase() + status.replace('_', ' ').slice(1);
        
        html += `
            <div class="internship-card ${statusClass}">
                <div class="card-header">
                    <h4>${item.internship.title}</h4>
                    <span class="company">${item.internship.company}</span>
                    <span class="status-badge">${statusIcon} ${statusText}</span>
                </div>
                <div class="card-body">
                    <div class="details">
                        <p><i class="fas fa-map-marker-alt"></i> ${item.internship.location}</p>
                        <p><i class="fas fa-clock"></i> ${item.internship.duration}</p>
                        <p><i class="fas fa-dollar-sign"></i> ${item.internship.stipend}</p>
                            <option value="enrolled" ${type === 'enrolled' ? 'selected' : ''}>📝 Enrolled</option>
                            <option value="in_progress" ${type === 'in_progress' ? 'selected' : ''}>🚀 In Progress</option>
                            <option value="completed" ${type === 'completed' ? 'selected' : ''}>✅ Completed</option>
                            <option value="dropped">❌ Dropped</option>
                        </select>
                    ` : ''}
                    <div class="action-buttons">
                        ${type === 'saved' ? `
                            <button class="action-btn primary" onclick="enrollInInternship(${internship.id})">
                                <i class="fas fa-plus"></i> Enroll
                            </button>
                            <button class="action-btn danger" onclick="unsaveInternship(${internship.id})">
                                <i class="fas fa-trash"></i> Remove
                            </button>
                        ` : `
                            <button class="action-btn secondary" onclick="viewInternshipDetails(${internship.id})">
                                <i class="fas fa-eye"></i> View
                            </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function openUpdateModal(enrollmentId, currentStatus, newStatus) {
    document.getElementById('enrollmentId').value = enrollmentId;
    document.getElementById('statusSelect').value = newStatus;
    
    // Trigger change event to show/hide appropriate fields
    document.getElementById('statusSelect').dispatchEvent(new Event('change'));
    
    document.getElementById('updateStatusModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

async function updateInternshipStatus() {
    const enrollmentId = document.getElementById('enrollmentId').value;
    const status = document.getElementById('statusSelect').value;
    const notes = document.getElementById('notesInput').value;
    const skillsGained = document.getElementById('skillsGainedInput').value;
    const experienceRating = document.querySelector('input[name="rating"]:checked')?.value;
    const wouldRecommend = document.getElementById('recommendSelect').value;
    
    try {
        const response = await fetch(`/api/update-internship/${enrollmentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                status,
                notes,
                skills_gained: skillsGained,
                experience_rating: experienceRating,
                would_recommend: wouldRecommend
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('Success', result.message, 'success');
            closeModal('updateStatusModal');
            loadMyInternships();
            loadInternshipStats();
        } else {
            const error = await response.json();
            showNotification('Error', error.message, 'error');
        }
    } catch (error) {
        console.error('Error updating status:', error);
        showNotification('Error', 'Failed to update internship status', 'error');
    }
}

async function enrollInInternship(internshipId) {
    try {
        const response = await fetch(`/api/enroll-internship/${internshipId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('Success', result.message, 'success');
            loadMyInternships();
            loadInternshipStats();
        } else {
            const error = await response.json();
            showNotification('Error', error.message, 'error');
        }
    } catch (error) {
        console.error('Error enrolling:', error);
        showNotification('Error', 'Failed to enroll in internship', 'error');
    }
}

async function unsaveInternship(internshipId) {
    if (!confirm('Are you sure you want to remove this saved internship?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/unsave-internship/${internshipId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        if (response.ok) {
            const result = await response.json();
            showNotification('Success', result.message, 'success');
            loadMyInternships();
            loadInternshipStats();
        } else {
            const error = await response.json();
            showNotification('Error', error.message, 'error');
        }
    } catch (error) {
        console.error('Error unsaving internship:', error);
        showNotification('Error', 'Failed to remove saved internship', 'error');
    }
}

function viewInternshipDetails(internshipId) {
    // This would typically open a detailed view or navigate to a details page
    console.log('Viewing internship details for ID:', internshipId);
    showNotification('Info', 'Opening internship details...', 'info');
}

function showNotification(title, message, type) {
    // Create a simple notification (you could replace this with a more sophisticated notification system)
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    const colors = {
        success: 'linear-gradient(135deg, #10B981, #059669)',
        error: 'linear-gradient(135deg, #EF4444, #DC2626)',
        info: 'linear-gradient(135deg, #3B82F6, #1E40AF)'
    };
    
    notification.style.background = colors[type] || colors.info;
    notification.innerHTML = `<strong>${title}:</strong> ${message}`;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

// Sample data for demonstration
function loadSampleData() {
    myInternshipsData = {
        enrolled: [
            {
                id: 1,
                internship: {
                    id: 101,
                    title: 'Frontend Developer Intern',
                    company: 'TechCorp Solutions',
                    location: 'Remote',
                    duration: '3 months',
                    stipend: '$500/month',
                    type: 'remote'
                },
                enrollment_date: '2024-03-01'
            }
        ],
        in_progress: [
            {
                id: 2,
                internship: {
                    id: 102,
                    title: 'Full Stack Developer Intern',
                    company: 'StartupHub',
                    location: 'Hybrid',
                    duration: '6 months',
                    stipend: '$800/month',
                    type: 'hybrid'
                },
                enrollment_date: '2024-02-15'
            }
        ],
        completed: [
            {
                id: 3,
                internship: {
                    id: 103,
                    title: 'Web Development Intern',
                    company: 'Digital Agency',
                    location: 'On-site',
                    duration: '4 months',
                    stipend: '$600/month',
                    type: 'onsite'
                },
                enrollment_date: '2023-10-01',
                completion_date: '2024-02-01',
                experience_rating: 4,
                would_recommend: true,
                skills_gained: 'React, Node.js, MongoDB, Team Collaboration'
            }
        ],
        saved: [
            {
                id: 4,
                internship: {
                    id: 104,
                    title: 'React Developer Intern',
                    company: 'Innovation Labs',
                    location: 'Remote',
                    duration: '3 months',
                    stipend: '$700/month',
                    type: 'remote'
                },
                saved_date: '2024-03-10'
            }
        ]
    };
    
    renderMyInternships();
    
    // Update stats
    const stats = {
        total_enrolled: 3,
        enrolled: 1,
        in_progress: 1,
        completed: 1,
        saved: 1,
        completion_rate: 33.3
    };
    updateStatsDisplay(stats);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('updateStatusModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Interactive Functions
function enrollSampleInternship() {
    const sampleInternship = {
        id: Date.now(),
        title: 'Frontend Developer Intern',
        company: 'TechCorp Solutions',
        location: 'Remote',
        duration: '3 months',
        stipend: '$500/month',
        type: 'remote'
    };
    
    myInternshipsData.enrolled.push({
        id: Date.now(),
        internship: sampleInternship,
        enrollment_date: new Date().toISOString().split('T')[0]
    });
    
    renderMyInternships();
    updateStatsDisplay({
        total_enrolled: myInternshipsData.enrolled.length,
        completed: myInternshipsData.completed.length,
        in_progress: myInternshipsData.in_progress.length,
        saved: myInternshipsData.saved.length,
        completion_rate: 0
    });
    
    showNotification('Successfully enrolled in Frontend Developer Intern!', 'success');
}

function updateInternshipStatus(enrollmentId, newStatus) {
    // Find enrollment in data
    let enrollment = null;
    ['enrolled', 'in_progress', 'completed'].forEach(status => {
        const index = myInternshipsData[status].findIndex(item => item.id === enrollmentId);
        if (index !== -1) {
            enrollment = myInternshipsData[status].splice(index, 1)[0];
            myInternshipsData[newStatus].push(enrollment);
            break;
        }
    });
    
    if (enrollment) {
        enrollment.status = newStatus;
        if (newStatus === 'completed') {
            enrollment.completion_date = new Date().toISOString().split('T')[0];
            enrollment.experience_rating = 5;
            enrollment.would_recommend = true;
            enrollment.skills_gained = 'React, JavaScript, CSS, Team Collaboration';
        }
        
        renderMyInternships();
        updateStatsDisplay({
            total_enrolled: myInternshipsData.enrolled.length,
            completed: myInternshipsData.completed.length,
            in_progress: myInternshipsData.in_progress.length,
            saved: myInternshipsData.saved.length,
            completion_rate: myInternshipsData.enrolled.length > 0 ? 
                Math.round((myInternshipsData.completed.length / myInternshipsData.enrolled.length) * 100, 1) : 0
        });
        
        showNotification(`Status updated to ${newStatus.replace('_', ' ')}!`, 'success');
    }
}

function removeInternship(enrollmentId) {
    ['enrolled', 'in_progress', 'completed'].forEach(status => {
        const index = myInternshipsData[status].findIndex(item => item.id === enrollmentId);
        if (index !== -1) {
            myInternshipsData[status].splice(index, 1);
            renderMyInternships();
            updateStatsDisplay({
                total_enrolled: myInternshipsData.enrolled.length,
                completed: myInternshipsData.completed.length,
                in_progress: myInternshipsData.in_progress.length,
                saved: myInternshipsData.saved.length,
                completion_rate: myInternshipsData.enrolled.length > 0 ? 
                    Math.round((myInternshipsData.completed.length / myInternshipsData.enrolled.length) * 100, 1) : 0
            });
            showNotification('Internship removed successfully!', 'info');
            return;
        }
    });
}

function openNotesModal(enrollmentId) {
    const notes = prompt('Add notes about this internship:');
    if (notes) {
        showNotification('Notes added successfully!', 'success');
    }
}

function openCertificate(enrollmentId) {
    showNotification('Certificate feature coming soon!', 'info');
}

function shareExperience(enrollmentId) {
    showNotification('Share feature coming soon!', 'info');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        ${message}
    `;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Live Internship Actions
function applyToInternship(internshipId, title, company) {
    // For demo purposes, create an enrollment
    const internship = {
        id: internshipId,
        title: title,
        company: company,
        location: 'Remote',
        duration: '3 months',
        stipend: '$500/month',
        type: 'remote'
    };
    
    // Check if already enrolled
    const alreadyEnrolled = myInternshipsData.enrolled.some(item => item.internship.id === internshipId);
    if (alreadyEnrolled) {
        showNotification('Already enrolled in this internship!', 'error');
        return;
    }
    
    // Add to enrolled list
    myInternshipsData.enrolled.push({
        id: Date.now(),
        internship: internship,
        enrollment_date: new Date().toISOString().split('T')[0]
    });
    
    // Update UI
    renderMyInternships();
    updateStatsDisplay({
        total_enrolled: myInternshipsData.enrolled.length,
        completed: myInternshipsData.completed.length,
        in_progress: myInternshipsData.in_progress.length,
        saved: myInternshipsData.saved.length,
        completion_rate: myInternshipsData.enrolled.length > 0 ? 
            Math.round((myInternshipsData.completed.length / myInternshipsData.enrolled.length) * 100, 1) : 0
    });
    
    showNotification(`Successfully applied to ${title} at ${company}!`, 'success');
    
    // Save to backend
    saveEnrollmentToBackend(internshipId);
}

function saveInternshipForLater(internshipId, title, company) {
    // Check if already saved
    const alreadySaved = myInternshipsData.saved.some(item => item.internship.id === internshipId);
    if (alreadySaved) {
        showNotification('Already saved this internship!', 'error');
        return;
    }
    
    const internship = {
        id: internshipId,
        title: title,
        company: company,
        location: 'Remote',
        duration: '3 months',
        stipend: '$500/month',
        type: 'remote'
    };
    
    // Add to saved list
    myInternshipsData.saved.push({
        id: Date.now(),
        internship: internship,
        saved_date: new Date().toISOString().split('T')[0]
    });
    
    // Update UI
    renderMyInternships();
    updateStatsDisplay({
        total_enrolled: myInternshipsData.enrolled.length,
        completed: myInternshipsData.completed.length,
        in_progress: myInternshipsData.in_progress.length,
        saved: myInternshipsData.saved.length,
        completion_rate: myInternshipsData.enrolled.length > 0 ? 
            Math.round((myInternshipsData.completed.length / myInternshipsData.enrolled.length) * 100, 1) : 0
    });
    
    showNotification(`${title} at ${company} saved for later!`, 'success');
    
    // Save to backend
    saveSavedInternshipToBackend(internshipId);
}

function saveEnrollmentToBackend(internshipId) {
    // This would save to your Django backend
    fetch(`/api/enroll-internship/${internshipId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            internship_id: internshipId,
            status: 'enrolled'
        })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Failed to save enrollment:', response);
        }
    })
    .catch(error => {
        console.error('Error saving enrollment:', error);
    });
}

function saveSavedInternshipToBackend(internshipId) {
    // This would save to your Django backend
    fetch(`/api/save-internship/${internshipId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            internship_id: internshipId
        })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Failed to save internship:', response);
        }
    })
    .catch(error => {
        console.error('Error saving internship:', error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

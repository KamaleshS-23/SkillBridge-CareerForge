let saved = 0;
let savedInternships = new Set();
let enrolled = 0;
let enrolledInternships = new Set();
let currentSearch = "";
let autoRefreshInterval;

/* REMOTIVE API */
async function fetchRemotive(keyword) {
    try {
        const response = await fetch(`https://remotive.com/api/remote-jobs?search=${keyword}`);
        const data = await response.json();
        
        return data.jobs
            .filter(job => {
                const title = job.title.toLowerCase();
                // Filter for internships and related roles
                return title.includes('internship') || 
                       title.includes('intern') ||
                       title.includes('trainee') ||
                       title.includes('graduate') ||
                       title.includes('co-op') ||
                       title.includes('apprentice') ||
                       (job.category && job.category.toLowerCase().includes('internship'));
            })
            .map(job => ({
                title: job.title,
                company: job.company_name,
                location: job.candidate_required_location,
                url: job.url,
                source: "Remotive"
            }));
    } catch (error) {
        console.error('Error fetching from Remotive:', error);
        return [];
    }
}

/* ADZUNA API */
async function fetchAdzuna(keyword) {
    try {
        // Note: You'll need to replace with actual API credentials
        const APP_ID = "YOUR_APP_ID";
        const APP_KEY = "YOUR_APP_KEY";
        
        // For demo purposes, return empty array
        // In production, uncomment and add your credentials:
        /*
        const response = await fetch(
            `https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=${APP_ID}&app_key=${APP_KEY}&what=internship ${keyword}` 
        );
        const data = await response.json();
        
        return data.results
            .filter(job => {
                const title = job.title.toLowerCase();
                return title.includes('internship') || 
                       title.includes('intern') ||
                       title.includes('trainee') ||
                       title.includes('graduate') ||
                       title.includes('co-op') ||
                       title.includes('apprentice');
            })
            .map(job => ({
                title: job.title,
                company: job.company.display_name,
                location: job.location.display_name,
                url: job.redirect_url,
                source: "Adzuna"
            }));
        */
        return [];
    } catch (error) {
        console.error('Error fetching from Adzuna:', error);
        return [];
    }
}

/* LINKEDIN SEARCH */
function getLinkedInLink(keyword) {
    return [{
        title: `${keyword} Internships on LinkedIn`,
        company: "LinkedIn",
        location: "Worldwide",
        url: `https://www.linkedin.com/jobs/internship-jobs/?keywords=${keyword}`,
        source: "LinkedIn"
    }];
}

/* ANGELLIST SEARCH */
function getAngelListLink(keyword) {
    return [{
        title: `${keyword} Internships on AngelList`,
        company: "AngelList",
        location: "Worldwide",
        url: `https://angel.co/job/${keyword}/internships`,
        source: "AngelList"
    }];
}

/* INDEED SEARCH */
function getIndeedLink(keyword) {
    return [{
        title: `${keyword} Internships on Indeed`,
        company: "Indeed",
        location: "Worldwide",
        url: `https://www.indeed.com/jobs?q=${keyword}+internship`,
        source: "Indeed"
    }];
}

/* GLASSDOOR SEARCH */
function getGlassdoorLink(keyword) {
    return [{
        title: `${keyword} Internships on Glassdoor`,
        company: "Glassdoor",
        location: "Worldwide",
        url: `https://www.glassdoor.com/Job/jobs.htm?sc.keyword=${keyword}+internship`,
        source: "Glassdoor"
    }];
}

/* COMPANY CAREER PAGES */
function getCompanyCareerPages(keyword) {
    const companies = [
        {
            name: "Google Careers",
            url: `https://careers.google.com/jobs/results/?category=INTERNSHIP&company=Google&q=${keyword}` 
        },
        {
            name: "Microsoft Careers", 
            url: `https://careers.microsoft.com/us/en/search-results?rw=true&pg=1&pgsz=20&ss=internship&c=All&sk=${keyword}` 
        },
        {
            name: "Amazon Jobs",
            url: `https://www.amazon.jobs/en/search?base_query=${keyword}&category=internship` 
        },
        {
            name: "Apple Careers",
            url: `https://jobs.apple.com/en-us/search?search=${keyword}&team=internships` 
        },
        {
            name: "Meta Careers",
            url: `https://www.metacareers.com/jobs/?searchType=detail&keyword=${keyword}&category=internships` 
        }
    ];

    return companies.map(company => ({
        title: `${keyword} Internships at ${company.name.split(' ')[0]}`,
        company: company.name,
        location: "Various",
        url: company.url,
        source: "Company Career"
    }));
}

/* INTERNSHIP.COM SEARCH */
function getInternshipsDotCom(keyword) {
    return [{
        title: `${keyword} Internships on Internships.com`,
        company: "Internships.com",
        location: "Worldwide",
        url: `https://www.internships.com/search?q=${keyword}`,
        source: "Internships.com"
    }];
}

/* WAYUP SEARCH */
function getWayup(keyword) {
    return [{
        title: `${keyword} Internships on WayUp`,
        company: "WayUp",
        location: "Worldwide",
        url: `https://www.wayup.com/j/${keyword}/internships`,
        source: "WayUp"
    }];
}

/* DISPLAY INTERNSHIPS */
function displayInternships(jobs) {
    const container = document.getElementById("internshipContainer");
    container.innerHTML = "";

    if (jobs.length === 0) {
        container.innerHTML = "<p style='grid-column: 1/-1; text-align: center; padding: 40px; color: var(--gray);'>No internships found</p>";
        return;
    }

    jobs.slice(0, 10).forEach(job => {
        const card = document.createElement("div");
        card.className = "card";
        
        card.innerHTML = `
            <span class="badge">🔥 Live</span>
            <h3>${escapeHtml(job.title)}</h3>
            <p class="company-name"><i class="fas fa-building"></i> ${escapeHtml(job.company)}</p>
            <p class="location"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(job.location)}</p>
            <p class="source">Source: ${escapeHtml(job.source)}</p>
            <div class="card-buttons">
                <button class="apply-btn" onclick="applyToInternship('${escapeHtml(job.title)}', '${escapeHtml(job.company)}', '${escapeHtml(job.url)}')">
                    <i class="fas fa-external-link-alt"></i> Apply
                </button>
                <button class="save-btn" onclick="saveInternship('${escapeHtml(job.title)}','${escapeHtml(job.company)}')">
                    <i class="fas fa-bookmark"></i> Save
                </button>
            </div>
        `;
        
        container.appendChild(card);
    });
}

/* ESCAPE HTML TO PREVENT XSS */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/* SAVE INTERNSHIP */
function saveInternship(title, company) {
    const key = title + "-" + company;
    
    if (savedInternships.has(key)) {
        showNotification("This internship is already saved!", "warning");
        return;
    }

    savedInternships.add(key);
    saved++;
    document.getElementById("savedInternships").innerText = saved;
    
    // Save to localStorage for persistence
    localStorage.setItem('savedInternships', JSON.stringify([...savedInternships]));
    localStorage.setItem('savedCount', saved);
    
    showNotification("Internship saved successfully!", "success");
}

/* APPLY TO INTERNSHIP */
function applyToInternship(title, company, url) {
    const key = title + "-" + company;
    
    if (enrolledInternships.has(key)) {
        showNotification("Already enrolled in this internship!", "warning");
        return;
    }

    enrolledInternships.add(key);
    enrolled++;
    document.getElementById("enrolledInternships").innerText = enrolled;
    
    // Save to localStorage for persistence
    localStorage.setItem('enrolledInternships', JSON.stringify([...enrolledInternships]));
    localStorage.setItem('enrolledCount', enrolled);
    
    showNotification(`Successfully applied to ${title} at ${company}!`, "success");
    
    // Open application page in new tab
    window.open(url, '_blank');
}

/* LOAD INTERNSHIPS */
async function loadInternships(role) {
    const loading = document.getElementById("loading");
    loading.innerText = "Loading internships...";
    loading.style.display = 'block';

    try {
        // Fetch from all sources in parallel
        const [remotiveJobs, adzunaJobs] = await Promise.all([
            fetchRemotive(role),
            fetchAdzuna(role)
        ]);

        const linkedin = getLinkedInLink(role);
        const angelList = getAngelListLink(role);
        const indeed = getIndeedLink(role);
        const glassdoor = getGlassdoorLink(role);
        const companyCareers = getCompanyCareerPages(role);
        const internshipsCom = getInternshipsDotCom(role);
        const wayup = getWayup(role);

        let jobs = [
            ...remotiveJobs,
            ...adzunaJobs,
            ...linkedin,
            ...angelList,
            ...indeed,
            ...glassdoor,
            ...companyCareers,
            ...internshipsCom,
            ...wayup
        ];

        // Remove duplicates
        jobs = Array.from(
            new Map(
                jobs.map(job => [job.title + job.company, job])
            ).values()
        );

        // Location filter
        const location = document.getElementById("locationFilter").value;
        if (location !== "") {
            jobs = jobs.filter(job => 
                job.location.toLowerCase().includes(location.toLowerCase())
            );
        }

        displayInternships(jobs);
        document.getElementById("totalInternships").innerText = jobs.length;
        loading.style.display = 'none';

    } catch (error) {
        console.error('Error loading internships:', error);
        loading.innerText = "Failed to load internships";
        loading.style.display = 'block';
    }
}

/* SEARCH INTERNSHIPS */
function searchInternships() {
    const keyword = document.getElementById("searchInput").value.trim();
    
    if (keyword === "") {
        showNotification("Enter job role or skill", "warning");
        return;
    }

    currentSearch = keyword;
    loadInternships(keyword);
    startAutoRefresh();
}

/* SEARCH BY COMPANY */
function searchCompany(company) {
    document.getElementById("searchInput").value = company;
    currentSearch = company;
    loadInternships(company);
    startAutoRefresh();
}

/* DISPLAY CURRENT INTERNSHIPS */
async function displayCurrentInternships() {
    const loading = document.getElementById("loading");
    loading.innerText = "Loading current internships...";
    loading.style.display = 'block';

    try {
        const remotiveJobs = await fetchRemotive("internship");
        const adzunaJobs = await fetchAdzuna("internship");
        const linkedin = getLinkedInLink("internship");
        const angelList = getAngelListLink("internship");
        const indeed = getIndeedLink("internship");
        const glassdoor = getGlassdoorLink("internship");
        const companyCareers = getCompanyCareerPages("internship");
        const internshipsCom = getInternshipsDotCom("internship");
        const wayup = getWayup("internship");

        let jobs = [
            ...remotiveJobs,
            ...adzunaJobs,
            ...linkedin,
            ...angelList,
            ...indeed,
            ...glassdoor,
            ...companyCareers,
            ...internshipsCom,
            ...wayup
        ];

        // If no jobs from APIs, show sample internships
        if (jobs.length === 0) {
            jobs = getSampleInternships();
        }

        // Remove duplicates
        jobs = Array.from(
            new Map(
                jobs.map(job => [job.title + job.company, job])
            ).values()
        );

        // Shuffle and take first 10 for variety
        jobs = jobs.sort(() => 0.5 - Math.random()).slice(0, 10);

        displayInternships(jobs);
        document.getElementById("totalInternships").innerText = jobs.length;
        loading.style.display = 'none';

    } catch (error) {
        console.error("Error loading internships:", error);
        loading.innerText = "Showing sample internships...";
        const fallbackJobs = getSampleInternships();
        displayInternships(fallbackJobs.slice(0, 10));
        document.getElementById("totalInternships").innerText = fallbackJobs.length;
        loading.style.display = 'none';
    }
}

/* SAMPLE INTERNSHIPS FALLBACK */
function getSampleInternships() {
    return [
        {
            title: "Software Engineering Intern",
            company: "Google",
            location: "Mountain View, CA / Remote",
            url: "https://careers.google.com/jobs/results/?category=INTERNSHIP",
            source: "Google Careers"
        },
        {
            title: "Data Science Intern",
            company: "Microsoft", 
            location: "Redmond, WA / Remote",
            url: "https://careers.microsoft.com/us/en/search-results?rw=true&pg=1&pgsz=20&ss=internship",
            source: "Microsoft Careers"
        },
        {
            title: "Product Management Intern",
            company: "Amazon",
            location: "Seattle, WA / Remote", 
            url: "https://www.amazon.jobs/en/search?base_query=internship&category=internship",
            source: "Amazon Jobs"
        },
        {
            title: "Frontend Development Intern",
            company: "Meta",
            location: "Menlo Park, CA / Remote",
            url: "https://www.metacareers.com/jobs/?searchType=detail&keyword=internship&category=internships",
            source: "Meta Careers"
        },
        {
            title: "UX Design Intern",
            company: "Apple",
            location: "Cupertino, CA / Remote",
            url: "https://jobs.apple.com/en-us/search?search=internship&team=internships",
            source: "Apple Careers"
        },
        {
            title: "Marketing Intern",
            company: "LinkedIn",
            location: "San Francisco, CA / Remote",
            url: "https://www.linkedin.com/jobs/internship-jobs/?keywords=marketing",
            source: "LinkedIn"
        },
        {
            title: "Business Analyst Intern",
            company: "Deloitte",
            location: "New York, NY / Remote",
            url: "https://www.linkedin.com/jobs/internship-jobs/?keywords=business%20analyst",
            source: "LinkedIn"
        },
        {
            title: "Cloud Engineering Intern",
            company: "IBM",
            location: "Armonk, NY / Remote",
            url: "https://www.linkedin.com/jobs/internship-jobs/?keywords=cloud%20engineering",
            source: "LinkedIn"
        },
        {
            title: "Mobile Development Intern",
            company: "TCS",
            location: "Mumbai, India / Remote",
            url: "https://www.linkedin.com/jobs/internship-jobs/?keywords=mobile%20development",
            source: "LinkedIn"
        },
        {
            title: "Cybersecurity Intern",
            company: "Zoho",
            location: "Chennai, India / Remote",
            url: "https://www.linkedin.com/jobs/internship-jobs/?keywords=cybersecurity",
            source: "LinkedIn"
        }
    ];
}

/* AUTO REFRESH */
function startAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }

    // Auto-refresh every 5 minutes (300,000 ms)
    autoRefreshInterval = setInterval(function() {
        if (currentSearch !== "") {
            loadInternships(currentSearch);
        }
    }, 300000);
}

/* SHOW NOTIFICATION */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    const colors = {
        success: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
        warning: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
        error: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)',
        info: 'linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)'
    };
    
    notification.style.background = colors[type] || colors.info;
    notification.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i> ${message}`;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

/* LOAD SAVED INTERNSHIPS FROM LOCALSTORAGE */
function loadSavedInternships() {
    const saved = localStorage.getItem('savedInternships');
    const count = localStorage.getItem('savedCount');
    
    if (saved) {
        savedInternships = new Set(JSON.parse(saved));
        document.getElementById("savedInternships").innerText = count || savedInternships.size;
    }
}

/* INITIALIZE PAGE LOAD */
window.addEventListener('DOMContentLoaded', function() {
    loadSavedInternships();
    displayCurrentInternships();
});

/* CLEANUP ON PAGE UNLOAD */
window.addEventListener('beforeunload', function() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});

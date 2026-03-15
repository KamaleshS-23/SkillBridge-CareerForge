let saved = 0;
let savedInternships = new Set();
let currentSearch = "";
let autoRefreshInterval;


/* REMOTIVE API */

async function fetchRemotive(keyword){

const response =
await fetch(`https://remotive.com/api/remote-jobs?search=${keyword}`);

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

}


/* ADZUNA API */

async function fetchAdzuna(keyword){

try{

const APP_ID = "YOUR_APP_ID";
const APP_KEY = "YOUR_APP_KEY";

const response =
await fetch(
`https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=${APP_ID}&app_key=${APP_KEY}&what=internship ${keyword}`
);

const data = await response.json();

return data.results
.filter(job => {
const title = job.title.toLowerCase();
// Filter for internships and related roles
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

}

catch{
return [];
}

}


/* LINKEDIN SEARCH */

function getLinkedInLink(keyword){
return [{
title: `${keyword} Internships on LinkedIn`,
company: "LinkedIn",
location: "Worldwide",
url: `https://www.linkedin.com/jobs/internship-jobs/?keywords=${keyword}`,
source: "LinkedIn"
}];
}

/* ANGELLIST SEARCH */

function getAngelListLink(keyword){
return [{
title: `${keyword} Internships on AngelList`,
company: "AngelList",
location: "Worldwide",
url: `https://angel.co/job/${keyword}/internships`,
source: "AngelList"
}];
}

/* INDEED SEARCH */

function getIndeedLink(keyword){
return [{
title: `${keyword} Internships on Indeed`,
company: "Indeed",
location: "Worldwide",
url: `https://www.indeed.com/jobs?q=${keyword}+internship`,
source: "Indeed"
}];
}

/* GLASSDOOR SEARCH */

function getGlassdoorLink(keyword){
return [{
title: `${keyword} Internships on Glassdoor`,
company: "Glassdoor",
location: "Worldwide",
url: `https://www.glassdoor.com/Job/jobs.htm?sc.keyword=${keyword}+internship`,
source: "Glassdoor"
}];
}

/* COMPANY CAREER PAGES */

function getCompanyCareerPages(keyword){
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

function getInternshipsDotCom(keyword){
return [{
title: `${keyword} Internships on Internships.com`,
company: "Internships.com",
location: "Worldwide",
url: `https://www.internships.com/search?q=${keyword}`,
source: "Internships.com"
}];
}

/* WAYUP SEARCH */

function getWayup(keyword){
return [{
title: `${keyword} Internships on WayUp`,
company: "WayUp",
location: "Worldwide",
url: `https://www.wayup.com/j/${keyword}/internships`,
source: "WayUp"
}];
}


/* DISPLAY INTERNSHIPS */

function displayInternships(jobs){

const container =
document.getElementById("internshipContainer");

container.innerHTML="";

if(jobs.length === 0){

container.innerHTML="<p>No internships found</p>";
return;

}

jobs.slice(0,10).forEach(job => {

const card =
document.createElement("div");

card.className="card";

card.innerHTML = `

<span class="badge">🔥 Live</span>

<h3>${job.title}</h3>

<p><b>${job.company}</b></p>

<p>${job.location}</p>

<p style="font-size:12px;color:gray;">Source: ${job.source}</p>

<a href="${job.url}" target="_blank">
<button class="apply">Apply</button>
</a>

<button class="save" onclick="saveInternship('${job.title}','${job.company}')">
Save
</button>

`;

container.appendChild(card);

});

}


/* SAVE INTERNSHIP */

function saveInternship(title, company){

const key = title + "-" + company;

if(savedInternships.has(key)){

alert("This internship is already saved!");
return;

}

savedInternships.add(key);

saved++;

document.getElementById("savedInternships").innerText = saved;

alert("Internship saved successfully!");

}


/* LOAD INTERNSHIPS */

async function loadInternships(role){

const loading =
document.getElementById("loading");

loading.innerText="Loading internships...";

try{

const remotiveJobs =
await fetchRemotive(role);

const adzunaJobs =
await fetchAdzuna(role);

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

/* REMOVE DUPLICATES */

jobs = Array.from(
new Map(
jobs.map(job =>
[job.title + job.company, job]
)
).values()
);


/* LOCATION FILTER */

const location =
document.getElementById("locationFilter").value;

if(location !== ""){

jobs = jobs.filter(job =>
job.location.toLowerCase().includes(location)
);

}

displayInternships(jobs);

document.getElementById("totalInternships").innerText = jobs.length;

loading.innerText="";

}

catch{

loading.innerText="Failed to load internships";

}

}


/* SEARCH INTERNSHIPS */

function searchInternships(){

const keyword =
document.getElementById("searchInput").value.trim();

if(keyword === ""){

alert("Enter job role or skill");
return;

}

currentSearch = keyword;

loadInternships(keyword);

startAutoRefresh();

}


/* SEARCH BY COMPANY */

function searchCompany(company){

document.getElementById("searchInput").value = company;

currentSearch = company;

loadInternships(company);

startAutoRefresh();

}


/* LOAD CURRENT INTERNSHIPS ON PAGE LOAD */

function loadCurrentInternships(){
const popularKeywords = [
"software engineering",
"data science", 
"product management",
"marketing",
"design",
"business development"
];

// Load internships for popular keywords
const randomKeyword = popularKeywords[Math.floor(Math.random() * popularKeywords.length)];
loadInternships(randomKeyword);
}

/* DISPLAY CURRENT INTERNSHIPS */

async function displayCurrentInternships(){
const loading = document.getElementById("loading");
loading.innerText = "Loading current internships...";

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
loading.innerText = "";

} catch (error) {
console.error("Error loading internships:", error);
loading.innerText = "Showing sample internships...";
const fallbackJobs = getSampleInternships();
displayInternships(fallbackJobs.slice(0, 10));
document.getElementById("totalInternships").innerText = fallbackJobs.length;
loading.innerText = "";
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

function startAutoRefresh(){

if(autoRefreshInterval){
clearInterval(autoRefreshInterval);
}

autoRefreshInterval = setInterval(function(){

if(currentSearch !== ""){
loadInternships(currentSearch);
}

},300000);

}

/* INITIALIZE PAGE LOAD */

window.addEventListener('DOMContentLoaded', function() {
displayCurrentInternships();
});
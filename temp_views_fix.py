# Temporary fix for the internship_finder function

def internship_finder(request):
    """
    Internship Finder Page - Live internship search across multiple platforms
    Integrates with Remotive, Adzuna, LinkedIn, AngelList, Indeed, Glassdoor, and company career pages
    """
    context = {
        'page_title': 'Internship Finder',
        'page_description': 'Search internships across top companies worldwide',
    }
    return render(request, 'core/internship.html', context)

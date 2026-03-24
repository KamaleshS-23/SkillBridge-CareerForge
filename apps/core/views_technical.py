from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import json
from apps.skills.models import TechnicalTestResult

User = get_user_model()

@login_required
@require_http_methods(["POST"])
def submit_technical_test(request):
    """
    Save technical test results to database
    Expects: {subject, difficulty, score, total_questions, percentage, grade, correct_answers, incorrect_answers, time_taken}
    """
    try:
        data = json.loads(request.body)
        subject = data.get('subject', '').strip()
        difficulty = data.get('difficulty', '').strip()
        score = data.get('score', 0)
        total_questions = data.get('total_questions', 0)
        percentage = data.get('percentage', 0.0)
        grade = data.get('grade', '').strip()
        correct_answers = data.get('correct_answers', [])
        incorrect_answers = data.get('incorrect_answers', [])
        time_taken = data.get('time_taken', None)
        
        if not all([subject, difficulty]):
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields: subject, difficulty'
            }, status=400)
        
        # Create test result record
        test_result = TechnicalTestResult.objects.create(
            user=request.user,
            subject=subject,
            difficulty=difficulty,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            grade=grade,
            correct_answers=json.dumps(correct_answers),
            incorrect_answers=json.dumps(incorrect_answers),
            time_taken=time_taken
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test results saved successfully',
            'test_id': test_result.id,
            'subject': subject,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'grade': grade,
            'test_date': test_result.test_date.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_technical_test_results(request):
    """
    Get user's technical test results
    Query params: subject (optional), limit (optional)
    """
    try:
        subject_filter = request.GET.get('subject', '').strip()
        limit = int(request.GET.get('limit', 10))
        
        # Build query
        results_query = TechnicalTestResult.objects.filter(user=request.user)
        
        if subject_filter:
            results_query = results_query.filter(subject__icontains=subject_filter)
        
        # Order by test date and limit
        results = results_query.order_by('-test_date')[:limit]
        
        # Format results
        results_data = []
        for result in results:
            results_data.append({
                'id': result.id,
                'subject': result.subject,
                'difficulty': result.difficulty,
                'score': result.score,
                'total_questions': result.total_questions,
                'percentage': result.percentage,
                'grade': result.grade,
                'correct_answers': json.loads(result.correct_answers) if result.correct_answers else [],
                'incorrect_answers': json.loads(result.incorrect_answers) if result.incorrect_answers else [],
                'time_taken': result.time_taken,
                'test_date': result.test_date.isoformat()
            })
        
        return JsonResponse({
            'status': 'success',
            'results': results_data,
            'total_count': results_query.count(),
            'subject_filter': subject_filter or 'all'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_technical_test_stats(request):
    """
    Get user's technical test statistics grouped by subject
    """
    try:
        # Get all results for user
        results = TechnicalTestResult.objects.filter(user=request.user)
        
        # Group by subject
        subject_stats = {}
        for result in results:
            subject = result.subject
            if subject not in subject_stats:
                subject_stats[subject] = {
                    'total_tests': 0,
                    'best_score': 0,
                    'best_percentage': 0.0,
                    'best_grade': '',
                    'average_score': 0.0,
                    'average_percentage': 0.0,
                    'last_test_date': None,
                    'difficulty_breakdown': {
                        'beginner': {'count': 0, 'best_score': 0},
                        'intermediate': {'count': 0, 'best_score': 0},
                        'advanced': {'count': 0, 'best_score': 0}
                    }
                }
            
            stats = subject_stats[subject]
            stats['total_tests'] += 1
            stats['average_score'] += result.score
            stats['average_percentage'] += result.percentage
            
            # Update best scores
            if result.score > stats['best_score']:
                stats['best_score'] = result.score
                stats['best_percentage'] = result.percentage
                stats['best_grade'] = result.grade
            
            # Update last test date
            if not stats['last_test_date'] or result.test_date > stats['last_test_date']:
                stats['last_test_date'] = result.test_date
            
            # Update difficulty breakdown
            difficulty_key = result.difficulty
            if difficulty_key in stats['difficulty_breakdown']:
                stats['difficulty_breakdown'][difficulty_key]['count'] += 1
                if result.score > stats['difficulty_breakdown'][difficulty_key]['best_score']:
                    stats['difficulty_breakdown'][difficulty_key]['best_score'] = result.score
        
        # Calculate averages
        for subject, stats in subject_stats.items():
            if stats['total_tests'] > 0:
                stats['average_score'] = round(stats['average_score'] / stats['total_tests'], 1)
                stats['average_percentage'] = round(stats['average_percentage'] / stats['total_tests'], 1)
        
        return JsonResponse({
            'status': 'success',
            'subject_stats': subject_stats,
            'total_tests': results.count(),
            'subjects_covered': len(subject_stats)
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

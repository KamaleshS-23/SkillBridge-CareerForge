from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import json

from .models import AptitudeTestResult


@login_required
@require_http_methods(["POST"])
def submit_aptitude_test(request):
    """
    Submit aptitude test results and store in database
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to submit test results'
            }, status=401)
        
        data = json.loads(request.body)
        
        # Extract scores from request
        scores = data.get('scores', {})
        time_taken_str = data.get('time_taken', '00:00:00')
        
        # Create test result record
        result = AptitudeTestResult.objects.create(
            user=request.user,
            quantitative_score=scores.get('quantitative', 0),
            verbal_score=scores.get('verbal', 0),
            logical_score=scores.get('logical', 0),
            data_interpretation_score=scores.get('data_interpretation', 0),
            abstract_reasoning_score=scores.get('abstract_reasoning', 0),
            max_score=data.get('max_score', 150),
            time_taken=time_taken_str,
            difficulty_level=data.get('difficulty_level', 'mixed')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Test results saved successfully!',
            'result_id': result.id,
            'total_score': result.total_score,
            'percentage': result.percentage,
            'scores': {
                'quantitative': result.quantitative_score,
                'verbal': result.verbal_score,
                'logical': result.logical_score,
                'data_interpretation': result.data_interpretation_score,
                'abstract_reasoning': result.abstract_reasoning_score
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error saving test results: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_aptitude_results(request):
    """
    Get user's aptitude test history
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'Please login to view test results'
            }, status=401)
        
        results = AptitudeTestResult.objects.filter(user=request.user).order_by('-test_date')
        
        results_data = []
        for result in results:
            results_data.append({
                'id': result.id,
                'test_date': result.test_date.strftime('%Y-%m-%d %H:%M'),
                'total_score': result.total_score,
                'max_score': result.max_score,
                'percentage': result.percentage,
                'difficulty_level': result.difficulty_level,
                'time_taken': str(result.time_taken),
                'scores': {
                    'quantitative': result.quantitative_score,
                    'verbal': result.verbal_score,
                    'logical': result.logical_score,
                    'data_interpretation': result.data_interpretation_score,
                    'abstract_reasoning': result.abstract_reasoning_score
                }
            })
        
        return JsonResponse({
            'status': 'success',
            'results': results_data,
            'total_tests': results.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error fetching test results: {str(e)}'
        }, status=500)

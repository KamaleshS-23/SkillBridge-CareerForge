from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models
from .models import TechnicalTestResult
import json


@login_required
@require_http_methods(["GET", "POST"])
def submit_technical_test(request):
    """Submit technical test results"""
    try:
        data = json.loads(request.body)
        
        # Create technical test result
        test_result = TechnicalTestResult.objects.create(
            user=request.user,
            topic=data.get('topic', 'Unknown Topic'),
            difficulty=data.get('difficulty', 'beginner'),
            score=data.get('score', 0),
            max_score=data.get('max_score', 10),
            correct_answers=data.get('correct_answers', 0),
            incorrect_answers=data.get('incorrect_answers', 0),
            time_taken=data.get('time_taken', '00:00:00')
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Technical test result saved successfully',
            'data': {
                'id': test_result.id,
                'topic': test_result.topic,
                'score': test_result.score,
                'percentage': test_result.percentage,
                'date': test_result.test_date.strftime('%Y-%m-%d'),
                'difficulty': test_result.difficulty,
                'score_display': test_result.score_display
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
@require_http_methods(["GET"])
def get_technical_test_results(request):
    """Get user's technical test results"""
    try:
        results = TechnicalTestResult.objects.filter(user=request.user).order_by('-test_date')
        
        results_data = []
        for result in results:
            results_data.append({
                'id': result.id,
                'topic': result.topic,
                'score': result.score,
                'max_score': result.max_score,
                'percentage': result.percentage,
                'date': result.test_date.strftime('%Y-%m-%d'),
                'difficulty': result.difficulty,
                'time_taken': result.time_taken,
                'score_display': result.score_display,
                'correct': result.correct_answers,
                'incorrect': result.incorrect_answers
            })
        
        return JsonResponse({
            'status': 'success',
            'data': results_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def get_technical_test_stats(request):
    """Get technical test statistics"""
    try:
        results = TechnicalTestResult.objects.filter(user=request.user)
        
        if not results.exists():
            return JsonResponse({
                'status': 'success',
                'data': {
                    'total_tests': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'recent_score': 0
                }
            })
        
        total_tests = results.count()
        avg_score = results.aggregate(avg_score=models.Avg('score'))['avg_score'] or 0
        best_score = results.aggregate(max_score=models.Max('score'))['max_score'] or 0
        recent_result = results.first()
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'total_tests': total_tests,
                'average_score': round(avg_score, 1),
                'best_score': best_score,
                'recent_score': recent_result.score if recent_result else 0,
                'recent_date': recent_result.test_date.strftime('%Y-%m-%d') if recent_result else None
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

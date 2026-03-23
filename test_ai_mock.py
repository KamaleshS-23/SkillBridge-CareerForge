#!/usr/bin/env python3

# Test AI Mock Interview Integration
import os

def test_ai_mock_interview():
    dashboard_path = 'skillbridge_careerforge_project/templates/core/dashboard.html'
    
    if not os.path.exists(dashboard_path):
        print("❌ dashboard.html not found")
        return False
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== AI MOCK INTERVIEW INTEGRATION TEST ===")
    
    # Core functionality checks
    checks = {
        'loadAIMockInterviewPage': 'loadAIMockInterviewPage()' in content,
        'ai_mock_container': 'ai-mock-interview-container' in content,
        'selectType_function': 'function selectType(' in content,
        'selectDifficulty_function': 'function selectDifficulty(' in content,
        'startInterview_function': 'function startInterview()' in content,
        'sendAnswer_function': 'function sendAnswer()' in content,
        'closeAIMockInterview_function': 'function closeAIMockInterview()' in content,
        'timer_functionality': 'startTimer()' in content and 'updateTimerDisplay()' in content,
        'question_system': 'getFirstQuestion(' in content,
        'chat_functionality': 'addMessage(' in content and 'getElementById("chat")' in content,
        'proper_html_structure': '<div class="ai-mock-interview-container">' in content,
    }
    
    # Button ID checks
    button_ids = ['btn-hr', 'btn-technical', 'btn-communication']
    missing_buttons = [btn_id for btn_id in button_ids if f'id="{btn_id}"' not in content]
    
    # Element ID checks
    element_ids = ['home', 'interview', 'chat', 'answer-input', 'timer-display']
    missing_elements = [elem_id for elem_id in element_ids if f'getElementById("{elem_id}")' not in content]
    
    all_passed = True
    print("\nFUNCTIONALITY CHECKS:")
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check_name}: {result}")
        if not result:
            all_passed = False
    
    if missing_buttons:
        print(f"\n⚠️  MISSING BUTTON IDs: {', '.join(missing_buttons)}")
        all_passed = False
    
    if missing_elements:
        print(f"\n⚠️  MISSING ELEMENT IDs: {', '.join(missing_elements)}")
        all_passed = False
    
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\n✅ AI Mock Interview should be working correctly")
        print("\n✅ Test by clicking 'AI Mock Interview System' in dashboard")
        return True
    else:
        print("\n❌ SOME CHECKS FAILED")
        return False

if __name__ == "__main__":
    test_ai_mock_interview()

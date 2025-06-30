from django.shortcuts import render, redirect
import requests
import random
def home(request):
    return render(request, 'home.html')
def quiz(request):
    if request.method == 'POST':
        score = 0
        results = []
        total = int(request.POST.get('total'))
        for i in range(total):
            selected = request.POST.get(f'question{i}')
            correct = request.POST.get(f'correct{i}')
            question = request.POST.get(f'question_text{i}')
            is_correct = selected == correct
            if is_correct:
                score += 1
            results.append({
                'question': question,
                'selected': selected,
                'correct': correct,
                'is_correct': is_correct
            })
        request.session['score'] = score
        request.session['total'] = total
        request.session['results'] = results

        return redirect('result')
    else:
        url = 'https://opentdb.com/api.php?amount=5&type=multiple'
        response = requests.get(url)
        data = response.json()
        questions = data['results']

        for q in questions:
            q['answers'] = q['incorrect_answers'] + [q['correct_answer']]
            random.shuffle(q['answers'])

        return render(request, 'quiz.html', {
            'questions': questions,
            'total': len(questions)
        })
def result(request):
    score = request.session.get('score', 0)
    total = request.session.get('total', 0)
    results = request.session.get('results', [])

    return render(request, 'result.html', {
        'score': score,
        'total': total,
        'results': results
    })



